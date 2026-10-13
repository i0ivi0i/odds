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
            # 放入一个合法的真实快照文件 (不含 T0~T4 凑数的新规范样本，matchId=3000474)
            valid_src = self.repo_root / "校验" / "测试" / "fixtures" / "golden_snapshot_sample.md"
            valid_dest = tmp_path / "3000474.md"
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
            self.assertIn("3000474", res_isolate.stdout)
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

    def test_cli_assemble_seals_manifest_and_blocks_single_punctuation_tampering(self):
        """测试U3端到端: cli.py --assemble 自动写入加密封条 manifest.json，随后只要篡改 .md 哪怕一个标点符号，cli.py --match 立即 exit 1 熔断"""
        from 校验.测试.test_assembler import TestSnapshotAssembler
        valid_data = TestSnapshotAssembler()._build_valid_verbatim_data()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_p = tmp_path / "2989999.json"
            md_p = tmp_path / "2989999.md"
            json_p.write_text(json.dumps(valid_data, ensure_ascii=False), encoding="utf-8")

            # 1. 执行 CLI 装配
            cmd_asm = [sys.executable, str(self.cli_py), "--assemble", str(json_p), "--output", str(md_p)]
            res_asm = subprocess.run(cmd_asm, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res_asm.returncode, 0, f"stderr: {res_asm.stderr}")
            self.assertTrue((tmp_path / "raw" / "2989999.json").exists())

            # 2. 未篡改时，CLI 校验必须 PASS (exit 0)
            cmd_chk = [sys.executable, str(self.cli_py), "--match", str(md_p)]
            res_chk = subprocess.run(cmd_chk, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res_chk.returncode, 0, f"stderr: {res_chk.stderr}")

            # 3. 篡改 .md 中仅仅一个标点符号，CLI 校验必须立即返回 exit 1 (TAMPERED_MARKDOWN_SEAL)
            tampered_text = md_p.read_text(encoding="utf-8") + "。"
            md_p.write_text(tampered_text, encoding="utf-8")
            res_tampered = subprocess.run(cmd_chk, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res_tampered.returncode, 1)
            self.assertIn("TAMPERED_MARKDOWN_SEAL", res_tampered.stderr + res_tampered.stdout)

    def test_cli_assemble_rejects_json_odds_mismatching_raw_1x2d_js(self):
        """测试漏洞封堵3: cli.py --assemble 在装配阶段即核对 rawFiles['1x2d.js']，若输入 JSON 欧指造假与原始报文不符，当场 exit 1 拒绝生成 .md"""
        from 校验.测试.test_assembler import TestSnapshotAssembler
        fake_data = TestSnapshotAssembler()._build_valid_verbatim_data()
        # 注入真实 1x2d.js 原文 (Bet365 为 2.15 -> 2.35)，但 JSON 中 Bet365 被篡改为 1.55 -> 1.53
        fake_data["rawFiles"] = {
            "1x2d.js": (
                'var hometeam_cn="大阪樱花";var guestteam_cn="横滨水手";'
                'var game=Array("281|101|Bet365|2.15|3.50|2.80|43.1|26.5|30.4|92.60|2.35|3.50|2.62|39.5|26.5|34.0|92.90|0.93|0.94|0.92|2026,10-1,10,17,55,00");'
            )
        }
        for c in fake_data["europe1x2"]:
            if c["company"] == "Bet365":
                c["initialOdds"] = ["1.55", "3.80", "5.20"]
                c["liveOdds"] = ["1.53", "3.85", "5.30"]

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_p = tmp_path / "2989999.json"
            md_p = tmp_path / "2989999.md"
            json_p.write_text(json.dumps(fake_data, ensure_ascii=False), encoding="utf-8")

            cmd_asm = [sys.executable, str(self.cli_py), "--assemble", str(json_p), "--output", str(md_p)]
            res_asm = subprocess.run(cmd_asm, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res_asm.returncode, 1)
            self.assertIn("RAW_PROVENANCE_MISMATCH", res_asm.stderr + res_asm.stdout)
            self.assertFalse(md_p.exists())

    def test_cli_assemble_raw_dir_end_to_end_zero_llm_touch(self):
        """U2红灯测试: cli.py --assemble-raw-dir 直接读取 raw/{matchId}/ 原始报文全量装配 .md 与 manifest.json，零行数截断、零状态篡改"""
        from datetime import datetime
        now_dt = datetime.now()
        mm_dd = now_dt.strftime("%m-%d")
        hh_mm = now_dt.strftime("%H:%M")
        js_time = f"2026,{now_dt.month}-1,{now_dt.day},{now_dt.hour:02d},{now_dt.minute:02d},00"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            raw_dir = tmp_path / "raw" / "3068865"
            raw_dir.mkdir(parents=True, exist_ok=True)
            md_p = tmp_path / "3068865.md"

            # 1. 写入 meta.json
            (raw_dir / "meta.json").write_text(
                json.dumps(
                    {
                        "matchId": "3068865",
                        "league": "日职乙",
                        "homeTeam": "鹿儿岛联",
                        "awayTeam": "鸟栖沙岩",
                        "kickoffTime": f"{now_dt.strftime('%Y-%m-%d')} 18:00",
                        "sportteryCode": "周二001",
                        "polymarketUrl": "https://polymarket.com/event/j2-kag-sag",
                        "lineupData": "- 主队伤停：暂无数据\n- 客队伤停：暂无数据",
                        "basicStatsText": "- 主队近况（鹿儿岛联）：近6场进8失6，主场胜率50%\n- 客队近况（鸟栖沙岩）：近6场进10失5，客场场均进球1.6\n- 历史交锋与盘路：近3次交手1胜1平1负",
                        "sporttery_hhad": [["+1", "1.45", "4.00", "5.10", "开售"]],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            # 2. 写入 1x2d.js (包含22家传统机构 + Lottery Official)
            comp_defs = [
                ("80", "Macauslot"), ("545", "Crown"), ("281", "Bet365"), ("90", "Easybets"),
                ("177", "Pinnacle"), ("517", "188bet"), ("432", "HKJC"), ("115", "William Hill"),
                ("82", "Ladbrokes"), ("255", "Bwin"), ("104", "Interwetten"), ("70", "SNAI"),
                ("81", "Vcbet"), ("2", "Betfair"), ("499", "SBO"), ("976", "IBC"),
                ("136", "Marathon"), ("659", "Betway"), ("386", "Unibet"), ("562", "Paddy Power"),
                ("16", "10BET"), ("478", "Lottery Official"),
            ]
            game_items = []
            for idx, (cid, cname) in enumerate(comp_defs, start=100):
                if cid == "478":
                    game_items.append(
                        f'"{cid}|{idx}|{cname}|2.32|3.50|2.42|37.9|25.1|36.3|87.98|2.32|3.50|2.42|37.9|25.1|36.3|87.98|0.87|0.91|0.88|{js_time}"'
                    )
                else:
                    game_items.append(
                        f'"{cid}|{idx}|{cname}|2.45|3.55|2.50|37.5|25.9|36.6|91.80|2.40|3.55|2.55|38.2|25.8|36.0|91.80|0.92|0.93|0.91|{js_time}"'
                    )
            raw_js = (
                'var hometeam_cn="鹿儿岛联";var guestteam_cn="鸟栖沙岩";var matchname_cn="日职乙";'
                f'var MatchTime="{js_time}";'
                f'var game=Array({",".join(game_items)});'
            )
            (raw_dir / "1x2d.js").write_text(raw_js, encoding="utf-8")

            # 3. 写入 polymarket.json
            (raw_dir / "polymarket.json").write_text(
                json.dumps(
                    {
                        "url": "https://polymarket.com/event/j2-kag-sag",
                        "initialPrices": [0.38, 0.25, 0.37],
                        "livePrices": [0.39, 0.25, 0.36],
                        "changeTime": f"{mm_dd} {hh_mm}",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            # 4. 写入 7 家核心机构的 ah_{cid}.html, ou_{cid}.html, eu_{cid}.html (含 '早' 状态字和多行)
            for cid in ("1", "3", "8", "12", "47", "42", "48"):
                (raw_dir / f"ah_{cid}.html").write_text(
                    f"""<table>
                    <tr><td>0.85</td><td>平手</td><td>0.95</td><td>{mm_dd} {hh_mm}</td><td>即</td></tr>
                    <tr><td>0.88</td><td>平手</td><td>0.92</td><td>{mm_dd} 08:30</td><td>早</td></tr>
                    <tr><td>0.90</td><td>平手</td><td>0.90</td><td>10-11 16:00</td><td>初盘</td></tr>
                    </table>""",
                    encoding="utf-8",
                )
                (raw_dir / f"ou_{cid}.html").write_text(
                    f"""<table>
                    <tr><td>0.92</td><td>2.5/3</td><td>0.88</td><td>{mm_dd} {hh_mm}</td><td>即</td></tr>
                    <tr><td>0.90</td><td>2.5/3</td><td>0.90</td><td>{mm_dd} 08:30</td><td>早</td></tr>
                    <tr><td>0.88</td><td>2.5/3</td><td>0.92</td><td>10-11 16:00</td><td>初盘</td></tr>
                    </table>""",
                    encoding="utf-8",
                )
                (raw_dir / f"eu_{cid}.html").write_text(
                    f"""<table>
                    <tr><td>2.40</td><td>3.55</td><td>2.55</td><td>91.80%</td><td>0.92</td><td>0.93</td><td>0.91</td><td>{mm_dd} {hh_mm}(即)</td></tr>
                    <tr><td>2.42</td><td>3.55</td><td>2.52</td><td>91.75%</td><td>0.93</td><td>0.93</td><td>0.90</td><td>{mm_dd} 08:30(早)</td></tr>
                    <tr><td>2.45</td><td>3.55</td><td>2.50</td><td>91.80%</td><td>0.94</td><td>0.93</td><td>0.89</td><td>10-11 16:00(初盘)</td></tr>
                    </table>""",
                    encoding="utf-8",
                )

            # 5. 写入 odds.html (含 Crown 波胆 10 项比分)
            (raw_dir / "odds.html").write_text(
                """<table>
                <tr><td>1:0</td><td>8.50</td><td>0:0</td><td>11.00</td><td>0:1</td><td>8.50</td></tr>
                <tr><td>2:0</td><td>12.00</td><td>1:1</td><td>6.50</td><td>0:2</td><td>12.00</td></tr>
                <tr><td>2:1</td><td>9.00</td><td>2:2</td><td>12.00</td><td>1:2</td><td>9.00</td></tr>
                <tr><td>3:0</td><td>23.00</td><td>3:3</td><td>41.00</td><td>0:3</td><td>23.00</td></tr>
                </table>""",
                encoding="utf-8",
            )

            # 6. 运行 --assemble-raw-dir
            cmd_asm = [sys.executable, str(self.cli_py), "--assemble-raw-dir", str(raw_dir), "--output", str(md_p)]
            res_asm = subprocess.run(cmd_asm, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res_asm.returncode, 0, f"stderr: {res_asm.stderr}\nstdout: {res_asm.stdout}")
            self.assertTrue(md_p.exists())
            md_text = md_p.read_text(encoding="utf-8")
            self.assertIn("| 早 |", md_text)
            self.assertNotIn("0.94/0.93/0.94", md_text)

            # 7. 运行 --match --max-age-minutes 30 必须 PASS (exit 0)
            cmd_chk = [sys.executable, str(self.cli_py), "--match", str(md_p), "--max-age-minutes", "30"]
            res_chk = subprocess.run(cmd_chk, cwd=str(self.repo_root), capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(res_chk.returncode, 0, f"stderr: {res_chk.stderr}\nstdout: {res_chk.stdout}")

    def test_cli_match_verify_network_flag(self):
        """TDD U3: 测试 cli.py --match 结合 --verify-network 选项进行源站物理网络抽验"""
        from unittest.mock import patch
        from 校验.src.adapter.cli import probe_remote_provenance

        # 测试探针函数自身逻辑 (使用 mock 模拟成功与失败)
        with patch("urllib.request.urlopen") as mock_url:
            # 1. 模拟 200 OK 且包含 matchId
            mock_resp = mock_url.return_value.__enter__.return_value
            mock_resp.status = 200
            mock_resp.read.return_value = b'var game=Array("3068865","J2");'
            ok, msg = probe_remote_provenance("3068865")
            self.assertTrue(ok)
            self.assertIn("源站物理核验通过", msg)

            # 2. 模拟 404 或内容不含 matchId
            mock_resp.read.return_value = b'var game=Array("9999999","J2"); var other="info";'
            ok2, msg2 = probe_remote_provenance("3068865")
            self.assertFalse(ok2)
            self.assertIn("未包含比赛 ID", msg2)


if __name__ == "__main__":
    unittest.main()





