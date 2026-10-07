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
import scripts.poisson_lib as old_lib
import io
import sys
import json


class TestPoissonDomain(unittest.TestCase):
    def setUp(self):
        self.params = PoissonParams.default()
        self.engine = PoissonEngine(params=self.params)

    def test_zero_drift_with_legacy_poisson_lib(self):
        """核心铁律：新领域模型与原 scripts/poisson_lib.py 算法输出必须 100% 零偏差 (误差 < 1e-10)"""
        old_params = old_lib.load_params("config/poisson_params.json")

        test_cases = [
            (1.20, 0.90),
            (1.50, 1.20),
            (2.10, 0.75),
            (0.80, 1.80),
            (1.35, 1.15),
            (2.80, 2.30),
            (0.50, 0.60),
        ]

        for l1, l2 in test_cases:
            # 旧算法计算
            old_scores = old_lib.score_probs(l1, l2, params=old_params, apply_low_score_factors=True)
            old_top6 = old_lib.format_top(old_scores, 6)

            # 新领域引擎计算
            new_result = self.engine.calculate(l1, l2, apply_low_score_factors=True)
            new_top6 = new_result.top_scores(6)

            self.assertEqual(len(old_top6), len(new_top6))
            for (old_score, old_prob), new_item in zip(old_top6, new_top6):
                self.assertEqual(old_score, new_item.score)
                # 浮点数零偏差断言 (< 1e-10)
                self.assertAlmostEqual(old_prob, new_item.probability, delta=1e-10,
                                       msg=f"比分 {old_score} 出现算法漂移失真！")

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


if __name__ == "__main__":
    unittest.main()
