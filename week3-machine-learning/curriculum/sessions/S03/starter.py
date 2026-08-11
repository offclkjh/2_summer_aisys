"""S03 starter: theoretical moments and fixed-sample statistics."""

from __future__ import annotations

import numpy as np


def theoretical_moments(
    values: np.ndarray, probabilities: np.ndarray
) -> tuple[float, float]:
    """Return the distribution expectation and variance."""
    # raise NotImplementedError("T3: theoretical_moments")
    avg, var = 0, 0
    for i in range(len(values)):
        avg += values[i] * probabilities[i]

    for i in range(len(probabilities)):
        var += (values[i] - avg) ** 2 * probabilities[i]
    return avg, var

def sample_moments(samples: np.ndarray) -> tuple[float, float]:
    """Return the sample mean and unbiased sample variance (denominator n - 1)."""
    # raise NotImplementedError("T3: sample_moments")
    savg, svar = samples.sum()/samples.size, 0
    for i in range(len(samples)):
        svar += (samples[i] - savg) ** 2
    svar /= (len(samples) - 1)
    return float(savg), float(svar)


def theoretical_covariance(
    x_values: np.ndarray,
    y_values: np.ndarray,
    probabilities: np.ndarray,
) -> float:
    """Return Cov(X, Y) for aligned outcomes and their probabilities."""
    # raise NotImplementedError("T4: theoretical_covariance")
    xavg, yavg = np.sum(x_values * probabilities), np.sum(y_values * probabilities)
    cov = np.sum((x_values - xavg) * (y_values - yavg) * probabilities)
    return float(cov)


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
