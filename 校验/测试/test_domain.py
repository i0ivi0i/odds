"""
校验/ 领域层模型单元测试 (TDD 红灯阶段)
"""

import unittest
from 校验.src.domain.model import (
    CheckStatus,
    DimensionType,
    DimensionResult,
    VerificationReceipt,
)
from 校验.src.domain.verifier import SnapshotVerifier


class TestDomainModel(unittest.TestCase):
    def test_dimension_result_immutability(self):
        """测试维度结果值对象的不可变性与字段完整性"""
        res = DimensionResult(
            dimension=DimensionType.ASIAN_HANDICAP,
            status=CheckStatus.PASS,
            message="澳彩/皇冠/365/易胜博4家亚盘齐全",
            detail={"count": 4},
        )
        self.assertEqual(res.dimension, DimensionType.ASIAN_HANDICAP)
        self.assertEqual(res.status, CheckStatus.PASS)
        with self.assertRaises(Exception):
            res.status = CheckStatus.FAIL  # type: ignore

    def test_verification_receipt_all_pass(self):
        """测试当所有 6 个维度均 PASS 时的收据状态"""
        results = [
            DimensionResult(DimensionType.BASIC_STATS, CheckStatus.PASS, "战绩齐全"),
            DimensionResult(DimensionType.EUROPE_1X2, CheckStatus.PASS, "欧指三巨头齐全"),
            DimensionResult(DimensionType.ASIAN_HANDICAP, CheckStatus.PASS, "亚盘四家齐全"),
            DimensionResult(DimensionType.OVER_UNDER, CheckStatus.PASS, "大小球四家齐全"),
            DimensionResult(DimensionType.TREND_HISTORY, CheckStatus.PASS, "变盘流水18行"),
            DimensionResult(DimensionType.CROWN_CORRECT_SCORE, CheckStatus.PASS, "Crown波胆齐全"),
        ]
        receipt = VerificationReceipt(match_id="2981506", results=results)
        self.assertEqual(receipt.overall_status, CheckStatus.PASS)
        self.assertTrue(receipt.is_valid)
        self.assertEqual(receipt.failed_count, 0)
        self.assertEqual(receipt.warn_count, 0)

    def test_verification_receipt_with_fail_blocks(self):
        """测试包含核心维度 FAIL 时必须物理熔断 (is_valid=False)"""
        results = [
            DimensionResult(DimensionType.BASIC_STATS, CheckStatus.PASS, "战绩齐全"),
            DimensionResult(DimensionType.EUROPE_1X2, CheckStatus.PASS, "欧指三巨头齐全"),
            DimensionResult(DimensionType.ASIAN_HANDICAP, CheckStatus.PASS, "亚盘四家齐全"),
            DimensionResult(DimensionType.OVER_UNDER, CheckStatus.PASS, "大小球四家齐全"),
            DimensionResult(DimensionType.TREND_HISTORY, CheckStatus.FAIL, "变盘流水仅1行，不足3行"),
            DimensionResult(DimensionType.CROWN_CORRECT_SCORE, CheckStatus.PASS, "Crown波胆齐全"),
        ]
        receipt = VerificationReceipt(match_id="2981506", results=results)
        self.assertEqual(receipt.overall_status, CheckStatus.FAIL)
        self.assertFalse(receipt.is_valid)  # 物理熔断
        self.assertEqual(receipt.failed_count, 1)

    def test_verification_receipt_with_warn_allows_proceed(self):
        """测试仅包含 WARN (如阵容暂无数据) 时允许通过 (is_valid=True)"""
        results = [
            DimensionResult(DimensionType.BASIC_STATS, CheckStatus.PASS, "战绩齐全"),
            DimensionResult(DimensionType.EUROPE_1X2, CheckStatus.PASS, "欧指三巨头齐全"),
            DimensionResult(DimensionType.ASIAN_HANDICAP, CheckStatus.PASS, "亚盘四家齐全"),
            DimensionResult(DimensionType.OVER_UNDER, CheckStatus.PASS, "大小球四家齐全"),
            DimensionResult(DimensionType.TREND_HISTORY, CheckStatus.PASS, "变盘流水18行"),
            DimensionResult(DimensionType.CROWN_CORRECT_SCORE, CheckStatus.PASS, "Crown波胆齐全"),
            DimensionResult(DimensionType.LINEUP_INJURY, CheckStatus.WARN, "伤停未核实(暂无数据)"),
        ]
        receipt = VerificationReceipt(match_id="2981506", results=results)
        self.assertEqual(receipt.overall_status, CheckStatus.WARN)
        self.assertTrue(receipt.is_valid)  # 允许继续推演
        self.assertEqual(receipt.warn_count, 1)
        self.assertEqual(receipt.failed_count, 0)


