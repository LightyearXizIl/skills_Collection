#!/usr/bin/env python3
"""Copy the bundled cut-motion runtime into a new isolated workspace."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare an isolated cut-motion workspace from the bundled runtime."
    )
    parser.add_argument("target", help="Absolute path to the new workspace")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parent.parent
    source = (skill_root / "assets" / "runtime").resolve()
    target = Path(args.target).expanduser()

    if not target.is_absolute():
        print("Error: target must be an absolute path.", file=sys.stderr)
        return 64

    target = target.resolve()
    if target == source or skill_root in target.parents:
        print("Error: workspace must be outside the installed Skill directory.", file=sys.stderr)
        return 64

    if not source.is_dir() or not (source / "AGENTS.md").is_file():
        print("Error: bundled cut-motion runtime is incomplete.", file=sys.stderr)
        return 66

    if target.exists() and any(target.iterdir()):
        print(f"Error: destination is not empty: {target}", file=sys.stderr)
        return 73

    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, dirs_exist_ok=True)
    print(f"Prepared cut-motion workspace: {target}")
    print("Next: read AGENTS.md, then run the documented environment preflight.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
