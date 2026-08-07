"""S03 starter: theoretical moments and fixed-sample statistics."""

from __future__ import annotations

import numpy as np


def theoretical_moments(
    values: np.ndarray, probabilities: np.ndarray
) -> tuple[float, float]:
    """Return the distribution expectation and variance."""
    raise NotImplementedError("T3: theoretical_moments")


def sample_moments(samples: np.ndarray) -> tuple[float, float]:
    """Return the sample mean and unbiased sample variance (denominator n - 1)."""
    raise NotImplementedError("T3: sample_moments")


def theoretical_covariance(
    x_values: np.ndarray,
    y_values: np.ndarray,
    probabilities: np.ndarray,
) -> float:
    """Return Cov(X, Y) for aligned outcomes and their probabilities."""
    raise NotImplementedError("T4: theoretical_covariance")


def main() -> None:
    x_values = np.array([-1.0, 1.0, 3.0], dtype=np.float64)
    y_values = np.array([2.0, 0.0, 4.0], dtype=np.float64)
    probabilities = np.array([0.25, 0.50, 0.25], dtype=np.float64)
    samples = np.array([-1.0, 1.0, 3.0, 3.0, 3.0], dtype=np.float64)

    print("theoretical E[X], Var(X):", theoretical_moments(x_values, probabilities))
    print("sample mean, unbiased variance:", sample_moments(samples))
    print("theoretical Cov(X, Y):", theoretical_covariance(x_values, y_values, probabilities))


if __name__ == "__main__":
    main()
