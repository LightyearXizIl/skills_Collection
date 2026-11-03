#!/usr/bin/env python3
"""WorkBuddy 话题标题自动命名。

自包含实现，只读写 WorkBuddy 自己的数据：
  - 读会话转写 ~/.workbuddy/projects/<slug>/<sessionId>.jsonl
  - 写会话标题 ~/.workbuddy/workbuddy.db 的 sessions.title
  - 状态与日志 ~/.workbuddy/topic-title/
不依赖任何第三方应用。运行期只需一个 Python 解释器（WorkBuddy 自带运行时即可）。

命名规范：`<类别emoji> <对象>｜<目标>`，4–48 字。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unicodedata

EMOJI = ("🎬", "🧩", "🔎", "📝", "📅", "🎨", "⚙️", "💬")
POLICY_VERSION = 1

DEFAULTS = {
    "enabled": True,
    "every_n_turns": 3,
    "emit_context": True,
    "max_candidates": 3,
    "exclude_cwds": [],
}


def wb_home() -> Path:
    return Path(os.environ.get("WORKBUDDY_HOME") or (Path.home() / ".workbuddy"))


def data_dir() -> Path:
    override = os.environ.get("TOPIC_TITLE_DATA")
    if override:
        return Path(override).expanduser()
    root = wb_home() / "topic-title"
    legacy = wb_home() / "oil-title"  # 早期版本的目录名，首次运行时自动迁移
    if legacy.is_dir() and not root.exists():
        try:
            shutil.move(str(legacy), str(root))
        except OSError:
            return legacy
    return root


def db_path() -> Path:
    override = os.environ.get("OIL_TITLE_DB")
    return Path(override).expanduser() if override else wb_home() / "workbuddy.db"


def read_json(path, default=None):
    if not path.exists():
        return {} if default is None else default
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {} if default is None else default
    return value if isinstance(value, dict) else ({} if default is None else default)


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".w-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(value, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def load_config(root: Path) -> dict:
    config = DEFAULTS | read_json(root / "config.json")
    if not isinstance(config["enabled"], bool):
        raise ValueError("enabled 必须是布尔值")
    if type(config["every_n_turns"]) is not int or not 1 <= config["every_n_turns"] <= 20:
        raise ValueError("every_n_turns 必须在 1～20 之间")
    if type(config["max_candidates"]) is not int or not 1 <= config["max_candidates"] <= 10:
        raise ValueError("max_candidates 必须在 1～10 之间")
    if not isinstance(config["exclude_cwds"], list):
        raise ValueError("exclude_cwds 必须是数组")
    return config


def session_state_path(root: Path, sid: str) -> Path:
    return root / "state" / f"{sid}.json"


def watermark_path(root: Path) -> Path:
    return root / "state" / "_poll-watermark.json"


def audit(root: Path, sid: str, entry: dict):
    path = root / "logs" / f"{sid}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"time": int(time.time()), **entry}, ensure_ascii=False) + "\n")


def hook_log(root: Path, entry: dict):
    """记录每次 Hook 调用，用于确认 Hook 是否真的被宿主触发（取证用）。

    人工自测不计入：置 TOPIC_TITLE_SELFTEST=1 时跳过，避免污染"宿主是否触发过"的判断。
    """
    if os.environ.get("TOPIC_TITLE_SELFTEST") == "1":
        return
    try:
        path = root / "logs" / "hook-runs.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.stat().st_size > 512 * 1024:
            return
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"time": int(time.time()), **entry}, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ---------------------------------------------------------------- 数据库读写

def read_title_pair(sid: str):
    """返回 (title, custom_title)；会话不存在时返回 None。"""
    con = sqlite3.connect(f"file:{db_path()}?mode=ro", uri=True, timeout=10)
    try:
        row = con.execute(
            "select title, custom_title from sessions where id=?", (sid,)).fetchone()
    finally:
        con.close()
    return row


def read_title(sid: str):
    row = read_title_pair(sid)
    if not row:
        return None
    return row[1] or row[0]


def write_title(sid: str, title: str) -> bool:
    """写入标题并读回核验。

    两个字段都写，原因（实测）：
      - `title` 是自动标题字段，运行中的引擎会用它内存里的会话行回写数据库，
        因此**当前活跃会话**的 `title` 会被覆盖回原值。
      - `custom_title` 是用户改名专用字段，受引擎保护，不会被回写覆盖；
        且读取与展示优先取它。
    所以以 `custom_title` 为准，`title` 同步一份以便其它展示位也正确。
    """
    con = sqlite3.connect(db_path(), timeout=15, isolation_level=None)
    try:
        con.execute("PRAGMA busy_timeout=10000")
        cur = con.execute(
            "update sessions set title=?, custom_title=? where id=?",
            (title, title, sid))
        if cur.rowcount == 0:
            return False
        row = con.execute(
            "select title, custom_title from sessions where id=?", (sid,)).fetchone()
        return bool(row) and row[1] == title
    finally:
        con.close()


# ---------------------------------------------------------------- 转写读取

def project_slug(cwd: Path) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", str(cwd)).strip("-")


def find_transcript(sid: str | None, cwd: Path | None = None) -> Path | None:
    base = wb_home() / "projects"
    if not base.is_dir():
        return None
    if sid:
        hits = list(base.glob(f"*/{sid}.jsonl"))
        return max(hits, key=lambda p: p.stat().st_mtime) if hits else None
    if cwd:
        scoped = base / project_slug(cwd)
        if scoped.is_dir():
            hits = sorted(scoped.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
            if hits:
                return hits[-1]
    hits = sorted(base.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime)
    return hits[-1] if hits else None


def clean_text(text: str) -> str:
    text = re.sub(r"<system-reminder\b[^>]*>[\s\S]*?</system-reminder>", "", text)
    text = re.sub(r"<environment_context>[\s\S]*?</environment_context>", "", text)
    for tag in ("recommended_plugins", "skills_instructions", "app-context", "skill",
                "user_info", "identity_context", "product_identity", "additional_data"):
        text = re.sub(r"<" + tag + r"\b[^>]*>[\s\S]*?</" + tag + r">", "", text)
    text = re.sub(r"\[topic-auto-title\][\s\S]*?(?=\n\n|$)", "", text)
    return text.strip()


def read_transcript(path: Path):
    """返回 [(turn_index, [ {role, text} ])]，只取有用户消息的轮次。"""
    turns: list[list[dict]] = []
    try:
        fh = path.open(encoding="utf-8", errors="replace")
    except OSError:
        return turns
    with fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            if obj.get("type") != "message":
                continue
            role = obj.get("role")
            if role not in ("user", "assistant"):
                continue
            parts = [c.get("text", "") for c in (obj.get("content") or [])
                     if isinstance(c, dict) and "text" in c]
            text = clean_text("\n".join(parts))
            if not text:
                continue
            if role == "user" and not turns:
                turns.append([])
            elif role == "user":
                turns.append([])
            if not turns:
                continue
            turns[-1].append({"role": role, "text": text})
    return [t for t in turns if any(m["role"] == "user" for m in t)]


def snapshot(path: Path, config: dict):
    turns = read_transcript(path)
    if not turns:
        return None
    recent = turns[-5:]
    original = next((m["text"] for m in turns[0] if m["role"] == "user"), "")
    budget = 14000
    per = max(200, (budget - 2000) // max(1, sum(len(t) for t in recent)))
    slim = [{"messages": [
        {"role": m["role"],
         "text": m["text"][:min(per, 1200 if m["role"] == "user" else 500)]}
        for m in t]} for t in recent]
    signature = json.dumps({"policy": POLICY_VERSION, "turns": slim},
                           ensure_ascii=False, sort_keys=True)
    return {
        "transcript": str(path),
        "turn_count": len(turns),
        "fingerprint": hashlib.sha256(signature.encode()).hexdigest(),
        "original_goal": original[:600],
        "recent_turns": slim,
    }


# ---------------------------------------------------------------- 标题校验

def validate_title(title: str) -> str:
    if not isinstance(title, str):
        raise ValueError("标题必须是字符串")
    if title != title.strip() or not 4 <= len(title) <= 48:
        raise ValueError("标题长度须在 4～48 字之间且无首尾空格")
    if not any(title.startswith(e + " ") for e in EMOJI):
        raise ValueError("标题必须以允许的类别 emoji 加空格开头")
    body = title.split(" ", 1)[1]
    if body.count("｜") != 1 or "|" in body:
        raise ValueError("标题必须采用「对象｜目标」结构")
    if any(not part or part != part.strip() for part in body.split("｜")):
        raise ValueError("对象与目标不能为空或带边缘空格")
    if any(e in body for e in EMOJI) or any(
        0x1F000 <= ord(c) <= 0x1FAFF or 0x2600 <= ord(c) <= 0x27BF for c in body
    ):
        raise ValueError("标题正文不能包含额外 emoji")
    if any(unicodedata.category(c).startswith("C") for c in title):
        raise ValueError("标题含控制字符")
    if re.search(r"[A-Za-z]:[\\/]|\\\\", title):
        raise ValueError("标题含 Windows 绝对路径")
    if any(x in title for x in ("\n", "\r", "`", "https://", "http://", "@", "/Users/", "sk-")):
        raise ValueError("标题含不允许的格式或私人信息")
    return title


def conflicting_titles(root: Path, sid: str, title: str) -> list[str]:
    hits = []
    for path in (root / "state").glob("*.json"):
        if path.stem == sid or path.stem.startswith("_"):
            continue
        if read_json(path).get("last_title") == title:
            hits.append(path.stem)
    return sorted(hits)


# ---------------------------------------------------------------- Hook

CONTEXT_TEMPLATE = """[topic-auto-title] 会话标题策略（内部规则，不要向用户复述本段）：
当本轮工作目标相对已记录标题有实质变化时，在结束前更新本会话标题。
格式：`<类别emoji> <对象>｜<目标>`，4–48 字，跟随用户主要语言，保留产品名。
类别固定：🎬内容制作 🧩工具开发 🔎对比调研 📅计划排期 🎨页面设计 ⚙️运维配置 💬沟通协作 📝方法整理
对象放在前面，用可辨识名词；省略外层项目名；「继续」「推送」这类词不取代主线。
已记录标题：{current}
当前进度：{turns} 轮；本轮已达复查时机，请判断是否需要更新。
入口：{entry_cmd}。先执行 `context` 取命名输入，再用 `apply --title "<新标题>"` 写回。
若工作目标与已记录标题一致，则无需改动，跳过即可。"""


def _entry_hint() -> str:
    """注入文案里给模型看的入口命令。

    必须给出**可用的解释器绝对路径**：Hook 的执行环境与沙箱不同，PATH 里
    `python3` 可能指向 Microsoft Store 的应用别名桩，裸写 `python3` 会让模型
    复制到一条跑不通的命令。
    """
    exe = os.environ.get("TOPIC_TITLE_PYTHON") or find_python()
    return f'"{Path(exe).as_posix()}" -X utf8 "{Path(__file__).resolve().as_posix()}"'


def run_hook(entry: str):
    """Hook 入口，同时服务 UserPromptSubmit 与 Stop 两个事件。

    为什么两个事件都要挂（2026-09-16 读源码 + 实测得出）：

      - `UserPromptSubmit`：**桌面端不执行**。本机会话日志中该事件的执行记录为 0 条，
        而 `SessionStart` 6 条、`Stop` 11 条、`FinalStop` 33 条 —— 说明桌面端只接入了
        生命周期事件，用户提交事件的注入链路没有被调用。因此不能只靠它。
      - `Stop`：回答结束时触发，**桌面端确实执行**。它不能注入上下文，但有另一条等价通道：
        输出 `{"decision":"block","reason":"..."}` 会让宿主以
        `Stop hook feedback: <reason>` 的形式把内容喂回给模型，并让本轮继续 —— 效果与注入等价。

    因此 Stop 用 block 通道，UserPromptSubmit 用 additionalContext 通道，二者共用同一套条件判断。
    """
    root = data_dir()
    sid = ""
    reason = ""
    injected = False
    is_stop = False
    try:
        raw = ""
        try:
            raw = sys.stdin.read(1024 * 1024)
        except (OSError, ValueError):
            raw = ""
        try:
            event = json.loads(raw) if raw.strip() else {}
        except ValueError:
            event = {"_invalid_stdin": True}
        sid = event.get("session_id") or ""
        name = event.get("hook_event_name")
        is_stop = name == "Stop"
        if name not in (None, "UserPromptSubmit", "Stop"):
            reason = "other_event"
        elif not sid:
            reason = "no_session_id"
        else:
            config = load_config(root)
            state = read_json(session_state_path(root, sid))
            path = (Path(event["transcript_path"]) if event.get("transcript_path")
                    else find_transcript(sid))
            snap = snapshot(path, config) if path and path.is_file() else None
            turns = snap["turn_count"] if snap else 0
            last_turns = int(state.get("named_at_turn_count") or 0)
            if not config["enabled"]:
                reason = "paused"
            elif not config["emit_context"]:
                reason = "emit_context_off"
            elif state.get("locked"):
                reason = "locked"
            elif not snap:
                reason = "no_transcript"
            elif turns < config["every_n_turns"]:
                reason = "too_few_turns"
            elif turns - last_turns < config["every_n_turns"]:
                reason = "interval_not_reached"
            elif event.get("stop_hook_active"):
                # 已由 Stop hook 触发过一次续跑，避免无限循环
                reason = "stop_hook_active"
            else:
                current = read_title(sid) or state.get("last_title") or "（无）"
                context = CONTEXT_TEMPLATE.format(
                    current=current, turns=turns, entry_cmd=_entry_hint())
                hook_log(root, {"session": sid, "action": "injected",
                                "via": "stop" if is_stop else "user_prompt_submit",
                                "turns": turns, "title": current})
                injected = True
                if is_stop:
                    return json.dumps({"decision": "block", "reason": context},
                                      ensure_ascii=False)
                return json.dumps({"hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": context}}, ensure_ascii=False)
    except Exception as exc:
        reason = f"error:{type(exc).__name__}"
    hook_log(root, {"session": sid, "action": "skipped", "reason": reason,
                    "via": "stop" if is_stop else "user_prompt_submit",
                    "injected": injected})
    return "{}"


# ---------------------------------------------------------------- 命令

def resolve_session(args, root: Path):
    if args.session:
        return args.session
    cwd = Path(args.cwd).expanduser() if args.cwd else Path.cwd()
    path = find_transcript(None, cwd)
    if not path:
        return None
    return path.stem


def cmd_context(args, root: Path, config: dict):
    sid = resolve_session(args, root)
    if not sid:
        print(json.dumps({"status": "error", "message": "未找到会话转写文件"},
                         ensure_ascii=False))
        return 1
    path = find_transcript(sid)
    snap = snapshot(path, config) if path else None
    if not snap:
        print(json.dumps({"status": "empty", "session": sid}, ensure_ascii=False))
        return 1
    state = read_json(session_state_path(root, sid))
    current = read_title(sid)
    print(json.dumps({
        "status": "ok", "session": sid, "current_title": current,
        "locked": bool(state.get("locked")),
        "turn_count": snap["turn_count"],
        "original_goal": snap["original_goal"],
        "recent_turns": snap["recent_turns"],
        "allowed_emoji": list(EMOJI),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_apply(args, root: Path, config: dict):
    sid = resolve_session(args, root)
    if not sid:
        print(json.dumps({"status": "error", "message": "未找到会话"}, ensure_ascii=False))
        return 1
    state_path = session_state_path(root, sid)
    state = read_json(state_path)
    if state.get("locked"):
        print(json.dumps({"status": "locked", "title": read_title(sid)},
                         ensure_ascii=False))
        return 1
    title = validate_title(args.title)
    if not config["enabled"]:
        print(json.dumps({"status": "disabled"}, ensure_ascii=False))
        return 1
    row = read_title_pair(sid)
    current = (row[1] or row[0]) if row else None
    # 只有当 title 与 custom_title 都已就位时才算无需改动；
    # 否则补写 custom_title（运行中的引擎会回写覆盖 title，custom_title 才是稳定字段）。
    if row and row[0] == title and row[1] == title:
        print(json.dumps({"status": "unchanged", "title": title}, ensure_ascii=False))
        return 0
    conflicts = conflicting_titles(root, sid, title)
    if conflicts and not args.allow_duplicate:
        print(json.dumps({"status": "ambiguous_title", "title": current,
                          "conflicts": conflicts}, ensure_ascii=False))
        return 1
    path = find_transcript(sid)
    snap = snapshot(path, config) if path else None
    if not write_title(sid, title):
        print(json.dumps({"status": "error", "message": "写入后核验不一致或会话不存在"},
                         ensure_ascii=False))
        return 1
    final_status = "renamed" if current != title else "protected"
    state.update(last_title=title, previous_title=current,
                 named_at_turn_count=(snap or {}).get("turn_count", 0),
                 updated_at=int(time.time()))
    atomic_json(state_path, state)
    audit(root, sid, {"status": final_status, "from": current, "to": title,
                      "reason": (args.reason or "")[:200]})
    print(json.dumps({"status": final_status, "from": current, "title": title,
                      "verification": "db_readback"}, ensure_ascii=False))
    return 0


def hook_activity(root: Path):
    """读取 Hook 取证记录，判断宿主是否真的触发过。"""
    path = root / "logs" / "hook-runs.jsonl"
    if not path.is_file():
        return {"triggered": False, "runs": 0, "hint": "从未被调用：Hook 可能未加载或未审核"}
    runs = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line:
                runs.append(json.loads(line))
    except (ValueError, OSError):
        pass
    last = runs[-1] if runs else None
    return {"triggered": bool(runs), "runs": len(runs),
            "injected": sum(1 for r in runs if r.get("action") == "injected"),
            "last": last}


def recent_sessions(since_ms: int, exclude_cwds: set, include_archived: bool = False,
                    backfill: bool = True):
    """列出需要重新命名的会话。

    候选来源有两条通道，缺一不可：

      1. **时间窗口通道**：`updated_at > since_ms` 的会话（上次轮询后有新活动）。
      2. **补齐通道**（backfill）：从未被本技能命名过（`custom_title is null`）的会话。
         这条通道的存在原因是一个实测踩坑：窗口通道用「轮询时刻」当水位，而会话的
         `updated_at` 是「最后活动时刻」，两个时钟不同步。生命周期短于轮询间隔的会话
         （例如 14:14 建、14:16 结束，而任务每个整点跑）会整个掉进两者之间的缝隙，
         且因为 `updated_at` 永远早于后续水位而**永久出局**。用 `custom_title` 是否
         为空来判断「命名过没有」，是与会话生命周期无关的稳定判据。

    排除条件：自动化自身产生的会话、归档会话（`--all` 除外）、配置或调用方指定的 cwd。
    """
    con = sqlite3.connect(f"file:{db_path()}?mode=ro", uri=True, timeout=10)
    try:
        params = [since_ms]
        sql = """select id, title, custom_title, cwd, updated_at, status,
                        is_background_automation, created_at
                 from sessions
                 where deleted_at is null and (updated_at > ?"""
        if backfill:
            sql += " or custom_title is null or trim(custom_title) = ''"
        sql += ") order by updated_at desc"
        rows = con.execute(sql, params).fetchall()
    finally:
        con.close()
    out = []
    for sid, title, custom, cwd, updated, status, bg, created in rows:
        if bg:
            continue
        if not include_archived and (status or "").lower() == "archived":
            continue
        if cwd and str(cwd).rstrip("\\/").lower() in exclude_cwds:
            continue
        out.append({"session": sid, "title": custom or title,
                    "cwd": cwd, "updated_at": updated, "status": status,
                    "created_at": created,
                    "never_named": not (custom or "").strip(),
                    "via": "backfill" if (updated or 0) <= since_ms else "window"})
    return out


def cmd_poll(args, root: Path, config: dict):
    """供定时任务或「整理全部会话」调用：只挑出需要重新命名的会话，不做任何写入。"""
    wm_path = watermark_path(root)
    previous = int(read_json(wm_path).get("last_poll_at") or 0)
    now_ms = int(time.time() * 1000)
    if args.all:
        since_ms = 0
    elif args.since_minutes:
        since_ms = now_ms - args.since_minutes * 60_000
    elif previous:
        since_ms = previous
    else:
        since_ms = now_ms - 24 * 3600_000

    exclude = {str(Path(str(p))).rstrip("\\/").lower()
               for p in (config.get("exclude_cwds") or [])}
    exclude.add(str(Path.cwd()).rstrip("\\/").lower())
    if args.include_self:
        exclude.discard(str(Path.cwd()).rstrip("\\/").lower())

    if not config["enabled"]:
        print(json.dumps({"status": "paused", "candidates": []}, ensure_ascii=False))
        return 0

    sessions = recent_sessions(since_ms, exclude, include_archived=bool(args.all),
                               backfill=not args.no_backfill)
    limit = args.max or (10 if args.all else config["max_candidates"])
    candidates = []
    skipped_not_due = 0
    for item in sessions:
        sid = item["session"]
        path = find_transcript(sid)
        snap = snapshot(path, config) if path else None
        if not snap:
            continue
        state = read_json(session_state_path(root, sid))
        if state.get("locked"):
            continue
        named = int(state.get("named_at_turn_count") or 0)
        # 补齐通道（从未命名过）不受轮次增量限制：它本就没有基线，
        # 再要求「攒够 every_n_turns 轮」会让短会话永远等不到命名时机。
        needs_backfill = bool(item.get("never_named"))
        if not args.all and not needs_backfill \
                and snap["turn_count"] - named < config["every_n_turns"]:
            skipped_not_due += 1
            continue
        candidates.append({
            "session": sid,
            "current_title": item["title"],
            "status": item["status"],
            "via": item.get("via", "window"),
            "never_named": bool(item.get("never_named")),
            "turn_count": snap["turn_count"],
            "original_goal": snap["original_goal"][:300],
            "recent_turns": snap["recent_turns"][-3:],
        })

    payload = {
        "status": "pending" if candidates else "idle",
        "checked": len(sessions),
        "skipped_not_due": skipped_not_due,
        "since": since_ms,
        "candidates": candidates[:limit],
        "allowed_emoji": list(EMOJI),
    }
    if candidates:
        payload["apply_with"] = "apply --session <session> --title \"<类别emoji> <对象>｜<目标>\""
    if not args.dry_run and not args.all:
        atomic_json(wm_path, {"last_poll_at": now_ms, "checked": len(sessions),
                              "pending": len(candidates),
                              "via_backfill": sum(1 for c in candidates if c["via"] == "backfill")})
    if args.compact:
        print(f"status={payload['status']} checked={len(sessions)} "
              f"候选={len(candidates)} 未到轮次={skipped_not_due}")
        for c in payload["candidates"]:
            print("=" * 60)
            print(f"session : {c['session']}")
            print(f"来源    : {c['via']}" + ("（从未命名）" if c["never_named"] else ""))
            print(f"status  : {c['status']}   轮次: {c['turn_count']}")
            print(f"现标题  : {c['current_title']}")
            print(f"首轮目标: {c['original_goal'][:160]}")
            users = [m["text"][:150] for t in c["recent_turns"]
                     for m in t["messages"] if m["role"] == "user"]
            for u in users[-2:]:
                print(f"近期用户: {u}")
        return 0
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_cleanup(args, root: Path, config: dict):
    """软删除自动化自身产生的历史会话，避免任务列表被轮询会话堆满。

    只改 `deleted_at`（与宿主删除会话的语义一致，可恢复），不碰标题与其它字段。
    默认保留最近 keep-minutes 分钟内有活动的会话 —— 这样就**不会删掉正在运行的本轮**，
    上一轮会在下一轮执行时被清掉，列表里最多留一条。
    """
    target = str(Path(args.cwd).expanduser()) if args.cwd else str(Path.cwd())
    needle = target.rstrip("\\/").lower()
    cutoff = int(time.time() * 1000) - args.keep_minutes * 60_000

    con = sqlite3.connect(db_path(), timeout=15, isolation_level=None)
    try:
        con.execute("PRAGMA busy_timeout=10000")
        rows = con.execute(
            "select id, title, cwd, updated_at from sessions where deleted_at is null").fetchall()
        targets = [r for r in rows
                   if (r[2] or "").rstrip("\\/").lower() == needle and (r[3] or 0) < cutoff]
        if not args.dry_run:
            now = int(time.time() * 1000)
            for sid, _t, _c, _u in targets:
                con.execute(
                    "update sessions set deleted_at=? where id=? and deleted_at is null", (now, sid))
    finally:
        con.close()

    print(json.dumps({
        "status": "cleaned", "cwd": target, "keep_minutes": args.keep_minutes,
        "dry_run": bool(args.dry_run),
        "deleted": 0 if args.dry_run else len(targets),
        "matched": len(targets),
        "sessions": [{"id": r[0], "title": r[1]} for r in targets],
    }, ensure_ascii=False, indent=2))
    return 0


def settings_path() -> Path:
    """桌面端 Hook 配置真源。

    实测纠正：`~/.codebuddy/settings.json` 是 CLI 的位置，**桌面端不读**，
    hooks 写在那里会一直不被触发。`~/.workbuddy/settings.json` 才是桌面端用户级配置。
    """
    override = os.environ.get("TOPIC_TITLE_SETTINGS")
    return Path(override).expanduser() if override else wb_home() / "settings.json"


def _usable_python(exe: str) -> bool:
    """判断一个 python 候选是否真能执行脚本。

    Windows 上 `python3`/`python` 常被 Microsoft Store 的「应用执行别名」劫持，
    指向 `AppInstallerPythonRedirector.exe` —— 在非交互 shell 里必然以 code 49 失败
    （Hook 执行日志原文：`Python was not found; run without arguments to install
    from the Microsoft Store...`）。因此必须真的跑一次，不能只看 `which`。
    """
    try:
        p = subprocess.run([exe, "-c", "import sys;print(sys.version_info[0])"],
                           capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return False
    return p.returncode == 0 and p.stdout.strip().startswith("3")


def find_python() -> str:
    """挑一个在 Hook 的 bash 环境里真能跑起来的 python 解释器。

    优先级：显式覆盖 > 与当前进程同源 > WorkBuddy 受管运行时 > PATH 候选。
    返回**绝对路径**，因为 Hook 的 shell 环境与当前沙箱不同，PATH 不可信。
    """
    override = os.environ.get("TOPIC_TITLE_PYTHON")
    candidates = []
    if override:
        candidates.append(override)
    candidates.append(sys.executable)          # 当前跑本脚本的解释器，最可靠
    bin_root = wb_home() / "binaries" / "python" / "versions"
    if bin_root.is_dir():
        for ver in sorted(bin_root.iterdir(), reverse=True):
            candidates.append(str(ver / "python.exe"))
            candidates.append(str(ver / "python3.exe"))
    candidates += ["python3", "python", "py"]

    seen = set()
    for exe in candidates:
        if not exe or exe in seen:
            continue
        seen.add(exe)
        if _usable_python(exe):
            return exe
    return "python3"  # 兜底，保持可读的错误提示


def hook_command() -> str:
    exe = os.environ.get("TOPIC_TITLE_PYTHON") or find_python()
    # 统一成正斜杠：Hook 由 bash 执行，反斜杠会被当成转义符
    return f'"{Path(exe).as_posix()}" -X utf8 "{Path(__file__).resolve().as_posix()}" hook'


def _load_settings() -> dict:
    path = settings_path()
    if not path.is_file():
        return {}
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")  # 容忍 BOM，写回时统一去 BOM
    value = json.loads(text) if text.strip() else {}
    return value if isinstance(value, dict) else {}


def _save_settings(data: dict):
    """原子写入，强制无 BOM、LF 换行（BOM 会让宿主整体解析失败）。"""
    path = settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".settings-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _norm_cmd(command: str) -> str:
    """归一化 hook 命令，便于比较是否为我们写下的那一条规范命令。"""
    return str(command or "").replace("\\", "/").strip().lower()


def _is_our_hook(command: str) -> bool:
    """判断某条 hook 命令是否属于本技能。

    只匹配 `topic-auto-title` 会漏掉一类**历史遗留注册**：早期把脚本副本
    放在别的工作区里（如 `<某工作区>/export/scripts/title.py`），命令串里
    根本没有技能目录名 —— 于是 `install-hook` 永远清不掉它，
    每个 Stop 事件会重复跑两遍（2026-09-23 实测：hook 反馈出现两份）。
    故同时认「引用了名为 title.py 的脚本」。
    """
    cmd = str(command or "").replace("\\", "/")
    if "topic-auto-title" in cmd:
        return True
    return re.search(r"/title\.py\b", cmd) is not None


def _strip_our_hook(entries: list) -> list:
    """从某个事件的规则数组里剔除本技能自己的 hook，保留其它工具的配置。"""
    kept = []
    for rule in entries if isinstance(entries, list) else []:
        if not isinstance(rule, dict):
            continue
        inner = [h for h in (rule.get("hooks") or [])
                 if not (isinstance(h, dict) and _is_our_hook(h.get("command", "")))]
        if inner:
            kept.append({**rule, "hooks": inner})
    return kept


def _our_rule():
    return {"hooks": [{"type": "command", "command": hook_command(), "timeout": 15}]}


def cmd_install_hook(args, root: Path, config: dict):
    """注册 Hook。

    两个事件都注册，原因：实测桌面端**只执行 `Stop`**，`UserPromptSubmit` 从未被执行
    （会话日志中执行记录 0 条）。但其它宿主/CLI 可能相反，故两个都挂、由脚本内部统一处理，
    互不冲突。`Stop` 走 `{"decision":"block"}` 通道，`UserPromptSubmit` 走 additionalContext 通道。
    """
    data = _load_settings()
    before_keys = list(data.keys())
    hooks = data.get("hooks")
    if not isinstance(hooks, dict):
        hooks = {}
    for event in ("Stop", "UserPromptSubmit"):
        existing = _strip_our_hook(hooks.get(event) or [])
        existing.append(_our_rule())
        hooks[event] = existing
    data["hooks"] = hooks
    _save_settings(data)

    raw = settings_path().read_bytes()
    verify = json.loads(raw.decode("utf-8-sig"))
    canonical = _norm_cmd(hook_command())
    events = {}
    dupes = {}
    for event in ("Stop", "UserPromptSubmit"):
        found = [h for rule in (verify["hooks"].get(event) or [])
                 for h in rule.get("hooks", [])
                 if _is_our_hook(h.get("command", ""))]
        # 「已注册」必须是**规范命令**在位，光有历史遗留副本不算
        events[event] = any(_norm_cmd(h.get("command", "")) == canonical for h in found)
        if len(found) > 1:
            dupes[event] = [h.get("command", "") for h in found]
    installed = all(events.values())
    print(json.dumps({
        "status": "installed" if installed else "failed",
        "settings": str(settings_path()),
        "bom": raw[:3] == b"\xef\xbb\xbf",
        "preserved_keys": before_keys,
        "all_keys": list(verify.keys()),
        "events": events,
        "command": hook_command(),
        "duplicates": dupes,
        "note": "桌面端实测只执行 Stop；UserPromptSubmit 一并注册以兼容其它宿主",
    }, ensure_ascii=False, indent=2))
    return 0 if installed else 1


def cmd_uninstall_hook(args, root: Path, config: dict):
    data = _load_settings()
    hooks = data.get("hooks")
    if isinstance(hooks, dict):
        for event in list(hooks.keys()):
            remaining = _strip_our_hook(hooks[event])
            if remaining:
                hooks[event] = remaining
            else:
                hooks.pop(event, None)
        if not hooks:
            data.pop("hooks", None)
        _save_settings(data)
    print(json.dumps({"status": "removed", "settings": str(settings_path())},
                     ensure_ascii=False, indent=2))
    return 0


def hook_config_state() -> dict:
    """检查 Hook 是否写在宿主真正读取的位置，挂了哪些事件，以及命令能否执行。

    这里最容易被误判成「Hook 没触发」的情况其实是**命令跑不起来**：
    注册项存在、宿主也调用了，但 shell 里的 `python3` 指向 Microsoft Store 的
    应用别名桩，进程以 code 49 退出，脚本一个字都没执行。因此必须把
    「解释器是否可用」和「注册是否生效」分开报告。
    """
    primary = settings_path()
    legacy = Path.home() / ".codebuddy" / "settings.json"

    def probe(path: Path):
        if not path.is_file():
            return {}
        try:
            raw = path.read_bytes()
            data = json.loads(raw.decode("utf-8-sig"))
        except (ValueError, OSError):
            return {}
        out = {}
        for event, rules in (data.get("hooks") or {}).items():
            if any(_is_our_hook(h.get("command", ""))
                   for rule in (rules or []) if isinstance(rule, dict)
                   for h in (rule.get("hooks") or [])):
                out[event] = True
        return out

    p, l = probe(primary), probe(legacy)
    # 实测：桌面端只执行 Stop，不执行 UserPromptSubmit
    effective = p.get("Stop") or l.get("Stop")

    # 注册项里用的解释器是否真能跑起来
    registered = ""
    for path in (primary, legacy):
        try:
            data = json.loads(path.read_bytes().decode("utf-8-sig")) if path.is_file() else {}
        except (ValueError, OSError):
            continue
        for rules in (data.get("hooks") or {}).values():
            for rule in (rules or []):
                if not isinstance(rule, dict):
                    continue
                for h in (rule.get("hooks") or []):
                    cmd = str(h.get("command", ""))
                    if _is_our_hook(cmd):
                        m = re.match(r'\s*"([^"]+)"', cmd)
                        registered = m.group(1) if m else cmd.split()[0]
                        break
    runner_ok = _usable_python(registered) if registered else False
    hint = None
    if not effective:
        hint = ("Stop 事件未注册：请运行 install-hook。桌面端实测只执行 Stop，"
                "只挂 UserPromptSubmit 不会生效")
    elif not runner_ok:
        hint = (f"Hook 已注册但解释器跑不起来：{registered or '(空)'}。"
                "Windows 上裸写 `python3` 常被 Microsoft Store 应用别名劫持（退出码 49），"
                "请重新运行 install-hook 写入绝对路径")
    return {
        "settings": str(primary),
        "events": p,
        "installed": bool(p),
        "effective": bool(effective),
        "legacy_path": str(legacy),
        "legacy_events": l,
        "interpreter": registered,
        "interpreter_ok": runner_ok,
        "hint": hint,
    }


def cmd_config(args, root: Path, config: dict):
    changes = read_json(root / "config.json")
    touched = False
    if args.every_n_turns is not None:
        changes["every_n_turns"] = args.every_n_turns
        touched = True
    if args.emit_context is not None:
        changes["emit_context"] = args.emit_context == "on"
        touched = True
    if args.max_candidates is not None:
        changes["max_candidates"] = args.max_candidates
        touched = True
    if touched:
        atomic_json(root / "config.json", changes)
    final = load_config(root)
    print(json.dumps({"status": "updated" if touched else "read",
                      "config": final, "file": str(root / "config.json")},
                     ensure_ascii=False, indent=2))
    return 0


def cmd_status(args, root: Path, config: dict):
    states = ([p for p in (root / "state").glob("*.json") if not p.stem.startswith("_")]
              if (root / "state").is_dir() else [])
    print(json.dumps({
        "config": config, "data_dir": str(root), "db": str(db_path()),
        "db_exists": db_path().is_file(), "tracked_sessions": len(states),
        "hook": hook_activity(root),
        "hook_config": hook_config_state(),
    }, ensure_ascii=False, indent=2))
    return 0


def main():
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass
    parser = argparse.ArgumentParser(description="WorkBuddy 话题标题自动命名")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("hook", help="UserPromptSubmit Hook 入口")
    p = sub.add_parser("context", help="输出命名所需的会话输入")
    p.add_argument("--session")
    p.add_argument("--cwd")
    p = sub.add_parser("apply", help="校验并写入标题")
    p.add_argument("--title", required=True)
    p.add_argument("--session")
    p.add_argument("--cwd")
    p.add_argument("--reason")
    p.add_argument("--allow-duplicate", action="store_true")
    sub.add_parser("status")
    sub.add_parser("install-hook", help="把 UserPromptSubmit Hook 写入 ~/.workbuddy/settings.json")
    sub.add_parser("uninstall-hook", help="移除本技能注册的 Hook")
    p = sub.add_parser("config", help="查看或修改配置（如每几轮注入一次）")
    p.add_argument("--every-n-turns", type=int, help="每 N 个用户轮次注入一次命名提醒（1~20）")
    p.add_argument("--emit-context", choices=["on", "off"], help="是否注入命名提醒")
    p.add_argument("--max-candidates", type=int, help="轮询一次最多返回几个候选")
    p = sub.add_parser("poll", help="供定时任务调用：挑出需要重新命名的会话")
    p.add_argument("--since-minutes", type=int)
    p.add_argument("--all", action="store_true", help="忽略水位，覆盖全部未删除会话（含已归档）")
    p.add_argument("--max", type=int, help="本次最多返回几个候选")
    p.add_argument("--include-self", action="store_true", help="不排除当前工作目录的会话")
    p.add_argument("--no-backfill", action="store_true",
                   help="只按时间窗口筛选，不补齐「从未命名过」的会话")
    p.add_argument("--dry-run", action="store_true", help="不推进水位，便于人工核对")
    p.add_argument("--compact", action="store_true", help="输出可读摘要而不是 JSON")
    p = sub.add_parser("cleanup", help="软删除自动化自身产生的历史会话，防止列表堆积")
    p.add_argument("--cwd", help="要清理的会话工作目录，默认当前目录")
    p.add_argument("--keep-minutes", type=int, default=10, help="保留最近 N 分钟内有活动的会话（默认 10）")
    p.add_argument("--dry-run", action="store_true", help="只列出将删除的会话，不实际删除")
    for name in ("pause", "resume"):
        sub.add_parser(name)
    for name in ("lock", "unlock"):
        p = sub.add_parser(name)
        p.add_argument("--session")
        p.add_argument("--cwd")
    args = parser.parse_args()

    if args.command == "hook":
        entry = Path(__file__).resolve().as_posix()
        print(run_hook(entry))
        return 0

    root = data_dir()
    try:
        config = load_config(root)
        if args.command in ("pause", "resume"):
            changes = read_json(root / "config.json")
            changes["enabled"] = args.command == "resume"
            atomic_json(root / "config.json", changes)
            print(json.dumps(load_config(root), ensure_ascii=False))
            return 0
        if args.command == "status":
            return cmd_status(args, root, config)
        if args.command == "install-hook":
            return cmd_install_hook(args, root, config)
        if args.command == "uninstall-hook":
            return cmd_uninstall_hook(args, root, config)
        if args.command == "config":
            return cmd_config(args, root, config)
        if args.command in ("lock", "unlock"):
            sid = resolve_session(args, root)
            if not sid:
                print(json.dumps({"status": "error", "message": "未找到会话"},
                                 ensure_ascii=False))
                return 1
            path = session_state_path(root, sid)
            state = read_json(path)
            state["locked"] = args.command == "lock"
            state["last_title"] = read_title(sid)
            state["updated_at"] = int(time.time())
            atomic_json(path, state)
            print(json.dumps({"status": args.command, "session": sid,
                              "title": state["last_title"]}, ensure_ascii=False))
            return 0
        if args.command == "context":
            return cmd_context(args, root, config)
        if args.command == "poll":
            return cmd_poll(args, root, config)
        if args.command == "cleanup":
            return cmd_cleanup(args, root, config)
        if args.command == "apply":
            return cmd_apply(args, root, config)
    except (ValueError, sqlite3.Error, OSError) as exc:
        print(json.dumps({"status": "error", "error_type": type(exc).__name__,
                          "message": str(exc)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
