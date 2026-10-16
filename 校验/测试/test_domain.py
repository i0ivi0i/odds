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
        """测试 Polymarket 真实标注未开盘且带双向核验证据时应返回 WARN 并允许推演"""
        warn_snapshot = dict(self.valid_snapshot)
        warn_snapshot["polymarket"] = {"status": "unopened", "url": "【平台未开放交易池/暂无流动性（经Gamma双向核验均无活跃标的）】"}
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
        """测试全量携带 tactics(物理底牌) 与 profiling(散户镜像) 的高密【推演源数据】全绿通过"""
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
            "polymarket": {"status": "active", "url": "https://polymarket.com/event/swe-got-vas-2026-10-09"}
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
        """测试真实性核验：若复制了第三方对阵，必须 FAIL 拦截"""
        snap = {
            "matchId": "3003899",
            "match": {"homeTeam": "阿森纳", "awayTeam": "利兹联", "league": "英超"},
            "asianOddsText": "大阪樱花 vs 横滨水手 澳彩 0.90 平半 0.94",
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("第三方比赛对阵", res.message)

    def test_authenticity_fails_on_generic_alien_match_leak(self):
        """测试通用真实性核验：阿森纳比赛若出现曼城 vs 切尔西，必须泛化拦截而无需硬编码"""
        snap = {
            "matchId": "3003899",
            "match": {"homeTeam": "阿森纳", "awayTeam": "利兹联", "league": "英超"},
            "asianOddsText": "曼城 vs 切尔西 澳彩 0.90 半球 0.95",
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("第三方比赛对阵", res.message)
        self.assertIn("曼城 vs 切尔西", res.message)

    def test_authenticity_passes_for_clean_data(self):
        """测试真实性核验：正常匹配的干净数据必须 PASS"""
        snap = {
            "matchId": "3003899",
            "match": {"homeTeam": "阿森纳", "awayTeam": "利兹联", "league": "英超"},
            "asianOddsText": "阿森纳 vs 利兹联 澳彩 0.85 球半 1.00",
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.PASS)

    def test_authenticity_fails_on_conflicting_match_urls(self):
        """测试真实性核验：【推演源数据】内 URL 引用了其他比赛 ID 时必须 FAIL 拦截"""
        snap = {
            "matchId": "3013719",
            "match": {"homeTeam": "巴列卡诺", "awayTeam": "毕尔巴鄂竞技", "league": "西甲"},
            "_raw_content": "巴列卡诺 vs 毕尔巴鄂竞技 https://vip.titan007.com/AsianOdds_n.aspx?id=3018828",
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("引用了其他场次比赛 ID", res.message)

    def test_authenticity_fails_on_meta_teams_mismatch(self):
        """测试真实性核验：【推演源数据】对阵与 meta.md 登记对阵冲突时必须 FAIL 拦截"""
        snap = {
            "matchId": "3013719",
            "match": {"homeTeam": "帕德博恩", "awayTeam": "斯图加特", "league": "德甲"},
            "_meta_info": {"home": "巴列卡诺", "away": "毕尔巴鄂竞技"},
            "_raw_content": "帕德博恩 vs 斯图加特",
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("与 meta.md 登记对阵", res.message)

    def test_crown_correct_score_fails_on_placeholders_or_too_few_scores(self):
        """测试波胆核验：包含占位符或少于 8 项比分时必须 FAIL 拦截"""
        snap_todo = {
            "correctScoreOdds": "| 比分 | 赔率 |\n| 1:0 | TODO |",
        }
        res1 = self.verifier._check_crown_correct_score(snap_todo)
        self.assertEqual(res1.status, CheckStatus.FAIL)
        self.assertIn("包含占位符", res1.message)

        snap_sparse = {
            "correctScoreOdds": "| 比分 | 赔率 |\n| 1:0 | 7.00 |\n| 0:0 | 8.00 |",
        }
        res2 = self.verifier._check_crown_correct_score(snap_sparse)
        self.assertEqual(res2.status, CheckStatus.FAIL)
        self.assertIn("少于 8 项", res2.message)

    def test_trend_history_fails_on_invalid_timestamp_bounds(self):
        """测试时序流水校验：时间戳小时或分钟越界(如18:62)必须 FAIL 拦截"""
        snap_bad_time = {
            "trendComparison": (
                "澳彩\t半球 0.94 0.86 10-10 18:62\n"
                "Crown\t半球 1.00 0.90 10-10 18:30\n"
                "Bet365\t半球 0.98 0.88 10-10 18:29\n"
                "易胜博\t半球 0.96 0.87 10-10 18:28\n"
                "平博\t半球 0.95 0.89 10-10 18:25\n"
                "188\t半球 0.93 0.87 10-10 18:23\n"
            )
        }
        res = self.verifier._check_trend_history(snap_bad_time)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("非法时间戳", res.message)
        self.assertIn("18:62", res.message)

    def test_verify_freshness_passes_when_recent(self):
        """测试新鲜度核验：当文件修改时间在允许阈值内时必须 PASS"""
        import time
        snap = dict(self.valid_snapshot)
        snap["_file_mtime"] = time.time() - 60  # 1分钟前
        snap["_max_age_minutes"] = 30
        receipt = self.verifier.verify(snap)
        self.assertTrue(receipt.is_valid)
        auth_res = [r for r in receipt.results if r.dimension == DimensionType.AUTHENTICITY][0]
        self.assertEqual(auth_res.status, CheckStatus.PASS)

    def test_verify_freshness_fails_when_stale(self):
        """测试新鲜度核验：当文件修改时间超过允许阈值时必须判定 FAIL (STALE_SNAPSHOT) 物理熔断"""
        import time
        snap = dict(self.valid_snapshot)
        snap["_file_mtime"] = time.time() - 3600  # 60分钟前 (超期)
        snap["_max_age_minutes"] = 30
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        auth_res = [r for r in receipt.results if r.dimension == DimensionType.AUTHENTICITY][0]
        self.assertEqual(auth_res.status, CheckStatus.FAIL)
        self.assertIn("STALE_SNAPSHOT", auth_res.message)

    def test_verify_stale_timeline_watermark_fails(self):
        """测试变盘流水时间戳水印核验：当正文流水时间戳落后文件修改时间超过 120 分钟时必须判定 FAIL (STALE_TIMELINE_WATERMARK)"""
        import time
        from datetime import datetime, timedelta
        snap = dict(self.valid_snapshot)
        now_dt = datetime.now()
        snap["_file_mtime"] = now_dt.timestamp()  # 文件刚刚修改
        snap["_max_age_minutes"] = 30
        # 构造一个 3 小时前的旧时序流水内容，包含合法主客队名
        old_time_str = (now_dt - timedelta(hours=3)).strftime("%m-%d %H:%M")
        home = snap.get("match", {}).get("homeTeam", "主队")
        away = snap.get("match", {}).get("awayTeam", "客队")
        snap["_raw_content"] = f"# 【测试】{home} vs {away}\n- **比赛 ID**：2981506\n| **T4 终盘关门** | {old_time_str} | 2.50 | 3.30 | 2.40 |"

        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        auth_res = [r for r in receipt.results if r.dimension == DimensionType.AUTHENTICITY][0]
        self.assertEqual(auth_res.status, CheckStatus.FAIL)
        self.assertIn("STALE_TIMELINE_WATERMARK", auth_res.message)

    def test_detect_single_company_patch_cheat(self):
        """测试反打补丁作弊：当仅有 1 家核心机构修改为最新时间戳而其余机构严重滞后时必须判定 FAIL (SUSPECTED_PATCH_CHEAT)"""
        from datetime import datetime, timedelta
        snap = dict(self.valid_snapshot)
        now_dt = datetime.now()
        snap["_file_mtime"] = now_dt.timestamp()
        snap["_max_age_minutes"] = 30
        home = snap.get("match", {}).get("homeTeam", "主队")
        away = snap.get("match", {}).get("awayTeam", "客队")
        recent_ts = now_dt.strftime("%m-%d %H:%M")
        old_ts = (now_dt - timedelta(hours=3)).strftime("%m-%d %H:%M")
        
        # 仅 Crown 被打了补丁为最新时间，澳彩/Bet365/易胜博/平博全停留在 3 小时前
        content = f"""# 【测试】{home} vs {away}
- **比赛 ID**：2981506
### 1. 澳彩
| T4 | {old_ts} | 0.90 | 0.90 |
### 2. Crown 皇冠
| T4 | {recent_ts} | 0.92 | 0.88 |
### 3. Bet365
| T4 | {old_ts} | 0.90 | 0.90 |
### 4. 易胜博
| T4 | {old_ts} | 0.91 | 0.89 |
### 5. 平博
| T4 | {old_ts} | 0.93 | 0.87 |
"""
        snap["_raw_content"] = content
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        auth_res = [r for r in receipt.results if r.dimension == DimensionType.AUTHENTICITY][0]
        self.assertEqual(auth_res.status, CheckStatus.FAIL)
        self.assertIn("SUSPECTED_PATCH_CHEAT", auth_res.message)

    def test_quiescent_bookmaker_with_valid_cryptographic_seal_passes(self):
        """测试合理做市商盘口静默：当文件具备有效加密封条且原始存证一致时，不误杀报 SUSPECTED_PATCH_CHEAT"""
        import hashlib
        from datetime import datetime, timedelta
        snap = dict(self.valid_snapshot)
        now_dt = datetime.now()
        snap["_file_mtime"] = now_dt.timestamp()
        snap["_max_age_minutes"] = 30
        home = snap.get("match", {}).get("homeTeam", "主队")
        away = snap.get("match", {}).get("awayTeam", "客队")
        recent_ts = now_dt.strftime("%m-%d %H:%M")
        old_ts = (now_dt - timedelta(hours=3)).strftime("%m-%d %H:%M")

        content = f"""# 【测试】{home} vs {away}
- **比赛 ID**：2981506
### 1. 澳彩
| T4 | {old_ts} | 0.90 | 0.90 |
### 2. Crown 皇冠
| T4 | {old_ts} | 0.92 | 0.88 |
### 3. Bet365
| T4 | {old_ts} | 0.90 | 0.90 |
### 4. 易胜博
| T4 | {old_ts} | 0.91 | 0.89 |
### 5. 平博
| T4 | {recent_ts} | 0.93 | 0.87 |
"""
        snap["_raw_content"] = content
        # 注入合法加密封条与原始报文存证
        c_sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
        snap["_markdown_sha256"] = c_sha
        snap["_raw_wire"] = {
            "manifest": {
                "markdown_sha256": c_sha,
                "raw_files_sha256": {},
            },
            "receipt": {
                "receivedAt": recent_ts,
                "endpoints": [],
            },
            "files": {},
        }
        receipt = self.verifier.verify(snap)
        auth_res = [r for r in receipt.results if r.dimension == DimensionType.AUTHENTICITY][0]
        # 合理静默场景下，绝对严禁误判为 SUSPECTED_PATCH_CHEAT
        self.assertNotIn("SUSPECTED_PATCH_CHEAT", auth_res.message)


    def test_genuine_multi_company_freshness_passes(self):
        """测试真实多机构活水同步：当 3 家以上核心机构均处于最新区间时必须 PASS"""
        from datetime import datetime, timedelta
        snap = dict(self.valid_snapshot)
        now_dt = datetime.now()
        snap["_file_mtime"] = now_dt.timestamp()
        snap["_max_age_minutes"] = 30
        home = snap.get("match", {}).get("homeTeam", "主队")
        away = snap.get("match", {}).get("awayTeam", "客队")
        t1 = (now_dt - timedelta(minutes=5)).strftime("%m-%d %H:%M")
        t2 = (now_dt - timedelta(minutes=10)).strftime("%m-%d %H:%M")
        t3 = (now_dt - timedelta(minutes=15)).strftime("%m-%d %H:%M")
        t4 = (now_dt - timedelta(minutes=20)).strftime("%m-%d %H:%M")
        
        content = f"""# 【测试】{home} vs {away}
- **比赛 ID**：2981506
### 1. 澳彩
| T4 | {t1} | 0.90 | 0.90 |
### 2. Crown 皇冠
| T4 | {t2} | 0.92 | 0.88 |
### 3. Bet365
| T4 | {t3} | 0.90 | 0.90 |
### 4. 易胜博
| T4 | {t4} | 0.91 | 0.89 |
### 5. 平博
| T4 | {t1} | 0.93 | 0.87 |
"""
        snap["_raw_content"] = content
        receipt = self.verifier.verify(snap)
    def test_polymarket_major_league_unopened_must_fail(self):
        """测试主流核心联赛（英超/意甲等）标记未开盘时必须判定 FAIL 阻断"""
        snap = dict(self.valid_snapshot)
        snap["match"] = dict(snap.get("match", {}))
        snap["match"]["league"] = "英超"
        snap["polymarket"] = {"status": "unopened", "url": "未开盘"}
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        pm_res = [r for r in receipt.results if r.dimension == DimensionType.POLYMARKET_LIQUIDITY][0]
        self.assertEqual(pm_res.status, CheckStatus.FAIL)
        self.assertIn("主流核心联赛", pm_res.message)

    def test_polymarket_expanded_core_leagues_unopened_must_fail(self):
        """测试扩充后的核心联赛（瑞典超/挪超/法乙/荷甲等）标记未开盘时必须判定 FAIL 阻断"""
        for lg in ["瑞典超", "挪超", "法乙", "荷甲", "美职联"]:
            snap = dict(self.valid_snapshot)
            snap["match"] = dict(snap.get("match", {}))
            snap["match"]["league"] = lg
            snap["polymarket"] = {"status": "unopened", "url": "未开放"}
            receipt = self.verifier.verify(snap)
            self.assertFalse(receipt.is_valid)
            pm_res = [r for r in receipt.results if r.dimension == DimensionType.POLYMARKET_LIQUIDITY][0]
            self.assertEqual(pm_res.status, CheckStatus.FAIL)
            self.assertIn("主流核心联赛", pm_res.message)

    def test_polymarket_unopened_allow_22_companies(self):
        """测试小众联赛合规双向检索未开盘时，允许欧指22家传统机构全齐而无需伪造第23家"""
        snap = dict(self.valid_snapshot)
        snap["match"] = dict(snap.get("match", {}))
        snap["match"]["league"] = "芬超"
        snap["is_markdown_baseline"] = True
        snap["polymarket"] = {"status": "unopened", "url": "未开放（经Gamma双向核验q=Haka与q=VPS均无活跃标的）"}
        comps = [
            "澳彩", "Bet365", "Crown", "易胜博", "平博", "188Bet", "香港马会", "威廉希尔",
            "立博", "Bwin", "Interwetten", "SNAI", "伟德", "必发", "SBO", "沙巴",
            "Marathon", "Betway", "Unibet", "Paddy Power", "10Bet", "中国体彩"
        ]
        snap["europe1x2"] = [
            {
                "company": c,
                "initial": {"odds": [2.0, 3.2, 3.4], "returnRate": 91.0},
                "latest": {"odds": [2.0, 3.2, 3.4], "returnRate": 91.0, "kelly": [0.92, 0.93, 0.95]},
            }
            for c in comps
        ]
        pm_res = self.verifier._check_polymarket(snap)
        self.assertEqual(pm_res.status, CheckStatus.WARN)
        euro_res = self.verifier._check_europe_1x2(snap)
        self.assertEqual(euro_res.status, CheckStatus.PASS)

    def test_polymarket_minor_league_without_dual_proof_fails(self):
        """测试次级冷门联赛若未开盘理由缺乏双向检索存证，必须判定 FAIL 阻断口头逃逸"""
        snap = dict(self.valid_snapshot)
        snap["match"] = dict(snap.get("match", {}))
        snap["match"]["league"] = "芬超"
        # 仅模糊写未开盘，无双向检索证据
        snap["polymarket"] = {"status": "unopened", "url": "未开盘"}
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        pm_res = [r for r in receipt.results if r.dimension == DimensionType.POLYMARKET_LIQUIDITY][0]
        self.assertEqual(pm_res.status, CheckStatus.FAIL)
        self.assertIn("存证不足", pm_res.message)

    def test_polymarket_internal_contradiction_must_fail(self):
        """测试内部逻辑矛盾：顶部标明未开盘，但正文/欧指编造 Polymarket 挂单数据必须 FAIL"""
        snap = dict(self.valid_snapshot)
        snap["match"] = dict(snap.get("match", {}))
        snap["match"]["league"] = "瑞典超"
        snap["polymarket"] = {"status": "unopened", "url": "未开盘"}
        snap["_raw_content"] = (
            "# 【周一003】瑞典超 马尔默 vs 卡尔马\n"
            "- **Polymarket 预测市场**：未开放\n"
            "| **23** | **Polymarket** | **T0** | 27¢ | 25¢ | 48¢ |"
        )
        receipt = self.verifier.verify(snap)
        self.assertFalse(receipt.is_valid)
        pm_res = [r for r in receipt.results if r.dimension == DimensionType.POLYMARKET_LIQUIDITY][0]
        self.assertEqual(pm_res.status, CheckStatus.FAIL)
        self.assertIn("矛盾", pm_res.message)

    def test_polymarket_valid_event_url_passes(self):
        """测试合法可点击的 Polymarket 事件链接必须判定 PASS"""
        snap = dict(self.valid_snapshot)
        snap["polymarket"] = {
            "status": "active",
            "url": "https://polymarket.com/event/sea-ata-ven-2026-10-12",
        }
        res = self.verifier._check_polymarket(snap)
        self.assertEqual(res.status, CheckStatus.PASS)
        self.assertIn("https://polymarket.com/event/sea-ata-ven-2026-10-12", res.message)


class TestMemoryCognitiveCardsVerifier(unittest.TestCase):
    def setUp(self):
        self.valid_card = """## 深度分析

### 意甲 亚特兰大 vs 威尼斯（编号: 周一002 比赛ID: 2993805，开球: 2026-10-13 00:30，分析: 2026-10-12 21:00）
🔗 https://zq.titan007.com/analysis/2993805cn.htm

#### 赔率摘要
- 欧指方向：一致看胜，主胜1.25/平5.50/客胜11.00

#### 综合评估
- 胜平负：首选 主胜｜次选 平局
- 胜/平/负点概率（OO-EPC去水）：胜 77.57% / 平 14.16% / 负 8.27%
- 【图谱认知基因】：[Egidi 攻防参数凸组合, 赔率分析推演十大公理] ｜ 演绎链：火力碾压 -> 深盘阻热 -> 正路设防
- 【认知契约卡】：
  - 选择与排除依据：亚特兰大火力与射正压制显著，威尼斯客场防线崩塌，排除客胜
  - 关键拍板依据：做市商球半超低水升球半两球，高门槛有效阻热
  - 庄家博弈假说与竞争解释：借深盘门槛阻挡主胜过热筹码，实控主胜赔付
  - 可推翻反证与改变条件：若临盘退盘至一球/球半高水，且主力射手突发缺阵，则推翻大胜假设降级防平
"""

    def test_valid_memory_passes(self):
        from 校验.src.domain.verifier import verify_memory_cognitive_cards
        ok, errors, count = verify_memory_cognitive_cards(self.valid_card, expected_matches=1)
        self.assertTrue(ok)
        self.assertEqual(count, 1)
        self.assertEqual(len(errors), 0)

    def test_missing_deep_analysis_section_fails(self):
        from 校验.src.domain.verifier import verify_memory_cognitive_cards
        ok, errors, count = verify_memory_cognitive_cards("## 赛前分析推演\n一些表格", expected_matches=1)
        self.assertFalse(ok)
        self.assertIn("深度分析", errors[0])

    def test_missing_graphify_gene_fails(self):
        from 校验.src.domain.verifier import verify_memory_cognitive_cards
        broken = self.valid_card.replace("【图谱认知基因】", "一些其他基因")
        ok, errors, count = verify_memory_cognitive_cards(broken, expected_matches=1)
        self.assertFalse(ok)
        self.assertTrue(any("图谱认知基因" in e for e in errors))

    def test_missing_dimension_in_contract_card_fails(self):
        from 校验.src.domain.verifier import verify_memory_cognitive_cards
        broken = self.valid_card.replace("可推翻反证与改变条件", "其他条件")
        ok, errors, count = verify_memory_cognitive_cards(broken, expected_matches=1)
        self.assertFalse(ok)
        self.assertTrue(any("可推翻反证与改变条件" in e for e in errors))

    def test_expected_matches_count_mismatch_fails(self):
        from 校验.src.domain.verifier import verify_memory_cognitive_cards
        ok, errors, count = verify_memory_cognitive_cards(self.valid_card, expected_matches=2)
        self.assertFalse(ok)
        self.assertTrue(any("低于预期场次" in e for e in errors))

    def test_verify_memory_detects_7col_table_vs_card_direction_conflict(self):
        """U4红灯测试: 当 memory.md 中 7 列汇总表的胜负平方向与下方深度分析卡片首选方向自相矛盾时，必须拦截 (MEMORY_INTERNAL_DIRECTION_CONFLICT)"""
        from 校验.src.domain.verifier import verify_memory_cognitive_cards
        conflicting_md = (
            "## 推荐汇总\n\n"
            "| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "| 周一002 00:30 | 亚特兰大 vs 威尼斯 | 客胜/平局 | -1 让负 | 77.57% / 14.16% / 8.27% | 诱主 | https://polymarket.com/event/sea-ata-ven-2026-10-12 |\n\n"
            + self.valid_card
        )
        ok, errors, _ = verify_memory_cognitive_cards(conflicting_md, expected_matches=1)
        self.assertFalse(ok)
        self.assertTrue(any("MEMORY_INTERNAL_DIRECTION_CONFLICT" in e for e in errors), f"Actual errors: {errors}")

    def test_verify_memory_cross_checks_source_snapshot_drift(self):
        """U4红灯测试: 当传入 data_dir 时，memory.md 必须与 data/{销售日}/{matchId}.md 源数据对阵与欧指真值交叉核对，不符则报 MEMORY_SOURCE_DRIFT"""
        import tempfile
        from pathlib import Path
        from 校验.src.domain.verifier import verify_memory_cognitive_cards

        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            # 构造与 memory 卡片 (主胜1.25/平5.50/客胜11.00) 截然不同的真实源数据快照 (主胜 2.85 / 平 3.30 / 客胜 2.40)
            (data_dir / "2993805.md").write_text(
                "# 【周一002】意甲 亚特兰大 vs 威尼斯\n"
                "- **比赛 ID**：2993805\n"
                "## 三、欧洲指数百家做市商清单（法定 23 家）\n"
                "| 机构类型 | 机构 | 初盘主胜 | 初盘平局 | 初盘客胜 | 初返还 | 即时主胜 | 即时平局 | 即时客胜 | 即时返还 | 凯利(主/平/客) |\n"
                "| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |\n"
                "| 核心做市 | Bet365 | 2.80 | 3.30 | 2.45 | 92.5% | 2.85 | 3.30 | 2.40 | 92.8% | 0.93/0.92/0.94 |\n",
                encoding="utf-8",
            )
            ok, errors, _ = verify_memory_cognitive_cards(self.valid_card, expected_matches=1, data_dir=str(data_dir))
            self.assertFalse(ok)
            self.assertTrue(any("MEMORY_SOURCE_DRIFT" in e for e in errors), f"Actual errors: {errors}")

    def test_verify_memory_detects_bold_shengfuping_direction_conflict(self):
        """红灯测试: 当卡片中写成加粗 **胜负平**: 平局 (次选客胜) 而表格首选写 主胜 时，必须精准拦截方向冲突，绝不被字序或加粗绕过"""
        from 校验.src.domain.verifier import verify_memory_cognitive_cards
        card_with_bold = self.valid_card.replace(
            "- 胜平负：首选 主胜｜次选 平局",
            "- **胜负平**: 平局 (次选客胜)"
        )
        table_with_home_win = (
            "## 推荐汇总\n\n"
            "| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "| 周一002 00:30 | 亚特兰大 vs 威尼斯 | 主胜 | -1 让胜 | 77.57% / 14.16% / 8.27% | 诱主 | https://polymarket.com/event/sea-ata-ven-2026-10-12 |\n\n"
            + card_with_bold
        )
        ok, errors, _ = verify_memory_cognitive_cards(table_with_home_win, expected_matches=1)
        self.assertFalse(ok)
        self.assertTrue(any("MEMORY_INTERNAL_DIRECTION_CONFLICT" in e for e in errors), f"Actual errors: {errors}")

    def test_verify_memory_detects_probability_drift(self):
        """红灯测试: 当 7 列表格点概率 (44.73% / ...) 与卡片点概率 (77.57% / ...) 偏差 > 0.5% 时，报 MEMORY_INTERNAL_PROBABILITY_DRIFT"""
        from 校验.src.domain.verifier import verify_memory_cognitive_cards
        table_with_wrong_prob = (
            "## 推荐汇总\n\n"
            "| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "| 周一002 00:30 | 亚特兰大 vs 威尼斯 | 主胜 | -1 让胜 | 44.73% / 22.87% / 32.40% | 诱主 | https://polymarket.com/event/sea-ata-ven-2026-10-12 |\n\n"
            + self.valid_card
        )
        ok, errors, _ = verify_memory_cognitive_cards(table_with_wrong_prob, expected_matches=1)
        self.assertFalse(ok)
        self.assertTrue(any("MEMORY_INTERNAL_PROBABILITY_DRIFT" in e for e in errors), f"Actual errors: {errors}")

    def test_verify_memory_detects_handicap_hallucination_against_source(self):
        """红灯测试: 当 7 列表格第 6 列诱盘破译脑补了源数据中从未开出的盘口 (如源数据只有半球盘，却脑补升盘半一) 时，报 MEMORY_TABLE_TIMELINE_HALLUCINATION"""
        import tempfile
        from pathlib import Path
        from 校验.src.domain.verifier import verify_memory_cognitive_cards

        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            (data_dir / "2993805.md").write_text(
                "# 【周一002】意甲 亚特兰大 vs 威尼斯\n"
                "- **比赛 ID**：2993805\n"
                "## 四、核心做市商与终端标的真实变盘时序流水\n"
                "#### 亚盘真实变盘流水\n"
                "| 变盘时间 | 盘口 | 主水 | 客水 | 状态 |\n"
                "| 10-12 21:00 | 半球 | 0.85 | 1.05 | 即 |\n"
                "| 10-10 18:00 | 半球 | 0.90 | 1.00 | 初盘 |\n",
                encoding="utf-8",
            )
            table_with_hallucinated_handicap = (
                "## 推荐汇总\n\n"
                "| 场次/时间 | 对阵双方 | 胜负平 | 让球 | 胜/平/负点概率（OO-EPC去水） | 庄家诱盘破译 | Polymarket 真实链接 |\n"
                "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
                "| 周一002 00:30 | 亚特兰大 vs 威尼斯 | 主胜 | -1 让胜 | 77.57% / 14.16% / 8.27% | 【初盘形态】半球 ➔【中盘演进】升盘半一0.98高阻 ➔【终盘真实意图】设防 | https://polymarket.com/event/sea-ata-ven-2026-10-12 |\n\n"
                + self.valid_card
            )
            ok, errors, _ = verify_memory_cognitive_cards(table_with_hallucinated_handicap, expected_matches=1, data_dir=str(data_dir))
            self.assertFalse(ok)
            self.assertTrue(any("MEMORY_TABLE_TIMELINE_HALLUCINATION" in e for e in errors), f"Actual errors: {errors}")


    def test_summary_table_assembler_deterministic_projection(self):
        """测试 SummaryTableAssembler 机械单射组装 7 列表格，杜绝任何人工转述篡改"""
        from 校验.src.domain.assembler import SummaryTableAssembler
        cards = [
            {
                "matchCode": "周四010",
                "kickoffTime": "03:00",
                "teams": "马赛 vs 奥林匹亚科斯",
                "primaryDirection": "平局 (次选客胜)",
                "handicapDirection": "[-1] 让负",
                "ooEpcProbabilities": "44.73% / 22.87% / 32.40%",
                "bookmakerTrapDeduction": "【初盘形态】平半高水 ➔【中盘演进】主水顶死在1.00满水 ➔【终盘真实意图】设防客队受让",
                "polymarketLink": "https://polymarket.com/event/uel-olm-oly-2026-10-15",
            }
        ]
        table_md = SummaryTableAssembler.assemble_table(cards)
        self.assertIn("| 周四010 03:00 | 马赛 vs 奥林匹亚科斯 | 平局 (次选客胜) | [-1] 让负 |", table_md)
        self.assertIn("44.73% / 22.87% / 32.40%", table_md)
        self.assertIn("https://polymarket.com/event/uel-olm-oly-2026-10-15", table_md)


class TestRawWireAntiFabrication(unittest.TestCase):
    """U3红灯测试: 原始报文哈希封条 (TAMPERED_MARKDOWN_SEAL) 与原文子串交叉校验 (RAW_PROVENANCE_MISMATCH)"""

    def setUp(self):
        self.verifier = SnapshotVerifier()

    def test_tampering_single_punctuation_in_md_breaks_sha256_seal(self):
        """测试U3: 只要手动修改 .md 中哪怕一个标点符号或一分钟时间戳，SHA-256 封条立即破裂触发 TAMPERED_MARKDOWN_SEAL 熔断"""
        import hashlib
        original_md = "# 【周一005】葡超 法马利康 vs 阿尔韦卡\n- **比赛 ID**：3023499\n"
        original_sha = hashlib.sha256(original_md.encode("utf-8")).hexdigest()
        # 篡改一个标点符号（将全角冒号改为半角或改一个数字）
        tampered_md = "# 【周一005】葡超 法马利康 vs 阿尔韦卡。\n- **比赛 ID**：3023499\n"
        tampered_sha = hashlib.sha256(tampered_md.encode("utf-8")).hexdigest()

        snap = {
            "matchId": "3023499",
            "match": {"league": "葡超", "homeTeam": "法马利康", "awayTeam": "阿尔韦卡"},
            "_raw_content": tampered_md,
            "_markdown_sha256": tampered_sha,
            "_raw_wire": {
                "manifest": {
                    "matchId": "3023499",
                    "markdown_sha256": original_sha,
                }
            },
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("TAMPERED_MARKDOWN_SEAL", res.message)

    def test_fabricated_odds_mismatch_against_raw_js_fails(self):
        """测试U3: 复现 10-12 3023499 造假案 —— 当 .md 欧指写 1.55->1.53 而 raw/3023499/1x2d.js 真实报文为 1.70->1.91 时，必须触发 RAW_PROVENANCE_MISMATCH 熔断"""
        import hashlib
        fake_md = "# 【周一005】葡超 法马利康 vs 阿尔韦卡\n- **比赛 ID**：3023499\n"
        md_sha = hashlib.sha256(fake_md.encode("utf-8")).hexdigest()
        raw_1x2_js = (
            'var hometeam_cn="法马利康";var guestteam_cn="阿尔韦卡";'
            'var game=Array("281|10001|Bet365|1.70|3.60|4.50|54.1|25.5|20.4|91.9|1.91|3.50|3.60|48.2|26.3|25.5|92.0|0.93|0.94|0.92|2026,10-1,12,18,30,00|104|10002|Interwetten|1.75|3.55|4.30|53.0|26.1|21.5|92.7|1.95|3.45|3.50|47.5|26.8|26.4|92.6|0.95|0.93|0.90|2026,10-1,12,18,15,00");'
        )
        snap = {
            "matchId": "3023499",
            "match": {"league": "葡超", "homeTeam": "法马利康", "awayTeam": "阿尔韦卡"},
            "_raw_content": fake_md,
            "_markdown_sha256": md_sha,
            "europe1x2": [
                {
                    "company": "Bet365",
                    "initial": {"odds": [1.55, 3.80, 5.50], "returnRate": 91.9},
                    "latest": {"odds": [1.53, 3.90, 5.80], "returnRate": 92.0, "kelly": [0.93, 0.94, 0.92]},
                }
            ],
            "_raw_wire": {
                "manifest": {
                    "matchId": "3023499",
                    "markdown_sha256": md_sha,
                },
                "1x2d.js": raw_1x2_js,
            },
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("RAW_PROVENANCE_MISMATCH", res.message)
        self.assertIn("Bet365", res.message)

    def test_raw_parser_extracts_verbatim_and_passes_seal_check(self):
        """测试U3: Titan007RawParser 从原始报文提取真实赔率与时序并生成加密封条 manifest.json"""
        from 校验.src.domain.raw_parser import Titan007RawParser
        parser = Titan007RawParser()
        raw_js = (
            'var hometeam_cn="法马利康";var guestteam_cn="阿尔韦卡";var matchname_cn="葡超";var MatchTime="2026,10-1,12,23,00,00";'
            'var game=Array('
            '"281|101|Bet365|1.70|3.60|4.50|54.1|25.5|20.4|91.90|1.91|3.50|3.60|48.2|26.3|25.5|92.00|0.93|0.94|0.92|2026,10-1,12,18,30,00",'
            '"80|102|Macauslot|1.68|3.55|4.40|54.1|25.5|20.4|90.10|1.88|3.45|3.55|48.2|26.3|25.5|90.20|0.91|0.93|0.91|2026,10-1,12,18,20,00"'
            ');'
        )
        parsed = parser.parse_1x2d_js(raw_js)
        self.assertEqual(parsed["homeTeam"], "法马利康")
        self.assertEqual(parsed["awayTeam"], "阿尔韦卡")
        self.assertEqual(len(parsed["europe1x2"]), 2)
        self.assertEqual(parsed["europe1x2"][0]["initialOdds"], ["1.70", "3.60", "4.50"])
        self.assertEqual(parsed["europe1x2"][0]["liveOdds"], ["1.91", "3.50", "3.60"])

    def test_authenticity_rejects_legacy_t0_t4_padding_and_fake_intervals(self):
        """测试漏洞封堵1: 若大模型偷懒手写包含『维持区间』『T0 初盘骨架』『做市形态学识别』或『10-08 12:00』的伪造时序，必须触发 FABRICATED_TIMELINE_PADDING 物理熔断"""
        for forbidden_token in ("维持区间", "T0 初盘骨架", "T2 中盘假摔", "做市形态学识别", "10-08 12:00"):
            snap = {
                "matchId": "3023499",
                "is_markdown_baseline": True,
                "match": {"league": "葡超", "homeTeam": "法马利康", "awayTeam": "阿尔韦卡"},
                "_raw_content": f"# 【周一005】葡超 法马利康 vs 阿尔韦卡\n- **比赛 ID**：3023499\n| {forbidden_token} | 0.88 | 半一 | 0.96 |",
            }
            res = self.verifier._check_authenticity(snap)
            self.assertEqual(res.status, CheckStatus.FAIL, f"Token '{forbidden_token}' was not blocked!")
            self.assertIn("FABRICATED_TIMELINE_PADDING", res.message)

    def test_authenticity_rejects_unsealed_markdown_in_live_mode(self):
        """测试漏洞封堵2: 在实时门禁模式 (_max_age_minutes 启用) 下，若 .md 缺少 raw/{matchId}/manifest.json 加密封条 (说明绕过 cli.py --assemble 直接用 write_to_file 手写)，必须触发 MISSING_CRYPTOGRAPHIC_SEAL 熔断"""
        from datetime import datetime, timedelta
        now_dt = datetime.now()
        t1 = (now_dt - timedelta(minutes=5)).strftime("%m-%d %H:%M")
        snap = {
            "matchId": "3023499",
            "is_markdown_baseline": True,
            "_file_mtime": now_dt.timestamp(),
            "_max_age_minutes": 30,
            "match": {"league": "葡超", "homeTeam": "法马利康", "awayTeam": "阿尔韦卡"},
            "_raw_content": (
                f"# 【周一005】葡超 法马利康 vs 阿尔韦卡\n- **比赛 ID**：3023499\n"
                f"### 1. 澳彩\n| {t1} | 澳彩 | 0.88 | 半一 | 0.96 |\n"
                f"### 2. Crown 皇冠\n| {t1} | Crown | 0.88 | 半一 | 0.96 |\n"
                f"### 3. Bet365\n| {t1} | Bet365 | 0.88 | 半一 | 0.96 |\n"
            ),
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("MISSING_CRYPTOGRAPHIC_SEAL", res.message)

    def test_memory_source_drift_catches_subtle_020_fabrication(self):
        """测试漏洞封堵4: 复现 1.85 伪造为 1.55 (差值 0.30) —— 只要记忆卡片引用的赔率与源数据偏差 > 0.05，立即触发 MEMORY_SOURCE_DRIFT 拦截"""
        import tempfile
        from pathlib import Path
        from 校验.src.domain.verifier import verify_memory_cognitive_cards

        card = """# 每日记忆
## 深度分析

### 葡超 法马利康 vs 阿尔韦卡（编号: 周一010 比赛ID: 3023499，开球: 2026-10-13 03:15，分析: 2026-10-12 21:00）
#### 赔率摘要
- 欧指方向：多公司一致看主胜，依据公司即时 主胜1.55/平3.80/客胜5.20
#### 综合评估
- 胜平负：首选 主胜｜次选 平局
- 胜/平/负点概率（OO-EPC去水）：胜 60.10% / 平 24.50% / 负 15.40%
- 【图谱认知基因】：[Egidi 攻防参数凸组合] ｜ 演绎链：主场压制 -> 正路
- 【认知契约卡】：
  - 选择与排除依据：主场占优
  - 关键拍板依据：深盘低水
  - 庄家博弈假说与竞争解释：阻上
  - 可推翻反证与改变条件：退盘
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            data_dir = Path(tmpdir)
            (data_dir / "3023499.md").write_text(
                "# 【周一010】葡超 法马利康 vs 阿尔韦卡\n"
                "- **比赛 ID**：3023499\n"
                "## 三、法定23家机构初即盘与凯利总表\n"
                "| 机构类型 | 机构 | 初盘主胜 | 初盘平局 | 初盘客胜 | 初返还 | 即时主胜 | 即时平局 | 即时客胜 | 即时返还 | 凯利(主/平/客) |\n"
                "| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |\n"
                "| 核心做市 | Bet365 | 1.85 | 3.50 | 4.20 | 92.5% | 1.75 | 3.60 | 4.50 | 92.8% | 0.93/0.92/0.94 |\n",
                encoding="utf-8",
            )
            ok, errors, _ = verify_memory_cognitive_cards(card, expected_matches=1, data_dir=str(data_dir))
            self.assertFalse(ok)
            self.assertTrue(any("MEMORY_SOURCE_DRIFT" in e for e in errors), f"Actual errors: {errors}")

    def test_raw_parser_never_fabricates_092_kelly_or_mutates_zao_to_ji(self):
        """U1红灯测试: Titan007RawParser 严禁使用 '0.92' 假凯利兜底，严禁将原始 '早' 篡改为 '即'"""
        from pathlib import Path
        from 校验.src.domain.raw_parser import Titan007RawParser

        repo_root = Path(__file__).resolve().parent.parent.parent
        raw_parser_src = (repo_root / "校验" / "src" / "domain" / "raw_parser.py").read_text(encoding="utf-8")
        self.assertNotIn('"0.92"', raw_parser_src, "raw_parser.py 仍存在 '0.92' 假凯利兜底")
        self.assertNotIn('st == "早"', raw_parser_src, "raw_parser.py 仍存在将 '早' 篡改为 '即' 的后门")

        parser = Titan007RawParser()
        # 1. 缺失凯利字段时必须返回 "-"，绝不返回 "0.92"
        raw_js = (
            'var hometeam_cn="鹿儿岛联";var guestteam_cn="鸟栖沙岩";'
            'var game=Array("281|101|Bet365|2.10|3.40|3.10|43.1|26.5|30.4|91.90|2.05|3.45|3.20|44.2|26.3|29.5|92.00||||2026,10-1,13,09,30,00");'
        )
        parsed = parser.parse_1x2d_js(raw_js)
        self.assertEqual(parsed["europe1x2"][0]["kelly"], ["-", "-", "-"])

        # 2. changeDetail.html 中状态为 "早" 时必须原样保留 "早"，绝不篡改为 "即"
        raw_html = """
        <table>
          <tr><td>0.85</td><td>平手/半球</td><td>0.95</td><td>10-13 09:49</td><td>即</td></tr>
          <tr><td>0.88</td><td>平手/半球</td><td>0.92</td><td>10-12 14:20</td><td>早</td></tr>
          <tr><td>0.90</td><td>平手/半球</td><td>0.90</td><td>10-11 18:00</td><td>初盘</td></tr>
        </table>
        """
        rows = parser.parse_change_detail_rows(raw_html)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0][4], "即")
        self.assertEqual(rows[1][4], "早")
        self.assertEqual(rows[2][4], "初盘")

    def test_raw_parser_extracts_1x2_detail_rows_verbatim(self):
        """U1红灯测试: Titan007RawParser.parse_1x2_detail_rows 原样提取 1x2.aspx 变盘流水且不截断、不改状态字"""
        from 校验.src.domain.raw_parser import Titan007RawParser
        parser = Titan007RawParser()
        raw_eu_html = """
        <table>
          <tr><td>2.08</td><td>3.55</td><td>2.85</td><td>89.96%</td><td>0.92</td><td>0.94</td><td>0.91</td><td>10-13 10:15(即)</td></tr>
          <tr><td>2.12</td><td>3.55</td><td>2.80</td><td>90.02%</td><td>0.94</td><td>0.94</td><td>0.89</td><td>10-12 22:10(早)</td></tr>
          <tr><td>2.15</td><td>3.50</td><td>2.75</td><td>89.80%</td><td>0.95</td><td>0.93</td><td>0.88</td><td>10-11 16:00(初盘)</td></tr>
        </table>
        """
        rows = parser.parse_1x2_detail_rows(raw_eu_html)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], ("10-13 10:15", "2.08", "3.55", "2.85", "89.96%", "0.92/0.94/0.91", "即"))
        self.assertEqual(rows[1], ("10-12 22:10", "2.12", "3.55", "2.80", "90.02%", "0.94/0.94/0.89", "早"))
        self.assertEqual(rows[2], ("10-11 16:00", "2.15", "3.50", "2.75", "89.80%", "0.95/0.93/0.88", "初盘"))

    def test_authenticity_detects_truncated_section4_timeline_rows_against_raw_html(self):
        """U3红灯测试: 当 .md 第四节时序表行数被截断(如原始报文有4行但.md只写了2行)或状态字'早'被改为'即'时，必须触发 RAW_PROVENANCE_MISMATCH"""
        import hashlib
        fake_md = "# 【周二001】日职乙 鹿儿岛联 vs 鸟栖沙岩\n- **比赛 ID**：3068865\n"
        md_sha = hashlib.sha256(fake_md.encode("utf-8")).hexdigest()
        raw_ah_80 = """
        <table>
          <tr><td>0.82</td><td>平手</td><td>0.98</td><td>10-13 10:12</td><td>即</td></tr>
          <tr><td>0.85</td><td>平手</td><td>0.95</td><td>10-13 08:30</td><td>早</td></tr>
          <tr><td>0.88</td><td>平手</td><td>0.92</td><td>10-12 21:15</td><td>早</td></tr>
          <tr><td>0.90</td><td>平手</td><td>0.90</td><td>10-11 16:00</td><td>初盘</td></tr>
        </table>
        """
        snap = {
            "matchId": "3068865",
            "match": {"league": "日职乙", "homeTeam": "鹿儿岛联", "awayTeam": "鸟栖沙岩"},
            "_raw_content": fake_md,
            "_markdown_sha256": md_sha,
            "companyTimelines": {
                "澳彩": {
                    # 被截断为2行，漏掉了中间2行 '早'
                    "ah": [
                        ("10-13 10:12", "平手", "0.82", "0.98", "即"),
                        ("10-11 16:00", "平手", "0.90", "0.90", "初盘"),
                    ],
                    "ou": [],
                    "eu": [],
                }
            },
            "_raw_wire": {
                "manifest": {
                    "matchId": "3068865",
                    "markdown_sha256": md_sha,
                },
                "files": {
                    "ah_80.html": raw_ah_80,
                },
            },
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("RAW_PROVENANCE_MISMATCH", res.message)
        self.assertIn("澳彩", res.message)

    def test_authenticity_detects_fabricated_sporttery_initial_timestamp(self):
        """U3红灯测试: 复现 3068865 体彩初盘假时间 10-12 11:00 —— 当 1x2d.js 中体彩仅有1个时间 10-13 09:05 但 .md 编造了 10-12 11:00 初盘行时，必须触发 RAW_PROVENANCE_MISMATCH"""
        import hashlib
        fake_md = "# 【周二001】日职乙 鹿儿岛联 vs 鸟栖沙岩\n- **比赛 ID**：3068865\n"
        md_sha = hashlib.sha256(fake_md.encode("utf-8")).hexdigest()
        raw_1x2_js = (
            'var hometeam_cn="鹿儿岛联";var guestteam_cn="鸟栖沙岩";'
            'var game=Array("478|1099|Lottery Official|2.32|3.50|2.42|37.9|25.1|36.3|87.98|2.32|3.50|2.42|37.9|25.1|36.3|87.98|0.87|0.91|0.88|2026,10-1,13,09,05,00");'
        )
        snap = {
            "matchId": "3068865",
            "match": {"league": "日职乙", "homeTeam": "鹿儿岛联", "awayTeam": "鸟栖沙岩"},
            "_raw_content": fake_md,
            "_markdown_sha256": md_sha,
            "sportteryHadRows": [
                ("10-13 09:05", "2.32", "3.50", "2.42", "87.98%", "0.87/0.91/0.88", "即"),
                ("10-12 11:00", "2.32", "3.50", "2.42", "87.98%", "0.87/0.91/0.88", "初盘"),
            ],
            "_raw_wire": {
                "manifest": {
                    "matchId": "3068865",
                    "markdown_sha256": md_sha,
                },
                "1x2d.js": raw_1x2_js,
                "files": {"1x2d.js": raw_1x2_js},
            },
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("RAW_PROVENANCE_MISMATCH", res.message)
        self.assertIn("10-12 11:00", res.message)

    def test_parse_1x2d_js_extracts_game_detail_bjt_timelines_and_intermediate_kellys(self):
        """漏洞1红灯测试: parse_1x2d_js 必须解析 var gameDetail=Array(...) 获取北京时间真实变盘流水及每行真实凯利，严禁误用 game 数组的 UTC 时间或丢失中间行凯利"""
        from 校验.src.domain.raw_parser import Titan007RawParser
        raw_js = (
            'var hometeam_cn="纽卡斯尔喷气机";var guestteam_cn="大阪钢巴";'
            'var game=Array("1129|159151625|Lottery Official|3.3|3.9|1.76|26.87|22.74|50.39|88.68|3.95|4.4|1.54|22.41|20.12|57.48|88.51|0.93|0.96|0.84|2026,10-1,13,05,07,00|0.78|0.85|0.96|0");'
            'var gameDetail=Array("159151625^3.95|4.4|1.54|10-13 13:07|0.93|0.96|0.84|2026;3.60|4.15|1.63|10-13 11:20|0.85|0.91|0.89|2026;3.3|3.9|1.76|10-13 09:46|0.78|0.85|0.96|2026");'
        )
        parsed = Titan007RawParser().parse_1x2d_js(raw_js)
        sp = parsed["byCompany"]["中国体彩"]
        self.assertEqual(sp["changeTime"], "10-13 13:07")
        detail_rows = sp.get("detailRows") or []
        self.assertEqual(len(detail_rows), 3)
        self.assertEqual(detail_rows[0], ("10-13 13:07", "3.95", "4.40", "1.54", "88.51%", "0.93/0.96/0.84", "即"))
        self.assertEqual(detail_rows[1], ("10-13 11:20", "3.60", "4.15", "1.63", "88.32%", "0.85/0.91/0.89", "即"))
        self.assertEqual(detail_rows[2], ("10-13 09:46", "3.30", "3.90", "1.76", "88.68%", "0.78/0.85/0.96", "初盘"))

    def test_parse_correct_score_html_parses_raw_html_crown_table(self):
        """漏洞2红灯测试: parse_correct_score_html 必须原生解析 odds.html 的 HTML 表格 (波胆/入球数/半全场/角球数)，绝不拿体彩 jcOdds 冒充 Crown 皇冠波胆"""
        from 校验.src.domain.raw_parser import Titan007RawParser
        raw_odds_html = (
            '<table width="100%"><tr class="bui"><td width="68"><b>波胆</b></td>'
            '<td>1:0</td><td>2:0</td><td>2:1</td><td>3:0</td><td>3:1</td><td>3:2</td><td>4:0</td><td>4:1</td><td>4:2</td><td>4:3</td>'
            '<td>0:0</td><td>1:1</td><td>2:2</td><td>3:3</td><td>4:4</td></tr>'
            '<tr class="odds"><td>主</td><td>20</td><td>30</td><td>13</td><td>60</td><td>30</td><td>25</td><td>140</td><td>80</td><td>70</td><td>85</td>'
            '<td rowspan="2">28</td><td rowspan="2">8.6</td><td rowspan="2">11.5</td><td rowspan="2">35</td><td rowspan="2">130</td></tr>'
            '<tr class="odds"><td>客</td><td>12</td><td>10.5</td><td>7.5</td><td>14</td><td>10</td><td>15.5</td><td>25</td><td>18</td><td>28</td><td>55</td></tr></table>'
            '<table><tr class="bui"><td><b>入球数</b></td><td>0~1</td><td>2~3</td><td>4~6</td><td>7+</td></tr>'
            '<tr class="odds"><td>5.4</td><td>1.25</td><td>1.1</td><td>8.6</td></tr></table>'
            '<table><tr class="bui"><td><b>半全场</b></td><td>主/主</td><td>主/和</td><td>主/客</td><td>和/主</td><td>和/和</td><td>和/客</td><td>客/主</td><td>客/和</td><td>客/客</td></tr>'
            '<tr class="odds"><td>5.9</td><td>14.5</td><td>17</td><td>9.5</td><td>7.3</td><td>4.1</td><td>30</td><td>14.5</td><td>1.38</td></tr></table>'
        )
        cs = Titan007RawParser().parse_correct_score_html(raw_odds_html)
        self.assertEqual(len(cs["correctScores"]), 10)
        self.assertEqual(cs["correctScores"][0], ("1:0", "20", "0:0", "28", "0:1", "12"))
        self.assertEqual(cs["correctScores"][1], ("2:0", "30", "1:1", "8.6", "0:2", "10.5"))
        self.assertIn("0~1球 (5.4)", cs["totalGoalsText"])
        self.assertIn("主/主(5.9)", cs["halfFullTimeText"])

    def test_parse_polymarket_json_gamma_api_without_initial_history_sets_initial_to_dash(self):
        """漏洞3红灯测试: Gamma API 仅含当前实时挂单价时，Polymarket 初盘列必须为 '-'，严禁把实时价复制冒充初盘"""
        import json
        from 校验.src.domain.raw_parser import Titan007RawParser
        gamma_json = json.dumps({
            "slug": "acle-nuj-gam-2026-10-13",
            "gameId": 73835472,
            "markets": [
                {"outcomePrices": '["0.22", "0.78"]', "updatedAt": "2026-10-13T05:36:14Z"},
                {"outcomePrices": '["0.205", "0.795"]', "updatedAt": "2026-10-13T05:36:14Z"},
                {"outcomePrices": '["0.575", "0.425"]', "updatedAt": "2026-10-13T05:36:14Z"},
            ],
        })
        res = Titan007RawParser().parse_polymarket_json(gamma_json)
        eu = res["europe1x2_entry"]
        self.assertEqual(eu["initialOdds"], ["-", "-", "-"])
        self.assertEqual(eu["initialReturn"], "-")
        self.assertEqual(eu["liveOdds"], ["4.55", "4.88", "1.74"])

    def test_parse_analysis_html_extracts_section1_and_section2_without_meta_json(self):
        """漏洞4红灯测试: Titan007RawParser.parse_analysis_html 原生从 analysis.html 提取场地天气、伤停评分、近况、赛程、盘路、技统与进球时段"""
        from 校验.src.domain.raw_parser import Titan007RawParser
        sample_analysis_md = """
[场地：亨特国际体育中心](//zq.titan007.com/cn/Venue/841.html)天气：间中有云 温度：18℃～19℃
联赛积分排名
| [**[澳超-1]纽卡斯尔喷气机**](//zq.titan007.com/cn/team/Summary/2915.html) |
| 全场 | 赛 | 胜 | 平 | 负 | 得 | 失 | 净 | 积分 | 排名 | 胜率 |
| 总 | 26 | 15 | 3 | 8 | 55 | 39 | 16 | 48 | 1 | 57.7% |
| 主 | 13 | 7 | 1 | 5 | 30 | 20 | 10 | 22 | 2 | 53.8% |
| 近6 | 6 | 2 | 2 | 2 | 12 | 9 | 3 | 8 | 33.3% |
| [**[日职联-18]大阪钢巴**](//zq.titan007.com/cn/team/Summary/207.html) |
| 全场 | 赛 | 胜 | 平 | 负 | 得 | 失 | 净 | 积分 | 排名 | 胜率 |
| 总 | 9 | 1 | 3 | 5 | 8 | 16 | -8 | 6 | 18 | 11.1% |
| 客 | 5 | 0 | 2 | 3 | 4 | 10 | -6 | 2 | 16 | 0.0% |
| 近6 | 6 | 0 | 2 | 4 | 2 | 9 | -7 | 2 | 0.0% |
相同盘路亚让
| [**纽卡斯尔喷气机**](//zq.titan007.com/cn/team/Summary/2915.html) |
| 初盘:受让半球 | 赢 | 走 | 输 | 赢盘率 |
| 总 | 52 | 0 | 51 | 50.5% |
| 主 | 17 | 0 | 14 | 54.8% |
| 近6场盘路走势: 赢 赢 赢 输 赢 输 |
| [**大阪钢巴**](//zq.titan007.com/cn/team/Summary/207.html) |
| 初盘:受让半球 | 赢 | 走 | 输 | 赢盘率 |
| 总 | 93 | 0 | 77 | 54.7% |
| 客 | 37 | 0 | 30 | 55.2% |
| 近6场盘路走势: 输 输 输 赢 输 赢 |
进球时间
|  | 1-10 | 11-20 | 21-30 | 31-40 | 41-45 | 46-50 | 51-60 | 61-70 | 71-80 | 81-90+ |
| 总 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
|  | 1-10 | 11-20 | 21-30 | 31-40 | 41-45 | 46-50 | 51-60 | 61-70 | 71-80 | 81-90+ |
| 总 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 2 |
未来五场
| [**纽卡斯尔喷气机**](//zq.titan007.com/cn/team/Summary/2915.html) |
| 10-17 | 澳超 | 中央海岸水手 - 纽卡斯尔喷气机 | 4 天 |
| [**大阪钢巴**](//zq.titan007.com/cn/team/Summary/207.html) |
| 10-17 | 日职联 | 清水鼓动 - 大阪钢巴 | 4 天 |
阵容情况
| [**纽卡斯尔喷气机**](//zq.titan007.com/cn/team/Summary/2915.html) |
| [2 (中卫) 艾利克斯·格兰特](url) | 未知的损伤 |
| [25 (左边锋) 奥斯卡·弗莱尔](url) | 十字韧带撕裂 |
| [**大阪钢巴**](//zq.titan007.com/cn/team/Summary/207.html) |
| [5 (中卫) 三浦弦太](url) | 膝关节损伤 |
| 球员上一场出场评分 |
| 主队近10场平均评分: * 5.94 * 7.11 * 6.68  客队近10场平均评分: * 6.17 * 6.57 * 7.24 |
"""
        parsed = Titan007RawParser().parse_analysis_html(sample_analysis_md, "纽卡斯尔喷气机", "大阪钢巴")
        self.assertIn("亨特国际体育中心", parsed["venueWeather"])
        self.assertIn("艾利克斯·格兰特", parsed["injuries"]["home"])
        self.assertIn("三浦弦太", parsed["injuries"]["away"])
        self.assertIn("15胜3平8负", parsed["homeStats"])
        self.assertIn("1胜3平5负", parsed["awayStats"])
        self.assertIn("50.5%", parsed["profiling"])
        self.assertIn("4 天", parsed["scheduleTrap"])

    def test_verifier_blocks_sporttery_jcodds_disguised_as_crown_correct_score(self):
        """漏洞5红灯测试: 当 .md 第5节 Crown 波胆赔率与 raw/odds.html 不一致 (如用体彩 jcOdds 1:1=9.30 冒充皇冠 1:1=8.60) 时，必须触发 RAW_PROVENANCE_MISMATCH"""
        import hashlib
        fake_md = (
            "# 【周二001】亚冠精英 纽卡斯尔喷气机 vs 大阪钢巴\n"
            "- **比赛 ID**：3068865\n"
            "## 五、Crown 皇冠全指数波胆与比分矩阵\n"
            "- **波胆比分赔率**：1:0 (20.00) ｜ 0:0 (28.00) ｜ 1:1 (9.30)\n"
        )
        md_sha = hashlib.sha256(fake_md.encode("utf-8")).hexdigest()
        raw_odds_html = (
            '<table><tr class="bui"><td><b>波胆</b></td><td>1:0</td><td>0:0</td><td>1:1</td></tr>'
            '<tr class="odds"><td>主</td><td>20</td><td rowspan="2">28</td><td rowspan="2">8.6</td></tr>'
            '<tr class="odds"><td>客</td><td>12</td></tr></table>'
        )
        snap = {
            "matchId": "3068865",
            "match": {"league": "亚冠精英", "homeTeam": "纽卡斯尔喷气机", "awayTeam": "大阪钢巴"},
            "_raw_content": fake_md,
            "_markdown_sha256": md_sha,
            "correctScore": {"1:0": 20.0, "0:0": 28.0, "1:1": 9.3},
            "_raw_wire": {
                "manifest": {"matchId": "3068865", "markdown_sha256": md_sha},
                "files": {"odds.html": raw_odds_html},
            },
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("RAW_PROVENANCE_MISMATCH", res.message)

    def test_authenticity_passes_when_valid_receipt_present(self):
        """TDD U2: 当 raw_wire 包含合法 receipt 时，真实性核验必须正常 PASS"""
        import hashlib
        fake_md = "# 【周二001】亚冠精英 纽卡斯尔喷气机 vs 大阪钢巴\n- **比赛 ID**：3068865\n"
        md_sha = hashlib.sha256(fake_md.encode("utf-8")).hexdigest()
        raw_1x2_js = 'var hometeam_cn="纽卡斯尔喷气机";var guestteam_cn="大阪钢巴";var game=Array();'
        fsha = hashlib.sha256(raw_1x2_js.encode("utf-8")).hexdigest()
        receipt = {
            "fetcher": "scrapling-mcp",
            "matchId": "3068865",
            "fetchedAt": "2026-10-13T16:00:00+08:00",
            "endpoints": [
                {
                    "file": "1x2d.js",
                    "url": "https://1x2d.titan007.com/3068865.js",
                    "status": 200,
                    "payload_sha256": fsha,
                }
            ],
        }
        snap = {
            "matchId": "3068865",
            "match": {"league": "亚冠精英", "homeTeam": "纽卡斯尔喷气机", "awayTeam": "大阪钢巴"},
            "_raw_content": fake_md,
            "_markdown_sha256": md_sha,
            "_raw_wire": {
                "manifest": {"matchId": "3068865", "markdown_sha256": md_sha, "raw_files_sha256": {"1x2d.js": fsha}},
                "files": {"1x2d.js": raw_1x2_js},
                "receipt": receipt,
            },
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.PASS)

    def test_authenticity_fails_when_receipt_payload_hash_mismatches(self):
        """TDD U2: 当 receipt 记录的 payload_sha256 与实际 raw_wire 报文哈希不符时，必须判定 FAIL (RECEIPT_PAYLOAD_MISMATCH)"""
        import hashlib
        fake_md = "# 【周二001】亚冠精英 纽卡斯尔喷气机 vs 大阪钢巴\n- **比赛 ID**：3068865\n"
        md_sha = hashlib.sha256(fake_md.encode("utf-8")).hexdigest()
        raw_1x2_js = 'var hometeam_cn="纽卡斯尔喷气机";var guestteam_cn="大阪钢巴";var game=Array();'
        fsha = hashlib.sha256(raw_1x2_js.encode("utf-8")).hexdigest()
        tampered_receipt = {
            "fetcher": "scrapling-mcp",
            "matchId": "3068865",
            "fetchedAt": "2026-10-13T16:00:00+08:00",
            "endpoints": [
                {
                    "file": "1x2d.js",
                    "url": "https://1x2d.titan007.com/3068865.js",
                    "status": 200,
                    "payload_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
                }
            ],
        }
        snap = {
            "matchId": "3068865",
            "match": {"league": "亚冠精英", "homeTeam": "纽卡斯尔喷气机", "awayTeam": "大阪钢巴"},
            "_raw_content": fake_md,
            "_markdown_sha256": md_sha,
            "_raw_wire": {
                "manifest": {"matchId": "3068865", "markdown_sha256": md_sha, "raw_files_sha256": {"1x2d.js": fsha}},
                "files": {"1x2d.js": raw_1x2_js},
                "receipt": tampered_receipt,
            },
        }
        res = self.verifier._check_authenticity(snap)
        self.assertEqual(res.status, CheckStatus.FAIL)
        self.assertIn("RECEIPT_PAYLOAD_MISMATCH", res.message)


if __name__ == "__main__":
    unittest.main()





