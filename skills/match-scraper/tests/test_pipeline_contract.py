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
        self.assertNotIn("DELETE FROM DB.match_meta", match_meta)
        self.assertIn("trim(f[2]) = (SELECT match_id FROM DB.endpoint_payload LIMIT 1)", match_meta)
        endpoint_payload = self.text.split("name: ENDPOINT_PAYLOAD", 1)[1].split("name: MATCH_META", 1)[0]
        self.assertNotIn("match_meta", endpoint_payload)
        self.assertNotIn("DELETE FROM DB.endpoint_payload", endpoint_payload)

    def test_business_tables_and_views_are_pipeline_owned(self):
        self.assertIn("name: BUSINESS_TABLES", self.text)
        self.assertIn("name: VIEWS", self.text)
        for name in (
            "球队基本情况", "欧指", "欧指变盘", "亚盘", "大小球",
            "v_euro_snapshot", "v_euro_history", "v_asian_odds",
            "v_over_under", "v_ah_history", "v_ou_history",
            "v_eu_detail_history", "v_injury", "v_lineup",
            "v_team_stats", "v_bookmaker_slots", "v_payload_coverage",
            "v_analysis_status",
        ):
            self.assertIn(name, self.text)
        self.assertIn("CREATE OR REPLACE TABLE", self.text)
        self.assertIn("CREATE OR REPLACE VIEW", self.text)

    def test_history_views_are_chronological_and_keep_latest_tie_last(self):
        for view in (
            "v_euro_history",
            "v_ah_history",
            "v_ou_history",
            "v_eu_detail_history",
        ):
            block = self.text.split(f'CREATE OR REPLACE VIEW "{view}"', 1)[1].split(";", 1)[0]
            self.assertIn("ORDER BY ts_iso ASC, source_index DESC", block, view)

    def test_euro_detail_has_clear_odds_columns_and_chronological_order(self):
        block = self.text.split('CREATE OR REPLACE TABLE "欧指变盘"', 1)[1].split(";", 1)[0]
        for column in ("主胜赔率", "平局赔率", "客胜赔率"):
            self.assertIn(column, block)
        self.assertIn("WHEN 80 THEN 1", block)
        self.assertIn("WHEN 1129 THEN 21", block)
        self.assertIn("END, h.ts_iso ASC, h.source_index DESC", block)

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
        self.assertIn("business_tables_present", gate)
        self.assertIn("read_views_present", gate)
        self.assertIn("manifest_payload_binding", gate)
        self.assertIn("main.sqlite_master", gate)
        self.assertNotIn("DB.v_bookmaker_slots", gate)


if __name__ == "__main__":
    unittest.main()
