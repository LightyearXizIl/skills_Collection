#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
ROUTES = json.loads((ROOT / "tests" / "routes.json").read_text(encoding="utf-8"))


class BookmarksExportContractTest(unittest.TestCase):
    def test_frontmatter_and_reference(self):
        match = re.match(r"^---\n(.*?)\n---\n", SKILL, re.S)
        self.assertIsNotNone(match)
        keys = {
            line.split(":", 1)[0]
            for line in match.group(1).splitlines()
            if line and not line.startswith(" ")
        }
        self.assertEqual(keys, {"name", "description"})
        self.assertIn("name: yichen-bookmarks-export", match.group(1))
        for platform in ("小红书", "抖音", "X/Twitter"):
            self.assertIn(platform, match.group(1))
        self.assertTrue((ROOT / "references" / "handoff-contract.md").is_file())

    def test_static_safety_gates(self):
        required = [
            "当轮授权",
            "不得执行搜索或发现",
            "不得下载媒体、正文、字幕或附件",
            "不得调用 `$yichen-content-archive`",
            "不得再次调用 `$yichen-bookmarks-export`",
            "~/.agents/skills/yichen-social-bookmarks-exporter",
            "download_authorized_this_turn",
            "不删除文件",
        ]
        for marker in required:
            self.assertIn(marker, SKILL)
        self.assertFalse((ROOT / "scripts").exists())

    def test_only_one_execution_route(self):
        execution_routes = {
            row["route_skill"]
            for row in ROUTES
            if "route_skill" in row
        }
        self.assertEqual(execution_routes, {"yichen-social-bookmarks-exporter"})
        for row in ROUTES:
            if not row["authorized_this_turn"]:
                self.assertEqual(row["decision"], "ask_authorization")
            if row["requested_action"] == "export_and_download":
                self.assertEqual(row["decision"], "export_only")
                self.assertFalse(row["download_authorized"])
            if row["requested_action"] == "search_bookmarks":
                self.assertEqual(row["decision"], "reject")

    def test_handoff_contract_is_identical(self):
        sibling = (
            ROOT.parent
            / "yichen-content-archive"
            / "references"
            / "handoff-contract.md"
        )
        self.assertTrue(sibling.is_file())
        self.assertEqual(
            (ROOT / "references" / "handoff-contract.md").read_bytes(),
            sibling.read_bytes(),
        )


if __name__ == "__main__":
    unittest.main()
