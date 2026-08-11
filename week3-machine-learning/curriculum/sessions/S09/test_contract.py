"""Contract tests for S09."""
import unittest
import numpy as np
from starter import center_data, covariance_matrix_mle, outer_product, transform_covariance
RTOL, ATOL = 1e-7, 1e-12

class S09Tests(unittest.TestCase):
    def setUp(self) -> None: self.data = np.array([[1., 1.], [2., 3.], [3., 2.]], dtype=np.float64)
    def test_center_and_outer(self) -> None:
        mean, centered = center_data(self.data)
        np.testing.assert_allclose(mean, self.data.mean(axis=0), rtol=RTOL, atol=ATOL); np.testing.assert_allclose(centered, self.data - mean, rtol=RTOL, atol=ATOL)
        np.testing.assert_allclose(outer_product(centered[0]), np.outer(centered[0], centered[0]), rtol=RTOL, atol=ATOL)
    def test_covariance_matrix(self) -> None:
        centered = self.data - self.data.mean(axis=0)
        expected = centered.T @ centered / self.data.shape[0]
        result = covariance_matrix_mle(self.data)
        self.assertEqual(result.shape, (2, 2)); self.assertEqual(result.dtype, np.float64)
        np.testing.assert_allclose(result, expected, rtol=RTOL, atol=ATOL); np.testing.assert_allclose(result, result.T, rtol=RTOL, atol=ATOL)
    def test_linear_transform(self) -> None:
        covariance = covariance_matrix_mle(self.data); matrix = np.array([[1., 1.]], dtype=np.float64)
        result = transform_covariance(matrix, covariance)
        self.assertEqual(result.shape, (1, 1)); np.testing.assert_allclose(result, matrix @ covariance @ matrix.T, rtol=RTOL, atol=ATOL)

    def test_other_valid_shape(self) -> None:
        data = np.array([[0., 1., 2.], [2., 1., 0.], [1., 3., 2.], [3., 0., 1.]], dtype=np.float64)
        centered = data - data.mean(axis=0)
        np.testing.assert_allclose(covariance_matrix_mle(data), centered.T @ centered / 4, rtol=RTOL, atol=ATOL)

if __name__ == "__main__": unittest.main()
