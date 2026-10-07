import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from 算法.src.domain.model import OddsVector
from 算法.src.domain.calculator import OoEpcCalculator
from 算法.src.application.use_cases import ConvertOddsUseCase


class TestAcademicBenchmarks(unittest.TestCase):
    """学术论文与实战赔率基准测试集 (Goto 2026 官方标准)"""

    def setUp(self):
        self.use_case = ConvertOddsUseCase()

    def _official_goto_reference(self, listOfOdds, total=1.0):
        """Kaito Goto (2026) 官方开源包原生代码基准参照物"""
        listOfProbabilities = [1.0 / x for x in listOfOdds]
        listOfSe = [pow((x - x ** 2.0) / x, 0.5) for x in listOfProbabilities]
        step = (sum(listOfProbabilities) - total) / sum(listOfSe)
        outputListOfProbabilities = [x - (y * step) for x, y in zip(listOfProbabilities, listOfSe)]
        if any(0.0 >= x for x in outputListOfProbabilities) or (sum(listOfProbabilities) <= 1.0):
            normalizer = sum(listOfProbabilities) / total
            outputListOfProbabilities = [x / normalizer for x in listOfProbabilities]
        return outputListOfProbabilities

    def test_bit_for_bit_identity_against_official_wheel(self):
        """对比官方 Wheel 原版函数，确保浮点精度 100% 完全相同"""
        test_cases = [
            [2.10, 3.40, 3.55],
            [1.80, 3.50, 4.20],
            [1.25, 6.00, 11.00],
            [1.95, 1.95],
            [1.85, 2.05],
            [2.80, 3.10, 2.65],
            [1.08, 10.50, 26.00],
        ]
        for odds in test_cases:
            expected = self._official_goto_reference(odds)
            res = self.use_case.execute(odds)
            for p_actual, p_exp in zip(res.probabilities, expected):
                self.assertAlmostEqual(p_actual, p_exp, places=12,
                                       msg=f"赔率 {odds} 在计算中出现偏差: actual={p_actual}, expected={p_exp}")
            self.assertAlmostEqual(res.total_probability, 1.0, places=12)

    def test_historical_match_kazakhstan(self):
        """周二003 哈萨克斯坦欧指 威廉希尔真实赔率 12.00 / 5.50 / 1.25"""
        res = self.use_case.execute([12.00, 5.50, 1.25])
        # 验证真实去水主胜、平局、客胜
        # 倒数: 0.0833, 0.1818, 0.8000 -> booksum = 1.0651
        self.assertAlmostEqual(res.total_probability, 1.0, places=12)
        # 客胜在 78.74%, 平局在 15.63%, 主胜在 5.63%
        self.assertTrue(0.77 < res.probabilities[2] < 0.80)
        self.assertTrue(0.14 < res.probabilities[1] < 0.17)
        self.assertTrue(0.05 < res.probabilities[0] < 0.07)

    def test_extreme_heavy_favorite(self):
        """极端深盘测试: 1.02 / 18.00 / 50.00"""
        res = self.use_case.execute([1.02, 18.00, 50.00])
        self.assertAlmostEqual(res.total_probability, 1.0, places=12)
        for p in res.probabilities:
            self.assertGreater(p, 0.0)
            self.assertLess(p, 1.0)

    def test_two_way_handicap_over_under(self):
        """两项盘测试 (大小球/亚盘): 1.90 / 1.90"""
        res = self.use_case.execute([1.90, 1.90])
        self.assertAlmostEqual(res.probabilities[0], 0.50, places=12)
        self.assertAlmostEqual(res.probabilities[1], 0.50, places=12)
        self.assertEqual(res.percentages, ("50.00%", "50.00%"))


if __name__ == '__main__':
    unittest.main()
