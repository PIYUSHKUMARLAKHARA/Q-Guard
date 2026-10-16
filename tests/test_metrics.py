"""Tests for quantum metrics, statistical uncertainty, and threshold decisions."""

import unittest
from qguard.metrics import (
    expectation_from_counts,
    observable_uncertainty,
    bell_fidelity,
    fidelity_uncertainty,
    fidelity_from_correlations,
    evaluate_threshold,
    filter_counts,
)


class TestMetrics(unittest.TestCase):

    def test_zz_correlation(self):
        counts = {"00": 500, "11": 500}
        self.assertAlmostEqual(expectation_from_counts(counts, "ZZ"), 1.0)

        counts_odd = {"01": 500, "10": 500}
        self.assertAlmostEqual(expectation_from_counts(counts_odd, "ZZ"), -1.0)

    def test_observable_uncertainty(self):
        # Pure correlation: <M> = 1.0 -> sigma_M = 0.0
        counts_pure = {"00": 1000}
        self.assertAlmostEqual(observable_uncertainty(counts_pure, "ZZ"), 0.0)

        # Equal split: <M> = 0.0, Var = 1.0 -> sigma_M = 1 / sqrt(1000)
        counts_split = {"00": 500, "01": 500}
        unc = observable_uncertainty(counts_split, "ZZ")
        self.assertGreater(unc, 0.0)
        self.assertAlmostEqual(unc, 1.0 / (1000 ** 0.5), places=4)

    def test_ideal_bell_fidelity(self):
        self.assertAlmostEqual(bell_fidelity(1.0, -1.0, 1.0), 1.0)

    def test_zero_correlations_fidelity(self):
        self.assertAlmostEqual(bell_fidelity(0.0, 0.0, 0.0), 0.25)

    def test_fidelity_clipping(self):
        self.assertEqual(bell_fidelity(2.0, -2.0, 2.0), 1.0)
        self.assertEqual(bell_fidelity(-2.0, 2.0, -2.0), 0.0)

    def test_fidelity_uncertainty(self):
        # sigma_F = 0.25 * sqrt(0.01^2 + 0.01^2 + 0.01^2)
        unc = fidelity_uncertainty(0.01, 0.01, 0.01)
        expected = 0.25 * ((3 * 0.01**2) ** 0.5)
        self.assertAlmostEqual(unc, expected)

    def test_evaluate_threshold(self):
        # High fidelity with small uncertainty -> passes
        res_pass = evaluate_threshold(fidelity=0.95, uncertainty=0.01, threshold=0.5)
        self.assertTrue(res_pass["passed"])
        self.assertGreater(res_pass["margin"], 0.0)

        # Low fidelity -> fails
        res_fail = evaluate_threshold(fidelity=0.51, uncertainty=0.02, threshold=0.5)
        self.assertFalse(res_fail["passed"])
        self.assertLess(res_fail["margin"], 0.0)

    def test_filter_counts_unprotected(self):
        counts = {"00": 300, "11": 700}
        acc_counts, acc, tot, rate = filter_counts(counts, protected=False)
        self.assertEqual(acc, 1000)
        self.assertEqual(tot, 1000)
        self.assertEqual(rate, 1.0)
        self.assertEqual(acc_counts, {"00": 300, "11": 700})

    def test_filter_counts_protected(self):
        # bitstring is c2c1c0 (ancilla is leftmost)
        counts = {"000": 400, "011": 400, "101": 100, "110": 100}
        acc_counts, acc, tot, rate = filter_counts(counts, protected=True)
        self.assertEqual(acc, 800)
        self.assertEqual(tot, 1000)
        self.assertAlmostEqual(rate, 0.8)
        self.assertEqual(acc_counts, {"00": 400, "11": 400})

    def test_filter_counts_zero_accepted(self):
        counts = {"100": 50, "111": 50}
        acc_counts, acc, tot, rate = filter_counts(counts, protected=True)
        self.assertEqual(acc, 0)
        self.assertEqual(tot, 100)
        self.assertEqual(rate, 0.0)
        self.assertEqual(acc_counts, {})

    def test_invalid_counts_raises(self):
        with self.assertRaises(ValueError):
            expectation_from_counts({}, "ZZ")
        with self.assertRaises(ValueError):
            filter_counts({"INVALID": 10}, protected=False)


if __name__ == "__main__":
    unittest.main()
