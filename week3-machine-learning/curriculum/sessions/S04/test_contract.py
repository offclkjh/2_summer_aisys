"""Verification tests for the contracts stated in S04 PROBLEM.md."""

import math
import unittest

import numpy as np

from starter import cross_entropy, entropy, kl_divergence


def reference_entropy(probabilities: np.ndarray) -> float:
    """Compute base-2 entropy independently with scalar standard-library calls."""
    return math.fsum(
        -float(probability) * math.log2(float(probability))
        for probability in probabilities
    )


def reference_cross_entropy(p: np.ndarray, q: np.ndarray) -> float:
    """Compute base-2 cross-entropy independently from its scalar definition."""
    return math.fsum(
        -float(p_i) * math.log2(float(q_i))
        for p_i, q_i in zip(p, q, strict=True)
    )


def reference_kl(p: np.ndarray, q: np.ndarray) -> float:
    """Compute base-2 KL independently from its scalar definition."""
    return math.fsum(
        float(p_i) * math.log2(float(p_i) / float(q_i))
        for p_i, q_i in zip(p, q, strict=True)
    )


class InformationMeasureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.p = np.array([0.50, 0.25, 0.25], dtype=np.float64)
        self.q = np.array(
            [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0],
            dtype=np.float64,
        )

    def test_center_case_matches_definitions_and_returns_floats(self) -> None:
        entropy_result = entropy(self.p)
        cross_entropy_result = cross_entropy(self.p, self.q)
        kl_result = kl_divergence(self.p, self.q)

        self.assertIs(type(entropy_result), float)
        self.assertIs(type(cross_entropy_result), float)
        self.assertIs(type(kl_result), float)
        self.assertTrue(np.isclose(entropy_result, reference_entropy(self.p)))
        self.assertTrue(
            np.isclose(
                cross_entropy_result,
                reference_cross_entropy(self.p, self.q),
            )
        )
        self.assertTrue(np.isclose(kl_result, reference_kl(self.p, self.q)))

    def test_cross_entropy_decomposes_into_entropy_and_kl(self) -> None:
        self.assertTrue(
            np.isclose(
                cross_entropy(self.p, self.q),
                entropy(self.p) + kl_divergence(self.p, self.q),
            )
        )

    def test_matching_distributions_have_zero_kl(self) -> None:
        self.assertTrue(np.isclose(kl_divergence(self.p, self.p), 0.0))


class GeneralValidInputTests(unittest.TestCase):
    def test_four_category_nonuniform_inputs_match_definitions(self) -> None:
        p = np.array([0.10, 0.20, 0.30, 0.40], dtype=np.float64)
        q = np.array([0.40, 0.30, 0.20, 0.10], dtype=np.float64)

        self.assertTrue(np.isclose(entropy(p), reference_entropy(p)))
        self.assertTrue(
            np.isclose(cross_entropy(p, q), reference_cross_entropy(p, q))
        )
        self.assertTrue(np.isclose(kl_divergence(p, q), reference_kl(p, q)))

    def test_kl_direction_follows_the_first_argument_weights(self) -> None:
        p = np.array([0.60, 0.25, 0.15], dtype=np.float64)
        q = np.array([0.20, 0.30, 0.50], dtype=np.float64)

        forward = kl_divergence(p, q)
        reverse = kl_divergence(q, p)
        self.assertTrue(np.isclose(forward, reference_kl(p, q)))
        self.assertTrue(np.isclose(reverse, reference_kl(q, p)))
        self.assertFalse(np.isclose(forward, reverse))


if __name__ == "__main__":
    unittest.main()
