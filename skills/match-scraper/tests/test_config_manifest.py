import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATASOURCES = ROOT / "config" / "datasources.json"
ENDPOINTS = ROOT / "config" / "endpoints.json"

EURO_CIDS = {
    80, 545, 281, 90, 177, 432, 115, 82, 81, 104, 255,
    110, 2, 474, 649, 800, 482, 386, 826, 16, 1129,
}
CHANGE_CIDS = {1, 3, 8, 12, 47, 42, 48}
NON_ROSTER_CIDS = {71, 370, 18, 517, 976}


class ContractDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datasources = json.loads(DATASOURCES.read_text(encoding="utf-8"))
        cls.endpoints = json.loads(ENDPOINTS.read_text(encoding="utf-8"))
        cls.primary = cls.datasources["datasources"]["primary_odds"]
        cls.roster = cls.primary["tracked_bookmakers"]

    def test_endpoint_manifest_has_28_unique_keys(self):
        endpoints = self.endpoints["endpoints"]
        keys = [entry["key"] for entry in endpoints]
        self.assertEqual(len(endpoints), 28)
        self.assertEqual(len(set(keys)), 28)
        self.assertEqual(
            Counter(entry["group"] for entry in endpoints),
            Counter({"core": 4, "ah": 7, "ou": 7, "eu": 7, "polymarket": 1, "panorama": 2}),
        )
        for entry in endpoints:
            self.assertTrue(entry["required"], entry["key"])
            self.assertTrue(entry["url"], entry["key"])
            self.assertTrue(entry["encoding"], entry["key"])
            self.assertTrue(entry["empty_state"], entry["key"])

    def test_change_endpoint_keys_match_change_cids(self):
        keys = {entry["key"] for entry in self.endpoints["endpoints"]}
        for group in ("ah", "ou", "eu"):
            for cid in CHANGE_CIDS:
                self.assertIn(f"{group}_{cid}.html", keys)

    def test_roster_has_23_slots_and_exact_cid_sets(self):
        self.assertEqual(len(self.roster), 23)
        names = [entry["official_name"] for entry in self.roster]
        self.assertEqual(len(set(names)), 23)
        euro = [entry["euro_cid"] for entry in self.roster if entry["euro_cid"] is not None]
        change = [entry["change_cid"] for entry in self.roster if entry["change_cid"] is not None]
        self.assertEqual(len(euro), 21)
        self.assertEqual(len(set(euro)), 21)
        self.assertEqual(set(euro), EURO_CIDS)
        self.assertEqual(len(change), 7)
        self.assertEqual(len(set(change)), 7)
        self.assertEqual(set(change), CHANGE_CIDS)

    def test_188bet_and_polymarket_are_special_cases(self):
        by_name = {entry["official_name"]: entry for entry in self.roster}
        self.assertIsNone(by_name["188Bet"]["euro_cid"])
        self.assertEqual(by_name["188Bet"]["change_cid"], 42)
        self.assertIsNone(by_name["Polymarket"]["euro_cid"])
        self.assertIsNone(by_name["Polymarket"]["change_cid"])

    def test_endpoint_semantics_match_the_real_pages(self):
        by_key = {entry["key"]: entry for entry in self.endpoints["endpoints"]}
        expected = {
            "1x2d.js": "euro_market_history",
            "analysis.html": "analysis_stats",
            "odds.html": "lineup",
            "analy.json": "events",
        }
        for key, label in expected.items():
            self.assertEqual(by_key[key]["aggregation_source"], label, key)

    def test_eu_urls_use_euro_cids_and_eu42_is_skipped(self):
        by_key = {entry["key"]: entry for entry in self.endpoints["endpoints"]}
        expected = {
            "eu_1.html": "/80/",
            "eu_3.html": "/545/",
            "eu_8.html": "/281/",
            "eu_12.html": "/90/",
            "eu_47.html": "/177/",
            "eu_48.html": "/432/",
        }
        for key, fragment in expected.items():
            self.assertIn(fragment, by_key[key]["url"], key)
        self.assertTrue(by_key["eu_42.html"].get("skip_request"), "eu_42 must not request 18Bet")

    def test_188bet_has_forbidden_alias_and_sporttery_has_no_fake_analy_source(self):
        by_name = {entry["official_name"]: entry for entry in self.roster}
        self.assertIn("18Bet", by_name["188Bet"].get("forbidden_aliases", []))
        self.assertNotIn("analy.json", by_name["中国体彩"]["required_endpoints"])
        self.assertIn("1x2d.js", by_name["中国体彩"]["required_endpoints"])

    def test_roster_entries_are_four_tuple_shape(self):
        allowed = {
            "official_name", "aliases", "euro_cid", "change_cid",
            "required_endpoints", "no_open_rule", "role", "forbidden_aliases",
        }
        for entry in self.roster:
            self.assertTrue(set(entry).issubset(allowed), entry)
            self.assertIn("official_name", entry)
            self.assertIn("aliases", entry)
            self.assertIn("required_endpoints", entry)
            self.assertIn("no_open_rule", entry)
            self.assertNotIn("id", entry)
            self.assertNotIn("alt_id", entry)

    def test_non_roster_cids_are_documented(self):
        non_roster = set(self.primary.get("non_roster_cids", []))
        self.assertEqual(non_roster, NON_ROSTER_CIDS)

    def test_schedule_points_to_feed_not_index_page(self):
        schedule = self.primary["base_urls"]["schedule"]
        self.assertIn("bf_jc.txt", schedule)
        self.assertNotIn("index.aspx", schedule)


if __name__ == "__main__":
    unittest.main()
