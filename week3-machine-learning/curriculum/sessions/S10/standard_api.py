"""S10 standard NumPy/SciPy API examples after the direct implementation."""

import numpy as np
from scipy.stats import multivariate_normal


def main() -> None:
    mean = np.array([0.0, 0.0], dtype=np.float64)
    covariance = np.array([[2.0, 1.0], [1.0, 2.0]], dtype=np.float64)
    observations = np.array([[1.0, 0.0], [0.0, 2.0]], dtype=np.float64)

    residuals = observations - mean
    solutions = np.linalg.solve(covariance, residuals.T).T
    mahalanobis_squared = np.einsum("nd,nd->n", residuals, solutions)
    sign, logabsdet = np.linalg.slogdet(covariance)
    logpdf = multivariate_normal.logpdf(
        observations,
        mean=mean,
        cov=covariance,
    )

    print("Mahalanobis squared:", mahalanobis_squared)
    print("slogdet:", (sign, logabsdet))
    print("multivariate Gaussian logpdf:", logpdf)


if __name__ == "__main__":
    main()
