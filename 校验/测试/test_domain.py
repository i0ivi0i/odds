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
                "半球 0.94 0.86 10-07 21:33\n"
                "半球 1.00 0.90 10-07 21:30\n"
                "半球 0.98 0.88 10-07 21:29\n"
                "半球 0.96 0.87 10-07 21:28\n"
                "半球 0.97 0.92 10-07 21:21\n"
                "半球 0.99 0.91 10-07 21:16\n"
                "半球 0.92 0.86 10-07 20:48\n"
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
        good_snapshot["markets"] = {
            "europeCompanies": [
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
        }
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
        full_snapshot["markets"] = {
            "halfTime": {
                "crown": {"ahInitial": "平/半 0.85", "ahLatest": "半球 1.02", "ouInitial": "1 0.90", "ouLatest": "1 0.88"},
                "macau": {"ahInitial": "平/半 0.82", "ahLatest": "平/半 0.95", "ouInitial": "1 0.85", "ouLatest": "1 0.92"},
            }
        }
        receipt = self.verifier.verify(full_snapshot)
        self.assertTrue(receipt.is_valid)
        self.assertEqual(receipt.overall_status, CheckStatus.PASS)
        self.assertEqual(receipt.failed_count, 0)
        self.assertTrue(receipt.metadata.get("has_dual_track"))


if __name__ == "__main__":
    unittest.main()
