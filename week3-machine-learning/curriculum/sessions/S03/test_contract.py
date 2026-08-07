"""Verification tests for the contracts stated in S03 PROBLEM.md."""

import unittest

import numpy as np

from starter import sample_moments, theoretical_covariance, theoretical_moments


class TheoreticalMomentTests(unittest.TestCase):
    def test_weighted_moments_match_definition(self) -> None:
        values = np.array([-1.0, 1.0, 3.0], dtype=np.float64)
        probabilities = np.array([0.25, 0.50, 0.25], dtype=np.float64)
        mean, variance = theoretical_moments(values, probabilities)
        expected_mean = np.sum(values * probabilities)
        expected_variance = np.sum(probabilities * (values - expected_mean) ** 2)
        self.assertTrue(np.isclose(mean, expected_mean))
        self.assertTrue(np.isclose(variance, expected_variance))


class SampleMomentTests(unittest.TestCase):
    def test_uses_fixed_sample_and_n_minus_one_denominator(self) -> None:
        samples = np.array([-1.0, 1.0, 3.0, 3.0, 3.0], dtype=np.float64)
        mean, variance = sample_moments(samples)
        self.assertTrue(np.isclose(mean, np.mean(samples)))
        self.assertTrue(np.isclose(variance, np.var(samples, ddof=1)))


class CovarianceTests(unittest.TestCase):
    def test_weighted_covariance_matches_definition(self) -> None:
        x = np.array([-1.0, 1.0, 3.0], dtype=np.float64)
        y = np.array([2.0, 0.0, 4.0], dtype=np.float64)
        p = np.array([0.25, 0.50, 0.25], dtype=np.float64)
        result = theoretical_covariance(x, y, p)
        expected = np.sum(p * (x - np.sum(p * x)) * (y - np.sum(p * y)))
        self.assertTrue(np.isclose(result, expected))


if __name__ == "__main__":
    unittest.main()
