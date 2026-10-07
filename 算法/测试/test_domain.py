import unittest
import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from 算法.src.domain.model import OddsVector, ImpliedProbabilities
from 算法.src.domain.calculator import OoEpcCalculator


class TestDomainOddsVector(unittest.TestCase):
    def test_valid_odds_vector(self):
        vec = OddsVector([2.10, 3.40, 3.55])
        self.assertEqual(len(vec.odds), 3)
        self.assertAlmostEqual(vec.odds[0], 2.10)
        self.assertAlmostEqual(vec.odds[1], 3.40)
        self.assertAlmostEqual(vec.odds[2], 3.55)
        # Check inverse probabilities
        self.assertAlmostEqual(vec.inverse_probs[0], 1.0 / 2.10)
        self.assertAlmostEqual(vec.booksum, sum(1.0 / x for x in [2.10, 3.40, 3.55]))

    def test_invalid_odds_length(self):
        with self.assertRaises(ValueError):
            OddsVector([2.10])
        with self.assertRaises(ValueError):
            OddsVector([])

    def test_invalid_odds_values(self):
        with self.assertRaises(ValueError):
            OddsVector([2.10, 0.95, 3.55])
        with self.assertRaises(ValueError):
            OddsVector([2.10, 0.0, 3.55])
        with self.assertRaises(ValueError):
            OddsVector([2.10, -1.5, 3.55])

    def test_immutable_odds(self):
        vec = OddsVector([2.10, 3.40, 3.55])
        with self.assertRaises(TypeError):
            vec.odds[0] = 2.50


class TestDomainOoEpcCalculator(unittest.TestCase):
    def test_three_way_calculation(self):
        vec = OddsVector([2.10, 3.40, 3.55])
        implied = OoEpcCalculator.calculate(vec)
        self.assertIsInstance(implied, ImpliedProbabilities)
        self.assertEqual(len(implied.probabilities), 3)
        # Sum must be 1.0
        self.assertAlmostEqual(implied.total, 1.0, places=12)
        # Precise benchmark values from Goto (2026)
        self.assertAlmostEqual(implied.probabilities[0], 0.4605842498286713, places=10)
        self.assertAlmostEqual(implied.probabilities[1], 0.2760010189659046, places=10)
        self.assertAlmostEqual(implied.probabilities[2], 0.2634147312054241, places=10)

    def test_two_way_calculation(self):
        vec = OddsVector([1.95, 1.95])
        implied = OoEpcCalculator.calculate(vec)
        self.assertEqual(len(implied.probabilities), 2)
        self.assertAlmostEqual(implied.total, 1.0, places=12)
        self.assertAlmostEqual(implied.probabilities[0], 0.5, places=10)
        self.assertAlmostEqual(implied.probabilities[1], 0.5, places=10)

    def test_fallback_when_no_margin(self):
        # Odds with no bookmaker margin (1/2 + 1/2 = 1.0)
        vec = OddsVector([2.0, 2.0])
        implied = OoEpcCalculator.calculate(vec)
        self.assertAlmostEqual(implied.probabilities[0], 0.5, places=10)
        self.assertAlmostEqual(implied.probabilities[1], 0.5, places=10)


if __name__ == '__main__':
    unittest.main()