class TestSnapshotVerifier(unittest.TestCase):
    def setUp(self):
        self.verifier = SnapshotVerifier()
        self.valid_snapshot = {
            "matchId": "2981506",
            "match": {
                "league": "欧国联",
                "homeTeam": "苏格兰",
                "awayTeam": "克罗地亚",
                "homeGoals": "近6场进10失8 主场进5失4",
                "awayGoals": "近6场进8失7 客场进4失5",
            },
            "lineupData": "苏格兰\n球员 缺阵原因\n1 (中场) 肯尼·麦克莱恩 十字韧带扭伤\n2 (后卫) 罗伯逊 肌肉拉伤",
            "trendComparison": (
                "澳彩\t半球 0.94 0.86 10-07 21:33\n"
                "Crown\t半球 1.00 0.90 10-07 21:30\n"
                "Bet365\t半球 0.98 0.88 10-07 21:29\n"
                "易胜博\t半球 0.96 0.87 10-07 21:28\n"
                "平博\t半球 0.95 0.89 10-07 21:25\n"
                "188\t半球 0.93 0.87 10-07 21:23\n"
                "澳彩\t半球 0.97 0.92 10-07 21:21\n"
                "Crown\t半球 0.99 0.91 10-07 21:16\n"
                "Bet365\t半球 0.92 0.86 10-07 20:48\n"
            ),
            "correctScoreOdds": "波胆1:0 2:0 2:1 3:0 0:0 1:1 主3.75 6.2 8.1 5.1 客8.2 25",
            "asianOddsText": "澳彩 半球/一球 0.85 皇冠 半球/一球 0.88 365 半球/一球 0.86 易胜博 半球/一球 0.84",
            "overUnderText": "澳彩 2.5 0.90 皇冠 2.5 0.92 365 2.5 0.91 易胜博 2.5 0.89",
            "european1x2Text": (
                "公司 初盘(主/和/客/返还率/凯利主/和/客) 即时盘(主/和/客/返还率/凯利主/和/客)\n"
                "威廉 2.50 3.10 2.63 94.1% 0.96 0.92 0.94 即 1.91 3.40 3.60 94.2% 0.93 0.95 0.95\n"
                "立博 2.50 3.30 2.70 94.0% 0.96 0.98 0.90 即 2.00 3.50 3.60 94.5% 0.95 0.96 0.92\n"
                "365 2.50 3.20 2.70 93.8% 0.95 0.94 0.92 即 1.95 3.50 4.00 94.2% 0.93 0.97 0.96\n"
                "澳彩 2.13 3.18 2.95 90.5% 0.92 0.90 0.91 即 1.92 3.38 3.23 90.8% 0.91 0.93 0.91\n"
                "99家平均 2.38 3.22 2.85 93.2% 0.94 0.93 0.92 即 1.95 3.42 3.75 94.0% 0.93 0.95 0.94"
            ),
            "polymarket": {
                "slug": "unl-sco-cro-2026-10-07",
                "url": "https://polymarket.com/zh/sports/uefa-nations-league/unl-sco-cro-2026-10-07",
            },
            "markets": {
                "europeHistories": [
                    {
                        "company": "澳彩",
                        "timeline": [
                            {"h": 1.48, "d": 3.93, "a": 5.00, "timestamp": "10-04 20:40", "status": "初盘"},
                            {"h": 1.45, "d": 4.20, "a": 5.00, "timestamp": "10-04 22:32", "status": "即"},
                            {"h": 1.47, "d": 4.15, "a": 4.90, "timestamp": "10-08 00:26", "status": "即"},
                            {"h": 1.42, "d": 4.30, "a": 5.35, "timestamp": "10-08 15:40", "status": "即"},
                        ],
                    }
                ]
            },
        }

    def test_verify_valid_snapshot_all_pass(self):
        receipt = self.verifier.verify(self.valid_snapshot)
        self.assertEqual(receipt.overall_status, CheckStatus.PASS)
        self.assertTrue(receipt.is_valid)
        self.assertEqual(receipt.failed_count, 0)

    def test_verify_missing_trend_history_fails(self):
        bad_snapshot = dict(self.valid_snapshot)
        bad_snapshot["trendComparison"] = "仅有单行"  # 少于3行
        receipt = self.verifier.verify(bad_snapshot)
        self.assertFalse(receipt.is_valid)
        self.assertEqual(receipt.overall_status, CheckStatus.FAIL)
        # 验证变盘流水维度报错
        trend_res = [r for r in receipt.results if r.dimension == DimensionType.TREND_HISTORY][0]
        self.assertEqual(trend_res.status, CheckStatus.FAIL)

    def test_verify_missing_crown_score_fails(self):
        bad_snapshot = dict(self.valid_snapshot)
        bad_snapshot["correctScoreOdds"] = ""  # 空波胆
        receipt = self.verifier.verify(bad_snapshot)
        self.assertFalse(receipt.is_valid)
        score_res = [r for r in receipt.results if r.dimension == DimensionType.CROWN_CORRECT_SCORE][0]
        self.assertEqual(score_res.status, CheckStatus.FAIL)

    def test_verify_warn_on_unverified_lineup(self):
        warn_snapshot = dict(self.valid_snapshot)
        warn_snapshot["lineupData"] = "主队: 暂无数据\n客队: 暂无数据"
        receipt = self.verifier.verify(warn_snapshot)
        self.assertTrue(receipt.is_valid)  # 仍然允许推演
        self.assertEqual(receipt.overall_status, CheckStatus.WARN)
        lineup_res = [r for r in receipt.results if r.dimension == DimensionType.LINEUP_INJURY][0]
        self.assertEqual(lineup_res.status, CheckStatus.WARN)

    def test_verify_narrative_lineup_without_structure_fails(self):
        """测试用概括套话冒充伤停名单时必须物理判定 FAIL 熔断"""
        bad_snapshot = dict(self.valid_snapshot)
        bad_snapshot["lineupData"] = "两队主力阵容基本齐整，战意强烈，无重大伤病停赛困扰，全员健康出战。"
        receipt = self.verifier.verify(bad_snapshot)
        self.assertFalse(receipt.is_valid)
        self.assertEqual(receipt.overall_status, CheckStatus.FAIL)
        lineup_res = [r for r in receipt.results if r.dimension == DimensionType.LINEUP_INJURY][0]
        self.assertEqual(lineup_res.status, CheckStatus.FAIL)
        self.assertIn("套话", lineup_res.message)

    def test_verify_trend_without_timestamps_fails(self):
        """测试缺少分秒时间戳的伪时序流水必须物理判定 FAIL"""
        bad_snapshot = dict(self.valid_snapshot)
        # 仅有初即两端或无时间戳
        bad_snapshot["trendComparison"] = (
            "澳* 初 2.10 3.20 3.50 即 2.30 3.10 3.20\n"
            "Crow* 初 2.15 3.25 3.25 即 2.44 2.88 3.10\n"
            "365 初 2.10 3.20 3.50 即 2.38 3.10 3.30"
        )
        receipt = self.verifier.verify(bad_snapshot)
        self.assertFalse(receipt.is_valid)
        trend_res = [r for r in receipt.results if r.dimension == DimensionType.TREND_HISTORY][0]
        self.assertEqual(trend_res.status, CheckStatus.FAIL)
        self.assertIn("时间戳", trend_res.message)

    def test_verify_trend_insufficient_timestamps_fails(self):
        """测试时间戳流水行数不足 6 行时必须物理判定 FAIL"""
        bad_snapshot = dict(self.valid_snapshot)
        # 仅有 2 行带时间戳
        bad_snapshot["trendComparison"] = (
            "半球 0.94 0.86 10-07 21:33\n"
            "半球 1.00 0.90 10-07 21:30"
        )
        receipt = self.verifier.verify(bad_snapshot)
        self.assertFalse(receipt.is_valid)
        trend_res = [r for r in receipt.results if r.dimension == DimensionType.TREND_HISTORY][0]
        self.assertEqual(trend_res.status, CheckStatus.FAIL)
        self.assertIn("不足", trend_res.message)

    def test_verify_basic_stats_without_goals_numbers_fails(self):
        """测试缺少真实进失球攻防数字时必须判定 FAIL"""
        bad_snapshot = dict(self.valid_snapshot)
        bad_snapshot["match"] = {
            "league": "巴西甲",
            "homeTeam": "里莫",
            "awayTeam": "格雷米奥",
            # 无任何进失球或比分数字
        }
        bad_snapshot["basicStatsText"] = "双方状态良好，比赛激烈"
        receipt = self.verifier.verify(bad_snapshot)
        self.assertFalse(receipt.is_valid)
        stats_res = [r for r in receipt.results if r.dimension == DimensionType.BASIC_STATS][0]
        self.assertEqual(stats_res.status, CheckStatus.FAIL)
        self.assertIn("进失球", stats_res.message)

    def test_verify_polymarket_unopened_returns_warn(self):
        """测试 Polymarket 真实标注未开盘时应返回 WARN 并允许推演"""
        warn_snapshot = dict(self.valid_snapshot)
        warn_snapshot["polymarket"] = {"status": "unopened", "url": "【平台未开放交易池/暂无流动性】"}
        receipt = self.verifier.verify(warn_snapshot)
        self.assertTrue(receipt.is_valid)
        pm_res = [r for r in receipt.results if r.dimension == DimensionType.POLYMARKET_LIQUIDITY][0]
        self.assertEqual(pm_res.status, CheckStatus.WARN)
        self.assertIn("未开放", pm_res.message)

    def test_verify_polymarket_fabricated_template_url_fails(self):
        """测试包含模板占位符的伪造 Polymarket 链接必须物理判定 FAIL"""
        bad_snapshot = dict(self.valid_snapshot)
        bad_snapshot["polymarket"] = {"url": "https://polymarket.com/zh/sports/{league}/{slug}"}
        receipt = self.verifier.verify(bad_snapshot)
        self.assertFalse(receipt.is_valid)
        pm_res = [r for r in receipt.results if r.dimension == DimensionType.POLYMARKET_LIQUIDITY][0]
        self.assertEqual(pm_res.status, CheckStatus.FAIL)
        self.assertIn("伪造", pm_res.message)

    def test_verify_europe_1x2_missing_kelly_and_return_fails(self):
        """测试欧洲指数若仅有 3 个静态赔率而缺失凯利指数与返还率时必须判定 FAIL 熔断"""
        bad_snapshot = dict(self.valid_snapshot)
        # 仅有静态主平客三项，缺少凯利与返还率
        bad_snapshot["european1x2Text"] = (
            "威廉 1.65 3.50 4.80 即 1.60 3.60 5.00\n"
            "立博 1.62 3.40 5.00 即 1.58 3.50 5.20\n"
            "365 1.66 3.55 4.80 即 1.62 3.60 5.00"
        )
        receipt = self.verifier.verify(bad_snapshot)
        self.assertFalse(receipt.is_valid)
        self.assertEqual(receipt.overall_status, CheckStatus.FAIL)
        euro_res = [r for r in receipt.results if r.dimension == DimensionType.EUROPE_1X2][0]
        self.assertEqual(euro_res.status, CheckStatus.FAIL)
        self.assertIn("凯利", euro_res.message)

    def test_verify_europe_1x2_structured_passes(self):
        """测试欧洲指数包含结构化 europeCompanies 且含凯利和返还率时判定 PASS"""
        good_snapshot = dict(self.valid_snapshot)
        good_snapshot["european1x2Text"] = ""
        good_snapshot["markets"] = dict(good_snapshot.get("markets", {}))
        good_snapshot["markets"]["europeCompanies"] = [
            {
                "name": "威廉希尔",
                "initial": {"h": 2.50, "d": 3.10, "a": 2.63, "return_rate": 0.941, "kelly": [0.96, 0.92, 0.94]},
                "latest": {"h": 1.91, "d": 3.40, "a": 3.60, "return_rate": 0.942, "kelly": [0.93, 0.95, 0.95]},
            },
            {
                "name": "立博",
                "initial": {"h": 2.50, "d": 3.30, "a": 2.70, "return_rate": 0.940, "kelly": [0.96, 0.98, 0.90]},
                "latest": {"h": 2.00, "d": 3.50, "a": 3.60, "return_rate": 0.945, "kelly": [0.95, 0.96, 0.92]},
            },
        ]
        receipt = self.verifier.verify(good_snapshot)
        self.assertTrue(receipt.is_valid)
        euro_res = [r for r in receipt.results if r.dimension == DimensionType.EUROPE_1X2][0]
        self.assertEqual(euro_res.status, CheckStatus.PASS)

    def test_verify_basic_stats_enhanced_with_tactical_stats(self):
        """测试基础战绩支持结构化 tactics.technicalStats 真实技统校验"""
        snapshot = dict(self.valid_snapshot)
        snapshot["tactics"] = {
            "technicalStats": {
                "home": {"possession": "58%", "shots": 16, "shotsOnTarget": 6, "corners": 7},
                "away": {"possession": "42%", "shots": 8, "shotsOnTarget": 2, "corners": 3},
            },
            "goalTimeDistribution": {
                "home": {"scored": [2, 1, 3, 2, 4, 3], "conceded": [1, 2, 1, 0, 2, 2]},
                "away": {"scored": [1, 0, 1, 2, 1, 2], "conceded": [3, 2, 1, 4, 2, 3]},
            },
            "futureSchedule": [
                {"team": "home", "daysInterval": 4, "opponent": "弗拉门戈", "league": "巴西甲"},
            ]
        }
        receipt = self.verifier.verify(snapshot)
        self.assertTrue(receipt.is_valid)
        stats_res = [r for r in receipt.results if r.dimension == DimensionType.BASIC_STATS][0]
        self.assertEqual(stats_res.status, CheckStatus.PASS)
        self.assertIn("tactics", stats_res.detail)

    def test_verify_asian_handicap_enhanced_with_profiling(self):
        """测试亚洲盘口支持结构化 profiling 散户偏见镜像与操盘画像校验"""
        snapshot = dict(self.valid_snapshot)
        snapshot["profiling"] = {
            "identicalOddsHistory": {
                "handicapLine": "半球",
                "homeWinRate": "62.5%",
                "drawRate": "25.0%",
                "awayWinRate": "12.5%",
                "coverRate": "62.5%",
            },
            "handicapTrends": {
                "homeRecent10": {"cover": 6, "push": 1, "lose": 3, "streak": "赢输赢赢"},
                "awayRecent10": {"cover": 4, "push": 0, "lose": 6, "streak": "输输赢输"},
            }
        }
        receipt = self.verifier.verify(snapshot)
        self.assertTrue(receipt.is_valid)
        ah_res = [r for r in receipt.results if r.dimension == DimensionType.ASIAN_HANDICAP][0]
        self.assertEqual(ah_res.status, CheckStatus.PASS)
        self.assertIn("profiling", ah_res.detail)

    def test_verify_full_dual_track_snapshot_all_pass(self):
        """测试全量携带 tactics(物理底牌) 与 profiling(散户镜像) 的高密快照全绿通过"""
        full_snapshot = dict(self.valid_snapshot)
        full_snapshot["tactics"] = {
            "technicalStats": {
                "home": {"possession": "54%", "shots": 14, "shotsOnTarget": 5, "corners": 6},
                "away": {"possession": "46%", "shots": 9, "shotsOnTarget": 3, "corners": 4},
            },
            "goalTimeDistribution": {
                "home": {"scored": [1, 2, 1, 3, 2, 1], "conceded": [0, 1, 1, 2, 1, 1]},
                "away": {"scored": [0, 1, 2, 1, 1, 0], "conceded": [2, 1, 2, 1, 2, 2]},
            },
            "futureSchedule": [
                {"team": "home", "daysInterval": 3, "opponent": "圣保罗", "league": "巴西甲"},
            ]
        }
        full_snapshot["profiling"] = {
            "identicalOddsHistory": {
                "handicapLine": "半球",
                "homeWinRate": "60.0%",
                "coverRate": "60.0%",
            },
            "handicapTrends": {
                "homeRecent10": {"cover": 5, "push": 2, "lose": 3},
                "awayRecent10": {"cover": 3, "push": 1, "lose": 6},
            }
        }
        full_snapshot["markets"] = dict(full_snapshot.get("markets", {}))
        full_snapshot["markets"]["halfTime"] = {
            "crown": {"ahInitial": "平/半 0.85", "ahLatest": "半球 1.02", "ouInitial": "1 0.90", "ouLatest": "1 0.88"},
            "macau": {"ahInitial": "平/半 0.82", "ahLatest": "平/半 0.95", "ouInitial": "1 0.85", "ouLatest": "1 0.92"},
        }
        receipt = self.verifier.verify(full_snapshot)
        self.assertTrue(receipt.is_valid)
        self.assertEqual(receipt.overall_status, CheckStatus.PASS)
        self.assertEqual(receipt.failed_count, 0)
        self.assertTrue(receipt.metadata.get("has_dual_track"))

    def test_clean_a11y_noise(self):
        from 校验.src.domain.verifier import clean_a11y_noise
        raw = '- cell "4.50" [ref=e1365]\n- link "新球体育" [ref=e1]\n- listitem [level=1]\n- list'
        cleaned = clean_a11y_noise(raw)
        self.assertNotIn("[ref=", cleaned)
        self.assertNotIn("- cell", cleaned)
        self.assertIn("4.50", cleaned)
        self.assertIn("新球体育", cleaned)

    def test_get_match_property(self):
        from 校验.src.domain.verifier import get_match_property
        snap_flat = {"homeTeam": "巴西国际", "match": {"awayTeam": "科林蒂安"}}
        self.assertEqual(get_match_property(snap_flat, "homeTeam"), "巴西国际")
        self.assertEqual(get_match_property(snap_flat, "awayTeam"), "科林蒂安")
        self.assertIsNone(get_match_property(snap_flat, "league"))
        self.assertEqual(get_match_property(snap_flat, "league", "巴甲"), "巴甲")

    def test_verify_cleans_a11y_and_enriches_profiling(self):
        snap = dict(self.valid_snapshot)
        snap["european1x2Text"] = snap["european1x2Text"] + '\n- cell "4.50" [ref=e999]'
        snap["profiling"] = {
            "identicalOddsHistory": {
                "raw": "巴西国际\n初盘:平手/半球\t赢\t走\t输\t赢盘率\n总\t10\t0\t5\t66.7%\n近6场盘路走势: 赢 输 赢 输 赢 输"
            }
        }
        receipt = self.verifier.verify(snap)
        self.assertTrue(receipt.is_valid)
        self.assertNotIn("[ref=", snap["european1x2Text"])
        self.assertIn("items", snap["profiling"]["identicalOddsHistory"])
        self.assertEqual(len(snap["profiling"]["identicalOddsHistory"]["items"]), 1)

    def test_negative_market_consensus_blocked(self):
        """测试负面清单：包含 marketConsensus 或 百家平均 判定 FAIL 熔断"""
        snap = dict(self.valid_snapshot)
        snap["marketConsensus"] = {"h": 2.10, "d": 3.20, "a": 3.40}
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        euro_res = [r for r in receipt.results if r.dimension == DimensionType.EUROPE_1X2][0]
        self.assertEqual(euro_res.status, CheckStatus.FAIL)
        self.assertIn("算术平均", euro_res.message)

    def test_negative_navigation_garbage_blocked(self):
        """测试负面清单：包含全页导航栏垃圾 判定 FAIL 熔断"""
        snap = dict(self.valid_snapshot)
        snap["lineupData"] = "首页\n足球直播\n分析师\n新\nV计划\n暂无数据"
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        lineup_res = [r for r in receipt.results if r.dimension == DimensionType.LINEUP_INJURY][0]
        self.assertEqual(lineup_res.status, CheckStatus.FAIL)
        self.assertIn("导航栏垃圾文本", lineup_res.message)

    def test_negative_html_skeleton_blocked(self):
        """测试负面清单：包含未清洗 HTML 骨架标签 判定 FAIL 熔断"""
        snap = dict(self.valid_snapshot)
        snap["asianOddsText"] = "<!DOCTYPE html><html><body>公司\t盘口\t水位</body></html>"
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        asia_res = [r for r in receipt.results if r.dimension == DimensionType.ASIAN_HANDICAP][0]
        self.assertEqual(asia_res.status, CheckStatus.FAIL)
        self.assertIn("HTML 空骨架标签", asia_res.message)

    def test_negative_gun_inplay_trend_blocked(self):
        """测试负面清单：变盘时序混入滚球盘口 判定 FAIL 熔断"""
        snap = dict(self.valid_snapshot)
        snap["trendComparison"] = (
            "Crown\t\t\t0.80\t半球\t1.05\t10-07 20:00\t即\n"
            "Crown\t\t\t0.85\t半球\t1.00\t10-07 19:30\t早\n"
            "Crown\t\t\t0.90\t半球\t0.95\t10-07 18:00\t滚\n"
            "Crown\t\t\t0.95\t半球\t0.90\t10-07 17:00\t早\n"
            "Crown\t\t\t1.00\t半球\t0.85\t10-07 16:00\t早\n"
            "Crown\t\t\t1.05\t半球\t0.80\t10-07 15:00\t早"
        )
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        trend_res = [r for r in receipt.results if r.dimension == DimensionType.TREND_HISTORY][0]
        self.assertEqual(trend_res.status, CheckStatus.FAIL)
        self.assertIn("滚", trend_res.message)

    def test_negative_missing_core_bookmakers_blocked(self):
        """测试负面清单：核心做市商覆盖不足判定 FAIL 熔断"""
        snap = dict(self.valid_snapshot)
        snap["european1x2Text"] = ""
        snap["markets"] = {
            "europeCompanies": [
                {"company": "野鸡小庄A", "initial": {"return_rate": 0.9, "kelly": [0.9, 0.9, 0.9]}},
                {"company": "野鸡小庄B", "initial": {"return_rate": 0.9, "kelly": [0.9, 0.9, 0.9]}},
                {"company": "野鸡小庄C", "initial": {"return_rate": 0.9, "kelly": [0.9, 0.9, 0.9]}},
            ]
        }
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        euro_res = [r for r in receipt.results if r.dimension == DimensionType.EUROPE_1X2][0]
        self.assertEqual(euro_res.status, CheckStatus.FAIL)
        self.assertIn("核心做市商覆盖不足", euro_res.message)

    def test_self_healing_tactics_physical_goals_passes(self):
        """测试自愈机制：攻防进失球在 tactics.home/away 结构体中自愈通过"""
        snap = dict(self.valid_snapshot)
        snap["match"] = {"homeTeam": "主队", "awayTeam": "客队", "league": "芬超"}
        snap.pop("basicStatsText", None)
        snap["tactics"] = {
            "home": {"name": "主队", "recent6": "得8失5", "avgGoalsScored": 1.5},
            "away": {"name": "客队", "recent6": "得4失7", "avgGoalsConceded": 1.2},
        }
        receipt = self.verifier.verify(snap)
        self.assertTrue(receipt.is_valid)
        basic_res = [r for r in receipt.results if r.dimension == DimensionType.BASIC_STATS][0]
        self.assertEqual(basic_res.status, CheckStatus.PASS)

    def test_verify_europe_1x2_missing_timeline_blocked(self):
        """测试负面清单硬拦截：欧指仅有初即盘切片而缺少连续变盘时序流水时判定 FAIL"""
        snap = dict(self.valid_snapshot)
        snap["markets"] = dict(snap.get("markets", {}))
        snap["markets"]["europeHistories"] = []
        snap["trendComparison"] = "半球 0.94 0.86 10-07 21:33\n半球 1.00 0.90 10-07 21:30\n半球 0.98 0.88 10-07 21:29"
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        euro_res = [r for r in receipt.results if r.dimension == DimensionType.EUROPE_1X2][0]
        self.assertEqual(euro_res.status, CheckStatus.FAIL)
        self.assertIn("缺少连续变盘时序流水", euro_res.message)
        self.assertIn("严禁仅用初即盘切片偷懒", euro_res.message)

    def test_verify_europe_1x2_with_timeline_passes(self):
        """测试欧指包含4条以上带时间戳变盘流水判定 PASS"""
        snap = dict(self.valid_snapshot)
        receipt = self.verifier.verify(snap)
        self.assertTrue(receipt.is_valid)
        euro_res = [r for r in receipt.results if r.dimension == DimensionType.EUROPE_1X2][0]
        self.assertEqual(euro_res.status, CheckStatus.PASS)
        self.assertIn("分钟级时序完整", euro_res.message)

    def test_verify_trend_history_insufficient_companies_blocked(self):
        """测试防偷懒硬门禁：时序流水中核心做市商少于3家（如仅抓澳彩和Crown）判定 FAIL 熔断"""
        snap = dict(self.valid_snapshot)
        # 虽有6行时间戳，但仅有澳彩和Crown 2家公司
        snap["trendComparison"] = (
            "澳彩\t半球 0.94 0.86 10-07 21:33\n"
            "澳彩\t半球 1.00 0.90 10-07 21:30\n"
            "澳彩\t半球 0.98 0.88 10-07 21:29\n"
            "Crown\t半球 0.96 0.87 10-07 21:28\n"
            "Crown\t半球 0.97 0.92 10-07 21:21\n"
            "Crown\t半球 0.99 0.91 10-07 21:16\n"
        )
        snap["markets"] = dict(snap.get("markets", {}))
        snap["markets"]["asianHistories"] = []
        snap["markets"]["europeHistories"] = []
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        trend_res = [r for r in receipt.results if r.dimension == DimensionType.TREND_HISTORY][0]
        self.assertEqual(trend_res.status, CheckStatus.FAIL)
        self.assertIn("核心做市商覆盖不足", trend_res.message)
        self.assertIn("严禁偷懒漏抓做市商", trend_res.message)

    def test_verify_trend_history_multi_companies_passes(self):
        """测试时序流水覆盖5家以上主流做市商判定 PASS"""
        snap = dict(self.valid_snapshot)
        receipt = self.verifier.verify(snap)
        self.assertTrue(receipt.is_valid)
        trend_res = [r for r in receipt.results if r.dimension == DimensionType.TREND_HISTORY][0]
        self.assertEqual(trend_res.status, CheckStatus.PASS)
        self.assertIn("涵盖核心做市商", trend_res.message)

    def test_asian_handicap_profiling_alone_cannot_pass(self):
        """测试U2: 只有 profiling 叙述不能替代真实盘口，无AH盘口与水位必须 FAIL"""
        snap = dict(self.valid_snapshot)
        snap["asianOddsText"] = ""
        snap["markets"] = dict(snap.get("markets", {}))
        snap["markets"]["asianHistories"] = []
        snap["profiling"] = {"identicalOddsHistory": {"sampleCount": 15, "winRate": 0.6}}
        receipt = self.verifier.verify(snap)
        ah_res = [r for r in receipt.results if r.dimension == DimensionType.ASIAN_HANDICAP][0]
        self.assertEqual(ah_res.status, CheckStatus.FAIL)
        self.assertIn("缺失", ah_res.message)

    def test_asian_handicap_empty_containers_fail(self):
        """测试U2: 六个空历史容器和只有名称的公司不能通过AH验收"""
        snap = dict(self.valid_snapshot)
        snap["asianOddsText"] = ""
        snap["markets"] = dict(snap.get("markets", {}))
        snap["markets"]["asianHistories"] = [
            {"company": "澳彩", "records": []},
            {"company": "皇冠", "records": []},
        ]
        receipt = self.verifier.verify(snap)
        ah_res = [r for r in receipt.results if r.dimension == DimensionType.ASIAN_HANDICAP][0]
        self.assertEqual(ah_res.status, CheckStatus.FAIL)

    def test_over_under_empty_containers_fail(self):
        """测试U2: 空历史容器不能通过大小球验收"""
        snap = dict(self.valid_snapshot)
        snap["overUnderText"] = ""
        snap["overUnderOddsText"] = ""
        snap["markets"] = dict(snap.get("markets", {}))
        snap["markets"]["overUnderHistories"] = [
            {"company": "澳彩", "records": []}
        ]
        receipt = self.verifier.verify(snap)
        ou_res = [r for r in receipt.results if r.dimension == DimensionType.OVER_UNDER][0]
        self.assertEqual(ou_res.status, CheckStatus.FAIL)

    def test_europe_histories_cannot_satisfy_over_under(self):
        """测试U2: 欧指流水不能抵消大小球缺口，OU必须单独报缺口"""
        snap = dict(self.valid_snapshot)
        snap["overUnderText"] = ""
        snap["overUnderOddsText"] = ""
        snap["markets"] = dict(snap.get("markets", {}))
        snap["markets"]["overUnderHistories"] = []
        # 虽然 europeHistories 有完整流水，但 OU 为空
        receipt = self.verifier.verify(snap)
        ou_res = [r for r in receipt.results if r.dimension == DimensionType.OVER_UNDER][0]
        self.assertEqual(ou_res.status, CheckStatus.FAIL)

    def test_trend_history_empty_containers_do_not_count_as_records(self):
        """测试U2: 空历史容器不能伪充变盘记录行数"""
        snap = dict(self.valid_snapshot)
        snap["trendComparison"] = "澳彩\t半球 0.94 0.86 10-07 21:33\nCrown\t半球 1.00 0.90 10-07 21:30"
        snap["asianOddsText"] = ""
        snap["markets"] = dict(snap.get("markets", {}))
        snap["markets"]["asianHistories"] = [{}, {}, {}, {}, {}, {}]  # 6个空容器
        snap["markets"]["europeHistories"] = []
        receipt = self.verifier.verify(snap)
        trend_res = [r for r in receipt.results if r.dimension == DimensionType.TREND_HISTORY][0]
        self.assertEqual(trend_res.status, CheckStatus.FAIL)
        self.assertIn("记录不足", trend_res.message)

    def test_trend_history_fetched_at_earlier_than_trend_timestamps_fails(self):
        """测试U2: 抓取时间早于嵌入报价时间（混批次/时点倒挂）时判定 FAIL 阻断"""
        snap = dict(self.valid_snapshot)
        snap["fetchedAt"] = "2026-10-07 16:00:00"  # 早盘 16:00
        snap["trendComparison"] = (
            "澳彩\t半球 0.94 0.86 10-07 21:33\n"
            "Crown\t半球 1.00 0.90 10-07 21:30\n"
            "Bet365\t半球 0.98 0.88 10-07 21:29\n"
            "易胜博\t半球 0.96 0.87 10-07 21:28\n"
            "平博\t半球 0.95 0.89 10-07 21:25\n"
            "188\t半球 0.93 0.87 10-07 21:23\n"
        )
        receipt = self.verifier.verify(snap)
        trend_res = [r for r in receipt.results if r.dimension == DimensionType.TREND_HISTORY][0]
        self.assertEqual(trend_res.status, CheckStatus.FAIL)
        self.assertIn("冲突", trend_res.message)

    def test_europe_1x2_null_return_rate_fails(self):
        """测试U2: 缺客赔、return_rate 为 null 时不能被认作有效数字"""
        snap = dict(self.valid_snapshot)
        snap["european1x2Text"] = ""
        snap["markets"] = dict(snap.get("markets", {}))
        snap["markets"]["europeCompanies"] = [
            {
                "company": "澳彩",
                "initial": {"h": 2.10, "d": 3.10, "a": 3.20, "return_rate": None, "kelly": [0.9, 0.9, 0.9]},
                "latest": {"h": 2.00, "d": 3.20, "a": 3.40, "return_rate": None, "kelly": [0.9, 0.9, 0.9]},
            },
            {
                "company": "Crown",
                "initial": {"h": 2.10, "d": 3.10, "a": 3.20, "return_rate": False, "kelly": [0.9, 0.9, 0.9]},
                "latest": {"h": 2.00, "d": 3.20, "a": 3.40, "return_rate": False, "kelly": [0.9, 0.9, 0.9]},
            },
            {
                "company": "Bet365",
                "initial": {"h": 2.10, "d": 3.10, "a": 3.20, "return_rate": "", "kelly": [0.9, 0.9, 0.9]},
                "latest": {"h": 2.00, "d": 3.20, "a": 3.40, "return_rate": "", "kelly": [0.9, 0.9, 0.9]},
            },
        ]
        receipt = self.verifier.verify(snap)
        euro_res = [r for r in receipt.results if r.dimension == DimensionType.EUROPE_1X2][0]
        self.assertEqual(euro_res.status, CheckStatus.FAIL)
        self.assertIn("缺少主流机构返还率与凯利指数", euro_res.message)

    def test_clean_json_schema_passes_all_checks(self):
        """测试方案B：纯净结构化 JSON（无制表符大转义字符串）通过全量安检门禁"""
        snap = {
            "matchId": "2912286",
            "sportteryCode": "周五004",
            "fetchedAt": "2026-10-09 23:42:16",
            "match": {
                "league": "瑞典超",
                "homeTeam": "哥德堡",
                "awayTeam": "瓦斯特拉斯",
                "homeGoals": "近6场进11失7 主场战力充沛",
                "awayGoals": "近6场进8失9 客场韧性均衡",
            },
            "lineupData": "哥德堡\n暂无数据\n\n韦斯特罗\n暂无数据",
            "correctScoreOdds": "波胆 1:0 8.5, 2:0 10.5, 1:1 6.8",
            "europe1x2": [
                {
                    "company": "竞彩官方",
                    "initial": {"odds": [1.48, 4.10, 4.80], "returnRate": 88.66, "kelly": [0.85, 0.90, 0.95]},
                    "latest": {"odds": [1.53, 3.95, 4.50], "returnRate": 88.58, "kelly": [0.84, 0.93, 0.99]},
                },
                {
                    "company": "Bet365",
                    "initial": {"odds": [1.70, 3.80, 4.33], "returnRate": 92.39, "kelly": [0.90, 0.90, 0.90]},
                    "latest": {"odds": [1.73, 3.80, 4.50], "returnRate": 94.04, "kelly": [0.94, 0.89, 0.99]},
                },
                {
                    "company": "澳彩",
                    "initial": {"odds": [1.53, 4.15, 4.25], "returnRate": 88.60, "kelly": [0.92, 0.89, 0.82]},
                    "latest": {"odds": [1.68, 3.78, 3.72], "returnRate": 88.60, "kelly": [0.92, 0.89, 0.82]},
                },
            ],
            "asianHandicap": [
                {
                    "company": "澳彩",
                    "initial": {"handicap": "半球", "home": 0.88, "away": 0.94},
                    "latest": {"handicap": "平/半", "home": 0.92, "away": 0.92},
                },
                {
                    "company": "Crown",
                    "initial": {"handicap": "平/半", "home": 0.81, "away": 1.07},
                    "latest": {"handicap": "半/一", "home": 0.94, "away": 0.95},
                },
            ],
            "overUnder": [
                {
                    "company": "澳彩",
                    "initial": {"goal": 2.5, "over": 0.88, "under": 0.92},
                    "latest": {"goal": 2.5, "over": 0.90, "under": 0.90},
                }
            ],
            "timeSeriesFlow": [
                {"company": "澳彩", "time": "10-09 21:21", "handicap": "平/半", "home": 0.92, "away": 0.92, "odds": [1.70, 3.80, 4.33]},
                {"company": "Crown", "time": "10-09 21:21", "handicap": "平/半", "home": 0.92, "away": 0.92, "odds": [1.70, 3.80, 4.33]},
                {"company": "Bet365", "time": "10-09 21:18", "handicap": "平/半", "home": 0.90, "away": 0.90, "odds": [1.73, 3.80, 4.50]},
                {"company": "易胜博", "time": "10-09 21:10", "handicap": "平/半", "home": 0.90, "away": 0.90, "odds": [1.72, 3.80, 4.40]},
                {"company": "平博", "time": "10-09 21:05", "handicap": "平/半", "home": 0.91, "away": 0.91, "odds": [1.74, 3.82, 4.45]},
                {"company": "188", "time": "10-09 20:55", "handicap": "平/半", "home": 0.92, "away": 0.92, "odds": [1.70, 3.80, 4.33]},
            ],
            "tactics": {
                "technicalStats": {
                    "home": {"avgGoals": 1.7, "avgCorners": 5.2},
                    "away": {"avgGoals": 1.2, "avgCorners": 4.3},
                }
            },
            "profiling": {
                "identicalOddsHistory": {"home": {"winRate": 0.52}},
                "handicapTrends": {"home": "平稳"}
            },
            "polymarket": {"status": "unopened", "url": "未开放"}
        }
        receipt = self.verifier.verify(snap)
        self.assertTrue(receipt.is_valid)
        self.assertEqual(receipt.failed_count, 0)

    def test_authenticity_fails_when_template_placeholders_present(self):
        """测试真实性核验：包含未填充占位符时必须 FAIL 拦截"""
        snap = {
            "matchId": "2981506",
            "match": {"homeTeam": "{homeTeam}", "awayTeam": "切尔西", "league": "英超"},
            "basicStatsText": "主场进球 1.5",
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("未填充的模板占位符", res.message)

    def test_authenticity_fails_when_cloning_fixture_detected(self):
        """测试真实性核验：非 3000474 比赛若复制了测试夹具队名，必须 FAIL 拦截"""
        snap = {
            "matchId": "3003899",
            "match": {"homeTeam": "阿森纳", "awayTeam": "利兹联", "league": "英超"},
            "asianOddsText": "大阪樱花 vs 横滨水手 澳彩 0.90 平半 0.94",
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("测试夹具专属特征", res.message)

    def test_authenticity_passes_for_clean_data(self):
        """测试真实性核验：正常匹配的干净数据必须 PASS"""
        snap = {
            "matchId": "3003899",
            "match": {"homeTeam": "阿森纳", "awayTeam": "利兹联", "league": "英超"},
            "asianOddsText": "阿森纳 vs 利兹联 澳彩 0.85 球半 1.00",
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.PASS)


if __name__ == "__main__":
    unittest.main()
