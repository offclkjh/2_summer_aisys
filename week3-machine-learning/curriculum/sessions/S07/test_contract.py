"""Contract tests for S07."""
import unittest
import numpy as np
from starter import class_priors, conditional_probabilities, log_joint_scores, predict_class
RTOL, ATOL = 1e-7, 1e-12

class S07Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.fc = np.array([[3, 1, 0], [1, 4, 0]], dtype=np.int64)

    def test_priors_and_unsmoothed_conditionals(self) -> None:
        np.testing.assert_allclose(class_priors(self.fc), [4 / 9, 5 / 9], rtol=RTOL, atol=ATOL)
        np.testing.assert_allclose(conditional_probabilities(self.fc, 0.0), self.fc / np.array([[4.0], [5.0]]), rtol=RTOL, atol=ATOL)

    def test_additive_smoothing(self) -> None:
        expected = (self.fc + 1.0) / np.array([[7.0], [8.0]])
        result = conditional_probabilities(self.fc, 1.0)
        np.testing.assert_allclose(result, expected, rtol=RTOL, atol=ATOL)
        np.testing.assert_allclose(result.sum(axis=1), np.ones(2), rtol=RTOL, atol=ATOL)

    def test_zero_count_and_prediction(self) -> None:
        priors = class_priors(self.fc)
        with np.errstate(divide="ignore"):
            raw = log_joint_scores(priors, conditional_probabilities(self.fc, 0.0), 2)
        self.assertTrue(np.all(np.isneginf(raw)))
        smooth = log_joint_scores(priors, conditional_probabilities(self.fc, 1.0), 2)
        self.assertTrue(np.all(np.isfinite(smooth))); self.assertEqual(predict_class(priors, conditional_probabilities(self.fc, 1.0), 2), 1)

    def test_other_valid_table(self) -> None:
        counts = np.array([[1, 2], [3, 1], [2, 2]], dtype=np.int64)
        priors = class_priors(counts); probs = conditional_probabilities(counts, 0.5)
        self.assertEqual(priors.shape, (3,)); self.assertEqual(probs.shape, (3, 2))
        np.testing.assert_allclose(priors.sum(), 1.0, rtol=RTOL, atol=ATOL)
        np.testing.assert_allclose(probs.sum(axis=1), np.ones(3), rtol=RTOL, atol=ATOL)

if __name__ == "__main__": unittest.main()
