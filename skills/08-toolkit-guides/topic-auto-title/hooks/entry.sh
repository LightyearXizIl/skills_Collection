#!/usr/bin/env bash
# topic-auto-title 的 Hook 入口脚本（兼容层）。
#
# 用途：当宿主无法用注册命令直接调 Python 时，可把 Hook 指向本脚本。
# 本脚本按顺序探测可用解释器，**每个候选都真跑一次验证**，最后无论成败都输出合法 JSON。
#
# 为什么不能只用 `command -v python3` 判断：
#   Windows 上 `python3` 常被 Microsoft Store 的「应用执行别名」劫持，
#   指向 AppInstallerPythonRedirector.exe。`command -v` 会返回成功，
#   但非交互执行必然退出码 49、脚本一个字都不跑。
#   ⇒ 必须真的执行一次来验证。
#
# 需要处理的三个 Windows 环境问题：
#   1. Hook 在 Git Bash 中执行，PATH 不可信 → 逐个探测并验证
#   2. Windows 上的 Python 需要 Windows 风格路径（POSIX /c/... 会被解析成 C:\c\...）
#   3. 中文 Windows 的 Python 默认用 GBK 输出，必须强制 UTF-8，否则注入内容乱码

export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1

DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$DIR/../scripts/title.py"

# Windows 风格路径
if command -v cygpath >/dev/null 2>&1; then
  SCRIPT="$(cygpath -m "$SCRIPT")"
fi

# 验证候选解释器是否真能执行（关键：不能只看 command -v）
usable() {
  [ -n "$1" ] || return 1
  "$1" -c 'import sys;sys.exit(0 if sys.version_info[0]==3 else 1)' >/dev/null 2>&1
}

OUT=""

# 按优先级收集候选，命中第一个可用者即停止
# 1) 显式覆盖
# 2) PATH 中的解释器
# 3) WorkBuddy / CodeBuddy 受管运行时（不硬编码用户名）
# 4) Windows Python Launcher
CANDIDATES=""
[ -n "${TOPIC_TITLE_PYTHON:-}" ] && CANDIDATES="$TOPIC_TITLE_PYTHON"
CANDIDATES="$CANDIDATES python3 python"

for HOME_DIR in "$HOME" "$USERPROFILE"; do
  [ -n "$HOME_DIR" ] || continue
  for BASE in "$HOME_DIR/.workbuddy" "$HOME_DIR/.codebuddy"; do
    for CAND in "$BASE"/binaries/python/versions/*/python.exe "$BASE"/binaries/python/versions/*/python3.exe; do
      [ -e "$CAND" ] && CANDIDATES="$CANDIDATES $CAND"
    done
  done
done
CANDIDATES="$CANDIDATES py"

for PY in $CANDIDATES; do
  if usable "$PY"; then
    OUT="$("$PY" -X utf8 "$SCRIPT" hook 2>/dev/null)"
    break
  fi
done

[ -n "$OUT" ] || OUT="{}"
printf '%s\n' "$OUT"
