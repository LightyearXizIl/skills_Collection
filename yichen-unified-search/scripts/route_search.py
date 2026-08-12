#!/usr/bin/env python3
"""Create an offline search route plan without invoking any backend."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PLATFORM_SITES = {
    "github": "github.com",
    "wechat": "mp.weixin.qq.com",
    "xiaohongshu": "xiaohongshu.com",
    "douyin": "douyin.com",
    "toutiao": "toutiao.com",
    "x": "x.com",
    "bilibili": "bilibili.com",
    "youtube": "youtube.com",
    "xiaoyuzhou": "xiaoyuzhoufm.com",
}

PLATFORM_HINTS = (
    ("xiaohongshu", (r"小红书", r"\bxiaohongshu\b", r"\bxhs\b")),
    ("douyin", (r"抖音", r"\bdouyin\b")),
    ("toutiao", (r"今日头条", r"\btoutiao\b")),
    ("wechat", (r"微信公众号", r"微信文章", r"\bweixin\b", r"\bwechat\b")),
    ("bilibili", (r"哔哩哔哩", r"B站", r"\bbilibili\b")),
    ("youtube", (r"\byoutube\b",)),
    ("xiaoyuzhou", (r"小宇宙", r"\bxiaoyuzhou\b")),
    ("github", (r"\bgithub\b", r"\bissue\b", r"\bpull request\b")),
    ("x", (r"推特", r"\btwitter\b", r"\bx\.com\b")),
)

ANYSEARCH_RUNTIME = Path(
    os.environ.get(
        "ANYSEARCH_RUNTIME_CONFIG",
        str(Path.home() / ".agents/skills/anysearch/runtime.conf"),
    )
).expanduser()


@dataclass(frozen=True)
class Request:
    queries: tuple[str, ...]
    platform: str
    mode: str
    input_kind: str
    limit: int
    days: int | None
    domain: str | None
    login_approved: bool
    private_data: bool
    candidate_url: str | None
    candidate_from_search: bool


def detect_platform(queries: Iterable[str]) -> str:
    text = " ".join(queries)
    for platform, patterns in PLATFORM_HINTS:
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            return platform
    return "web"


def is_url(value: str) -> bool:
    return (
        re.fullmatch(r"https?://[^\s]+", value.strip(), flags=re.IGNORECASE)
        is not None
    )


def contains_url(value: str) -> bool:
    return re.search(r"https?://[^\s]+", value, flags=re.IGNORECASE) is not None


def handoff_content_archive(reason: str) -> dict:
    return {
        "schema_version": "1.0",
        "status": "handoff_required",
        "reason": reason,
        "authorization": "not_applicable",
        "route": None,
        "handoff_skill": "yichen-content-archive",
        "steps": [],
        "limitations": [
            "Known-URL reading, downloading, and archiving are outside unified-search."
        ],
    }


def anysearch_steps(request: Request, queries: list[str]) -> list[dict]:
    max_results = min(request.limit, 10)
    steps: list[dict] = [
        {
            "action": "read_runtime",
            "path": str(ANYSEARCH_RUNTIME),
            "field": "Command",
        }
    ]
    if request.mode == "verify-candidate":
        if request.candidate_url is None:
            raise ValueError("verify-candidate requires candidate_url")
        steps.append(
            {
                "action": "invoke_anysearch",
                "subcommand": "extract",
                "argv": [request.candidate_url],
            }
        )
    elif request.mode == "batch" or len(queries) > 1:
        for offset in range(0, len(queries), 5):
            payload = [
                {"query": query, "max_results": max_results}
                for query in queries[offset : offset + 5]
            ]
            steps.append(
                {
                    "action": "invoke_anysearch",
                    "subcommand": "batch_search",
                    "argv": ["--queries", json.dumps(payload, ensure_ascii=False)],
                }
            )
    elif request.domain:
        steps.extend(
            [
                {
                    "action": "invoke_anysearch",
                    "subcommand": "get_sub_domains",
                    "argv": ["--domain", request.domain],
                },
                {
                    "action": "invoke_anysearch",
                    "subcommand": "search",
                    "argv": [
                        queries[0],
                        "--domain",
                        request.domain,
                        "--sub_domain",
                        "<from-get_sub_domains>",
                        "--sub_domain_params",
                        "<all-required-params>",
                        "--max_results",
                        str(max_results),
                    ],
                },
            ]
        )
    else:
        steps.append(
            {
                "action": "invoke_anysearch",
                "subcommand": "search",
                "argv": [queries[0], "--max_results", str(max_results)],
            }
        )
    return steps


def native_steps(platform: str, request: Request) -> list[dict]:
    query = request.queries[0]
    limit = request.limit
    days = request.days if request.days is not None else 1
    if platform == "x":
        arguments: dict[str, object] = {
            "query": query,
            "max_results": limit,
        }
        if request.days not in {None, 0}:
            arguments["hours"] = request.days * 24
        return [
            {
                "action": "invoke_plugin_tool",
                "backend": "grok-consult",
                "tool": "search_x_with_grok",
                "arguments": arguments,
                "primary_route": "official_grok_cli_account_quota",
                "account_oauth_used": True,
                "contains_read_only_chain": [
                    "official_grok_cli_account_quota",
                    "fxtwitter-public",
                    "opencli",
                    "xreach",
                ],
                "fxtwitter_when": "explicit_account_quota_exhausted_only",
                "must_stop_without_fallback_when": [
                    "authentication_error",
                    "authorization_error",
                    "invalid_request",
                    "timeout",
                    "network_error",
                    "service_error",
                    "unverified_native_search",
                ],
            },
        ]
    commands = {
        "github": ["gh", "search", "repos", query, "--limit", str(limit)],
        "wechat": [
            "opencli",
            "weixin",
            "search",
            query,
            "--page",
            "1",
            "--limit",
            str(limit),
        ],
        "xiaohongshu": [
            "opencli",
            "xiaohongshu",
            "search",
            query,
            "--days",
            str(days),
            "--content",
            "all",
            "--limit",
            str(min(limit, 30)),
            "--enrich",
            "-f",
            "yaml",
        ],
        "douyin": [
            "opencli",
            "douyin",
            "search",
            query,
            "--days",
            str(days),
            "--content",
            "all",
            "--limit",
            str(min(limit, 30)),
            "--enrich",
            "-f",
            "yaml",
        ],
        "toutiao": [
            "opencli",
            "toutiao",
            "search",
            query,
            "--days",
            str(days),
            "--limit",
            str(min(limit, 50)),
            "-f",
            "yaml",
        ],
        "bilibili": [
            "bili",
            "search",
            query,
            "--type",
            "video",
            "--page",
            "1",
            "-n",
            str(limit),
            "--json",
        ],
        "youtube": [
            "yt-dlp",
            "--flat-playlist",
            "--dump-single-json",
            f"ytsearch{limit}:{query}",
        ],
    }
    return [{"action": "invoke_existing_adapter", "argv": commands[platform]}]


def plan(request: Request) -> dict:
    if request.private_data:
        return {
            "schema_version": "1.0",
            "status": "blocked",
            "reason": "private collections, feeds, messages, drafts, and account backends are out of scope",
            "authorization": "not_applicable",
            "route": None,
            "steps": [],
            "limitations": ["This skill only searches public or authenticated-public content."],
        }

    queries_contain_url = any(contains_url(query) for query in request.queries)
    if request.input_kind == "known-url":
        return handoff_content_archive(
            "the request explicitly classifies its input as known content"
        )
    if queries_contain_url and request.input_kind != "url-seed":
        return handoff_content_archive(
            "a directly supplied known URL is not a search query"
        )
    if request.input_kind == "url-seed" and not queries_contain_url:
        return {
            "schema_version": "1.0",
            "status": "invalid_request",
            "reason": "input_kind url-seed requires a URL in the search query",
            "authorization": "not_applicable",
            "route": None,
            "steps": [],
            "limitations": [],
        }

    if request.mode == "verify-candidate":
        if not request.candidate_url or not is_url(request.candidate_url):
            return handoff_content_archive(
                "candidate verification requires a valid candidate URL"
            )
        if not request.candidate_from_search:
            return handoff_content_archive(
                "the URL was not marked as a candidate produced by the current search"
            )
        return {
            "schema_version": "1.0",
            "status": "ready",
            "authorization": "not_required",
            "route": {
                "platform": request.platform if request.platform != "auto" else "web",
                "backend": "anysearch",
                "mode": "verify-candidate",
                "reason": "verify_candidate_from_current_search",
                "login_state_used": False,
            },
            "steps": anysearch_steps(request, list(request.queries)),
            "limitations": [
                "Use extract only for original verification or light enrichment; do not download or archive."
            ],
        }

    platform = detect_platform(request.queries) if request.platform == "auto" else request.platform
    limitations: list[str] = []
    if request.input_kind == "url-seed":
        limitations.append(
            "The URL is used only as a discovery seed; this plan does not read, download, or archive the URL itself."
        )
    if request.days is not None:
        if platform in {"xiaohongshu", "douyin"} and request.days not in {0, 1, 7, 180}:
            return {
                "schema_version": "1.0",
                "status": "invalid_request",
                "reason": "xiaohongshu and douyin --days must be one of 0, 1, 7, or 180",
                "authorization": "not_applicable",
                "route": None,
                "steps": [],
                "limitations": [],
            }
        if platform == "toutiao" and not 1 <= request.days <= 30:
            return {
                "schema_version": "1.0",
                "status": "invalid_request",
                "reason": "toutiao --days must be between 1 and 30",
                "authorization": "not_applicable",
                "route": None,
                "steps": [],
                "limitations": [],
            }

    if request.mode == "batch" or request.domain or platform == "web":
        queries = list(request.queries)
        route_reason = "public_web_default"
        if request.mode == "batch" and platform in PLATFORM_SITES:
            site = PLATFORM_SITES[platform]
            queries = [f"site:{site} {query}" for query in queries]
            route_reason = "platform_batch_via_public_web_index"
            limitations.append(
                "Public site-index results are not equivalent to the platform's native or complete index."
            )
        if request.limit > 10:
            limitations.append(
                "AnySearch returns at most 10 candidates per query; the route plan clamps max_results to 10."
            )
        if request.days is not None:
            limitations.append(
                "The generic AnySearch route does not translate --days; express the time range in the query or discovered vertical parameters."
            )
        return {
            "schema_version": "1.0",
            "status": "ready",
            "authorization": "not_required",
            "route": {
                "platform": platform,
                "backend": "anysearch",
                "mode": request.mode,
                "reason": route_reason,
                "login_state_used": False,
            },
            "steps": anysearch_steps(request, queries),
            "limitations": limitations,
        }

    if platform == "xiaoyuzhou":
        query = f"site:{PLATFORM_SITES[platform]} {request.queries[0]}"
        return {
            "schema_version": "1.0",
            "status": "ready",
            "authorization": "not_required",
            "route": {
                "platform": platform,
                "backend": "anysearch",
                "mode": "search",
                "reason": "no_native_full_site_keyword_search",
                "login_state_used": False,
            },
            "steps": anysearch_steps(request, [query]),
            "limitations": [
                "This is public web discovery, not Xiaoyuzhou's complete native index.",
                *(
                    [
                        "AnySearch returns at most 10 candidates per query; the route plan clamps max_results to 10."
                    ]
                    if request.limit > 10
                    else []
                ),
            ],
        }

    if platform in {"xiaohongshu", "douyin"} and not request.login_approved:
        return {
            "schema_version": "1.0",
            "status": "needs_authorization",
            "authorization": "explicit_current_turn_chrome_login_required",
            "route": {
                "platform": platform,
                "backend": "opencli",
                "mode": "search",
                "reason": "platform_native_search",
                "login_state_used": True,
            },
            "steps": [],
            "limitations": [
                "State the platform, exact query, and result limit before asking for authorization."
            ],
        }

    backend = {
        "github": "gh",
        "wechat": "opencli-weixin-public",
        "xiaohongshu": "opencli",
        "douyin": "opencli",
        "toutiao": "opencli-toutiao-anonymous",
        "x": "grok-consult",
        "bilibili": "bili-cli",
        "youtube": "yt-dlp-flat-search",
    }.get(platform)
    if backend is None:
        raise ValueError(f"Unsupported platform: {platform}")

    if platform == "toutiao":
        limitations.append("Single keyword, low frequency, current public non-video results only.")
    if platform == "x":
        limitations.extend(
            [
                "Every X keyword search starts with official Grok CLI account OAuth and native x_search.",
                "Only explicit Grok account quota or usage-limit exhaustion may enter anonymous FxTwitter.",
                "Authentication, authorization, timeout, network, service, zero-result, and unverified-search failures must stop without FxTwitter fallback.",
                "After an eligible quota fallback, FxTwitter remains a third-party public index and is not an official or exhaustive X search.",
                "Stop and request authorization before any fallback reads a browser login state.",
            ]
        )

    return {
        "schema_version": "1.0",
        "status": "ready",
        "authorization": "approved" if request.login_approved else "not_required",
        "route": {
            "platform": platform,
            "backend": backend,
            "mode": "search",
            "reason": (
                "grok_native_x_search_primary"
                if platform == "x"
                else "platform_native_search"
            ),
            "login_state_used": platform in {"xiaohongshu", "douyin", "x"},
        },
        "steps": native_steps(platform, request),
        "limitations": limitations,
    }


def parse_args() -> Request:
    parser = argparse.ArgumentParser(
        description="Create an offline route plan; never invokes a search backend."
    )
    parser.add_argument("--query", action="append", required=True)
    parser.add_argument(
        "--platform",
        default="auto",
        choices=("auto", "web", *PLATFORM_SITES.keys()),
    )
    parser.add_argument(
        "--mode",
        choices=("search", "batch", "verify-candidate"),
        default="search",
    )
    parser.add_argument(
        "--input-kind",
        choices=("auto", "keyword", "url-seed", "known-url"),
        default="auto",
        help=(
            "Classify URLs safely: known-url hands off to content archive; "
            "url-seed keeps a URL inside a discovery query."
        ),
    )
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--days", type=int)
    parser.add_argument("--domain")
    parser.add_argument("--login-approved", action="store_true")
    parser.add_argument("--private-data", action="store_true")
    parser.add_argument("--candidate-url")
    parser.add_argument(
        "--candidate-from-search",
        action="store_true",
        help="Assert that --candidate-url came from the current unified-search result set.",
    )
    args = parser.parse_args()
    if not 1 <= args.limit <= 50:
        parser.error("--limit must be between 1 and 50")
    if args.days is not None and not 0 <= args.days <= 180:
        parser.error("--days must be between 0 and 180")
    if args.mode == "verify-candidate":
        if len(args.query) != 1:
            parser.error("--mode verify-candidate requires exactly one source --query")
        if not args.candidate_url:
            parser.error("--mode verify-candidate requires --candidate-url")
    elif args.candidate_url or args.candidate_from_search:
        parser.error(
            "--candidate-url and --candidate-from-search require --mode verify-candidate"
        )
    return Request(
        queries=tuple(args.query),
        platform=args.platform,
        mode=args.mode,
        input_kind=args.input_kind,
        limit=args.limit,
        days=args.days,
        domain=args.domain,
        login_approved=args.login_approved,
        private_data=args.private_data,
        candidate_url=args.candidate_url,
        candidate_from_search=args.candidate_from_search,
    )


def main() -> int:
    request = parse_args()
    print(json.dumps(plan(request), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
