"""
校验/测试/test_assembler.py
快照组装器单元测试: 确保 SnapshotAssembler 输出的 Markdown 能 100% 通过物理门禁
"""

import unittest
from 校验.src.domain.assembler import SnapshotAssembler
from 校验.src.domain.verifier import SnapshotVerifier
from 校验.src.application.use_cases import VerifySnapshotUseCase


class TestSnapshotAssembler(unittest.TestCase):
    def setUp(self):
        self.assembler = SnapshotAssembler()
        self.use_case = VerifySnapshotUseCase()

    def test_assembled_markdown_passes_full_verification(self):
        """测试组装器输出的标准快照能直接通过用例层完整物理门禁"""
        data = {
            "matchId": "2989999",
            "league": "英超",
            "homeTeam": "曼城",
            "awayTeam": "切尔西",
            "kickoffTime": "2026-10-10 22:00",
            "sportteryCode": "周六020",
            "polymarketUrl": "https://polymarket.com/sports/epl/mci-che",
            "lineupData": "- 主队伤停：\n  - 罗德里 (主力中场，膝伤缺阵)\n- 客队伤停：\n  - 帕尔默 (主力前锋，肌肉拉伤)",
            "basicStatsText": "- 主队近况（曼城）：主场胜率 80%，场均进球 2.5\n- 客队近况（切尔西）：客场防守稳健，场均失球 1.0\n- 赛事性质与战意博弈：强强对话\n- 赛程陷阱：无\n- 盘路画像：近期赢盘率正常",
            "europe1x2": [
                {"zone": "核心做市", "company": cname, "initialOdds": [1.90, 3.50, 3.80], "initialReturn": 91.5, "liveOdds": [1.95, 3.50, 3.70], "liveReturn": 91.5, "kelly": [0.93, 0.94, 0.95]}
                for cname in [
                    "澳彩", "Crown", "Bet365", "易胜博", "平博", "188Bet", "香港马会",
                    "威廉希尔", "立博", "Bwin", "Interwetten", "SNAI", "伟德", "必发",
                    "SBO", "沙巴", "Marathon", "Betway", "Unibet", "Paddy Power", "10Bet",
                    "中国体彩", "Polymarket"
                ]
            ],
            "correctScores": [
                ("1:0", 7.50, "0:0", 9.00, "0:1", 8.50),
                ("2:0", 9.00, "1:1", 6.20, "0:2", 12.00),
                ("2:1", 8.00, "2:2", 13.00, "1:2", 10.00),
                ("3:0", 15.00, "3:3", 40.00, "0:3", 25.00),
            ]
        }
        md_text = self.assembler.assemble(data)
        self.assertIn("# 【周六020】英超 曼城 vs 切尔西", md_text)
        self.assertIn("## 三、欧洲指数百家做市商清单（法定 23 家）", md_text)

        # 解析并执行门禁
        snap = self.use_case._parse_markdown_snapshot(md_text, "2989999")
        snap["_raw_content"] = md_text
        receipt = self.use_case.verifier.verify(snap)

        self.assertTrue(receipt.is_valid, f"验证失败: {[r.message for r in receipt.results if r.status.value == 'FAIL']}")
        self.assertEqual(receipt.failed_count, 0)


if __name__ == "__main__":
    unittest.main()
