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


if __name__ == "__main__":
    unittest.main()
