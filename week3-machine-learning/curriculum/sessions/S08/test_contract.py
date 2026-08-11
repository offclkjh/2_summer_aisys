"""Contract tests for S08."""
import math
import unittest
import numpy as np
from starter import gaussian_logpdf, gaussian_mean_mle, gaussian_nll, gaussian_variance_mle, squared_error_sum
RTOL, ATOL = 1e-7, 1e-12

class S08Tests(unittest.TestCase):
    def setUp(self) -> None: self.data = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    def test_logpdf_and_nll(self) -> None:
        expected = -0.5 * (np.log(2 * np.pi * 2.0) + (self.data - 1.5) ** 2 / 2.0)
        result_array = gaussian_logpdf(self.data, 1.5, 2.0)
        self.assertEqual(result_array.shape, self.data.shape); self.assertEqual(result_array.dtype, np.float64)
        np.testing.assert_allclose(result_array, expected, rtol=RTOL, atol=ATOL)
        result = gaussian_nll(self.data, 1.5, 2.0)
        self.assertIs(type(result), float); self.assertTrue(math.isclose(result, float(-expected.sum()), rel_tol=RTOL, abs_tol=ATOL))
    def test_sse_and_mles(self) -> None:
        self.assertTrue(math.isclose(squared_error_sum(self.data, 1.5), float(np.sum((self.data - 1.5) ** 2)), rel_tol=RTOL, abs_tol=ATOL))
        mean = gaussian_mean_mle(self.data)
        self.assertIs(type(mean), float); self.assertTrue(math.isclose(mean, 2.0, rel_tol=RTOL, abs_tol=ATOL))
        variance = gaussian_variance_mle(self.data, mean)
        self.assertIs(type(variance), float); self.assertTrue(math.isclose(variance, float(np.var(self.data, ddof=0)), rel_tol=RTOL, abs_tol=ATOL))
    def test_fixed_variance_nll_difference_tracks_sse(self) -> None:
        a, b, v = 1.0, 2.0, 1.5
        lhs = gaussian_nll(self.data, a, v) - gaussian_nll(self.data, b, v)
        rhs = (squared_error_sum(self.data, a) - squared_error_sum(self.data, b)) / (2 * v)
        self.assertTrue(math.isclose(lhs, rhs, rel_tol=RTOL, abs_tol=ATOL))

    def test_shifted_valid_data(self) -> None:
        shifted = self.data + 10.0
        self.assertTrue(math.isclose(gaussian_mean_mle(shifted), 12.0, rel_tol=RTOL, abs_tol=ATOL))
        self.assertTrue(math.isclose(gaussian_variance_mle(shifted, 12.0), gaussian_variance_mle(self.data, 2.0), rel_tol=RTOL, abs_tol=ATOL))

if __name__ == "__main__": unittest.main()
