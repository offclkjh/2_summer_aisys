"""Verification tests for the contracts stated in S05 PROBLEM.md."""

import math
import unittest

import numpy as np

from starter import (
    bernoulli_likelihood,
    bernoulli_log_likelihood,
    bernoulli_mle,
    bernoulli_pmf,
    binomial_pmf,
)


def reference_sequence_likelihood(data: np.ndarray, theta: float) -> float:
    return math.prod(
        theta if int(observation) == 1 else 1.0 - theta
        for observation in data
    )


class BernoulliTests(unittest.TestCase):
    def test_pmf_for_both_outcomes(self) -> None:
        theta = 0.37
        self.assertIs(type(bernoulli_pmf(0, theta)), float)
        self.assertIs(type(bernoulli_pmf(1, theta)), float)
        self.assertTrue(math.isclose(bernoulli_pmf(0, theta), 1.0 - theta))
        self.assertTrue(math.isclose(bernoulli_pmf(1, theta), theta))

    def test_sequence_likelihood_matches_product_definition(self) -> None:
        data = np.array([1, 0, 1, 1, 0], dtype=np.int64)
        theta = 0.4
        expected = reference_sequence_likelihood(data, theta)
        result = bernoulli_likelihood(data, theta)
        self.assertIs(type(result), float)
        self.assertTrue(math.isclose(result, expected))

    def test_log_likelihood_is_natural_log_of_likelihood(self) -> None:
        data = np.array([0, 1, 0, 0, 1, 1, 0], dtype=np.int64)
        theta = 0.28
        likelihood = reference_sequence_likelihood(data, theta)
        result = bernoulli_log_likelihood(data, theta)
        self.assertIs(type(result), float)
        self.assertTrue(math.isclose(result, math.log(likelihood)))


class BinomialAndMleTests(unittest.TestCase):
    def test_binomial_pmf_adds_the_number_of_matching_sequences(self) -> None:
        data = np.array([1, 0, 1, 1, 0], dtype=np.int64)
        theta = 0.4
        k = int(data.sum())
        sequence_probability = reference_sequence_likelihood(data, theta)
        expected = math.comb(data.size, k) * sequence_probability
        result = binomial_pmf(k, data.size, theta)
        self.assertIs(type(result), float)
        self.assertTrue(math.isclose(result, expected))

    def test_mle_is_sample_success_fraction_for_other_valid_data(self) -> None:
        data = np.array([0, 1, 1, 0, 1, 0, 0, 0], dtype=np.int64)
        result = bernoulli_mle(data)
        self.assertIs(type(result), float)
        self.assertTrue(math.isclose(result, float(data.mean())))


if __name__ == "__main__":
    unittest.main()
