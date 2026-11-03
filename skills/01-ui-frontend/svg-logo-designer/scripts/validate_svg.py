#!/usr/bin/env python3
"""Validate SVG logo files for structure, unsafe content, and portability."""

from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


FORBIDDEN_ELEMENTS = {"script", "foreignObject", "iframe", "object", "embed"}
HREF_NAMES = {"href", "{http://www.w3.org/1999/xlink}href"}
NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")
EXTERNAL_URL_RE = re.compile(r"url\(\s*['\"]?(?:https?:|//|data:)", re.IGNORECASE)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_input(path: str) -> bytes:
    if path == "-":
        return sys.stdin.buffer.read()
    return Path(path).read_bytes()


def validate(path: str) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        data = read_input(path)
    except OSError as exc:
        return {"path": path, "errors": [f"read failed: {exc}"], "warnings": []}

    upper = data.upper()
    if b"<!DOCTYPE" in upper or b"<!ENTITY" in upper:
        errors.append("DOCTYPE/ENTITY declarations are not allowed")

    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        errors.append(f"XML parse error: {exc}")
        return {"path": path, "errors": errors, "warnings": warnings}

    if local_name(root.tag) != "svg":
        errors.append("root element must be <svg>")

    view_box = root.attrib.get("viewBox")
    if not view_box:
        errors.append("missing viewBox")
    else:
        parts = NUMBER_RE.findall(view_box)
        if len(parts) != 4:
            errors.append("viewBox must contain four numbers")
        else:
            try:
                width, height = float(parts[2]), float(parts[3])
                if width <= 0 or height <= 0:
                    errors.append("viewBox width and height must be positive")
            except ValueError:
                errors.append("viewBox contains invalid numbers")

    ids: set[str] = set()
    duplicate_ids: set[str] = set()
    title_count = 0
    desc_count = 0
    text_count = 0

    for element in root.iter():
        name = local_name(element.tag)
        if name in FORBIDDEN_ELEMENTS:
            errors.append(f"forbidden element: <{name}>")
        if name == "title":
            title_count += 1
        elif name == "desc":
            desc_count += 1
        elif name == "text":
            text_count += 1

        element_id = element.attrib.get("id")
        if element_id:
            if element_id in ids:
                duplicate_ids.add(element_id)
            ids.add(element_id)

        for attr_name, value in element.attrib.items():
            attr_local = local_name(attr_name)
            if attr_local.lower().startswith("on"):
                errors.append(f"event-handler attribute not allowed: {attr_local}")
            if attr_name in HREF_NAMES or attr_local == "href":
                value = value.strip()
                if value and not value.startswith("#"):
                    errors.append(f"external or embedded resource not allowed: {attr_local}")
            if EXTERNAL_URL_RE.search(value):
                errors.append(f"external URL in attribute: {attr_local}")

    if duplicate_ids:
        errors.append("duplicate IDs: " + ", ".join(sorted(duplicate_ids)))
    if title_count == 0:
        warnings.append("missing <title>")
    if desc_count == 0:
        warnings.append("missing <desc>")
    if root.attrib.get("role") != "img":
        warnings.append('root should usually use role="img" for meaningful logos')
    if "aria-labelledby" not in root.attrib and root.attrib.get("aria-hidden") != "true":
        warnings.append("missing aria-labelledby (or aria-hidden for decorative SVG)")
    if text_count:
        warnings.append("contains <text>; verify font availability or convert approved lettering to paths")

    return {"path": path, "errors": sorted(set(errors)), "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="SVG paths; use - for stdin")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    results = [validate(path) for path in args.paths]
    failed = any(result["errors"] for result in results)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            errors = result["errors"]
            warnings = result["warnings"]
            status = "FAIL" if errors else "OK"
            print(f"[{status}] {result['path']}")
            for message in errors:
                print(f"  error: {message}")
            for message in warnings:
                print(f"  warning: {message}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
