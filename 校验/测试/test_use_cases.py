"""
校验/ 测试用例: 应用层用例单元测试 (TDD 红灯阶段)
"""

import json
import os
import unittest
from pathlib import Path
from 校验.src.application.use_cases import (
    VerifySnapshotUseCase,
    CheckConsistencyUseCase,
)
from 校验.src.domain.model import CheckStatus


class TestUseCases(unittest.TestCase):
    def setUp(self):
        self.verify_use_case = VerifySnapshotUseCase()
        self.consistency_use_case = CheckConsistencyUseCase()
        self.repo_root = Path(".").resolve()

    def test_verify_real_match_snapshot_passes(self):
        """测试对真实存在的快照 data/2026-10-06/2981506.json 的检验"""
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


if __name__ == "__main__":
    unittest.main()
