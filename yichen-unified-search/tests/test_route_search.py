import importlib.util
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "route_search", ROOT / "scripts" / "route_search.py"
)
ROUTER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = ROUTER
SPEC.loader.exec_module(ROUTER)


def request(**overrides):
    values = {
        "queries": ("agent memory best practices",),
        "platform": "auto",
        "mode": "search",
        "input_kind": "auto",
        "limit": 10,
        "days": None,
        "domain": None,
        "login_approved": False,
        "private_data": False,
        "candidate_url": None,
        "candidate_from_search": False,
    }
    values.update(overrides)
    return ROUTER.Request(**values)


class RouteTests(unittest.TestCase):
    def test_general_web_defaults_to_anysearch(self):
        result = ROUTER.plan(request())
        self.assertEqual(result["route"]["backend"], "anysearch")
        self.assertEqual(result["status"], "ready")

    def test_vertical_search_discovers_subdomains_first(self):
        result = ROUTER.plan(request(domain="legal"))
        self.assertEqual(result["steps"][1]["subcommand"], "get_sub_domains")
        self.assertEqual(result["steps"][2]["subcommand"], "search")

    def test_batch_platform_scope_uses_public_site_index(self):
        result = ROUTER.plan(
            request(
                queries=("topic one", "topic two"),
                platform="xiaohongshu",
                mode="batch",
            )
        )
        self.assertEqual(result["route"]["backend"], "anysearch")
        payload = result["steps"][1]["argv"][1]
        self.assertIn("site:xiaohongshu.com", payload)
        self.assertTrue(result["limitations"])

    def test_anysearch_clamps_per_query_limit_to_ten(self):
        result = ROUTER.plan(request(limit=50))
        self.assertEqual(result["steps"][1]["argv"][-1], "10")
        self.assertTrue(result["limitations"])

    def test_anysearch_batch_is_split_into_groups_of_five(self):
        queries = tuple(f"query {index}" for index in range(11))
        result = ROUTER.plan(request(queries=queries, mode="batch"))
        batch_steps = [
            step for step in result["steps"] if step.get("subcommand") == "batch_search"
        ]
        self.assertEqual(len(batch_steps), 3)

    def test_xiaohongshu_requires_current_turn_authorization(self):
        result = ROUTER.plan(request(platform="xiaohongshu"))
        self.assertEqual(result["status"], "needs_authorization")
        self.assertEqual(result["steps"], [])

    def test_xiaohongshu_routes_after_authorization(self):
        result = ROUTER.plan(request(platform="xiaohongshu", login_approved=True))
        self.assertEqual(result["route"]["backend"], "opencli")
        self.assertTrue(result["route"]["login_state_used"])

    def test_invalid_xiaohongshu_days_is_rejected_offline(self):
        result = ROUTER.plan(request(platform="xiaohongshu", days=30))
        self.assertEqual(result["status"], "invalid_request")
        self.assertEqual(result["steps"], [])

    def test_invalid_toutiao_days_is_rejected_offline(self):
        result = ROUTER.plan(request(platform="toutiao", days=180))
        self.assertEqual(result["status"], "invalid_request")
        self.assertEqual(result["steps"], [])

    def test_wechat_search_is_public_and_never_uses_wechat_ui(self):
        result = ROUTER.plan(request(platform="wechat"))
        self.assertEqual(result["route"]["backend"], "opencli-weixin-public")
        self.assertFalse(result["route"]["login_state_used"])

    def test_x_routes_to_grok_then_fxtwitter_only_on_quota(self):
        result = ROUTER.plan(request(platform="x"))
        self.assertEqual(result["route"]["backend"], "grok-consult")
        self.assertTrue(result["route"]["login_state_used"])
        self.assertEqual(result["steps"][0]["backend"], "grok-consult")
        self.assertEqual(result["steps"][0]["tool"], "search_x_with_grok")
        self.assertEqual(
            result["steps"][0]["fxtwitter_when"],
            "explicit_account_quota_exhausted_only",
        )
        self.assertEqual(
            result["steps"][0]["contains_read_only_chain"],
            [
                "official_grok_cli_account_quota",
                "fxtwitter-public",
                "opencli",
                "xreach",
            ],
        )
        self.assertIn(
            "timeout",
            result["steps"][0]["must_stop_without_fallback_when"],
        )

    def test_x_days_is_forwarded_to_grok_as_hours(self):
        result = ROUTER.plan(request(platform="x", days=1))
        self.assertEqual(result["steps"][0]["arguments"]["hours"], 24)

    def test_xiaoyuzhou_keyword_search_uses_public_site_discovery(self):
        result = ROUTER.plan(request(platform="xiaoyuzhou"))
        self.assertEqual(result["route"]["backend"], "anysearch")
        self.assertIn("site:xiaoyuzhoufm.com", result["steps"][1]["argv"][0])

    def test_private_data_is_blocked(self):
        result = ROUTER.plan(request(private_data=True))
        self.assertEqual(result["status"], "blocked")
        self.assertIsNone(result["route"])

    def test_direct_known_url_handoffs_to_content_archive(self):
        result = ROUTER.plan(request(queries=("https://example.com/article",)))
        self.assertEqual(result["status"], "handoff_required")
        self.assertEqual(result["handoff_skill"], "yichen-content-archive")
        self.assertEqual(result["steps"], [])

    def test_known_url_embedded_in_instruction_also_handoffs(self):
        result = ROUTER.plan(
            request(queries=("请读一下 https://example.com/article",))
        )
        self.assertEqual(result["status"], "handoff_required")
        self.assertEqual(result["handoff_skill"], "yichen-content-archive")

    def test_url_can_be_an_explicit_discovery_seed(self):
        result = ROUTER.plan(
            request(
                queries=(
                    "搜索引用 https://example.com/research 的公开报道",
                ),
                platform="web",
                input_kind="url-seed",
            )
        )
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["route"]["backend"], "anysearch")
        self.assertIn("discovery seed", " ".join(result["limitations"]))

    def test_url_seed_without_url_is_rejected(self):
        result = ROUTER.plan(request(input_kind="url-seed"))
        self.assertEqual(result["status"], "invalid_request")
        self.assertEqual(result["steps"], [])

    def test_explicit_known_url_always_handoffs(self):
        result = ROUTER.plan(
            request(
                queries=("请搜索这个网页",),
                input_kind="known-url",
            )
        )
        self.assertEqual(result["status"], "handoff_required")
        self.assertEqual(result["handoff_skill"], "yichen-content-archive")

    def test_unprovenanced_candidate_url_handoffs_to_content_archive(self):
        result = ROUTER.plan(
            request(
                mode="verify-candidate",
                candidate_url="https://example.com/article",
            )
        )
        self.assertEqual(result["status"], "handoff_required")
        self.assertEqual(result["handoff_skill"], "yichen-content-archive")

    def test_current_search_candidate_can_use_extract_for_verification(self):
        result = ROUTER.plan(
            request(
                mode="verify-candidate",
                candidate_url="https://example.com/article",
                candidate_from_search=True,
            )
        )
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["route"]["mode"], "verify-candidate")
        self.assertEqual(result["steps"][1]["subcommand"], "extract")
        self.assertEqual(
            result["steps"][1]["argv"], ["https://example.com/article"]
        )


if __name__ == "__main__":
    unittest.main()
