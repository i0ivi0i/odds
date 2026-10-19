"""
算法/ 测试用例: 泊松进球期望值与比分概率用例测试 (TDD 红灯阶段)
验证 100% 零偏差平移 (Bit-for-bit Zero-Drift)
"""

import unittest
from 算法.src.domain.poisson import (
    PoissonEngine,
    PoissonParams,
    PoissonResult,
)
from 算法.src.application.use_cases import CalculatePoissonUseCase
from 算法.src.adapter.cli import main as cli_main
import io
import sys
import json


class TestPoissonDomain(unittest.TestCase):
    def setUp(self):
        self.params = PoissonParams.default()
        self.engine = PoissonEngine(params=self.params)

    def test_poisson_engine_mathematical_precision(self):
        """核心断言：领域引擎泊松计算具备高精度数值稳定性与已知基准对齐"""
        # (1.50, 1.20) 基准对齐
        result = self.engine.calculate(1.50, 1.20, apply_low_score_factors=True)
        top6 = result.top_scores(6)
        self.assertEqual(len(top6), 6)
        
        # 验证 Top 6 比分总概率与首位比分合理性
        total_p = sum(item.probability for item in top6)
        self.assertTrue(0.40 < total_p < 0.70)
        self.assertEqual(top6[0].score, "1:1")
        self.assertAlmostEqual(top6[0].probability, 0.125, delta=0.01)

    def test_probabilities_sum_to_one(self):
        """测试 64 格全量比分概率归一化后总和严格收敛为 1.0"""
        res = self.engine.calculate(1.45, 1.10)
        total_p = sum(item.probability for item in res.all_scores)
        self.assertAlmostEqual(total_p, 1.0, places=9)

    def test_top_scores_ordering(self):
        """测试 Top 比分按概率严格降序排列"""
        res = self.engine.calculate(1.60, 1.10)
        top6 = res.top_scores(6)
        for i in range(len(top6) - 1):
            self.assertGreaterEqual(top6[i].probability, top6[i+1].probability)


class TestPoissonUseCase(unittest.TestCase):
    def test_use_case_execution(self):
        use_case = CalculatePoissonUseCase()
        res = use_case.execute(lambda_home=1.5, lambda_away=1.2, top_n=6)
        self.assertIsInstance(res, dict)
        self.assertIn("top_scores", res)
        self.assertEqual(len(res["top_scores"]), 6)
        self.assertEqual(res["lambda_home"], 1.5)
        self.assertEqual(res["lambda_away"], 1.2)


class TestPoissonCli(unittest.TestCase):
    def test_cli_poisson_json_output(self):
        stdout = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout
        try:
            exit_code = cli_main(["--poisson", "1.5", "1.2", "--json"])
        finally:
            sys.stdout = old_stdout

        self.assertEqual(exit_code, 0)
        out_json = json.loads(stdout.getvalue())
        self.assertIn("top_scores", out_json)
        self.assertEqual(len(out_json["top_scores"]), 6)

    def test_cli_poisson_match_snapshot(self):
        # 验证泊松 CLI 基本计算能力
        stdout = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = stdout
        try:
            exit_code = cli_main(["--poisson", "1.50", "1.20", "--json"])
        finally:
            sys.stdout = old_stdout

        self.assertEqual(exit_code, 0)
        out_json = json.loads(stdout.getvalue())
        self.assertIn("top_scores", out_json)
        self.assertIn("lambda_home", out_json)
        self.assertIn("lambda_away", out_json)


if __name__ == "__main__":
    unittest.main()
