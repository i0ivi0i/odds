"""
校验/测试/test_integrity_auditor.py
数据纯净度、全链路防失真与五重轮番穿透质检单元测试
理论依据：
1. Winkelmann (2026) 微观结构状态守恒与防抖保真
2. Wheatcroft (2019) 盘口信息率不变量理论
3. 单调子序列与 SHA-256 不可篡改数学公理
"""

import unittest
from pathlib import Path
import json
import hashlib
from 校验.src.domain.integrity_auditor import (
    IntegrityAuditor,
    IntegrityAuditReport,
    AuditDimension,
    AuditStatus,
)


class TestIntegrityAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = IntegrityAuditor()
        self.sample_raw_path = "data/2026-10-13/raw/3008263.json"
        self.sample_md_path = "data/2026-10-13/3008263.md"

    def test_real_match_integrity_audit_passes(self):
        """测试真实落盘数据在五重质检下 100% 全部通过 (PASS)"""
        if not Path(self.sample_raw_path).exists() or not Path(self.sample_md_path).exists():
            self.skipTest("实盘数据文件不存在，跳过")

        report: IntegrityAuditReport = self.auditor.audit_match(
            self.sample_raw_path, self.sample_md_path
        )
        self.assertTrue(report.is_valid, f"质检未通过: {report.summary_failures()}")
        self.assertEqual(report.extremum_coverage_rate, 1.0, "极值覆盖率必须为 100%")
        self.assertEqual(report.extremum_lost_count, 0, "极值丢失数必须为 0")
        self.assertEqual(report.temporal_inversions_count, 0, "时序倒置数必须为 0")
        self.assertEqual(report.fabricated_rows_count, 0, "伪造插值行数必须为 0")

    def test_tampered_sha256_seal_detected(self):
        """测试篡改哪怕一个字符，SHA-256 封条质检立即报 FAIL"""
        if not Path(self.sample_raw_path).exists() or not Path(self.sample_md_path).exists():
            self.skipTest("实盘数据文件不存在，跳过")

        md_text = Path(self.sample_md_path).read_text(encoding="utf-8")
        tampered_md = md_text + "\n<!-- Tampered Comment -->"

        report = self.auditor.audit_content(self.sample_raw_path, tampered_md)
        self.assertFalse(report.is_valid)
        seal_res = report.get_result(AuditDimension.SHA256_SEAL)
        self.assertIsNotNone(seal_res)
        self.assertEqual(seal_res.status, AuditStatus.FAIL)

    def test_temporal_inversion_detected(self):
        """测试人为颠倒时序表格中的行，时序单调性检查立即报 FAIL"""
        if not Path(self.sample_raw_path).exists() or not Path(self.sample_md_path).exists():
            self.skipTest("实盘数据文件不存在，跳过")

        md_text = Path(self.sample_md_path).read_text(encoding="utf-8")
        # 寻找变盘时间行并对调两行时间戳导致时序倒置
        lines = md_text.splitlines()
        swapped = False
        for i in range(len(lines) - 1):
            if lines[i].startswith("| 10-") and lines[i + 1].startswith("| 10-"):
                lines[i], lines[i + 1] = lines[i + 1], lines[i]
                swapped = True
                break
        self.assertTrue(swapped, "未能找到可交换的时间行")
        inverted_md = "\n".join(lines)

        report = self.auditor.audit_content(self.sample_raw_path, inverted_md, skip_seal=True)
        self.assertFalse(report.is_valid)
        mono_res = report.get_result(AuditDimension.MONOTONIC_TIMELINE)
        self.assertIsNotNone(mono_res)
        self.assertEqual(mono_res.status, AuditStatus.FAIL)

    def test_missing_extremum_detected(self):
        """测试人为削掉极值点（如最高水或最低水），极值守恒检测立即报 FAIL"""
        # 构造微型 raw 与人为漏掉极值点的 md 进行纯单元测试
        raw_rows = [
            ("10-13 20:00", "半球", "0.85", "1.05", "即"),
            ("10-13 18:00", "半球", "0.77", "1.13", "即"),  # 0.77 为最低水极值
            ("10-13 12:00", "半球", "0.90", "0.95", "初盘"),
        ]
        # md 中故意缺失 0.77 这一行
        md_table_rows = [
            ("10-13 20:00", "半球", "0.85", "1.05", "即"),
            ("10-13 12:00", "半球", "0.90", "0.95", "初盘"),
        ]
        res = self.auditor.check_extremum_preservation(
            company="皇冠", market="ah", raw_rows=raw_rows, md_rows=md_table_rows
        )
        self.assertFalse(res["passed"])
        self.assertIn("0.77", str(res["lost_extrema"]))

    def test_fabricated_synthetic_row_detected(self):
        """测试 md 中出现原始报文中不存在的虚构数字，单调子序列防伪立即报 FAIL"""
        raw_rows = [
            ("10-13 20:00", "半球", "0.85", "1.05", "即"),
            ("10-13 12:00", "半球", "0.90", "0.95", "初盘"),
        ]
        md_table_rows = [
            ("10-13 20:00", "半球", "0.85", "1.05", "即"),
            ("10-13 15:00", "半球", "0.88", "1.00", "即"),  # 伪造行
            ("10-13 12:00", "半球", "0.90", "0.95", "初盘"),
        ]
        res = self.auditor.check_verbatim_subsequence(
            company="皇冠", market="ah", raw_rows=raw_rows, md_rows=md_table_rows
        )
        self.assertFalse(res["passed"])
        self.assertEqual(res["fabricated_count"], 1)

    def test_missing_initial_or_latest_line_detected(self):
        """测试初盘或即时盘被错改，不变量守恒立即报 FAIL"""
        raw_rows = [
            ("10-13 20:00", "半球", "0.85", "1.05", "即"),
            ("10-13 12:00", "半球", "0.90", "0.95", "初盘"),
        ]
        # 错改初盘
        md_table_rows = [
            ("10-13 20:00", "半球", "0.85", "1.05", "即"),
            ("10-13 12:00", "半球", "0.92", "0.93", "初盘"),  # 篡改初盘数值
        ]
        res = self.auditor.check_invariants_conservation(
            company="皇冠", market="ah", raw_rows=raw_rows, md_rows=md_table_rows
        )
        self.assertFalse(res["passed"])
        self.assertIn("初盘不一致", res["message"])


if __name__ == "__main__":
    unittest.main()
