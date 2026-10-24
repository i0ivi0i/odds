import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = ROOT / "data" / "schema.sql"


class SchemaContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = SCHEMA.read_text(encoding="utf-8")

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.executescript(self.schema)

    def tearDown(self):
        self.conn.close()

    def test_match_meta_table_has_identity_columns(self):
        columns = {
            row[1] for row in self.conn.execute("PRAGMA table_info(match_meta)")
        }
        self.assertEqual(
            columns,
            {
                "match_id",
                "sales_date",
                "match_no",
                "league",
                "home_team",
                "away_team",
                "kickoff_at",
                "source",
            },
        )

    def test_match_meta_rejects_missing_and_duplicate_identity(self):
        sql = """
            INSERT INTO match_meta (
              match_id, sales_date, match_no, league, home_team,
              away_team, kickoff_at, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        row = (
            "3018847", "2026-10-24", "周六011", "德甲",
            "RB莱比锡", "埃弗斯堡", "2026-10-24 21:30",
            "data/2026-10-24/meta.md",
        )
        self.conn.execute(sql, row)
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(sql, row)
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(sql, tuple(["3018847", "2026-10-24", "周六011", "德甲", None, "埃弗斯堡", "2026-10-24 21:30", "x"]))

    def test_four_entry_views_exist(self):
        names = {
            row[0]
            for row in self.conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'view'"
            )
        }
        self.assertTrue(
            {"球队基本情况", "欧指", "亚盘", "大小球"}.issubset(names)
        )

    def test_four_entry_views_have_stable_fact_columns(self):
        expected = {
            "球队基本情况": {
                "比赛ID", "数据类型", "联赛", "主队", "客队",
                "开球时间", "竞彩编号", "销售日", "队伍", "身份",
                "姓名", "伤停原因",
            },
            "欧指": {
                "比赛ID", "机构编号", "机构",
                "初盘主胜", "初盘平局", "初盘客胜", "初盘返还率",
                "最新主胜", "最新平局", "最新客胜", "最新返还率",
                "数据时间", "变盘行数", "首笔时间", "末笔时间",
            },
            "亚盘": {
                "比赛ID", "机构编号", "机构",
                "初盘主水", "初盘盘口", "初盘客水",
                "最新主水", "最新盘口", "最新客水", "更新时间",
                "变盘行数", "首笔时间", "末笔时间",
            },
            "大小球": {
                "比赛ID", "机构编号", "机构",
                "初盘大球", "初盘盘口", "初盘小球",
                "最新大球", "最新盘口", "最新小球", "更新时间",
                "变盘行数", "首笔时间", "末笔时间",
            },
        }
        forbidden = {
            "prediction", "recommendation", "confidence", "verdict", "score",
            "预测", "推荐", "信心", "结论", "评分",
        }
        for view, columns in expected.items():
            actual = {
                row[1]
                for row in self.conn.execute(f'PRAGMA table_info("{view}")')
            }
            self.assertEqual(actual, columns, view)
            self.assertFalse(actual & forbidden, view)

    def test_team_view_contains_match_lineup_and_injury_details(self):
        self.conn.execute(
            """
            INSERT INTO match_meta (
              match_id, sales_date, match_no, league, home_team,
              away_team, kickoff_at, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("3018847", "2026-10-24", "周六011", "德甲", "RB莱比锡", "埃弗斯堡", "2026-10-24 21:30", "meta.md"),
        )
        self.conn.execute(
            """
            INSERT INTO lineup (
              match_id, side, role, source_index, number, name,
              player_id, position, formation, source_endpoint
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("3018847", "home", "starter", 1, "1", "古拉西", "p1", "门将", "", "odds.html"),
        )
        self.conn.execute(
            """
            INSERT INTO injury (
              match_id, side, source_index, number, name, player_id,
              position, injury_reason, captain_type, player_kind, source_endpoint
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("3018847", "away", 1, "9", "伤员甲", "p2", "前锋", "肌肉拉伤", 0, 0, "analysis.html"),
        )
        self.conn.execute(
            """
            INSERT INTO team_stats (
              match_id, section, side, item, metric, value,
              text_value, source_index, source_endpoint
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ("3018847", "xg", "home", "xG", "xg", 1.75, None, 1, "analy.json"),
        )
        rows = self.conn.execute(
            'SELECT "数据类型", "联赛", "主队", "客队", "队伍", "身份", "姓名", "伤停原因" FROM "球队基本情况"'
        ).fetchall()
        self.assertIn(("比赛信息", "德甲", "RB莱比锡", "埃弗斯堡", "比赛", None, None, None), rows)
        self.assertIn(("阵容", None, None, None, "主队", "首发", "古拉西", None), rows)
        self.assertIn(("伤停", None, None, None, "客队", None, "伤员甲", "肌肉拉伤"), rows)
        self.assertNotIn("技术统计", [row[0] for row in rows])

    def test_four_entry_views_do_not_read_raw_payload(self):
        for view in ("球队基本情况", "欧指", "亚盘", "大小球"):
            sql = self.conn.execute(
                "SELECT sql FROM sqlite_master WHERE type = 'view' AND name = ?",
                (view,),
            ).fetchone()[0]
            self.assertNotIn("endpoint_payload", sql, view)
            self.assertNotIn("endpoint_parse_status", sql, view)

    def test_history_views_order_by_timestamp(self):
        self.conn.execute(
            """
            INSERT INTO euro_snapshot (
              match_id, cid, bookmaker, record_id, hist_count,
              initial_home, initial_draw, initial_away,
              initial_prob_home, initial_prob_draw, initial_prob_away, initial_return,
              latest_home, latest_draw, latest_away,
              latest_prob_home, latest_prob_draw, latest_prob_away, latest_return,
              source_time, alias
            ) VALUES (
              '3018847', 80, '澳彩', 'r1', 2,
              2.00, 3.20, 3.60, 0.50, 0.31, 0.28, 0.94,
              2.10, 3.10, 3.50, 0.48, 0.32, 0.29, 0.93,
              '2026-10-24 21:00', '澳彩'
            )
            """
        )
        rows = [
            ("3018847", 80, "r1", 2, "2026-10-24 20:30", "2026-10-24 20:30", 2026, 2.10, 3.10, 3.50, 0.9, 0.9, 0.9),
            ("3018847", 80, "r1", 1, "2026-10-24 20:00", "2026-10-24 20:00", 2026, 2.00, 3.20, 3.60, 0.9, 0.9, 0.9),
        ]
        self.conn.executemany(
            """
            INSERT INTO euro_history (
              match_id, cid, record_id, source_index, ts_local, ts_iso, year,
              home, draw, away, kelly_home, kelly_draw, kelly_away
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        ordered = [
            row[0]
            for row in self.conn.execute("SELECT ts_iso FROM v_euro_history")
        ]
        self.assertEqual(ordered, sorted(ordered))


if __name__ == "__main__":
    unittest.main()
