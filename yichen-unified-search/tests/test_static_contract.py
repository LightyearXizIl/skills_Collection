import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


class StaticContractTests(unittest.TestCase):
    def test_frontmatter_has_only_name_and_description(self):
        text = SKILL.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
        self.assertIsNotNone(match)
        keys = []
        for line in match.group(1).splitlines():
            if line and not line.startswith((" ", "\t")) and ":" in line:
                keys.append(line.split(":", 1)[0])
        self.assertEqual(keys, ["name", "description"])

    def test_required_contract_language_is_present(self):
        text = SKILL.read_text(encoding="utf-8")
        required = (
            "AnySearch",
            "绝对不得操控微信",
            "不下载媒体",
            "不读取、同步或搜索私人收藏",
            "candidate-schema.md",
            "routes.md",
            "doctor_yichen.py",
            "$yichen-content-archive",
            "本次搜索所得候选",
            "官方 Grok CLI",
            "明确额度耗尽",
            "FxTwitter",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_linked_files_exist(self):
        for relative in (
            "references/routes.md",
            "references/candidate-schema.md",
            "scripts/route_search.py",
        ):
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_router_does_not_import_network_clients(self):
        text = (ROOT / "scripts" / "route_search.py").read_text(encoding="utf-8")
        for forbidden in ("requests", "urllib", "http.client", "subprocess"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)

    def test_fxtwitter_adapter_is_a_separate_runtime_step(self):
        adapter = ROOT / "scripts" / "fxtwitter_search.py"
        self.assertTrue(adapter.is_file())
        source = adapter.read_text(encoding="utf-8")
        self.assertIn("https://api.fxtwitter.com/2/search", source)
        self.assertIn("no automatic pagination or retry", source)

    def test_frontmatter_does_not_trigger_on_known_url_reading(self):
        text = SKILL.read_text(encoding="utf-8")
        frontmatter = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL).group(1)
        self.assertNotIn("URL 正文提取", frontmatter)
        self.assertIn("不用于读取或下载用户直接给出的已知 URL", frontmatter)

    def test_generic_extract_mode_is_removed(self):
        router = (ROOT / "scripts" / "route_search.py").read_text(encoding="utf-8")
        self.assertNotIn('choices=("search", "batch", "extract")', router)
        self.assertIn("verify-candidate", router)


if __name__ == "__main__":
    unittest.main()
