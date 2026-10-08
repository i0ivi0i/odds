import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from 校验.src.domain.tactics_parser import TacticsParser


class TestTacticsParser(unittest.TestCase):
    def setUp(self):
        self.parser = TacticsParser()
        self.sample_tech_raw = """球队\t全部\t同主客
胜\t平\t负\t进球\t失球\t净胜球\t场均进球\t场均角球\t场均黄牌\t进球\t失球\t净胜球\t场均进球\t胜\t平\t负
巴西国际\t10%\t40%\t50%\t9\t14\t-5\t0.9\t4.8\t3\t3\t4\t-1\t0.75\t0%\t75%\t25%
科林蒂安\t10%\t20%\t70%\t7\t14\t-7\t0.7\t4.8\t2.2\t3\t5\t-2\t0.75\t0%\t50%\t50%
"""
        self.sample_sched_raw = """巴西国际
时间\t赛事\t对阵\t分析\t直播\t相隔
10-12\t巴西甲\t格雷米奥 - 巴西国际\t分析\t\t4 天
10-17\t巴西甲\t米拉索 - 巴西国际\t分析\t\t9 天
\t
科林蒂安
时间\t赛事\t对阵\t分析\t直播\t相隔
10-12\t巴西甲\t帕尔梅拉斯 - 科林蒂安\t分析\t\t4 天
"""
        self.sample_goal_time_raw = """1-10\t11-20\t21-30\t31-40\t41-45\t46-50\t51-60\t61-70\t71-80\t81-90+
总\t2\t1\t6\t2\t1\t3\t3\t3\t4\t5
主\t1\t0\t5\t2\t0\t2\t1\t1\t1\t3
客\t1\t1\t1\t0\t1\t1\t2\t2\t3\t2
第一个进球的时间统计
总\t2\t1\t5\t2\t1\t2\t1\t1\t2\t2
主\t1\t0\t4\t2\t0\t1\t0\t0\t0\t2
客\t1\t1\t1\t0\t1\t1\t1\t1\t2\t0
"""

    def test_parse_technical_stats(self):
        items = self.parser.parse_technical_stats(self.sample_tech_raw)
        self.assertEqual(len(items), 2)
        
        t1 = items[0]
        self.assertEqual(t1["team"], "巴西国际")
        self.assertEqual(t1["goals"], 9)
        self.assertEqual(t1["conceded"], 14)
        self.assertEqual(t1["avg_goals"], 0.9)
        self.assertEqual(t1["avg_corners"], 4.8)
        self.assertEqual(t1["avg_yellow_cards"], 3.0)
        self.assertEqual(t1["home_away_avg_goals"], 0.75)

        t2 = items[1]
        self.assertEqual(t2["team"], "科林蒂安")
        self.assertEqual(t2["goals"], 7)
        self.assertEqual(t2["conceded"], 14)
        self.assertEqual(t2["avg_goals"], 0.7)
        self.assertEqual(t2["avg_corners"], 4.8)

    def test_parse_future_schedule(self):
        sched = self.parser.parse_future_schedule(self.sample_sched_raw)
        self.assertEqual(len(sched), 2)
        
        s1 = sched[0]
        self.assertEqual(s1["team"], "巴西国际")
        self.assertEqual(len(s1["matches"]), 2)
        self.assertEqual(s1["matches"][0]["days_interval"], 4)
        self.assertEqual(s1["matches"][0]["opponent_match"], "格雷米奥 - 巴西国际")

        s2 = sched[1]
        self.assertEqual(s2["team"], "科林蒂安")
        self.assertEqual(len(s2["matches"]), 1)
        self.assertEqual(s2["matches"][0]["days_interval"], 4)

    def test_parse_goal_time(self):
        gt = self.parser.parse_goal_time_distribution(self.sample_goal_time_raw)
        self.assertIn("distribution", gt)
        dist = gt["distribution"]
        self.assertIn("total", dist)
        self.assertEqual(dist["total"]["21-30"], 6)
        self.assertEqual(dist["total"]["81-90+"], 5)
        self.assertIn("first_goal", gt)
        self.assertEqual(gt["first_goal"]["total"]["21-30"], 5)

    def test_enrich_tactics(self):
        tactics = {
            "technicalStats": {"raw": self.sample_tech_raw},
            "futureSchedule": {"raw": self.sample_sched_raw},
            "goalTimeDistribution": {"raw": self.sample_goal_time_raw}
        }
        enriched = self.parser.enrich_tactics(tactics)
        self.assertIn("items", enriched["technicalStats"])
        self.assertEqual(len(enriched["technicalStats"]["items"]), 2)
        self.assertIn("items", enriched["futureSchedule"])
        self.assertEqual(len(enriched["futureSchedule"]["items"]), 2)
        self.assertIn("structured", enriched["goalTimeDistribution"])


if __name__ == "__main__":
    unittest.main()
