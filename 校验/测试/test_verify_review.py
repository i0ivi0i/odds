"""
校验/测试用例: 赛后复盘机械质检门禁单元与端到端测试 (TDD 红灯阶段)
"""

import sys
import subprocess
import unittest
from pathlib import Path

class TestVerifyReview(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(".").resolve()
        self.cli_py = self.repo_root / "校验" / "src" / "adapter" / "cli.py"
        self.memory_file = self.repo_root / "memory" / "2026-10-16.md"
        self.memory_md = self.repo_root / "MEMORY.md"

    def test_verify_review_valid_file_passes(self):
        """测试对真实有效的 2026-10-16.md 复盘报告执行质检，必须返回 Exit 0 且输出 PASS"""
        from 校验.src.domain.verifier import verify_review_report
        content = self.memory_file.read_text(encoding="utf-8")
        memory_md_content = self.memory_md.read_text(encoding="utf-8")
        ok, errors, count = verify_review_report(content, memory_md_content=memory_md_content)
        self.assertTrue(ok, f"Verification failed with errors: {errors}")
        self.assertEqual(count, 10)
        self.assertEqual(len(errors), 0)

    def test_verify_review_missing_review_section_fails(self):
        """测试缺失 ## 赛后复盘 章节时必须返回 False 且报错"""
        from 校验.src.domain.verifier import verify_review_report
        broken = "# 2026-10-16\n## 推荐\n一些内容\n"
        ok, errors, count = verify_review_report(broken)
        self.assertFalse(ok)
        self.assertTrue(any("MISSING_REVIEW_SECTION" in err for err in errors))

    def test_verify_review_detects_forbidden_second_table(self):
        """测试复盘中若违规增设'表二'等冗余表格，必须报错熔断 (FORBIDDEN_SECOND_TABLE)"""
        from 校验.src.domain.verifier import verify_review_report
        valid_content = self.memory_file.read_text(encoding="utf-8")
        # 违规注入表二
        content_with_second_table = valid_content + "\n\n### 表二：待验证打卡表\n| 编号 | 假设 | 结果 |\n|---|---|---|\n| 1 | 测试 | 成功 |\n"
        ok, errors, _ = verify_review_report(content_with_second_table)
        self.assertFalse(ok)
        self.assertTrue(any("FORBIDDEN_SECOND_TABLE" in err for err in errors))

    def test_verify_review_detects_missing_handicap_checkmarks(self):
        """测试第 4 列让球对账缺失 ✅/❌ 判定时必须报错熔断"""
        from 校验.src.domain.verifier import verify_review_report
        valid_content = self.memory_file.read_text(encoding="utf-8")
        # 把让球对账的 ✅ 抹去
        tampered = valid_content.replace("[+1] 让负（次选让平） 【首选中 ✅】", "[+1] 让负（次选让平）")
        ok, errors, _ = verify_review_report(tampered)
        self.assertFalse(ok)
        self.assertTrue(any("MISSING_HANDICAP_RESULT" in err for err in errors))

    def test_verify_review_cli_command(self):
        """测试 CLI 命令行 --verify-review 执行端到端检验，正常返回 Exit 0"""
        cmd = [sys.executable, str(self.cli_py), "--verify-review", str(self.memory_file)]
        res = subprocess.run(cmd, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(res.returncode, 0, f"stderr: {res.stderr}\nstdout: {res.stdout}")
        self.assertIn("赛后复盘质检通过 (PASS)", res.stdout)


if __name__ == "__main__":
    unittest.main()
