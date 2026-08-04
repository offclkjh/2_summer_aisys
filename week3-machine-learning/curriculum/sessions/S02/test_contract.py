"""Verification tests for the contracts stated in S02 PROBLEM.md."""

import unittest

import numpy as np

from starter import compute_alarm_posterior, compute_marginals, normalize_joint


class JointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.counts = np.array([[72, 8], [6, 14]], dtype=np.int64)

    def test_normalized_joint_has_documented_structure(self) -> None:
        joint = normalize_joint(self.counts)
        self.assertEqual(joint.shape, (2, 2))
        self.assertEqual(joint.dtype, np.dtype("float64"))
        self.assertTrue(np.isclose(joint.sum(), 1.0))

    def test_normalization_preserves_cell_proportions(self) -> None:
        joint = normalize_joint(self.counts)
        np.testing.assert_allclose(joint * self.counts.sum(), self.counts)


class MarginalTests(unittest.TestCase):
    def setUp(self) -> None:
        counts = np.array([[72, 8], [6, 14]], dtype=np.int64)
        self.joint = counts / counts.sum()

    def test_returns_two_length_two_vectors(self) -> None:
        p_a, p_y = compute_marginals(self.joint)
        self.assertEqual(p_a.shape, (2,))
        self.assertEqual(p_y.shape, (2,))

    def test_alarm_marginal_matches_rows(self) -> None:
        p_a, _ = compute_marginals(self.joint)
        np.testing.assert_allclose(p_a, np.array([0.8, 0.2]))

    def test_detector_marginal_matches_columns(self) -> None:
        _, p_y = compute_marginals(self.joint)
        np.testing.assert_allclose(p_y, np.array([0.78, 0.22]))


class PosteriorTests(unittest.TestCase):
    def setUp(self) -> None:
        counts = np.array([[72, 8], [6, 14]], dtype=np.int64)
        self.joint = counts / counts.sum()

    def test_direct_and_bayes_results_agree(self) -> None:
        direct, bayes = compute_alarm_posterior(self.joint)
        self.assertTrue(np.isclose(direct, bayes))

    def test_posterior_matches_joint_definition(self) -> None:
        direct, _ = compute_alarm_posterior(self.joint)
        self.assertTrue(np.isclose(direct, 14 / 22))


if __name__ == "__main__":
    unittest.main()
