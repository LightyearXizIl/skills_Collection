#!/usr/bin/env python3

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class RouterContractTests(unittest.TestCase):
    def test_router_names_all_children(self) -> None:
        source = (ROOT / "yichen-web-research/SKILL.md").read_text(encoding="utf-8")
        for name in (
            "yichen-unified-search",
            "yichen-content-archive",
            "yichen-bookmarks-export",
            "yichen-asr",
        ):
            self.assertIn(name, source)

    def test_router_is_the_only_top_level_entry(self) -> None:
        retired_name = "agent" + "-reach"
        self.assertFalse((ROOT / retired_name).exists())
        source = (ROOT / "yichen-web-research/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("唯一的互联网研究总入口", source)
        self.assertIn("Use when an internet-research request", source)

    def test_download_executors_have_single_source(self) -> None:
        archive_scripts = ROOT / "yichen-content-archive/scripts"
        router_scripts = ROOT / "yichen-web-research/scripts"
        for name in (
            "wechat_mp_local.py",
            "xiaoyuzhou_stepfun.py",
            "xiaoyuzhou_opencli.py",
            "x_known_url.py",
        ):
            self.assertTrue((archive_scripts / name).is_file())
            self.assertFalse((router_scripts / name).exists())
        self.assertEqual(
            {path.name for path in router_scripts.glob("*.py")},
            {"doctor_yichen.py", "validate_family.py"},
        )

    def test_search_and_archive_do_not_auto_chain(self) -> None:
        search = (ROOT / "yichen-unified-search/SKILL.md").read_text(
            encoding="utf-8"
        )
        archive = (ROOT / "yichen-content-archive/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("不下载媒体、不归档", search)
        self.assertIn("不得执行关键词搜索", archive)

    def test_x_search_and_known_url_have_separate_children(self) -> None:
        router = (ROOT / "yichen-web-research/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Grok CLI 原生 `x_search` 优先", router)
        self.assertIn("匿名 FxTwitter → Jina 优先", router)

    def test_asr_uses_unified_child_route(self) -> None:
        router = (ROOT / "yichen-web-research/SKILL.md").read_text(
            encoding="utf-8"
        )
        asr = (ROOT / "yichen-asr/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("| `$yichen-asr` |", router)
        self.assertIn("Step ASR 与豆包 ASR", asr)
        self.assertIn("不得跨服务商重提", asr)

    def test_trigger_matrix_has_unambiguous_expected_skill(self) -> None:
        matrix = json.loads(
            (ROOT / "yichen-web-research/tests/trigger_matrix.json").read_text(
                encoding="utf-8"
            )
        )
        by_case = {row["case"]: row["expected_skill"] for row in matrix}
        self.assertEqual(
            by_case["four_platform_search_only"],
            "yichen-unified-search",
        )
        self.assertEqual(
            by_case["search_then_archive"],
            "yichen-web-research",
        )
        self.assertEqual(
            by_case["negative_opinion_daily_report"],
            "public-opinion-monitor",
        )
        self.assertEqual(len(by_case), len(matrix))

    def test_public_opinion_does_not_claim_generic_search(self) -> None:
        path = ROOT / "public-opinion-monitor/SKILL.md"
        if not path.is_file():
            self.skipTest("optional public-opinion-monitor is not installed")
        source = path.read_text(
            encoding="utf-8"
        )
        frontmatter = source.split("---", 2)[1]
        self.assertNotIn("“四平台搜索”", frontmatter)
        self.assertIn("普通跨平台关键词搜索", frontmatter)
        self.assertIn("yichen-unified-search", frontmatter)
        self.assertIn("当轮明确授权", source)
        self.assertIn("--allow-chrome-login", source)

    def test_bookmark_backend_contains_no_download_commands(self) -> None:
        source = (
            ROOT / "yichen-bookmarks-export/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("不得下载媒体、正文、字幕或附件", source)
        self.assertIn("导出授权不等于下载授权", source)


if __name__ == "__main__":
    unittest.main()
