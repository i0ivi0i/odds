"""
校验/ 测试用例: 适配器层 CLI 单元与端到端测试 (TDD 红灯阶段)
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class TestAdapterCli(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(".").resolve()
        self.cli_py = self.repo_root / "校验" / "src" / "adapter" / "cli.py"
        self.valid_snapshot = self.repo_root / "data" / "2026-10-06" / "2981506.json"

    def test_cli_match_valid_snapshot_exit_0(self):
        """测试对真实完整【推演源数据】执行 CLI，必须输出 PASS 且退出码为 0"""
        cmd = [sys.executable, str(self.cli_py), "--match", str(self.valid_snapshot)]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(res.returncode, 0, f"CLI stderr: {res.stderr}")
        self.assertIn("验收全部通过 (PASS)", res.stdout)
        self.assertIn("2981506", res.stdout)

    def test_cli_match_json_flag_outputs_valid_json(self):
        """测试 CLI 携带 --json 时输出紧凑结构化 JSON 且退出码为 0"""
        cmd = [sys.executable, str(self.cli_py), "--match", str(self.valid_snapshot), "--json"]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertTrue(data.get("is_valid"))
        self.assertEqual(data.get("match_id"), "2981506")
        self.assertEqual(data.get("overall_status"), "PASS")

    def test_cli_match_non_existent_file_exit_1(self):
        """测试对不存在的残缺【推演源数据】执行 CLI，必须被物理阻断且退出码为 1"""
        cmd = [sys.executable, str(self.cli_py), "--match", "data/not_exist.json"]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(res.returncode, 1)  # 物理熔断！
        self.assertIn("验收失败 (FAIL)", res.stderr or res.stdout)

    def test_cli_system_consistency_exit_0(self):
        """测试 CLI 执行系统全库巡检 --system，必须退出码为 0"""
        cmd = [sys.executable, str(self.cli_py), "--system"]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
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

    def test_cli_max_age_minutes_blocks_stale_file(self):
        """测试 CLI 传入 --max-age-minutes 拦截历史过期【推演源数据】返回退出码 1"""
        cmd = [sys.executable, str(self.cli_py), "--match", str(self.valid_snapshot), "--max-age-minutes", "1"]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(res.returncode, 1)
        self.assertIn("STALE_SNAPSHOT", res.stderr + res.stdout)

    def test_cli_rejects_excessive_max_age_minutes(self):
        """测试 CLI 严禁传入超过 45 分钟的新鲜度阈值，防止擅自调大逃避过期"""
        cmd = [sys.executable, str(self.cli_py), "--match", str(self.valid_snapshot), "--max-age-minutes", "300"]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(res.returncode, 1)
        self.assertIn("超过系统法定允许最大值", res.stderr + res.stdout)


    def test_cli_batch_isolate_failed_quarantines_and_passes_valid(self):
        """测试 CLI 批量安检模式下启用 --isolate-failed：自动隔离违规快照并放行合格集群"""
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            # 放入一个合法的真实快照文件
            valid_src = self.repo_root / "data" / "2026-10-11" / "3003906.md"
            valid_dest = tmp_path / "3003906.md"
            shutil.copy(str(valid_src), str(valid_dest))

            # 放入一个破损违规的快照文件
            corrupt_dest = tmp_path / "9999999.md"
            corrupt_dest.write_text("# 破损残缺快照", encoding="utf-8")

            # 未开启 --isolate-failed 时：必须退出码 1 熔断
            cmd_strict = [sys.executable, str(self.cli_py), "--batch", str(tmp_path)]
            res_strict = subprocess.run(cmd_strict, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res_strict.returncode, 1)
            self.assertIn("批量安检失败", res_strict.stderr + res_strict.stdout)

            # 开启 --isolate-failed 时：自动隔离违规文件，合格场次放行 (退出码 0)
            cmd_isolate = [sys.executable, str(self.cli_py), "--batch", str(tmp_path), "--isolate-failed"]
            res_isolate = subprocess.run(cmd_isolate, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res_isolate.returncode, 0, f"stderr: {res_isolate.stderr}")
            self.assertIn("故障隔离触发", res_isolate.stdout)
            self.assertIn("3003906", res_isolate.stdout)
            self.assertTrue((tmp_path / ".quarantine" / "9999999.md").exists())
            self.assertFalse(corrupt_dest.exists())

    def test_cli_verify_memory_success(self):
        """测试 CLI 使用 --verify-memory 核验合法认知契约卡，返回退出码 0"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_mem = Path(tmpdir) / "test_memory.md"
            content = """# 测试记忆
## 深度分析

### 意甲 亚特兰大 vs 威尼斯（编号: 周一002 比赛ID: 2993805，开球: 2026-10-13 00:30，分析: 2026-10-12 21:00）
#### 综合评估
- 胜平负：首选 主胜｜次选 平局
- 胜/平/负点概率（OO-EPC去水）：胜 77.57% / 平 14.16% / 负 8.27%
- 【图谱认知基因】：[Egidi 攻防参数凸组合, 赔率分析推演十大公理] ｜ 演绎链：火力碾压 -> 深盘阻热 -> 正路设防
- 【认知契约卡】：
  - 选择与排除依据：火力碾压排除客胜
  - 关键拍板依据：深盘高门槛有效阻热
  - 庄家博弈假说与竞争解释：实控主胜赔付
  - 可推翻反证与改变条件：若退盘则推翻
"""
            tmp_mem.write_text(content, encoding="utf-8")
            cmd = [sys.executable, str(self.cli_py), "--verify-memory", str(tmp_mem), "--expected-matches", "1"]
            res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res.returncode, 0)
            self.assertIn("验收全部通过", res.stdout)

    def test_cli_verify_memory_failure_missing_dimension_exit_1(self):
        """测试 CLI 使用 --verify-memory 核验缺失维度的残缺契约卡，必须退出码 1 熔断"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_mem = Path(tmpdir) / "test_memory.md"
            content = """# 测试记忆
## 深度分析

### 意甲 亚特兰大 vs 威尼斯（编号: 周一002 比赛ID: 2993805）
#### 综合评估
- 胜平负：首选 主胜
- 【认知契约卡】：
  - 选择与排除依据：火力碾压
"""
            tmp_mem.write_text(content, encoding="utf-8")
            cmd = [sys.executable, str(self.cli_py), "--verify-memory", str(tmp_mem)]
            res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res.returncode, 1)
            self.assertIn("验收拦截失败", res.stderr + res.stdout)


if __name__ == "__main__":
    unittest.main()


