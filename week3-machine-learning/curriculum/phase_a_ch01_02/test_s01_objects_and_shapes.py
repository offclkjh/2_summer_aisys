"""Public contract tests for S01.

Failures caused by ``NotImplementedError`` are expected on the first run.
Use test names and failure messages to guide the implementation order.
"""

import numpy as np
import torch
import unittest

from s01_objects_and_shapes import (
    numpy_to_torch,
    validate_coin_observations,
    validate_linear_layer_contract,
    validate_noisy_sensor_batch,
)


class S01ContractTests(unittest.TestCase):
    def test_coin_accepts_nonempty_rank_one_integer_binary_observations(self) -> None:
        validate_coin_observations(np.array([1, 0, 1], dtype=np.int64))

    def test_coin_rejects_invalid_rank_or_empty_data(self) -> None:
        cases = [np.array([[1, 0]], dtype=np.int64), np.array([], dtype=np.int64)]
        for invalid in cases:
            with self.subTest(shape=invalid.shape):
                with self.assertRaises(ValueError):
                    validate_coin_observations(invalid)

    def test_coin_rejects_invalid_dtype_or_value(self) -> None:
        cases = [
            (np.array([0.0, 1.0], dtype=np.float32), TypeError),
            (np.array([0, 2], dtype=np.int64), ValueError),
        ]
        for invalid, error_type in cases:
            with self.subTest(dtype=invalid.dtype, values=invalid.tolist()):
                with self.assertRaises(error_type):
                    validate_coin_observations(invalid)

    def test_sensor_accepts_matching_batch_contract(self) -> None:
        features = np.zeros((2, 8, 3), dtype=np.float32)
        labels = np.array([0, 1], dtype=np.int64)
        validate_noisy_sensor_batch(features, labels)

    def test_sensor_rejects_invalid_rank_shape_or_dtype(self) -> None:
        cases = [
            (np.zeros((8, 3), dtype=np.float32), np.array([0], dtype=np.int64), ValueError),
            (np.zeros((2, 8, 3), dtype=np.int64), np.array([0, 1], dtype=np.int64), TypeError),
            (np.zeros((2, 8, 3), dtype=np.float32), np.array([0.0, 1.0]), TypeError),
            (np.zeros((2, 8, 3), dtype=np.float32), np.array([0], dtype=np.int64), ValueError),
        ]
        for features, labels, error_type in cases:
            with self.subTest(feature_shape=features.shape, label_shape=labels.shape):
                with self.assertRaises(error_type):
                    validate_noisy_sensor_batch(features, labels)

    def test_numpy_to_torch_preserves_values_and_shape_and_honors_target_contract(self) -> None:
        source = np.array([[1, 2], [3, 4]], dtype=np.int64)
        result = numpy_to_torch(source, dtype=torch.float32, device="cpu")

        self.assertEqual(result.shape, source.shape)
        self.assertEqual(result.dtype, torch.float32)
        self.assertEqual(result.device.type, "cpu")
        self.assertTrue(np.array_equal(result.cpu().numpy(), source))

    def test_linear_accepts_compatible_shape_dtype_and_device(self) -> None:
        inputs = torch.zeros((5, 4), dtype=torch.float32)
        weight = torch.zeros((3, 4), dtype=torch.float32)
        bias = torch.zeros((3,), dtype=torch.float32)
        validate_linear_layer_contract(inputs, weight, bias)

    def test_linear_rejects_incompatible_rank_shape_or_dtype(self) -> None:
        cases = [
            (torch.zeros(4), torch.zeros((3, 4)), torch.zeros(3), ValueError),
            (torch.zeros((5, 4)), torch.zeros((3, 2)), torch.zeros(3), ValueError),
            (torch.zeros((5, 4)), torch.zeros((3, 4)), torch.zeros(2), ValueError),
            (
                torch.zeros((5, 4), dtype=torch.float32),
                torch.zeros((3, 4), dtype=torch.float64),
                torch.zeros(3, dtype=torch.float32),
                TypeError,
            ),
        ]
        for inputs, weight, bias, error_type in cases:
            with self.subTest(
                input_shape=inputs.shape,
                weight_shape=weight.shape,
                bias_shape=bias.shape,
            ):
                with self.assertRaises(error_type):
                    validate_linear_layer_contract(inputs, weight, bias)


if __name__ == "__main__":
    unittest.main()
