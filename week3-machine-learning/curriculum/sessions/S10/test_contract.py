"""Contract tests for S10."""
import unittest
import numpy as np
from starter import mahalanobis_squared, multivariate_gaussian_logpdf
RTOL, ATOL = 1e-7, 1e-12

def reference_logpdf(observations: np.ndarray, mean: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    sign, logdet = np.linalg.slogdet(covariance)
    if sign <= 0: raise ValueError("covariance must have positive determinant")
    residuals = observations - mean
    solved = np.linalg.solve(covariance, residuals.T).T
    return -0.5 * (mean.size * np.log(2 * np.pi) + logdet + np.sum(residuals * solved, axis=1))

class S10Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.mean = np.array([0., 0.], dtype=np.float64)
        self.cov = np.array([[2., 1.], [1., 2.]], dtype=np.float64)
        self.obs = np.array([[1., 0.], [0., 2.]], dtype=np.float64)
    def test_mahalanobis_uses_linear_system_result(self) -> None:
        residual = self.obs[0] - self.mean
        expected = float(residual @ np.linalg.solve(self.cov, residual))
        result = mahalanobis_squared(self.obs[0], self.mean, self.cov)
        self.assertIs(type(result), float); self.assertTrue(np.isclose(result, expected, rtol=RTOL, atol=ATOL))
    def test_batched_logpdf(self) -> None:
        result = multivariate_gaussian_logpdf(self.obs, self.mean, self.cov)
        self.assertEqual(result.shape, (2,)); self.assertEqual(result.dtype, np.float64)
        np.testing.assert_allclose(result, reference_logpdf(self.obs, self.mean, self.cov), rtol=RTOL, atol=ATOL)
    def test_non_diagonal_covariance_matters(self) -> None:
        full = multivariate_gaussian_logpdf(self.obs, self.mean, self.cov)
        diagonal = multivariate_gaussian_logpdf(self.obs, self.mean, np.diag(np.diag(self.cov)))
        self.assertFalse(np.allclose(full, diagonal, rtol=RTOL, atol=ATOL))

    def test_other_spd_covariance_and_single_item_shape(self) -> None:
        covariance = np.array([[3.0, 0.5], [0.5, 1.5]], dtype=np.float64)
        observations = np.array([[2.0, -1.0]], dtype=np.float64)
        result = multivariate_gaussian_logpdf(observations, self.mean, covariance)
        self.assertEqual(result.shape, (1,))
        np.testing.assert_allclose(result, reference_logpdf(observations, self.mean, covariance), rtol=RTOL, atol=ATOL)

if __name__ == "__main__": unittest.main()
