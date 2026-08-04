"""S01: Express probabilistic objects and array shapes as code contracts.

This is a learning skeleton. Answer the prediction questions in ``S01_NOTES.md``
before implementing each TODO. A ``NotImplementedError`` from a core function
means that its exercise has not been completed yet.
"""

from __future__ import annotations

import numpy as np
import torch


def validate_coin_observations(observations: np.ndarray) -> None:
    """Validate the input contract for coin observations.

    Args:
        observations: A NumPy array with shape ``(N,)``. ``N >= 1``, every
            element must be a binary observation, and the dtype must be integer.

    Returns:
        ``None`` when the contract is satisfied.

    Raises:
        TypeError: If the array or dtype contract is violated.
        ValueError: If the rank, size, or value contract is violated.
    """
    # TODO: Check type, rank, non-emptiness, dtype, and values in that order.
    raise NotImplementedError("S01 TODO: validate_coin_observations")


def validate_noisy_sensor_batch(
    features: np.ndarray,
    labels: np.ndarray,
) -> None:
    """Validate that a batch of noisy sensor observations is compatible.

    Args:
        features: Floating-point sensor signals with shape ``(N, T, C)``.
            The axes represent batch, time, and channel, respectively.
        labels: Integer observation labels with shape ``(N,)``.

    Returns:
        ``None`` when both inputs satisfy the rank, dtype, and batch contracts.

    Note:
        A latent variable representing the true sensor state is not included in
        this function's observed inputs.
    """
    # TODO: Check both arrays' types, ranks, dtypes, and shared batch size.
    raise NotImplementedError("S01 TODO: validate_noisy_sensor_batch")


def numpy_to_torch(
    array: np.ndarray,
    *,
    dtype: torch.dtype,
    device: torch.device | str = "cpu",
) -> torch.Tensor:
    """Convert a NumPy array to a tensor with an explicit dtype and device.

    Input and output shapes and values must match. The returned tensor's dtype
    and device must follow the caller-provided contract.
    """
    # TODO: Preserve values and shape while honoring the dtype/device contract.
    raise NotImplementedError("S01 TODO: numpy_to_torch")


def validate_linear_layer_contract(
    inputs: torch.Tensor,
    weight: torch.Tensor,
    bias: torch.Tensor,
) -> None:
    """Validate tensor contracts before computing a linear layer.

    Args:
        inputs: A floating-point tensor with shape ``(B, D_in)``.
        weight: A learned parameter with shape ``(D_out, D_in)``.
        bias: A learned parameter with shape ``(D_out,)``.

    Returns:
        ``None`` when ranks, connected dimensions, dtypes, and devices match.

    Note:
        This function does not compute the numerical output. Record the expected
        output shape in the worksheet before running the code.
    """
    # TODO: Check ranks, connected dimensions, floating dtypes, and devices.
    raise NotImplementedError("S01 TODO: validate_linear_layer_contract")


def main() -> None:
    """Prepare small examples. Failure is expected before TODOs are complete."""
    coin_observations = np.array([1, 0, 1, 1], dtype=np.int64)
    sensor_features = np.zeros((2, 4, 1), dtype=np.float32)
    sensor_labels = np.array([0, 1], dtype=np.int64)
    linear_inputs = torch.zeros((3, 4), dtype=torch.float32)
    linear_weight = torch.zeros((2, 4), dtype=torch.float32)
    linear_bias = torch.zeros((2,), dtype=torch.float32)

    # Predict before running:
    # 1. Which objects are observed, latent, learned, or fixed in each example?
    # 2. What does each axis count, and where must batch sizes agree?
    # 3. What must be preserved or explicitly changed in NumPy-to-Torch conversion?
    validate_coin_observations(coin_observations)
    validate_noisy_sensor_batch(sensor_features, sensor_labels)
    numpy_to_torch(sensor_features, dtype=torch.float32, device="cpu")
    validate_linear_layer_contract(linear_inputs, linear_weight, linear_bias)


if __name__ == "__main__":
    main()
