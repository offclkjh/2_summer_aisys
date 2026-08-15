"""Starter code for S11 Gaussian marginalization and conditioning."""

import numpy as np


def gaussian_marginal(
    mean: np.ndarray,
    covariance: np.ndarray,
    indices: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the selected Gaussian marginal mean and covariance."""
    pass


def gaussian_conditional(
    mean: np.ndarray,
    covariance: np.ndarray,
    target_indices: np.ndarray,
    observed_indices: np.ndarray,
    observed_values: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return target mean and covariance conditional on observed values."""
    pass


def main() -> None:
    mean = np.array([1.0, 2.0], dtype=np.float64)
    covariance = np.array([[4.0, 2.0], [2.0, 2.0]], dtype=np.float64)
    target_indices = np.array([0], dtype=np.int64)
    observed_indices = np.array([1], dtype=np.int64)
    observed_values = np.array([4.0], dtype=np.float64)

    marginal_mean, marginal_covariance = gaussian_marginal(
        mean,
        covariance,
        target_indices,
    )
    conditional_mean, conditional_covariance = gaussian_conditional(
        mean,
        covariance,
        target_indices,
        observed_indices,
        observed_values,
    )

    print("marginal mean:", marginal_mean)
    print("marginal covariance:\n", marginal_covariance)
    print("conditional mean:", conditional_mean)
    print("conditional covariance:\n", conditional_covariance)


if __name__ == "__main__":
    main()
