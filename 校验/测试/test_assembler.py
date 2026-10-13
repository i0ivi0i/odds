"""
校验/测试/test_assembler.py
【推演源数据】组装器单元测试: 确保 SnapshotAssembler 输出的 Markdown 能 100% 通过物理门禁
"""

import hashlib
import json
import re
import unittest
from pathlib import Path
from 校验.src.domain.assembler import SnapshotAssembler
from 校验.src.domain.verifier import SnapshotVerifier
from 校验.src.application.use_cases import VerifySnapshotUseCase


class TestSnapshotAssembler(unittest.TestCase):
    def setUp(self):
        self.assembler = SnapshotAssembler()
        self.use_case = VerifySnapshotUseCase()

    def _build_valid_verbatim_data(self):
        return {
            "matchId": "2989999",
            "league": "英超",
            "homeTeam": "曼城",
            "awayTeam": "切尔西",
            "kickoffTime": "2026-10-10 22:00",
            "sportteryCode": "周六020",
            "polymarketUrl": "https://polymarket.com/sports/epl/mci-che",
            "lineupData": "- 主队伤停：\n  - 罗德里 (主力中场，膝伤缺阵)\n- 客队伤停：\n  - 帕尔默 (主力前锋，肌肉拉伤)",
            "basicStatsText": "- 主队近况（曼城）：联赛排名第2，近6场进14失4，主场胜率 80%，场均进球 2.5\n- 客队近况（切尔西）：联赛排名第4，近6场进11失6，客场场均失球 1.0\n- 历史交锋与盘路：近6次交手曼城4胜2平，相同初盘赢盘率65%",
            "europe1x2": [
                {
                    "zone": "核心做市",
                    "company": cname,
                    "initialOdds": ["1.90", "3.50", "3.80"],
                    "initialReturn": "91.50%",
                    "liveOdds": ["1.95", "3.50", "3.70"],
                    "liveReturn": "91.50%",
                    "kelly": ["0.93", "0.94", "0.95"],
                    "changeTime": "10-10 19:30",
                }
                for cname in [
                    "澳彩", "Crown", "Bet365", "易胜博", "平博", "188Bet", "香港马会",
                    "威廉希尔", "立博", "Bwin", "Interwetten", "SNAI", "伟德", "必发",
                    "SBO", "沙巴", "Marathon", "Betway", "Unibet", "Paddy Power", "10Bet",
                    "中国体彩", "Polymarket"
                ]
            ],
            "澳彩_ah": [("10-10 19:30", "平半", "0.82", "1.02", "即"), ("10-09 20:00", "半球", "0.90", "0.94", "初盘")],
            "皇冠_ah": [("10-10 19:28", "平半", "0.83", "1.05", "即"), ("10-09 20:05", "半球", "0.91", "0.97", "初盘")],
            "Bet365_ah": [("10-10 19:25", "平半", "0.82", "1.05", "即"), ("10-10 14:10", "平半", "0.85", "1.02", "即"), ("10-09 19:50", "半球", "0.90", "0.95", "初盘")],
            "易胜博_ah": [("10-10 19:20", "平半", "0.84", "1.04", "即"), ("10-09 20:10", "半球", "0.90", "0.96", "初盘")],
            "平博_ah": [("10-10 19:30", "平半", "0.83", "1.06", "即"), ("10-09 21:00", "半球", "0.92", "0.96", "初盘")],
            "188Bet_ah": [("10-10 19:15", "平半", "0.82", "1.06", "即"), ("10-09 20:30", "半球", "0.90", "0.98", "初盘")],
            "香港马会_ah": [("10-10 19:10", "平半", "0.80", "1.00", "即"), ("10-09 18:00", "半球", "0.88", "0.92", "初盘")],
            "澳彩_ou": [("10-10 19:30", "2.5", "0.95", "0.85", "即"), ("10-09 20:00", "2.5", "0.88", "0.92", "初盘")],
            "皇冠_ou": [("10-10 19:28", "2.5", "0.96", "0.92", "即"), ("10-09 20:05", "2.5", "0.89", "0.99", "初盘")],
            "Bet365_ou": [("10-10 19:25", "2.5", "0.95", "0.90", "即"), ("10-09 19:50", "2.5", "0.88", "0.98", "初盘")],
            "易胜博_ou": [("10-10 19:20", "2.5", "0.94", "0.92", "即"), ("10-09 20:10", "2.5", "0.88", "0.98", "初盘")],
            "平博_ou": [("10-10 19:30", "2.5", "0.96", "0.92", "即"), ("10-09 21:00", "2.5", "0.89", "0.99", "初盘")],
            "188Bet_ou": [("10-10 19:15", "2.5", "0.95", "0.91", "即"), ("10-09 20:30", "2.5", "0.88", "0.98", "初盘")],
            "香港马会_ou": [("10-10 19:10", "2.5", "0.92", "0.84", "即"), ("10-09 18:00", "2.5", "0.85", "0.91", "初盘")],
            "澳彩_eu": [("10-10 19:30", "1.95", "3.50", "3.70", "91.50%", "0.93/0.94/0.95", "即"), ("10-09 20:00", "1.90", "3.50", "3.80", "91.50%", "0.91/0.94/0.97", "初盘")],
            "皇冠_eu": [("10-10 19:28", "1.95", "3.50", "3.70", "91.50%", "0.93/0.94/0.95", "即"), ("10-09 20:05", "1.90", "3.50", "3.80", "91.50%", "0.91/0.94/0.97", "初盘")],
            "Bet365_eu": [("10-10 19:25", "1.95", "3.50", "3.70", "91.50%", "0.93/0.94/0.95", "即"), ("10-09 19:50", "1.90", "3.50", "3.80", "91.50%", "0.91/0.94/0.97", "初盘")],
            "correctScores": [
                ("1:0", "7.50", "0:0", "9.00", "0:1", "8.50"),
                ("2:0", "9.00", "1:1", "6.20", "0:2", "12.00"),
                ("2:1", "8.00", "2:2", "13.00", "1:2", "10.00"),
                ("3:0", "15.00", "3:3", "40.00", "0:3", "25.00"),
            ],
            "sporttery_had": [("10-10 19:00", "1.82", "3.35", "3.65", "88.50%", "0.88/0.92/0.91", "即"), ("10-09 12:00", "1.78", "3.40", "3.75", "88.50%", "0.86/0.93/0.93", "初盘")],
            "sporttery_hhad": [("-1", "3.45", "3.40", "1.82", "开售")],
        }

    def test_zero_hardcoded_fake_constants_in_codebase(self):
        """U1红灯测试: 静态扫描 assembler.py 与 use_cases.py，严禁存在任何硬编码假赔率、假时间或假文案兜底"""
        repo_root = Path(__file__).resolve().parent.parent.parent
        assembler_src = (repo_root / "校验" / "src" / "domain" / "assembler.py").read_text(encoding="utf-8")
        use_cases_src = (repo_root / "校验" / "src" / "application" / "use_cases.py").read_text(encoding="utf-8")

        forbidden_in_assembler = [
            "周--000",
            "联赛排名良好，主场进球稳定",
            "常规联赛轮次积分争夺",
            "2.10 | 3.25 | 3.40",
            "初始精算物理基准",
            "10-09 20:00",
            "10-10 19:30",
            "让平设防1球小胜",
            "胜 (2.10) | 平 (3.20) | 负 (3.10)",
            "54¢",
        ]
        for token in forbidden_in_assembler:
            self.assertNotIn(token, assembler_src, f"assembler.py 仍残留硬编码造假后门: {token}")

        forbidden_in_use_cases = [
            "10-08 12:00",
            "近6场数据完整",
            "主场战力充沛",
            "波胆 1:0 8.1, 2:0 11.5",
            "[0.94, 0.88, 0.84]",
        ]
        for token in forbidden_in_use_cases:
            self.assertNotIn(token, use_cases_src, f"use_cases.py 仍残留静默解析造假兜底: {token}")

    def test_assembler_rejects_missing_required_fields_without_fake_fallback(self):
        """U1红灯测试: 当缺失必填字段(basicStatsText、europe1x2、亚盘流水或波胆)时，必须直接抛出 ValueError，绝不填假数据"""
        incomplete = {
            "matchId": "2989999",
            "league": "英超",
            "homeTeam": "曼城",
            "awayTeam": "切尔西",
            "kickoffTime": "2026-10-10 22:00",
            "sportteryCode": "周六020",
        }
        with self.assertRaises(ValueError):
            self.assembler.assemble(incomplete)

        # 当某家欧指缺少赔率数组时，也必须抛出 ValueError
        bad_eu = self._build_valid_verbatim_data()
        bad_eu["europe1x2"] = [{"company": "Bet365"}]  # 缺失 initialOdds / liveOdds / kelly
        with self.assertRaises(ValueError):
            self.assembler.assemble(bad_eu)

    def test_assembled_markdown_passes_full_verification_and_has_no_t0_t4_padding(self):
        """U2红灯测试: 组装器输出的纯净无损【推演源数据】不含 T0~T4 凑数与主观形态列，且 100% 通过门禁"""
        data = self._build_valid_verbatim_data()
        md_text = self.assembler.assemble(data)
        self.assertIn("# 【周六020】英超 曼城 vs 切尔西", md_text)
        self.assertIn("## 三、欧洲指数百家做市商清单（法定 23 家）", md_text)

        # 严格断言已废除 T0~T4 凑数标签、废除“做市形态学识别”主观列、废除第二战区14家伪时序表
        self.assertNotIn("T0 初盘骨架", md_text)
        self.assertNotIn("T2 中盘假摔", md_text)
        self.assertNotIn("做市形态学识别", md_text)
        self.assertNotIn("### 第二战区：欧洲大陆与国际纯欧指做市商", md_text)

        # 解析并执行门禁
        snap = self.use_case._parse_markdown_snapshot(md_text, "2989999")
        snap["_raw_content"] = md_text
        receipt = self.use_case.verifier.verify(snap)

        self.assertTrue(receipt.is_valid, f"验证失败: {[r.message for r in receipt.results if r.status.value == 'FAIL']}")
        self.assertEqual(receipt.failed_count, 0)

    def test_assembler_filters_alien_bookmakers_and_never_fabricates_missing_companies(self):
        """测试装配器过滤外来野鸡机构，且当某法定机构未在 europe1x2 提供时绝不伪造 2.10/3.25/3.40"""
        data = self._build_valid_verbatim_data()
        data["europe1x2"].append({
            "company": "All British Casino",
            "initialOdds": ["10.0", "7.0", "1.2"],
            "initialReturn": "92.0%",
            "liveOdds": ["12.0", "8.5", "1.15"],
            "liveReturn": "93.0%",
            "kelly": ["0.90", "0.90", "0.90"],
        })
        # 移除 SNAI 模拟该场 SNAI 未开盘
        data["europe1x2"] = [r for r in data["europe1x2"] if r["company"] != "SNAI"]
        md_text = self.assembler.assemble(data)
        self.assertNotIn("All British Casino", md_text)
        self.assertNotIn("2.10 | 3.25 | 3.40", md_text)
        self.assertIn("| 老庄机构 | SBO |", md_text)
        self.assertIn("| 论文样本 | Marathon |", md_text)
        self.assertIn("| 终端履约 | 中国体彩 |", md_text)

    def test_run_assemble_prints_physical_receipt(self):
        """测试 CLI run_assemble 生成【推演源数据】时输出包含完整属性的法定收据"""
        import io
        import tempfile
        import json
        from unittest.mock import patch
        from 校验.src.adapter.cli import run_assemble

        data = self._build_valid_verbatim_data()
        with tempfile.TemporaryDirectory() as tmpdir:
            json_p = Path(tmpdir) / "test.json"
            md_p = Path(tmpdir) / "test.md"
            json_p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                exit_code = run_assemble(str(json_p), str(md_p))
                self.assertEqual(exit_code, 0)
                out = mock_stdout.getvalue()
                self.assertIn("[PHYSICAL_RECEIPT]", out)
                self.assertIn("sha256=", out)
                self.assertIn("mtime=", out)
                self.assertTrue(md_p.exists())

    def test_assembler_allows_dash_kelly_for_polymarket_and_single_row_sporttery(self):
        """U1红灯测试: 组装器必须支持 Polymarket 凯利列为 '-' 且体彩初即一致时单行真实记录，绝不强逼填假凯利或假初盘时间"""
        data = self._build_valid_verbatim_data()
        for c in data["europe1x2"]:
            if c["company"] == "Polymarket":
                c["kelly"] = ["-", "-", "-"]
                c["initialReturn"] = "98.97%"
                c["liveReturn"] = "98.97%"
        data["sporttery_had"] = [("10-13 09:05", "2.32", "3.50", "2.42", "87.98%", "0.87/0.91/0.88", "即")]

        md_text = self.assembler.assemble(data)
        self.assertIn("| 终端履约 | Polymarket | 1.90 | 3.50 | 3.80 | 98.97% | 1.95 | 3.50 | 3.70 | 98.97% | - |", md_text)
        self.assertNotIn("0.94/0.93/0.94", md_text)

        snap = self.use_case._parse_markdown_snapshot(md_text, "2989999")
        snap["_raw_content"] = md_text
        receipt = self.use_case.verifier.verify(snap)
        self.assertTrue(receipt.is_valid, f"验证失败: {[r.message for r in receipt.results if r.status.value == 'FAIL']}")

    def test_raw_parser_parse_raw_payloads_in_memory_and_build_atomic_bundle(self):
        """TDD RED 1: 测试 Titan007RawParser.parse_raw_payloads 纯内存解析与 build_atomic_bundle 单文件原子包打包"""
        from 校验.src.domain.raw_parser import Titan007RawParser

        raw_files = {
            "1x2d.js": 'var game=Array("3068865","葡甲","2026-10-13 18:00:00","费伦斯","波尔蒂芒尼斯");\nvar gameDetail=Array();\nvar hometeam="费伦斯";var guestteam="波尔蒂芒尼斯";',
            "meta.json": json.dumps({"matchId": "3068865", "matchNumber": "周二001", "homeTeam": "费伦斯", "awayTeam": "波尔蒂芒尼斯", "league": "葡甲", "kickoffTime": "2026-10-13 18:00", "polymarketUrl": "未开盘"}),
        }
        parser = Titan007RawParser()
        assembled, out_raw = parser.parse_raw_payloads("3068865", raw_files)
        self.assertEqual(assembled["matchId"], "3068865")
        self.assertEqual(assembled["homeTeam"], "费伦斯")
        self.assertEqual(assembled["sportteryCode"], "周二001")

        md_sample = "# 【周二001】葡甲 费伦斯 vs 波尔蒂芒尼斯\n\n- **比赛 ID**：3068865"
        bundle = parser.build_atomic_bundle("3068865", md_sample, raw_files)
        self.assertEqual(bundle["matchId"], "3068865")
        self.assertIn("markdown_sha256", bundle)
        self.assertIn("raw_files_sha256", bundle)
        self.assertIn("1x2d.js", bundle["payloads"])
        self.assertEqual(bundle["raw_files_sha256"]["1x2d.js"], hashlib.sha256(raw_files["1x2d.js"].encode("utf-8")).hexdigest())

    def test_verifier_authenticity_with_atomic_json_bundle(self):
        """TDD RED 2: 测试 VerifySnapshotUseCase 直接读取 raw/{matchId}.json 单文件原子包校验防伪通过与篡改拦截"""
        import tempfile
        from 校验.src.domain.raw_parser import Titan007RawParser

        data = self._build_valid_verbatim_data()
        md_text = self.assembler.assemble(data)

        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            md_path = base_dir / "2989999.md"
            md_path.write_text(md_text, encoding="utf-8")

            raw_dir = base_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)
            bundle_path = raw_dir / "2989999.json"

            raw_payloads = {
                "1x2d.js": 'var game=Array("2989999","荷乙","2026-10-13 02:00:00","埃因霍温FC","海牙");\nvar gameDetail=Array();\nvar hometeam="埃因霍温FC";var guestteam="海牙";',
            }
            bundle_obj = Titan007RawParser.build_atomic_bundle("2989999", md_text, raw_payloads)
            bundle_path.write_text(json.dumps(bundle_obj, ensure_ascii=False, indent=2), encoding="utf-8")

            # 正常验证单文件原子包: 必须正常加载 _raw_wire 并通过
            receipt = self.use_case.execute(str(md_path))
            self.assertTrue(receipt.is_valid, f"单文件原子包验证未通过: {[r.message for r in receipt.results if r.status.value == 'FAIL']}")

            # 篡改 .md 内容: 必须触发 TAMPERED_MARKDOWN_SEAL
            md_path.write_text(md_text + "\n<!-- tamper -->", encoding="utf-8")
            tamper_receipt = self.use_case.execute(str(md_path))
            self.assertFalse(tamper_receipt.is_valid)
            fail_msgs = [r.message for r in tamper_receipt.results if r.status.value == "FAIL"]
            self.assertTrue(any("TAMPERED_MARKDOWN_SEAL" in m for m in fail_msgs))

    def test_build_atomic_bundle_includes_valid_receipt(self):
        """TDD U1: 测试 build_atomic_bundle 必须自动生成合法的 network_receipt 结构并绑定端点哈希"""
        from 校验.src.domain.raw_parser import Titan007RawParser
        data = self._build_valid_verbatim_data()
        md_text = self.assembler.assemble(data)
        raw_payloads = {
            "1x2d.js": "var game=Array();",
            "odds.html": "<table>crown odds</table>",
        }
        bundle = Titan007RawParser.build_atomic_bundle("2989999", md_text, raw_payloads)
        self.assertIn("receipt", bundle)
        receipt = bundle["receipt"]
        self.assertEqual(receipt["fetcher"], "scrapling-mcp")
        self.assertEqual(receipt["matchId"], "2989999")
        self.assertEqual(receipt["endpointCount"], 2)
        self.assertEqual(len(receipt["endpoints"]), 2)
        ep_map = {e["file"]: e for e in receipt["endpoints"]}
        self.assertIn("1x2d.js", ep_map)
        self.assertEqual(ep_map["1x2d.js"]["status"], 200)
        self.assertEqual(ep_map["1x2d.js"]["payload_sha256"], bundle["raw_files_sha256"]["1x2d.js"])
        self.assertTrue(ep_map["1x2d.js"]["url"].startswith("https://1x2d.titan007.com/"))


    def test_run_assemble_bundle_creates_single_atomic_json_and_removes_loose_directory(self):
        """TDD RED 3: 测试 cli.py --assemble-bundle 纯离线装配生成 .md 与 raw/{matchId}.json，并自动清理旧碎文件目录"""
        import tempfile
        from 校验.src.adapter.cli import run_assemble_bundle
        from 校验.src.domain.raw_parser import Titan007RawParser

        data = self._build_valid_verbatim_data()
        md_text = self.assembler.assemble(data)

        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            date_dir = base_dir / "2026-10-13"
            date_dir.mkdir(parents=True, exist_ok=True)
            raw_dir = date_dir / "raw"
            raw_dir.mkdir(parents=True, exist_ok=True)

            # 模拟旧的乱糟糟 28 个碎文件目录
            loose_dir = raw_dir / "2989999"
            loose_dir.mkdir(parents=True, exist_ok=True)
            (loose_dir / "1x2d.js").write_text("old 1x2", encoding="utf-8")
            (loose_dir / "ah_1.html").write_text("old ah", encoding="utf-8")

            # 准备单文件原子包输入
            bundle_in_path = date_dir / "input_bundle.json"
            raw_payloads = {
                "1x2d.js": 'var game=Array("2989999","荷乙","2026-10-13 02:00:00","埃因霍温FC","海牙");\nvar gameDetail=Array();\nvar hometeam="埃因霍温FC";var guestteam="海牙";',
                "meta.json": json.dumps(data),
            }
            bundle_obj = {
                "matchId": "2989999",
                "payloads": raw_payloads,
            }
            bundle_in_path.write_text(json.dumps(bundle_obj, ensure_ascii=False), encoding="utf-8")

            out_md_path = date_dir / "2989999.md"
            exit_code = run_assemble_bundle(str(bundle_in_path), str(out_md_path))
            self.assertEqual(exit_code, 0)
            self.assertTrue(out_md_path.exists())

            # 检查单一原子存证文件已落盘
            target_atomic_json = raw_dir / "2989999.json"
            self.assertTrue(target_atomic_json.exists())

            # 检查旧的乱糟糟 28 个碎文件目录已被干净清理删除
            self.assertFalse(loose_dir.exists(), "旧的 loose raw/{matchId}/ 碎文件目录必须被自动清理删除！")


if __name__ == "__main__":
    unittest.main()




