"""
校验/ 测试用例: 适配器层 CLI 单元与端到端测试 (TDD 红灯阶段)
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path


class TestAdapterCli(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(".").resolve()
        self.cli_py = self.repo_root / "校验" / "src" / "adapter" / "cli.py"
        self.valid_snapshot = self.repo_root / "data" / "2026-10-06" / "2981506.json"

    def test_cli_match_valid_snapshot_exit_0(self):
        """测试对真实完整快照执行 CLI，必须输出 PASS 且退出码为 0"""
        cmd = [sys.executable, str(self.cli_py), "--match", str(self.valid_snapshot)]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"CLI stderr: {res.stderr}")
        self.assertIn("验收全部通过 (PASS)", res.stdout)
        self.assertIn("2981506", res.stdout)

    def test_cli_match_json_flag_outputs_valid_json(self):
        """测试 CLI 携带 --json 时输出紧凑结构化 JSON 且退出码为 0"""
        cmd = [sys.executable, str(self.cli_py), "--match", str(self.valid_snapshot), "--json"]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertTrue(data.get("is_valid"))
        self.assertEqual(data.get("match_id"), "2981506")
        self.assertEqual(data.get("overall_status"), "PASS")

    def test_cli_match_non_existent_file_exit_1(self):
        """测试对不存在的残缺快照执行 CLI，必须被物理阻断且退出码为 1"""
        cmd = [sys.executable, str(self.cli_py), "--match", "data/not_exist.json"]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True)
        self.assertEqual(res.returncode, 1)  # 物理熔断！
        self.assertIn("验收失败 (FAIL)", res.stderr or res.stdout)

    def test_cli_system_consistency_exit_0(self):
        """测试 CLI 执行系统全库巡检 --system，必须退出码为 0"""
        cmd = [sys.executable, str(self.cli_py), "--system"]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("全库一致性与图谱连通性正常", res.stdout)

    def test_cli_console_output_warn_status_shows_warning_not_all_pass(self):
        """测试U2: 当收据为 WARN 状态时，控制台明确输出‘验收存在警告 (WARN)’而不是‘验收全部通过’"""
        from 校验.src.domain.model import CheckStatus, DimensionType, DimensionResult, VerificationReceipt
        from 校验.src.adapter.cli import format_receipt_console

        results = [
            DimensionResult(DimensionType.BASIC_STATS, CheckStatus.PASS, "战绩齐全"),
            DimensionResult(DimensionType.EUROPE_1X2, CheckStatus.PASS, "欧指齐全"),
            DimensionResult(DimensionType.ASIAN_HANDICAP, CheckStatus.PASS, "亚盘齐全"),
            DimensionResult(DimensionType.OVER_UNDER, CheckStatus.PASS, "大小球齐全"),
            DimensionResult(DimensionType.TREND_HISTORY, CheckStatus.PASS, "时序完整"),
            DimensionResult(DimensionType.CROWN_CORRECT_SCORE, CheckStatus.PASS, "波胆齐全"),
            DimensionResult(DimensionType.LINEUP_INJURY, CheckStatus.WARN, "伤停未核实(暂无数据)"),
        ]
        receipt = VerificationReceipt(match_id="999999", results=results)
        output = format_receipt_console(receipt)
        self.assertIn("验收存在警告 (WARN)", output)
        self.assertNotIn("验收全部通过", output)


if __name__ == "__main__":
    unittest.main()
