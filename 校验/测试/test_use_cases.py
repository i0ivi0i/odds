"""
校验/ 测试用例: 应用层用例单元测试 (TDD 红灯阶段)
"""

import json
import os
import re
import unittest
from pathlib import Path
from 校验.src.application.use_cases import (
    VerifySnapshotUseCase,
    CheckConsistencyUseCase,
)
from 校验.src.domain.model import CheckStatus, DimensionType


class TestUseCases(unittest.TestCase):
    def setUp(self):
        self.verify_use_case = VerifySnapshotUseCase()
        self.consistency_use_case = CheckConsistencyUseCase()
        self.repo_root = Path(".").resolve()

    def test_verify_real_match_snapshot_passes(self):
        """测试对真实存在的【推演源数据】 data/2026-10-06/2981506.json 的检验"""
        real_file = self.repo_root / "data" / "2026-10-06" / "2981506.json"
        if not real_file.exists():
            self.skipTest(f"{real_file} 不存在，跳过真实文件测试")

        receipt = self.verify_use_case.execute(str(real_file))
        self.assertTrue(receipt.is_valid)
        self.assertEqual(receipt.match_id, "2981506")
        self.assertEqual(receipt.failed_count, 0)

    def test_verify_non_existent_file_returns_fail(self):
        """测试传入不存在的文件路径必须返回 FAIL 收据"""
        receipt = self.verify_use_case.execute("data/not_exist_match.json")
        self.assertFalse(receipt.is_valid)
        self.assertEqual(receipt.overall_status, CheckStatus.FAIL)
        self.assertIn("文件不存在", receipt.results[0].message)

    def test_verify_corrupted_json_returns_fail(self):
        """测试传入格式损坏的非法 JSON 必须返回 FAIL 收据"""
        temp_broken = self.repo_root / "data" / "temp_broken_test.json"
        temp_broken.write_text("{broken json", encoding="utf-8")
        try:
            receipt = self.verify_use_case.execute(str(temp_broken))
            self.assertFalse(receipt.is_valid)
            self.assertEqual(receipt.overall_status, CheckStatus.FAIL)
            self.assertIn("JSON格式解析失败", receipt.results[0].message)
        finally:
            if temp_broken.exists():
                temp_broken.unlink()

    def test_system_consistency_check_runs_and_passes(self):
        """测试全库系统一致性巡检用例执行"""
        result = self.consistency_use_case.execute(root_dir=str(self.repo_root))
        self.assertTrue(result["is_clean"])
        self.assertEqual(result["findings_count"], 0)
        self.assertTrue(result["graph_connected"])
        self.assertTrue(result["algo_tests_passed"])

    def test_verify_snapshot_binds_content_hash_and_metadata(self):
        """测试U3: 用例层在读取【推演源数据】时必须绑定 content_hash (SHA256) 与文件元数据"""
        real_file = self.repo_root / "data" / "2026-10-06" / "2981506.json"
        if not real_file.exists():
            self.skipTest("真实【推演源数据】不存在")
        receipt = self.verify_use_case.execute(str(real_file))
        self.assertIn("content_hash", receipt.metadata)
        self.assertEqual(len(receipt.metadata["content_hash"]), 64)
        self.assertIn("file_path", receipt.metadata)
        self.assertIn("fetchedAt", receipt.metadata)

    def test_verify_snapshot_match_id_mismatch_fails(self):
        """测试U3: 【推演源数据】内 matchId 与文件名 stem 不符时判定 FAIL 阻断"""
        temp_file = self.repo_root / "data" / "temp_mismatch_test_999999.json"
        content = json.dumps({"matchId": "888888", "match": {"league": "英超"}}, ensure_ascii=False)
        temp_file.write_text(content, encoding="utf-8")
        try:
            receipt = self.verify_use_case.execute(str(temp_file))
            self.assertFalse(receipt.is_valid)
            self.assertEqual(receipt.overall_status, CheckStatus.FAIL)
            self.assertIn("比赛ID不一致", receipt.results[0].message)
        finally:
            if temp_file.exists():
                temp_file.unlink()

    def test_markdown_snapshot_full_absorption_without_reversal_or_drops(self):
        """测试黄金【推演源数据】契约规范全量字段吸收：不丢行、不反序、不假凯利"""
        fixture_file = self.repo_root / "校验" / "测试" / "fixtures" / "golden_snapshot_sample.md"
        if not fixture_file.exists():
            self.skipTest("黄金【推演源数据】测试样本不存在")
        content = fixture_file.read_text(encoding="utf-8")
        m_id = re.search(r"\*\*比赛 ID\*\*：(\d+)", content)
        fixture_match_id = m_id.group(1) if m_id else "fixture_sample"
        snap = self.verify_use_case._parse_markdown_snapshot(content, fixture_match_id)
        self.assertEqual(len(snap["europe1x2"]), 23)
        self.assertEqual(snap["europe1x2"][0]["latest"]["kelly"], [0.92, 0.93, 0.98])
        self.assertEqual(len(snap["asianHandicap"]), 7)
        self.assertEqual(snap["asianHandicap"][0]["initial"]["home"], 0.90)
        self.assertEqual(snap["asianHandicap"][0]["latest"]["home"], 1.04)
        self.assertEqual(len(snap["overUnder"]), 7)
        self.assertEqual(len(snap["timeSeriesFlow"]), 59)
        self.assertIn("客队下周中亚冠客场远征", snap["tactics"]["futureSchedule"]["raw"])
        self.assertEqual(snap["sportteryHandicap"]["handicap"], "-1")
        self.assertEqual(len(snap["polymarketTimeSeries"]), 5)

    def test_markdown_snapshot_missing_hkjc_over_under_fails(self):
        """测试门禁物理拦截：一旦缺失香港马会大小球，必须返回 FAIL 并明确报错"""
        fixture_file = self.repo_root / "校验" / "测试" / "fixtures" / "golden_snapshot_sample.md"
        if not fixture_file.exists():
            self.skipTest("黄金【推演源数据】测试样本不存在")
        content = fixture_file.read_text(encoding="utf-8")
        m_id = re.search(r"\*\*比赛 ID\*\*：(\d+)", content)
        fixture_match_id = m_id.group(1) if m_id else "fixture_sample"
        # 模拟仅漏掉香港马会大小球
        corrupted = re.sub(
            r"(### 7\. 香港马会.*?)\n#### 大小球真实变盘流水.*?(?=\n#### 欧指真实变盘流水)",
            r"\1",
            content,
            flags=re.DOTALL,
        )
        temp_md = self.repo_root / "data" / f"temp_missing_hkjc_test_{fixture_match_id}.md"
        temp_md.write_text(corrupted, encoding="utf-8")
        try:
            receipt = self.verify_use_case.execute(str(temp_md))
            self.assertFalse(receipt.is_valid)
            self.assertEqual(receipt.overall_status, CheckStatus.FAIL)
            ou_fails = [r for r in receipt.results if r.dimension == DimensionType.OVER_UNDER and r.status == CheckStatus.FAIL]
            self.assertTrue(len(ou_fails) > 0)
            self.assertIn("香港马会", ou_fails[0].message)
        finally:
            if temp_md.exists():
                temp_md.unlink()

    def test_parse_markdown_polymarket_with_reason(self):
        """测试 Markdown 解析器在未开盘时完整保留举证理由文本"""
        md_text = """# 【周一003】瑞典超 马尔默 vs 卡尔马
- **比赛 ID**：3013720
- **开球时间**：2026-10-12 23:00
- **Polymarket 预测市场**：未开放（经Gamma API真实核验q=Malmo FF返回空）
- **体彩官方玩法**：HAD / HHAD 齐全
"""
        snap = self.verify_use_case._parse_markdown_snapshot(md_text, "3013720")
        self.assertEqual(snap["polymarket"]["status"], "unopened")
        self.assertIn("经Gamma API真实核验q=Malmo FF返回空", snap["polymarket"]["url"])

    def test_parse_markdown_polymarket_bare_url(self):
        """测试 Markdown 解析器支持不带方括号的裸 URL 提取"""
        md_text = """# 【周一002】意甲 亚特兰大 vs 威尼斯
- **比赛 ID**：3013718
- **开球时间**：2026-10-12 22:30
- **Polymarket 预测市场**：https://polymarket.com/event/sea-ata-ven-2026-10-12
- **体彩官方玩法**：HAD / HHAD 齐全
"""
        snap = self.verify_use_case._parse_markdown_snapshot(md_text, "3013718")
        self.assertEqual(snap["polymarket"]["status"], "active")
        self.assertEqual(snap["polymarket"]["url"], "https://polymarket.com/event/sea-ata-ven-2026-10-12")

    def test_parse_markdown_never_injects_fake_goal_numbers_when_missing(self):
        """测试U1: 当 Markdown 缺失真实进失球数字时，严禁静默注入 1.25/0.25/1.50/1.00 假均值"""
        md_text = """# 【周一001】芬超 哈卡 vs 瓦萨
- **比赛 ID**：3011111
## 二、基础战绩与攻防客观底牌
- **主队近况**：状态一般
- **客队近况**：状态尚可
"""
        snap = self.verify_use_case._parse_markdown_snapshot(md_text, "3011111")
        self.assertEqual(snap["tactics"]["technicalStats"]["home"]["goals"], 0.0)
        self.assertEqual(snap["tactics"]["technicalStats"]["away"]["goals"], 0.0)
        self.assertEqual(snap["match"]["homeGoals"], "")
        self.assertEqual(snap["match"]["awayGoals"], "")

    def test_parse_markdown_never_injects_fake_kelly_or_return_rate(self):
        """测试U1: 当 Markdown 欧指表缺失返还率或凯利值时，严禁静默回退到 90.0 或 [0.94, 0.88, 0.84]"""
        md_text = """# 【周一001】芬超 哈卡 vs 瓦萨
- **比赛 ID**：3011111
## 三、法定23家机构初即盘与凯利总表
| 机构类型 | 机构 | 初盘主胜 | 初盘平局 | 初盘客胜 | 初返还 | 即时主胜 | 即时平局 | 即时客胜 | 即时返还 | 凯利(主/平/客) |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| 核心做市 | Bet365 | 2.10 | 3.40 | 3.10 | - | 2.25 | 3.50 | 3.00 | - | - |
"""
        snap = self.verify_use_case._parse_markdown_snapshot(md_text, "3011111")
        self.assertEqual(len(snap["europe1x2"]), 1)
        self.assertIsNone(snap["europe1x2"][0]["initial"]["returnRate"])
        self.assertEqual(snap["europe1x2"][0]["latest"]["kelly"], [])

    def test_system_consistency_blocks_t0_t4_pollution_in_graph_and_docs(self):
        """U5红灯测试: 全库一致性检查必须核查 docs/倍率时序波动分析手册.md、STRATEGY.md 与 graphify-out/graph.json 中无 T0~T4 五阶段矩阵残留"""
        manual_p = self.repo_root / "docs" / "倍率时序波动分析手册.md"
        strategy_p = self.repo_root / "STRATEGY.md"
        graph_p = self.repo_root / "graphify-out" / "graph.json"

        manual_text = manual_p.read_text(encoding="utf-8")
        strategy_text = strategy_p.read_text(encoding="utf-8")
        graph_text = graph_p.read_text(encoding="utf-8")

        self.assertNotIn("五阶段时序生命周期矩阵（T0~T4）", manual_text)
        self.assertNotIn("T0~T4 五阶段分钟级时序矩阵", strategy_text)
        self.assertNotIn("t0_t4_five_phase_matrix", graph_text)
        self.assertNotIn("T0~T4 五阶段时序生命周期矩阵", graph_text)


if __name__ == "__main__":
    unittest.main()


