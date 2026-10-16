import unittest

from qguard.metrics import (
    expectation_from_counts,
    bell_fidelity,
    fidelity_from_correlations,
)


class TestQGuardMetrics(unittest.TestCase):

    def test_zz_positive_correlation(self):
        counts = {
            "00": 500,
            "11": 500,
        }

        result = expectation_from_counts(counts, "ZZ")

        self.assertAlmostEqual(result, 1.0)

    def test_negative_correlation(self):
        counts = {
            "01": 500,
            "10": 500,
        }

        result = expectation_from_counts(counts, "XX")

        self.assertAlmostEqual(result, -1.0)

    def test_ideal_bell_fidelity(self):
        result = bell_fidelity(
            xx=1.0,
            yy=-1.0,
            zz=1.0,
        )

        self.assertAlmostEqual(result, 1.0)

    def test_zero_fidelity(self):
        result = bell_fidelity(
            xx=0.0,
            yy=0.0,
            zz=0.0,
        )

        self.assertAlmostEqual(result, 0.25)

    def test_fidelity_from_correlations(self):
        correlations = {
            "XX": 1.0,
            "YY": -1.0,
            "ZZ": 1.0,
        }

        result = fidelity_from_correlations(correlations)

        self.assertAlmostEqual(result, 1.0)

    def test_invalid_observable(self):
        with self.assertRaises(ValueError):
            expectation_from_counts(
                {"00": 100},
                "AB",
            )


if __name__ == "__main__":
    unittest.main()
