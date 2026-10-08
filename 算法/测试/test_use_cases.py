import unittest
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from 算法.src.application.use_cases import ConvertOddsUseCase, OddsConversionResult


class TestApplicationUseCases(unittest.TestCase):
    def setUp(self):
        self.use_case = ConvertOddsUseCase()

    def test_execute_standard_three_way(self):
        result = self.use_case.execute([2.10, 3.40, 3.55])
        self.assertIsInstance(result, OddsConversionResult)
        self.assertEqual(result.odds, (2.10, 3.40, 3.55))
        self.assertEqual(len(result.probabilities), 3)
        self.assertAlmostEqual(result.total_probability, 1.0, places=12)
        
        # Check percentage strings
        self.assertEqual(result.percentages, ('46.06%', '27.60%', '26.34%'))
        self.assertAlmostEqual(result.probabilities[0], 0.4605842498286713, places=10)
        self.assertEqual(result.algorithm, 'Goto-OO-EPC')

    def test_to_dict_serialization(self):
        result = self.use_case.execute([2.10, 3.40, 3.55])
        d = result.to_dict()
        self.assertIn('odds', d)
        self.assertIn('probabilities', d)
        self.assertIn('percentages', d)
        self.assertIn('booksum', d)
        self.assertIn('margin', d)
        self.assertIn('algorithm', d)
        self.assertEqual(d['algorithm'], 'Goto-OO-EPC')
        self.assertIn('prob_1x2', d)
        self.assertIn('home', d['prob_1x2'])
        self.assertIn('draw', d['prob_1x2'])
        self.assertIn('away', d['prob_1x2'])
        self.assertAlmostEqual(d['prob_1x2']['home'], 0.460584, places=5)
        self.assertIn('percentages_1x2', d)
        self.assertEqual(d['percentages_1x2']['home'], '46.06%')

    def test_two_way_does_not_have_prob_1x2(self):
        result = self.use_case.execute([1.90, 1.95])
        d = result.to_dict()
        self.assertNotIn('prob_1x2', d)
        self.assertNotIn('percentages_1x2', d)

    def test_unknown_strategy_raises_error(self):
        with self.assertRaises(ValueError):
            self.use_case.execute([2.10, 3.40, 3.55], strategy='unsupported_algo')


if __name__ == '__main__':
    unittest.main()
