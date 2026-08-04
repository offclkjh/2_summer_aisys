"""Contract tests for requirements already stated in S01 PROBLEM.md."""

import unittest

import numpy as np

from starter import inspect_observations, validate_coin_observations


class InspectTests(unittest.TestCase):
    def test_returns_the_four_documented_properties(self) -> None:
        observations = np.array([1, 0, 1, 1], dtype=np.int64)
        result = inspect_observations(observations)
        self.assertEqual(result[0], (4,))
        self.assertEqual(result[1], np.dtype("int64"))
        self.assertEqual(result[2], 1)
        self.assertEqual(result[3], 4)


class ValidationTests(unittest.TestCase):
    def test_accepts_documented_input(self) -> None:
        validate_coin_observations(np.array([1, 0, 1, 1], dtype=np.int64))

    def test_rejects_non_array(self) -> None:
        with self.assertRaises(TypeError):
            validate_coin_observations([1, 0, 1])

    def test_rejects_rank_two(self) -> None:
        with self.assertRaises(ValueError):
            validate_coin_observations(np.array([[1, 0]], dtype=np.int64))

    def test_rejects_empty_array(self) -> None:
        with self.assertRaises(ValueError):
            validate_coin_observations(np.array([], dtype=np.int64))

    def test_rejects_float_dtype(self) -> None:
        with self.assertRaises(TypeError):
            validate_coin_observations(np.array([1.0, 0.0], dtype=np.float32))

    def test_rejects_non_binary_value(self) -> None:
        with self.assertRaises(ValueError):
            validate_coin_observations(np.array([1, 2], dtype=np.int64))

    def test_accepts_other_integer_dtypes(self) -> None:
        validate_coin_observations(np.array([0, 1], dtype=np.int32))


if __name__ == "__main__":
    unittest.main()
