#!/usr/bin/env python3
"""Local-only WeChat public-account search and article download client.

This client talks only to a loopback wechat-article-exporter. It never controls
WeChat, prints auth keys, or silently falls back to a remote service.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable


DEFAULT_API_BASE = "http://127.0.0.1:18901"
DEFAULT_KV_BASE = Path(
    os.environ.get(
        "WECHAT_ARTICLE_EXPORTER_KV",
        str(
            Path.home()
            / "Library/Application Support/wechat-article-exporter/kv"
        ),
    )
).expanduser()
URL_RE = re.compile(r"https?://mp\.weixin\.qq\.com/[^\s\"'<>]+", re.I)


class ClientError(RuntimeError):
    pass


class LoginRequired(ClientError):
    pass


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def run_id() -> str:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = hashlib.sha256(f"{stamp}-{time.time()}".encode()).hexdigest()[:8]
    return f"{stamp}-{suffix}"


def safe_name(value: str, fallback: str) -> str:
    value = re.sub(r"[\\/:*?\"<>|]+", "_", value or "").strip()
    value = re.sub(r"\s+", " ", value)
    return value[:100] or fallback


def strip_markup(value: Any) -> str:
    text = re.sub(r"<[^>]+>", "", str(value or ""))
    return html.unescape(text).strip()


def title_from_body(body: str, fmt: str, fallback: str) -> str:
    if fmt == "markdown":
        for line in body.splitlines()[:40]:
            if line.startswith("# "):
                return line[2:].strip() or fallback
    if fmt == "html":
        match = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
        if match:
            return re.sub(r"\s+", " ", match.group(1)).strip() or fallback
    if fmt == "json":
        try:
            payload = json.loads(body)
            if isinstance(payload, dict) and payload.get("title"):
                return str(payload["title"]).strip() or fallback
        except json.JSONDecodeError:
            pass
    return fallback


def ensure_local_api_base(value: str) -> str:
    normalized = value.rstrip("/")
    if normalized != DEFAULT_API_BASE:
        raise ClientError(f"API base is fixed to {DEFAULT_API_BASE}")
    return normalized


def make_opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


class LocalExporterClient:
    def __init__(self, api_base: str, kv_base: Path, timeout: int = 45):
        self.api_base = ensure_local_api_base(api_base)
        self.kv_base = kv_base.expanduser()
        self.timeout = timeout
        self.opener = make_opener()
        self._auth_key: str | None = None

    def request(
        self,
        path: str,
        query: dict[str, Any] | None = None,
        *,
        auth_key: str | None = None,
        expect_json: bool = True,
    ) -> Any:
        url = self.api_base + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        headers = {"User-Agent": "yichen-web-research-wechat-local/1.0"}
        if auth_key:
            headers["X-Auth-Key"] = auth_key
        req = urllib.request.Request(url, headers=headers)
        try:
            with self.opener.open(req, timeout=self.timeout) as resp:
                raw = resp.read()
                charset = resp.headers.get_content_charset() or "utf-8"
                text = raw.decode(charset, errors="replace")
                if expect_json:
                    return json.loads(text)
                return text
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(detail)
                detail = payload.get("statusMessage") or payload.get("message") or detail
            except json.JSONDecodeError:
                pass
            raise ClientError(f"local exporter HTTP {exc.code}: {detail[:300]}") from exc
        except urllib.error.URLError as exc:
            raise ClientError(f"local exporter unavailable at {self.api_base}: {exc.reason}") from exc

    def health(self) -> bool:
        try:
            self.request("/", expect_json=False)
            return True
        except ClientError:
            return False

    def _candidate_auth_keys(self) -> Iterable[str]:
        cookie_dir = self.kv_base / "cookie"
        if not cookie_dir.is_dir():
            return []
        paths = sorted(
            (path for path in cookie_dir.iterdir() if path.is_file()),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        return [path.name for path in paths]

    def current_auth_key(self) -> str:
        if self._auth_key:
            return self._auth_key
        for candidate in self._candidate_auth_keys():
            payload = self.request("/api/public/v1/authkey", auth_key=candidate)
            if isinstance(payload, dict) and payload.get("code") == 0:
                self._auth_key = candidate
                return candidate
        raise LoginRequired(
            f"login required; open {self.api_base}/dashboard/account and scan the QR code yourself"
        )

    def search_accounts(self, keyword: str, begin: int = 0, size: int = 5) -> list[dict[str, Any]]:
        payload = self.request(
            "/api/public/v1/account",
            {"keyword": keyword, "begin": begin, "size": size},
            auth_key=self.current_auth_key(),
        )
        base_resp = payload.get("base_resp", {}) if isinstance(payload, dict) else {}
        if base_resp.get("ret") != 0:
            raise ClientError(f"account search failed: {base_resp.get('err_msg', 'unknown error')}")
        return payload.get("list", [])

    def resolve_account(self, query: str) -> dict[str, Any]:
        accounts = self.search_accounts(query, size=5)
        normalized = query.casefold().strip()
        exact = [
            item
            for item in accounts
            if str(item.get("nickname", "")).casefold().strip() == normalized
            or str(item.get("alias", "")).casefold().strip() == normalized
        ]
        if len(exact) == 1:
            return exact[0]
        if len(accounts) == 1:
            return accounts[0]
        public_candidates = [
            {
                "nickname": item.get("nickname", ""),
                "alias": item.get("alias", ""),
                "fakeid": item.get("fakeid", ""),
            }
            for item in accounts
        ]
        if not public_candidates:
            raise ClientError(f"no public account matched: {query}")
        raise ClientError(
            "account name is ambiguous; use an exact nickname or alias. candidates="
            + json.dumps(public_candidates, ensure_ascii=False)
        )

    def list_articles(
        self,
        fakeid: str,
        *,
        keyword: str = "",
        limit: int = 100,
        page_size: int = 20,
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        seen: set[str] = set()
        begin = 0
        while len(rows) < limit:
            size = min(page_size, max(1, limit - len(rows)))
            payload = self.request(
                "/api/public/v1/article",
                {"fakeid": fakeid, "begin": begin, "size": size, "keyword": keyword},
                auth_key=self.current_auth_key(),
            )
            base_resp = payload.get("base_resp", {}) if isinstance(payload, dict) else {}
            if base_resp.get("ret") != 0:
                raise ClientError(f"article search failed: {base_resp.get('err_msg', 'unknown error')}")
            articles = payload.get("articles", [])
            if not articles:
                break
            for item in articles:
                url = str(item.get("link") or "").strip()
                if not url or url in seen:
                    continue
                seen.add(url)
                rows.append(item)
                if len(rows) >= limit:
                    break
            begin += size
        return rows

    def download(self, url: str, fmt: str) -> str:
        return self.request(
            "/api/public/v1/download",
            {"url": url, "format": fmt},
            expect_json=False,
        )


def extract_urls(text: str) -> list[str]:
    return [match.group(0).rstrip("），。；,;") for match in URL_RE.finditer(text)]


def read_urls(files: Iterable[str], inline: Iterable[str]) -> list[str]:
    urls: list[str] = []
    for value in inline:
        urls.extend(extract_urls(value))
    for value in files:
        path = Path(value).expanduser()
        urls.extend(extract_urls(path.read_text(encoding="utf-8")))
    return list(dict.fromkeys(urls))


def read_account_queries(files: Iterable[str], inline: Iterable[str]) -> list[str]:
    values = [item.strip() for item in inline if item.strip()]
    for value in files:
        path = Path(value).expanduser()
        values.extend(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    return list(dict.fromkeys(values))


def article_row(item: dict[str, Any], account: dict[str, Any]) -> dict[str, Any]:
    timestamp = item.get("update_time") or item.get("create_time") or 0
    published_at = ""
    if isinstance(timestamp, (int, float)) and timestamp > 0:
        published_at = dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc).isoformat()
    return {
        "account_name": account.get("nickname", ""),
        "account_alias": account.get("alias", ""),
        "fakeid": account.get("fakeid", ""),
        "title": strip_markup(item.get("title", "")),
        "url": item.get("link", ""),
        "author": item.get("author_name", ""),
        "digest": strip_markup(item.get("digest", "")),
        "published_at": published_at,
        "copyright_type": item.get("copyright_type"),
        "copyright_stat": item.get("copyright_stat"),
        "is_deleted": bool(item.get("is_deleted", False)),
    }


def allocate_unique_directory(base: Path) -> Path:
    for attempt in range(1, 10_001):
        candidate = base if attempt == 1 else base.with_name(f"{base.name}-run-{attempt}")
        try:
            candidate.mkdir(parents=True, exist_ok=False)
            return candidate
        except FileExistsError:
            continue
    raise ClientError(f"无法分配不冲突的输出目录: {base}")


def prepare_output_directory(
    requested: str,
    default_parent: Path,
    *,
    resume_existing: bool,
) -> tuple[Path, Path | None]:
    if resume_existing and not requested:
        raise ClientError("--resume-existing 必须同时显式提供既有 --output-dir")
    if requested:
        target = Path(requested).expanduser().resolve()
        if target.exists():
            if not target.is_dir():
                raise ClientError(f"用户指定的输出路径不是目录: {target}")
            if not resume_existing:
                raise ClientError(
                    f"用户指定的输出目录已存在，默认拒绝写入: {target}"
                )
            resume_dir = allocate_unique_directory(
                target.with_name(f"{target.name}-resume-{run_id()}")
            )
            return resume_dir, target
        if resume_existing:
            raise ClientError(f"--resume-existing 要求既有输出目录: {target}")
        target.mkdir(parents=True, exist_ok=False)
        return target, None
    return allocate_unique_directory(default_parent / run_id()), None


def successful_urls_from(directory: Path | None) -> set[str]:
    if directory is None:
        return set()
    index_path = directory / "index.csv"
    if not index_path.is_file():
        return set()
    completed: set[str] = set()
    with index_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("status") == "success" and row.get("url"):
                completed.add(str(row["url"]))
    return completed


def write_text_exclusive(path: Path, content: str) -> None:
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(content)
    except FileExistsError as exc:
        raise ClientError(f"拒绝覆盖既有输出文件: {path}") from exc


def write_json(path: Path, value: Any) -> None:
    write_text_exclusive(
        path,
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
    )


def download_rows(
    client: LocalExporterClient,
    rows: list[dict[str, Any]],
    output_dir: Path,
    fmt: str,
    sleep_seconds: float,
) -> dict[str, Any]:
    article_dir = output_dir / "articles"
    article_dir.mkdir(parents=True, exist_ok=False)
    suffix = {"markdown": ".md", "html": ".html", "text": ".txt", "json": ".json"}[fmt]
    index_rows: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []
    for position, row in enumerate(rows, 1):
        seq = f"{position:03d}"
        url = str(row.get("url") or "")
        title = str(row.get("title") or f"article-{seq}")
        try:
            body = client.download(url, fmt)
            if not title or title.startswith("article-"):
                title = title_from_body(body, fmt, title or f"article-{seq}")
                row["title"] = title
            relative = Path("articles") / f"{seq}-{safe_name(title, f'article-{seq}')}{suffix}"
            write_text_exclusive(output_dir / relative, body)
            index_rows.append(
                {
                    **{key: str(value) for key, value in row.items()},
                    "path": str(relative),
                    "status": "success",
                    "error": "",
                }
            )
        except Exception as exc:
            error = str(exc)
            index_rows.append(
                {
                    **{key: str(value) for key, value in row.items()},
                    "path": "",
                    "status": "failed",
                    "error": error,
                }
            )
            errors.append({"url": url, "error": error})
        if sleep_seconds > 0 and position < len(rows):
            time.sleep(sleep_seconds)

    fieldnames = [
        "account_name",
        "account_alias",
        "fakeid",
        "title",
        "url",
        "author",
        "digest",
        "published_at",
        "copyright_type",
        "copyright_stat",
        "is_deleted",
        "path",
        "status",
        "error",
    ]
    with (output_dir / "index.csv").open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(index_rows)
    write_json(output_dir / "errors.json", errors)
    return {
        "success_count": sum(1 for item in index_rows if item["status"] == "success"),
        "failure_count": len(errors),
        "failed_urls": [item["url"] for item in errors],
    }


def command_status(client: LocalExporterClient) -> int:
    service_ok = client.health()
    payload = {
        "ok": service_ok,
        "service_url": client.api_base,
        "localhost_only": client.api_base == DEFAULT_API_BASE,
        "service_reachable": service_ok,
        "login_status": "not_checked",
        "kv_directory_exists": client.kv_base.is_dir(),
        "private_session_read": False,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if service_ok else 1


def command_login(client: LocalExporterClient, should_open: bool) -> int:
    url = client.api_base + "/dashboard/account"
    if should_open:
        subprocess.run(["open", url], check=True)
    print(
        json.dumps(
            {"ok": True, "login_url": url, "manual_action": "scan QR and confirm on your phone"},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def command_download(client: LocalExporterClient, args: argparse.Namespace) -> int:
    urls = read_urls(args.file, args.urls)
    if not urls:
        raise ClientError("no mp.weixin.qq.com URLs found")
    output_dir, resume_from = prepare_output_directory(
        args.output_dir,
        Path.home() / "Downloads" / "yichen-web-research-wechat",
        resume_existing=args.resume_existing,
    )
    completed_urls = successful_urls_from(resume_from)
    pending_urls = [url for url in urls if url not in completed_urls]
    rows = [
        {
            "account_name": "",
            "account_alias": "",
            "fakeid": "",
            "title": f"article-{index:03d}",
            "url": url,
            "author": "",
            "digest": "",
            "published_at": "",
            "copyright_type": "",
            "copyright_stat": "",
            "is_deleted": "",
        }
        for index, url in enumerate(pending_urls, 1)
    ]
    result = download_rows(client, rows, output_dir, args.format, args.sleep)
    payload = {
        "ok": result["failure_count"] == 0,
        "output_dir": str(output_dir),
        "resume_from": str(resume_from) if resume_from else None,
        "skipped_existing_count": len(urls) - len(pending_urls),
        **result,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


def command_search(client: LocalExporterClient, args: argparse.Namespace) -> int:
    if not args.allow_local_account_session:
        raise ClientError(
            "search reads a local exporter account session; obtain current-turn "
            "authorization, then pass --allow-local-account-session"
        )
    queries = read_account_queries(args.accounts_file, args.account)
    if not queries:
        raise ClientError("provide --account or --accounts-file")
    output_dir, resume_from = prepare_output_directory(
        args.output_dir,
        Path.home() / "Downloads" / "yichen-web-research-wechat-search",
        resume_existing=args.resume_existing,
    )
    completed_urls = successful_urls_from(resume_from)
    client.current_auth_key()

    resolved: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    rows: list[dict[str, Any]] = []
    for query in queries:
        try:
            account = client.resolve_account(query)
            resolved.append(
                {
                    "query": query,
                    "nickname": account.get("nickname", ""),
                    "alias": account.get("alias", ""),
                    "fakeid": account.get("fakeid", ""),
                }
            )
            items = client.list_articles(
                str(account.get("fakeid", "")),
                keyword=args.article_keyword,
                limit=args.limit_per_account,
            )
            rows.extend(article_row(item, account) for item in items)
        except Exception as exc:
            failures.append({"query": query, "error": str(exc)})

    deduped = list({str(row["url"]): row for row in rows if row.get("url")}.values())
    pending_rows = [
        row for row in deduped if str(row.get("url") or "") not in completed_urls
    ]
    write_json(output_dir / "accounts.json", resolved)
    write_json(output_dir / "articles.json", deduped)
    write_json(output_dir / "search-errors.json", failures)
    write_text_exclusive(
        output_dir / "urls.txt",
        "\n".join(str(row["url"]) for row in deduped) + ("\n" if deduped else ""),
    )

    download_result: dict[str, Any] | None = None
    if args.download and pending_rows:
        download_result = download_rows(
            client,
            pending_rows,
            output_dir,
            args.format,
            args.sleep,
        )

    payload = {
        "ok": not failures and (not download_result or download_result["failure_count"] == 0),
        "output_dir": str(output_dir),
        "resume_from": str(resume_from) if resume_from else None,
        "account_count": len(resolved),
        "article_count": len(deduped),
        "skipped_existing_count": len(deduped) - len(pending_rows),
        "search_failure_count": len(failures),
        "download": download_result,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local-only WeChat public-account search and download")
    parser.add_argument("--timeout", type=int, default=45)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status")
    login = subparsers.add_parser("login")
    login.add_argument("--open", action="store_true")

    download = subparsers.add_parser("download")
    download.add_argument("urls", nargs="*")
    download.add_argument("--file", action="append", default=[])
    download.add_argument("--output-dir", default="")
    download.add_argument(
        "--resume-existing",
        action="store_true",
        help=(
            "Read successful URLs from an existing --output-dir, then write only pending "
            "items into a new sibling <name>-resume-* directory; never modify the existing run"
        ),
    )
    download.add_argument(
        "--format", choices=["markdown", "html", "text", "json"], default="markdown"
    )
    download.add_argument("--sleep", type=float, default=0.2)

    search = subparsers.add_parser("search")
    search.add_argument("--account", action="append", default=[])
    search.add_argument("--accounts-file", action="append", default=[])
    search.add_argument("--article-keyword", default="")
    search.add_argument("--limit-per-account", type=int, default=100)
    search.add_argument("--output-dir", default="")
    search.add_argument(
        "--resume-existing",
        action="store_true",
        help=(
            "Use an existing --output-dir only as a read-only checkpoint and write the "
            "new enumeration/download into a new sibling <name>-resume-* directory"
        ),
    )
    search.add_argument("--download", action="store_true")
    search.add_argument(
        "--format", choices=["markdown", "html", "text", "json"], default="markdown"
    )
    search.add_argument("--sleep", type=float, default=0.2)
    search.add_argument(
        "--allow-local-account-session",
        action="store_true",
        help=(
            "Confirm current-turn authorization to read the local exporter's "
            "account session for this exact account query"
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        client = LocalExporterClient(DEFAULT_API_BASE, DEFAULT_KV_BASE, args.timeout)
        if args.command == "status":
            return command_status(client)
        if args.command == "login":
            return command_login(client, args.open)
        if args.command == "download":
            return command_download(client, args)
        if args.command == "search":
            return command_search(client, args)
        raise ClientError(f"unknown command: {args.command}")
    except LoginRequired as exc:
        print(
            json.dumps(
                {"ok": False, "login_required": True, "error": str(exc)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 3
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
