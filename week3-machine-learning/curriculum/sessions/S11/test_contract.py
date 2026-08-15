"""Contract tests for S11."""

import unittest
from unittest.mock import patch

import numpy as np

from starter import gaussian_conditional, gaussian_marginal


RTOL = 1e-7
ATOL = 1e-12


def reference_conditional(
    mean: np.ndarray,
    covariance: np.ndarray,
    target_indices: np.ndarray,
    observed_indices: np.ndarray,
    observed_values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Independent contract calculation using block solves."""
    mean_target = mean[target_indices]
    mean_observed = mean[observed_indices]
    covariance_tt = covariance[np.ix_(target_indices, target_indices)]
    covariance_to = covariance[np.ix_(target_indices, observed_indices)]
    covariance_ot = covariance[np.ix_(observed_indices, target_indices)]
    covariance_oo = covariance[np.ix_(observed_indices, observed_indices)]

    residual_observed = observed_values - mean_observed
    mean_solution = np.linalg.solve(covariance_oo, residual_observed)
    covariance_solution = np.linalg.solve(covariance_oo, covariance_ot)
    conditional_mean = mean_target + covariance_to @ mean_solution
    conditional_covariance = covariance_tt - covariance_to @ covariance_solution
    return conditional_mean, conditional_covariance


class S11Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.mean = np.array([1.0, 2.0], dtype=np.float64)
        self.covariance = np.array(
            [[4.0, 2.0], [2.0, 2.0]],
            dtype=np.float64,
        )
        self.target_indices = np.array([0], dtype=np.int64)
        self.observed_indices = np.array([1], dtype=np.int64)
        self.observed_values = np.array([4.0], dtype=np.float64)

    def test_marginal_preserves_matrix_shape(self) -> None:
        marginal_mean, marginal_covariance = gaussian_marginal(
            self.mean,
            self.covariance,
            self.target_indices,
        )
        self.assertEqual(marginal_mean.shape, (1,))
        self.assertEqual(marginal_covariance.shape, (1, 1))
        self.assertEqual(marginal_mean.dtype, np.float64)
        self.assertEqual(marginal_covariance.dtype, np.float64)
        np.testing.assert_allclose(
            marginal_mean,
            self.mean[self.target_indices],
            rtol=RTOL,
            atol=ATOL,
        )
        np.testing.assert_allclose(
            marginal_covariance,
            self.covariance[np.ix_(self.target_indices, self.target_indices)],
            rtol=RTOL,
            atol=ATOL,
        )

    def test_central_conditional(self) -> None:
        expected_mean, expected_covariance = reference_conditional(
            self.mean,
            self.covariance,
            self.target_indices,
            self.observed_indices,
            self.observed_values,
        )
        conditional_mean, conditional_covariance = gaussian_conditional(
            self.mean,
            self.covariance,
            self.target_indices,
            self.observed_indices,
            self.observed_values,
        )
        self.assertEqual(conditional_mean.shape, (1,))
        self.assertEqual(conditional_covariance.shape, (1, 1))
        self.assertEqual(conditional_mean.dtype, np.float64)
        self.assertEqual(conditional_covariance.dtype, np.float64)
        np.testing.assert_allclose(
            conditional_mean,
            expected_mean,
            rtol=RTOL,
            atol=ATOL,
        )
        np.testing.assert_allclose(
            conditional_covariance,
            expected_covariance,
            rtol=RTOL,
            atol=ATOL,
        )

    def test_generic_partition_and_index_order(self) -> None:
        mean = np.array([0.5, -1.0, 2.0, 3.0], dtype=np.float64)
        factor = np.array(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.2, 1.1, 0.0, 0.0],
                [-0.3, 0.4, 0.9, 0.0],
                [0.5, -0.2, 0.3, 1.2],
            ],
            dtype=np.float64,
        )
        covariance = factor @ factor.T + 0.5 * np.eye(4, dtype=np.float64)
        target_indices = np.array([3, 0], dtype=np.int64)
        observed_indices = np.array([2, 1], dtype=np.int64)
        observed_values = np.array([1.5, -0.25], dtype=np.float64)

        expected_mean, expected_covariance = reference_conditional(
            mean,
            covariance,
            target_indices,
            observed_indices,
            observed_values,
        )
        conditional_mean, conditional_covariance = gaussian_conditional(
            mean,
            covariance,
            target_indices,
            observed_indices,
            observed_values,
        )
        self.assertEqual(conditional_mean.shape, (2,))
        self.assertEqual(conditional_covariance.shape, (2, 2))
        np.testing.assert_allclose(
            conditional_mean,
            expected_mean,
            rtol=RTOL,
            atol=ATOL,
        )
        np.testing.assert_allclose(
            conditional_covariance,
            expected_covariance,
            rtol=RTOL,
            atol=ATOL,
        )

        marginal_mean, marginal_covariance = gaussian_marginal(
            mean,
            covariance,
            target_indices,
        )
        np.testing.assert_allclose(
            marginal_mean,
            mean[target_indices],
            rtol=RTOL,
            atol=ATOL,
        )
        np.testing.assert_allclose(
            marginal_covariance,
            covariance[np.ix_(target_indices, target_indices)],
            rtol=RTOL,
            atol=ATOL,
        )

    def test_conditional_does_not_build_explicit_inverse(self) -> None:
        expected_mean, expected_covariance = reference_conditional(
            self.mean,
            self.covariance,
            self.target_indices,
            self.observed_indices,
            self.observed_values,
        )
        with patch(
            "numpy.linalg.inv",
            side_effect=AssertionError("use solve, not an explicit inverse"),
        ):
            conditional_mean, conditional_covariance = gaussian_conditional(
                self.mean,
                self.covariance,
                self.target_indices,
                self.observed_indices,
                self.observed_values,
            )
        np.testing.assert_allclose(
            conditional_mean,
            expected_mean,
            rtol=RTOL,
            atol=ATOL,
        )
        np.testing.assert_allclose(
            conditional_covariance,
            expected_covariance,
            rtol=RTOL,
            atol=ATOL,
        )

    def test_conditional_covariance_is_independent_of_observed_value(self) -> None:
        _, covariance_a = gaussian_conditional(
            self.mean,
            self.covariance,
            self.target_indices,
            self.observed_indices,
            self.observed_values,
        )
        _, covariance_b = gaussian_conditional(
            self.mean,
            self.covariance,
            self.target_indices,
            self.observed_indices,
            np.array([-3.0], dtype=np.float64),
        )
        np.testing.assert_allclose(covariance_a, covariance_b, rtol=RTOL, atol=ATOL)


if __name__ == "__main__":
    unittest.main()
