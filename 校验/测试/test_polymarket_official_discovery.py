import unittest
import json
from 校验.src.domain.raw_parser import Titan007RawParser
from 校验.src.domain.verifier import SnapshotVerifier, CheckStatus, DimensionType, verify_memory_cognitive_cards

class TestPolymarketOfficialDiscovery(unittest.TestCase):
    def setUp(self):
        self.parser = Titan007RawParser()
        self.verifier = SnapshotVerifier()

    def test_raw_parser_never_fabricates_disclaimer_on_empty(self):
        """测试1: 当 polymarket.json 为空时，绝不擅自伪造'官方未开盘（经Gamma双向核验...）'"""
        res_empty = self.parser.parse_polymarket_json("")
        self.assertNotIn("经Gamma双向核验", str(res_empty.get("polymarketUrl", "")))
        self.assertNotIn("经Gamma", str(res_empty.get("polymarketUrl", "")))
        self.assertEqual(res_empty.get("status"), "missing")
        self.assertEqual(res_empty.get("polymarketUrl"), "")

        res_invalid = self.parser.parse_polymarket_json("{not valid json")
        self.assertNotIn("经Gamma双向核验", str(res_invalid.get("polymarketUrl", "")))
        self.assertEqual(res_invalid.get("status"), "missing")
        self.assertEqual(res_invalid.get("polymarketUrl"), "")

    def test_verifier_core_league_championship_unopened_fails(self):
        """测试2: 英冠 (ELC) 赛事未开盘且无网络真实存证，门禁必须判定 FAIL"""
        snapshot = {
            "matchId": "3008269",
            "league": "英冠",
            "homeTeam": "诺维奇",
            "awayTeam": "南安普敦",
            "polymarket": {
                "status": "unopened",
                "url": "官方未开盘（经Gamma双向核验）"
            }
        }
        res = self.verifier._check_polymarket(snapshot)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("主流核心联赛", res.message)

    def test_verifier_valid_elc_slug_passes(self):
        """测试3: 合法英冠真实链接必须判定 PASS"""
        snapshot = {
            "matchId": "3008269",
            "league": "英冠",
            "homeTeam": "诺维奇",
            "awayTeam": "南安普敦",
            "polymarket": {
                "status": "active",
                "url": "https://polymarket.com/event/elc-nor-sot-2026-10-14"
            }
        }
        res = self.verifier._check_polymarket(snapshot)
        self.assertEqual(res.status, CheckStatus.PASS)
        self.assertIn("https://polymarket.com/event/elc-nor-sot-2026-10-14", res.message)

    def test_raw_parser_provenance_url_not_contain_bogus_match_id(self):
        """测试4: 溯源端点生成绝不可包含荒谬的 events?id={match_id}"""
        receipt = self.parser.generate_network_receipt("3008269", {"polymarket.json": "{}"})
        endpoints = receipt.get("endpoints", [])
        self.assertTrue(len(endpoints) > 0)
        pm_url = endpoints[0]["url"]
        self.assertNotIn("events?id=3008269", pm_url)

    def test_verifier_memory_cognitive_cards_fails_on_fake_disclaimer_in_core_league(self):
        """测试5: 7列表格中英冠比赛若填伪造未开盘，记忆核验必须拦截报错"""
        sample_memory = """# 2026-10-14 比赛记忆

## 赛前分析推演

| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **周三007 02:45** | 诺维奇 vs 南安普敦 | 首选胜 / 次选平 | [-1] 让平 | 40.6% / 26.2% / 33.1% | 平手低水 | 官方未开盘（经Gamma双向核验） |

## 深度分析

### 英冠 诺维奇 vs 南安普敦（编号: 周三007 比赛ID: 3008269，开球: 2026-10-15 02:45，分析: 2026-10-14 21:40）
- 胜平负：首选 主胜｜次选 平局
- 【认知契约卡】：
  - 选择与排除依据：测试
  - 关键拍板依据：测试
  - 庄家博弈假说与竞争解释：测试
  - 可推翻反证与改变条件：测试
"""
        is_ok, errors, count = verify_memory_cognitive_cards(sample_memory, expected_matches=1)
        self.assertFalse(is_ok)
        self.assertTrue(any("未开盘" in e or "主流核心联赛" in e or "Polymarket" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
