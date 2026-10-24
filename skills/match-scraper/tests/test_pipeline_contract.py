import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PIPELINE = ROOT / "data" / "pipeline.md"


class PipelineContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PIPELINE.read_text(encoding="utf-8")

    def test_all_attach_targets_use_fixed_staging(self):
        targets = re.findall(r"ATTACH '([^']+)' AS DB", self.text)
        self.assertTrue(targets)
        self.assertEqual(set(targets), {"data/.staging/build.db"})

    def test_lineup_step_reads_inline_lineup_obj(self):
        self.assertIn("name: LINEUP", self.text)
        self.assertIn("load_sql: land_lineup", self.text)
        for field in (
            "homePlayerList",
            "guestPlayerList",
            "homeBakPlayerList",
            "guestBakPlayerList",
            "homeFormation",
            "guestFormation",
        ):
            self.assertIn(field, self.text)
        self.assertIn("trim(player->>'name'", self.text)

    def test_team_stats_reads_xg_from_analy_json(self):
        team_stats = self.text.split("name: TEAM_STATS", 1)[1].split("name: ENDPOINT_STATUS", 1)[0]
        self.assertIn("endpoint_key = 'analy.json'", team_stats)
        self.assertIn("lastXgTechStat", team_stats)
        self.assertIn("json_extract(item, '$.home')", team_stats)
        self.assertIn("json_extract(item, '$.away')", team_stats)
        self.assertNotIn("xg_presence", team_stats)
        self.assertNotIn("no_structured_event_rows", team_stats)

    def test_endpoint_status_counts_lineup_and_reports_analy_json_truthfully(self):
        status = self.text.split("name: ENDPOINT_STATUS", 1)[1].split("name: BUILD_MANIFEST", 1)[0]
        self.assertIn("DB.lineup", status)
        self.assertIn("source_endpoint = 'analy.json'", status)
        self.assertIn("THEN 'xg rows parsed'", status)
        self.assertIn("THEN 'xg_parse_failed'", status)
        self.assertIn("THEN 'xg_not_present'", status)

    def test_match_meta_reads_schedule_index_without_new_payload_endpoint(self):
        match_meta = self.text.split("name: MATCH_META", 1)[1].split("name: EURO_SNAPSHOT", 1)[0]
        self.assertIn("read_text('data/{YYYY-MM-DD}/meta.md')", match_meta)
        self.assertIn("DELETE FROM DB.match_meta", match_meta)
        self.assertIn("trim(f[2]) = (SELECT match_id FROM DB.endpoint_payload LIMIT 1)", match_meta)
        endpoint_payload = self.text.split("name: ENDPOINT_PAYLOAD", 1)[1].split("name: MATCH_META", 1)[0]
        self.assertNotIn("match_meta", endpoint_payload)

    def test_gate_checks_match_meta_identity(self):
        gate = self.text.split("name: GATE_LIVE", 1)[1]
        self.assertIn("match_meta_rows", gate)
        self.assertIn("match_meta_identity", gate)
        self.assertIn("length(trim(home_team))", gate)

    def test_gate_blocks_synthetic_presence_rows(self):
        gate = self.text.split("name: GATE_LIVE", 1)[1]
        self.assertIn("presence_rows", gate)
        self.assertIn("metric = 'presence'", gate)
        self.assertIn("lineup_parse_consistency", gate)
        self.assertIn("lineup_count_matches", gate)
        self.assertIn("bookmaker_coverage", gate)
        self.assertIn("COUNT(DISTINCT company_id)", gate)
        self.assertIn("core_tables_present", gate)
        self.assertIn("source_endpoint = 'analysis.html'", gate)
        self.assertIn("payload_chars_mismatches", gate)
        self.assertIn("raw_hash_lengths", gate)
        self.assertIn("match_identity", gate)
        self.assertIn("content_types", gate)
        self.assertIn("capture_timestamp", gate)
        self.assertIn("xg_state", gate)


if __name__ == "__main__":
    unittest.main()
