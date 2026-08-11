"""Contract tests for S06."""
import math
import unittest
import numpy as np
from starter import categorical_likelihood, categorical_mle, counts_from_labels, multinomial_pmf, one_hot
RTOL, ATOL = 1e-7, 1e-12

class S06Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.labels = np.array([0, 2, 1, 2, 2], dtype=np.int64)
        self.theta = np.array([0.2, 0.3, 0.5], dtype=np.float64)

    def test_one_hot_contract(self) -> None:
        result = one_hot(self.labels, 3)
        expected = np.eye(3, dtype=np.float64)[self.labels]
        self.assertEqual(result.shape, (5, 3)); self.assertEqual(result.dtype, np.float64)
        np.testing.assert_array_equal(result, expected)

    def test_counts_contract(self) -> None:
        result = counts_from_labels(self.labels, 3)
        self.assertEqual(result.dtype, np.int64)
        np.testing.assert_array_equal(result, np.array([1, 1, 3], dtype=np.int64))

    def test_likelihoods_and_mle(self) -> None:
        counts = np.array([1, 1, 3], dtype=np.int64)
        seq = categorical_likelihood(self.labels, self.theta)
        multi = multinomial_pmf(counts, self.theta)
        coefficient = math.factorial(5) // math.prod(math.factorial(int(c)) for c in counts)
        self.assertIs(type(seq), float); self.assertIs(type(multi), float)
        self.assertTrue(math.isclose(seq, math.prod(float(self.theta[i]) for i in self.labels), rel_tol=RTOL, abs_tol=ATOL))
        self.assertTrue(math.isclose(multi, coefficient * seq, rel_tol=RTOL, abs_tol=ATOL))
        result = categorical_mle(counts)
        self.assertEqual(result.shape, (3,)); self.assertEqual(result.dtype, np.float64)
        np.testing.assert_allclose(result, counts / counts.sum(), rtol=RTOL, atol=ATOL)

    def test_other_valid_labels_prevent_center_case_hard_coding(self) -> None:
        labels = np.array([2, 2, 1, 0, 1], dtype=np.int64)
        theta = np.array([0.4, 0.35, 0.25], dtype=np.float64)
        counts = counts_from_labels(labels, 3)
        np.testing.assert_array_equal(counts, [1, 2, 2])
        self.assertTrue(math.isclose(categorical_likelihood(labels, theta), math.prod(float(theta[i]) for i in labels), rel_tol=RTOL, abs_tol=ATOL))

if __name__ == "__main__": unittest.main()
