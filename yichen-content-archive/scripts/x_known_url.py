#!/usr/bin/env python3
"""Read one known public X URL without using an account login state."""

from __future__ import annotations

import argparse
import json
import math
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any


FX_API = "https://api.fxtwitter.com/2"
JINA_READER = "https://r.jina.ai/http://x.com"
USER_AGENT = "yichen-content-archive/1.0 (+known public X URL reader)"
MAX_JSON_BYTES = 12 * 1024 * 1024
MAX_MARKDOWN_BYTES = 6 * 1024 * 1024
ALLOWED_HOSTS = {
    "x.com",
    "www.x.com",
    "twitter.com",
    "www.twitter.com",
    "mobile.twitter.com",
}


class KnownUrlError(RuntimeError):
    """A safe public error that never contains credentials."""

    def __init__(self, category: str, message: str) -> None:
        super().__init__(message)
        self.category = category
        self.message = message


def text_or_none(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None


def number_or_none(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not math.isfinite(value):
        return None
    return value


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_known_url(value: str) -> dict[str, str | None]:
    try:
        parsed = urllib.parse.urlsplit(value.strip())
    except ValueError as exc:
        raise KnownUrlError("invalid_url", "The supplied X URL is invalid.") from exc
    host = (parsed.hostname or "").lower()
    if parsed.scheme not in {"http", "https"} or host not in ALLOWED_HOSTS:
        raise KnownUrlError(
            "unsupported_url",
            "Only explicit x.com or twitter.com status and Article URLs are accepted.",
        )

    status_match = re.fullmatch(
        r"/(?P<handle>[^/]+)/status/(?P<id>\d+)(?:/.*)?",
        parsed.path.rstrip("/"),
    )
    if status_match:
        return {
            "input_kind": "x_status_url",
            "id": status_match.group("id"),
            "handle": status_match.group("handle"),
            "canonical_url": (
                f"https://x.com/{status_match.group('handle')}/status/"
                f"{status_match.group('id')}"
            ),
        }

    web_status_match = re.fullmatch(
        r"/i/(?:web/)?status/(?P<id>\d+)(?:/.*)?",
        parsed.path.rstrip("/"),
    )
    if web_status_match:
        return {
            "input_kind": "x_status_url",
            "id": web_status_match.group("id"),
            "handle": None,
            "canonical_url": f"https://x.com/i/status/{web_status_match.group('id')}",
        }

    article_match = re.fullmatch(
        r"/i/article/(?P<id>\d+)(?:/.*)?",
        parsed.path.rstrip("/"),
    )
    if article_match:
        return {
            "input_kind": "x_article_url",
            "id": article_match.group("id"),
            "handle": None,
            "canonical_url": f"https://x.com/i/article/{article_match.group('id')}",
        }

    raise KnownUrlError(
        "unsupported_url",
        "The URL is not a supported X status or Article URL.",
    )


def read_limited(response: Any, limit: int) -> bytes:
    body = response.read(limit + 1)
    if len(body) > limit:
        raise KnownUrlError("response_too_large", "The public response was too large.")
    return body


def fetch_json(path: str, *, query: dict[str, str | int] | None, timeout: int) -> dict:
    url = f"{FX_API}{path}"
    if query:
        url = f"{url}?{urllib.parse.urlencode(query)}"
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = read_limited(response, MAX_JSON_BYTES)
    except urllib.error.HTTPError as exc:
        category = {
            400: "invalid_request",
            404: "not_found",
            429: "rate_limited",
        }.get(exc.code, "upstream_http_error")
        raise KnownUrlError(
            category,
            f"FxTwitter returned HTTP {exc.code}.",
        ) from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise KnownUrlError(
            "network_error",
            "FxTwitter could not be reached.",
        ) from exc
    try:
        payload = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise KnownUrlError("invalid_response", "FxTwitter returned invalid JSON.") from exc
    if not isinstance(payload, dict):
        raise KnownUrlError("invalid_response", "FxTwitter returned an unexpected response.")
    if payload.get("code") != 200:
        raise KnownUrlError(
            "upstream_api_error",
            f"FxTwitter returned API code {payload.get('code')!r}.",
        )
    return payload


def status_from_payload(payload: dict[str, Any]) -> dict[str, Any]:
    status = payload.get("status")
    if not isinstance(status, dict) or status.get("type") == "tombstone":
        raise KnownUrlError("not_found", "The public status is unavailable.")
    return status


def find_article_parent(
    results: Any,
    article_id: str,
) -> dict[str, Any] | None:
    if not isinstance(results, list):
        return None
    for result in results:
        if not isinstance(result, dict):
            continue
        article = result.get("article")
        if isinstance(article, dict) and str(article.get("id")) == article_id:
            return result
        quote = result.get("quote")
        if isinstance(quote, dict):
            quote_article = quote.get("article")
            if (
                isinstance(quote_article, dict)
                and str(quote_article.get("id")) == article_id
            ):
                return quote
    return None


def canonical_status_url(status: dict[str, Any]) -> str | None:
    status_id = text_or_none(status.get("id"))
    if not status_id:
        return None
    author = status.get("author")
    handle = (
        text_or_none(author.get("screen_name"))
        if isinstance(author, dict)
        else None
    )
    if handle:
        return f"https://x.com/{handle}/status/{status_id}"
    return f"https://x.com/i/status/{status_id}"


def author_projection(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    return {
        "id": text_or_none(value.get("id")),
        "name": text_or_none(value.get("name")),
        "screen_name": text_or_none(value.get("screen_name")),
        "followers": number_or_none(value.get("followers")),
        "verified": (
            value.get("verification", {}).get("verified")
            if isinstance(value.get("verification"), dict)
            else None
        ),
    }


def media_url(media_info: Any) -> str | None:
    if not isinstance(media_info, dict):
        return None
    return text_or_none(
        media_info.get("original_img_url")
        or media_info.get("media_url_https")
        or media_info.get("media_url")
        or media_info.get("url")
        or media_info.get("thumbnail_url")
    )


def article_media(article: dict[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entity in article.get("media_entities", []):
        if not isinstance(entity, dict):
            continue
        url = media_url(entity.get("media_info"))
        if not url or url in seen:
            continue
        seen.add(url)
        output.append(
            {
                "id": text_or_none(entity.get("media_id"))
                or text_or_none(entity.get("media_key"))
                or text_or_none(entity.get("id")),
                "url": url,
            }
        )
    return output


def entity_map_by_key(content: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = content.get("entityMap")
    if isinstance(raw, dict):
        return {
            str(key): value
            for key, value in raw.items()
            if isinstance(value, dict)
        }
    if isinstance(raw, list):
        output = {}
        for item in raw:
            if not isinstance(item, dict):
                continue
            key = item.get("key")
            value = item.get("value")
            if key is not None and isinstance(value, dict):
                output[str(key)] = value
        return output
    return {}


def utf16_to_python_index(text: str, code_units: int) -> int:
    consumed = 0
    for index, character in enumerate(text):
        if consumed >= code_units:
            return index
        consumed += 2 if ord(character) > 0xFFFF else 1
    return len(text)


def apply_link_entities(
    text: str,
    ranges: Any,
    entities: dict[str, dict[str, Any]],
) -> str:
    if not isinstance(ranges, list):
        return text
    replacements = []
    for value in ranges:
        if not isinstance(value, dict):
            continue
        entity = entities.get(str(value.get("key")))
        if not isinstance(entity, dict) or entity.get("type") != "LINK":
            continue
        data = entity.get("data")
        url = text_or_none(data.get("url")) if isinstance(data, dict) else None
        offset = value.get("offset")
        length = value.get("length")
        if not url or not isinstance(offset, int) or not isinstance(length, int):
            continue
        start = utf16_to_python_index(text, offset)
        end = utf16_to_python_index(text, offset + length)
        if end > start:
            replacements.append((start, end, url))
    rendered = text
    for start, end, url in sorted(replacements, reverse=True):
        label = rendered[start:end]
        rendered = f"{rendered[:start]}[{label}]({url}){rendered[end:]}"
    return rendered


def media_lookup(article: dict[str, Any]) -> dict[str, str]:
    output: dict[str, str] = {}
    for item in article_media(article):
        if item["id"]:
            output[str(item["id"])] = item["url"]
            match = re.search(r"(\d{8,})$", str(item["id"]))
            if match:
                output[match.group(1)] = item["url"]
    return output


def render_atomic(
    block: dict[str, Any],
    entities: dict[str, dict[str, Any]],
    media_by_id: dict[str, str],
) -> str:
    ranges = block.get("entityRanges")
    if not isinstance(ranges, list) or not ranges:
        return ""
    entity = entities.get(str(ranges[0].get("key")))
    if not isinstance(entity, dict) or entity.get("type") != "MEDIA":
        return ""
    data = entity.get("data")
    if not isinstance(data, dict):
        return ""
    caption = text_or_none(data.get("caption")) or "X Article media"
    media_items = data.get("mediaItems")
    if isinstance(media_items, list):
        for media_item in media_items:
            if not isinstance(media_item, dict):
                continue
            media_id = text_or_none(media_item.get("mediaId"))
            url = media_by_id.get(media_id or "")
            if url:
                return f"![{caption}]({url})"
    return ""


def render_article_markdown(article: dict[str, Any]) -> str | None:
    content = article.get("content")
    if not isinstance(content, dict):
        return None
    blocks = content.get("blocks")
    if not isinstance(blocks, list):
        return None
    entities = entity_map_by_key(content)
    media_by_id = media_lookup(article)
    lines: list[str] = []
    ordered_index = 0
    previous_type = None
    for block in blocks:
        if not isinstance(block, dict):
            continue
        block_type = text_or_none(block.get("type")) or "unstyled"
        text = text_or_none(block.get("text")) or ""
        text = apply_link_entities(text, block.get("entityRanges"), entities)
        if block_type == "atomic":
            rendered = render_atomic(block, entities, media_by_id)
        elif block_type == "header-one":
            rendered = f"# {text}"
        elif block_type == "header-two":
            rendered = f"## {text}"
        elif block_type == "header-three":
            rendered = f"### {text}"
        elif block_type == "blockquote":
            rendered = "\n".join(f"> {line}" for line in text.splitlines())
        elif block_type == "unordered-list-item":
            rendered = f"- {text}"
        elif block_type == "ordered-list-item":
            ordered_index = ordered_index + 1 if previous_type == block_type else 1
            rendered = f"{ordered_index}. {text}"
        elif block_type == "code-block":
            rendered = f"```\n{text}\n```"
        else:
            rendered = text
        previous_type = block_type
        if rendered:
            lines.append(rendered)
    markdown = "\n\n".join(lines).strip()
    return markdown or None


def article_projection(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    article_id = text_or_none(value.get("id"))
    title = text_or_none(value.get("title"))
    preview = text_or_none(value.get("preview_text"))
    if not any((article_id, title, preview)):
        return None
    cover = None
    cover_media = value.get("cover_media")
    if isinstance(cover_media, dict):
        cover = media_url(cover_media.get("media_info"))
    markdown = render_article_markdown(value)
    return {
        "id": article_id,
        "title": title,
        "preview_text": preview,
        "cover_url": cover,
        "body_markdown": markdown,
        "block_count": (
            len(value.get("content", {}).get("blocks", []))
            if isinstance(value.get("content"), dict)
            and isinstance(value.get("content", {}).get("blocks"), list)
            else 0
        ),
        "media": article_media(value),
    }


def quote_projection(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    if value.get("type") == "tombstone":
        return {
            "availability": text_or_none(value.get("reason")) or "unavailable",
            "id": text_or_none(value.get("id")),
            "url": text_or_none(value.get("url")),
        }
    return {
        "availability": "public",
        "id": text_or_none(value.get("id")),
        "url": canonical_status_url(value),
        "text": text_or_none(value.get("text")),
        "author": author_projection(value.get("author")),
        "article": article_projection(value.get("article")),
    }


def normalize_status(status: dict[str, Any]) -> dict[str, Any]:
    article = article_projection(status.get("article"))
    quote = quote_projection(status.get("quote"))
    content_type = "x_article" if article else "x_quote_post" if quote else "x_post"
    return {
        "content_type": content_type,
        "id": text_or_none(status.get("id")),
        "url": canonical_status_url(status),
        "text": text_or_none(status.get("text")),
        "created_at": text_or_none(status.get("created_at")),
        "lang": text_or_none(status.get("lang")),
        "author": author_projection(status.get("author")),
        "metrics": {
            "likes": number_or_none(status.get("likes")),
            "reposts": number_or_none(status.get("reposts")),
            "quotes": number_or_none(status.get("quotes")),
            "replies": number_or_none(status.get("replies")),
            "bookmarks": number_or_none(status.get("bookmarks")),
            "views": number_or_none(status.get("views")),
        },
        "media": status.get("media") if isinstance(status.get("media"), dict) else None,
        "quote": quote,
        "article": article,
    }


def fetch_status(status_id: str, *, timeout: int) -> dict[str, Any]:
    return status_from_payload(fetch_json(f"/status/{status_id}", query=None, timeout=timeout))


def resolve_article(article_id: str, *, timeout: int) -> dict[str, Any]:
    search = fetch_json(
        "/search",
        query={"q": article_id, "feed": "latest", "count": 10},
        timeout=timeout,
    )
    parent = find_article_parent(search.get("results"), article_id)
    if parent is None:
        raise KnownUrlError(
            "article_parent_not_found",
            "The public index did not return an exact parent status for this Article ID.",
        )
    status_id = text_or_none(parent.get("id"))
    if status_id is None:
        raise KnownUrlError(
            "invalid_response",
            "The exact Article match did not contain a parent status ID.",
        )
    return fetch_status(status_id, timeout=timeout)


def jina_target_url(status_url: str) -> str:
    parsed = urllib.parse.urlsplit(status_url)
    return f"{JINA_READER}{parsed.path}"


def fetch_jina(status_url: str, *, timeout: int) -> str:
    request = urllib.request.Request(
        jina_target_url(status_url),
        headers={"Accept": "text/markdown", "User-Agent": USER_AGENT},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = read_limited(response, MAX_MARKDOWN_BYTES)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise KnownUrlError("jina_unavailable", "Jina Reader could not read the status.") from exc
    try:
        markdown = body.decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise KnownUrlError("invalid_response", "Jina Reader returned invalid text.") from exc
    lowered = markdown.lower()
    if not markdown or "log in to x" in lowered or "sign in to x" in lowered:
        raise KnownUrlError("login_wall", "Jina Reader reached an X login page.")
    return markdown


def authenticated_fallbacks(
    parsed: dict[str, str | None],
    status_url: str | None,
    content_type: str | None = None,
) -> list[dict[str, Any]]:
    target = status_url or parsed["canonical_url"]
    if (
        parsed["input_kind"] == "x_article_url"
        or content_type == "x_article"
    ):
        opencli_argv = ["opencli", "twitter", "article", target, "-f", "md"]
    else:
        opencli_argv = [
            "opencli",
            "twitter",
            "thread",
            target,
            "--limit",
            "1",
            "-f",
            "json",
        ]
    fallbacks = [
        {
            "backend": "opencli-twitter",
            "argv": opencli_argv,
            "login_state_used": True,
            "requires_current_turn_authorization": True,
        }
    ]
    if status_url or parsed["input_kind"] == "x_status_url":
        fallbacks.append(
            {
                "backend": "xreach",
                "argv": [
                    "xreach",
                    "--cookie-source",
                    "chrome",
                    "--json",
                    "tweet",
                    target,
                ],
                "login_state_used": True,
                "requires_current_turn_authorization": True,
            }
        )
    return fallbacks


def read_known_url(
    value: str,
    *,
    timeout: int,
    allow_jina_fallback: bool,
) -> dict[str, Any]:
    parsed = parse_known_url(value)
    errors: list[dict[str, str]] = []
    status = None
    normalized = None
    backend = None
    jina_markdown = None

    try:
        if parsed["input_kind"] == "x_article_url":
            status = resolve_article(str(parsed["id"]), timeout=timeout)
        else:
            status = fetch_status(str(parsed["id"]), timeout=timeout)
        normalized = normalize_status(status)
        backend = "fxtwitter-public"
        is_article = (
            parsed["input_kind"] == "x_article_url"
            or normalized.get("content_type") == "x_article"
        )
        if (
            is_article
            and (
                not normalized.get("article")
                or not normalized["article"].get("body_markdown")
            )
        ):
            errors.append(
                {
                    "backend": backend,
                    "category": "article_body_incomplete",
                    "message": "FxTwitter returned the Article parent without a full body.",
                }
            )
    except KnownUrlError as exc:
        errors.append(
            {
                "backend": "fxtwitter-public",
                "category": exc.category,
                "message": exc.message,
            }
        )

    status_url = normalized.get("url") if isinstance(normalized, dict) else None
    content_type = (
        normalized.get("content_type")
        if isinstance(normalized, dict)
        else None
    )
    is_article = (
        parsed["input_kind"] == "x_article_url"
        or content_type == "x_article"
    )
    needs_public_fallback = normalized is None or (
        is_article
        and (
            not normalized.get("article")
            or not normalized["article"].get("body_markdown")
        )
    )
    if allow_jina_fallback and needs_public_fallback and status_url:
        try:
            jina_markdown = fetch_jina(status_url, timeout=timeout)
            backend = "jina-reader"
        except KnownUrlError as exc:
            errors.append(
                {
                    "backend": "jina-reader",
                    "category": exc.category,
                    "message": exc.message,
                }
            )
    elif (
        allow_jina_fallback
        and needs_public_fallback
        and parsed["input_kind"] == "x_status_url"
    ):
        try:
            jina_markdown = fetch_jina(str(parsed["canonical_url"]), timeout=timeout)
            backend = "jina-reader"
        except KnownUrlError as exc:
            errors.append(
                {
                    "backend": "jina-reader",
                    "category": exc.category,
                    "message": exc.message,
                }
            )

    success = normalized is not None or jina_markdown is not None
    complete = bool(
        normalized
        and (
            not is_article
            or (
                normalized.get("article")
                and normalized["article"].get("body_markdown")
            )
        )
    ) or bool(jina_markdown)
    return {
        "schema_version": "1.0",
        "status": "success" if complete else "partial" if success else "failed",
        "input": parsed,
        "route": {
            "backend_used": backend,
            "login_state_used": False,
            "discovery_performed": False,
            "retrieved_at": utc_now_iso(),
        },
        "content": normalized,
        "jina_markdown": jina_markdown,
        "authenticated_fallbacks": (
            []
            if complete
            else authenticated_fallbacks(parsed, status_url, content_type)
        ),
        "errors": errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read one known public X status or Article URL anonymously."
    )
    parser.add_argument("url")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--no-jina-fallback", action="store_true")
    args = parser.parse_args()
    if not 5 <= args.timeout <= 60:
        parser.error("--timeout must be between 5 and 60 seconds")
    return args


def main() -> int:
    args = parse_args()
    try:
        result = read_known_url(
            args.url,
            timeout=args.timeout,
            allow_jina_fallback=not args.no_jina_fallback,
        )
    except KnownUrlError as exc:
        result = {
            "schema_version": "1.0",
            "status": "failed",
            "input": None,
            "route": {
                "backend_used": None,
                "login_state_used": False,
                "discovery_performed": False,
                "retrieved_at": utc_now_iso(),
            },
            "content": None,
            "jina_markdown": None,
            "authenticated_fallbacks": [],
            "errors": [
                {
                    "backend": None,
                    "category": exc.category,
                    "message": exc.message,
                }
            ],
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
