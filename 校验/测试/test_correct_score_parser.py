import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from 校验.src.domain.correct_score_parser import CorrectScoreParser


class TestCorrectScoreParser(unittest.TestCase):
    def setUp(self):
        self.parser = CorrectScoreParser()
        self.sample_raw = """5球6球7+球
-15.253.81.48\t8.253.453.453.657.8164070
胜\t1:0\t2:0\t2:1\t3:0\t3:1\t3:2\t4:0\t4:1\t4:2\t5:0\t5:1\t5:2\t胜其它
6\t11\t8.5\t23\t25\t40\t80\t70\t100\t200\t200\t250\t100
平\t0:0\t1:1\t2:2\t3:3\t平其它\t
8.25\t5\t14\t70\t550
负\t0:1\t0:2\t1:2\t0:3\t1:3\t2:3\t0:4\t1:4\t2:4\t0:5\t1:5\t2:5\t负其它
8\t16.5\t11\t42\t35\t50\t150\t100\t125\t450\t350\t450\t175
半全场\t胜/胜\t胜/平\t胜/负\t平/胜\t平/平\t平/负\t负/胜\t负/平\t负/负
4\t17.5\t50\t4.3\t3.8\t7.8\t42\t17.5\t5.8
"""

    def test_parse_correct_scores(self):
        res = self.parser.parse(self.sample_raw)
        self.assertIn("correctScores", res)
        scores = res["correctScores"]
        
        self.assertIn("homeWin", scores)
        self.assertIn("draw", scores)
        self.assertIn("awayWin", scores)
        self.assertIn("flat", scores)
        
        # 校验胜比分
        self.assertEqual(scores["homeWin"]["1:0"], 6.0)
        self.assertEqual(scores["homeWin"]["2:0"], 11.0)
        self.assertEqual(scores["homeWin"]["2:1"], 8.5)
        self.assertEqual(scores["homeWin"]["胜其它"], 100.0)
        
        # 校验平比分
        self.assertEqual(scores["draw"]["0:0"], 8.25)
        self.assertEqual(scores["draw"]["1:1"], 5.0)
        self.assertEqual(scores["draw"]["2:2"], 14.0)
        
        # 校验负比分
        self.assertEqual(scores["awayWin"]["0:1"], 8.0)
        self.assertEqual(scores["awayWin"]["1:2"], 11.0)
        
        # 校验 flat 扁平映射
        self.assertEqual(scores["flat"]["1:0"], 6.0)
        self.assertEqual(scores["flat"]["1:1"], 5.0)
        self.assertEqual(scores["flat"]["0:1"], 8.0)

    def test_parse_half_full_time(self):
        res = self.parser.parse(self.sample_raw)
        self.assertIn("halfFullTime", res)
        hft = res["halfFullTime"]
        self.assertEqual(hft["胜/胜"], 4.0)
        self.assertEqual(hft["胜/平"], 17.5)
        self.assertEqual(hft["平/胜"], 4.3)
        self.assertEqual(hft["平/平"], 3.8)
        self.assertEqual(hft["平/负"], 7.8)
        self.assertEqual(hft["负/负"], 5.8)

    def test_enrich_snapshot(self):
        snapshot = {
            "correctScoreOdds": self.sample_raw,
            "markets": {}
        }
        self.parser.enrich_snapshot(snapshot)
        self.assertIn("crowFullIndex", snapshot["markets"])
        self.assertIn("correctScores", snapshot["markets"]["crowFullIndex"])
        self.assertEqual(snapshot["markets"]["crowFullIndex"]["correctScores"]["flat"]["1:0"], 6.0)
        self.assertIn("halfFullTime", snapshot["markets"])
        self.assertEqual(snapshot["markets"]["halfFullTime"]["胜/胜"], 4.0)


if __name__ == "__main__":
    unittest.main()
