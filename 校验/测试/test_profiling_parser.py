import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from 校验.src.domain.profiling_parser import ProfilingParser


class TestProfilingParser(unittest.TestCase):
    def setUp(self):
        self.parser = ProfilingParser()
        self.sample_identical_raw = """
巴西国际
初盘:平手/半球\t赢\t走\t输\t赢盘率
总\t87\t0\t124\t41.2%
主\t41\t0\t52\t44.1%
客\t46\t0\t72\t39%
近6场盘路走势:\xa0赢\xa0输\xa0赢\xa0输\xa0赢\xa0输
\t
科林蒂安
初盘:平手/半球\t赢\t走\t输\t赢盘率
总\t140\t0\t84\t62.5%
主\t20\t0\t7\t74.1%
客\t120\t0\t77\t60.9%
近6场盘路走势:\xa0赢\xa0输\xa0赢\xa0赢\xa0输\xa0输
"""
        self.sample_trends_raw = """
巴西国际
全场\t亚让盘\t进球数
\xa0\t赛\t赢盘\t走水\t输盘\t赢盘率\t详细\t大球\t大球率\t小球\t小球率\t详细
总\t28\t10\t2\t16\t35.7%\t查看\t11\t39.3%\t16\t57.1%\t查看
主场\t14\t4\t1\t9\t28.6%\t查看\t5\t35.7%\t9\t64.3%\t查看
客场\t14\t6\t1\t7\t42.9%\t查看\t6\t42.9%\t7\t50%\t查看
近6场\t6\t输\xa0输\xa0输\xa0输\xa0赢\xa0输\xa0\t16.7%\t查看\t小\xa0小\xa0大\xa0大\xa0大\xa0小\xa0\t查看
\t
科林蒂安
全场\t亚让盘\t进球数
\xa0\t赛\t赢盘\t走水\t输盘\t赢盘率\t详细\t大球\t大球率\t小球\t小球率\t详细
总\t28\t13\t2\t13\t46.4%\t查看\t12\t42.9%\t16\t57.1%\t查看
主场\t15\t6\t1\t8\t40%\t查看\t6\t40%\t9\t60%\t查看
客场\t13\t7\t1\t5\t53.8%\t查看\t6\t46.2%\t7\t53.8%\t查看
近6场\t6\t输\xa0输\xa0输\xa0输\xa0赢\xa0输\xa0\t16.7%\t查看\t大\xa0大\xa0小\xa0大\xa0大\xa0大\xa0\t查看
"""

    def test_parse_identical_odds(self):
        items = self.parser.parse_identical_odds(self.sample_identical_raw)
        self.assertEqual(len(items), 2)
        
        item1 = items[0]
        self.assertEqual(item1["team"], "巴西国际")
        self.assertEqual(item1["initialHandicap"], "平手/半球")
        self.assertEqual(item1["stats"]["total"]["win"], 87)
        self.assertEqual(item1["stats"]["total"]["winRate"], "41.2%")
        self.assertEqual(item1["stats"]["home"]["win"], 41)
        self.assertEqual(item1["stats"]["away"]["loss"], 72)
        self.assertEqual(item1["recent6"], ["赢", "输", "赢", "输", "赢", "输"])

        item2 = items[1]
        self.assertEqual(item2["team"], "科林蒂安")
        self.assertEqual(item2["stats"]["total"]["win"], 140)
        self.assertEqual(item2["stats"]["total"]["winRate"], "62.5%")
        self.assertEqual(item2["recent6"], ["赢", "输", "赢", "赢", "输", "输"])

    def test_parse_handicap_trends(self):
        items = self.parser.parse_handicap_trends(self.sample_trends_raw)
        self.assertGreaterEqual(len(items), 2)
        
        item1 = items[0]
        self.assertEqual(item1["team"], "巴西国际")
        self.assertEqual(item1["scope"], "全场")
        self.assertEqual(item1["stats"]["total"]["played"], 28)
        self.assertEqual(item1["stats"]["total"]["winRate"], "35.7%")
        self.assertEqual(item1["stats"]["total"]["overRate"], "39.3%")
        self.assertEqual(item1["recent6_handicap"], ["输", "输", "输", "输", "赢", "输"])
        self.assertEqual(item1["recent6_overunder"], ["小", "小", "大", "大", "大", "小"])

    def test_empty_or_malformed_input(self):
        self.assertEqual(self.parser.parse_identical_odds(""), [])
        self.assertEqual(self.parser.parse_identical_odds(None), [])
        self.assertEqual(self.parser.parse_handicap_trends(""), [])
        self.assertEqual(self.parser.parse_handicap_trends("随机无规则垃圾字符"), [])

    def test_enrich_profiling(self):
        profiling = {
            "identicalOddsHistory": {"raw": self.sample_identical_raw},
            "handicapTrends": {"raw": self.sample_trends_raw}
        }
        enriched = self.parser.enrich_profiling(profiling)
        self.assertIn("items", enriched["identicalOddsHistory"])
        self.assertEqual(len(enriched["identicalOddsHistory"]["items"]), 2)
        self.assertIn("items", enriched["handicapTrends"])
        self.assertEqual(len(enriched["handicapTrends"]["items"]), 2)


if __name__ == "__main__":
    unittest.main()
