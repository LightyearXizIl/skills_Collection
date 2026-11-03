#!/usr/bin/env python3
"""Validate workflow definition files after direct edits."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


def find_repo_root(script_path: Path) -> Path:
    """Find the checkout root from both bundled and provisioned Skill layouts."""
    candidates = list(script_path.resolve().parents)
    configured_root = (
        os.getenv("DETERMINFLOW_ROOT")
        or os.getenv("AI_COMPANY_ROOT", "")
    ).strip()
    if configured_root:
        candidates.append(Path(configured_root).expanduser().resolve())
    for candidate in dict.fromkeys(candidates):
        if (candidate / "src" / "workflow" / "definition.py").is_file():
            return candidate
    raise RuntimeError(
        "无法定位 DeterminFlow 仓库根目录；应在仓库内运行已安装的 workflow-guide"
    )


REPO_ROOT = find_repo_root(Path(__file__))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.workflow.definition import WorkflowDef  # noqa: E402


PLACEHOLDER_RE = re.compile(r"{{\s*([A-Za-z0-9_.\[\]-]+)\s*}}")
SYSTEM_PREFIXES = ("_system.",)


def discover(target: str) -> list[Path]:
    if target == "--all":
        root = REPO_ROOT / "data" / "workflows"
        return sorted(root.glob("*/definition.json"))
    path = Path(target).expanduser().resolve()
    if path.is_file():
        return [path]
    if (path / "definition.json").is_file():
        return [path / "definition.json"]
    return sorted(path.rglob("definition.json"))


def validate_file(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"无法读取 JSON: {exc}"], warnings
    if not isinstance(payload, dict):
        return ["顶层必须是 JSON object"], warnings

    try:
        definition = WorkflowDef.from_dict(payload)
        errors.extend(definition.auto_pair_gateways())
        errors.extend(definition.validate())
    except (TypeError, ValueError, KeyError) as exc:
        errors.append(f"定义反序列化失败: {exc}")
        return errors, warnings

    ids = [node.id for node in definition.nodes] + [gateway.id for gateway in definition.gateways]
    duplicates = sorted({item for item in ids if ids.count(item) > 1})
    if duplicates:
        errors.append(f"节点或网关 ID 重复: {', '.join(duplicates)}")

    variable_keys = [variable.key for variable in definition.variables]
    bad_keys = sorted(key for key in variable_keys if key.startswith("_"))
    if bad_keys:
        errors.append(f"变量 key 使用了保留前缀 _: {', '.join(bad_keys)}")
    duplicate_vars = sorted({key for key in variable_keys if variable_keys.count(key) > 1})
    if duplicate_vars:
        errors.append(f"变量 key 重复: {', '.join(duplicate_vars)}")

    for node in definition.nodes:
        if not node.label:
            warnings.append(f"节点 {node.id} 缺少 label")
        if not isinstance(node.position, dict) or not {"x", "y"}.issubset(node.position):
            warnings.append(f"节点 {node.id} 缺少完整 position")

    declared = set(variable_keys)
    referenced: set[str] = set()
    for node in payload.get("nodes", []):
        blob = json.dumps(node, ensure_ascii=False)
        for raw in PLACEHOLDER_RE.findall(blob):
            root = raw.split("[", 1)[0].split(".", 1)[0]
            if not raw.startswith(SYSTEM_PREFIXES):
                referenced.add(root)
    undefined = sorted(referenced - declared)
    if undefined:
        warnings.append(f"引用但未声明的变量: {', '.join(undefined)}")
    unused_inputs = sorted(
        variable.key
        for variable in definition.variables
        if variable.source_type == "input" and variable.key not in referenced and not variable.hidden
    )
    if unused_inputs:
        warnings.append(f"声明但未引用的输入变量: {', '.join(unused_inputs)}")

    if path.parent.name != definition.workflow_id:
        warnings.append(
            f"目录名 {path.parent.name} 与 workflow_id {definition.workflow_id} 不一致"
        )
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", help="definition.json 或工作流目录")
    parser.add_argument("--all", action="store_true", dest="validate_all", help="校验所有工作流")
    args = parser.parse_args()
    if args.validate_all and args.target:
        parser.error("--all 不能与 target 同时使用")
    target = "--all" if args.validate_all else args.target
    if not target:
        parser.error("请提供 target 或 --all")
    paths = discover(target)
    if not paths:
        parser.error("未找到 definition.json")

    failed = False
    for path in paths:
        errors, warnings = validate_file(path)
        label = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
        print(f"[{('FAIL' if errors else 'PASS')}] {label}")
        for warning in warnings:
            print(f"  WARNING: {warning}")
        for error in errors:
            print(f"  ERROR: {error}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
