"""S10 reference: equivalent solve, Cholesky, and eigen views."""

import numpy as np
from scipy.stats import multivariate_normal


def main() -> None:
    mean = np.array([0.0, 0.0], dtype=np.float64)
    covariance = np.array([[2.0, 1.0], [1.0, 2.0]], dtype=np.float64)
    observations = np.array([[1.0, 0.0], [0.0, 2.0]], dtype=np.float64)

    residuals = observations - mean

    # Generic linear-system route used by the Core implementation.
    solutions = np.linalg.solve(covariance, residuals.T).T
    mahalanobis_solve = np.einsum("nd,nd->n", residuals, solutions)
    sign, logabsdet = np.linalg.slogdet(covariance)

    # SPD-specific Cholesky route: whiten first, then use Euclidean norms.
    cholesky = np.linalg.cholesky(covariance)
    whitened = np.linalg.solve(cholesky, residuals.T)
    mahalanobis_cholesky = np.sum(whitened**2, axis=0)
    logabsdet_cholesky = 2.0 * np.sum(np.log(np.diag(cholesky)))

    # Spectral route: rotate to principal axes and scale by eigenvalues.
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    principal_coordinates = residuals @ eigenvectors
    mahalanobis_eigen = np.sum(
        principal_coordinates**2 / eigenvalues,
        axis=1,
    )

    np.testing.assert_allclose(mahalanobis_solve, mahalanobis_cholesky)
    np.testing.assert_allclose(mahalanobis_solve, mahalanobis_eigen)
    np.testing.assert_allclose(logabsdet, logabsdet_cholesky)

    logpdf = multivariate_normal.logpdf(
        observations,
        mean=mean,
        cov=covariance,
    )

    print("Mahalanobis squared (solve):", mahalanobis_solve)
    print("Mahalanobis squared (Cholesky):", mahalanobis_cholesky)
    print("Mahalanobis squared (eigen):", mahalanobis_eigen)
    print("slogdet:", (sign, logabsdet))
    print("eigenvalues:", eigenvalues)
    print("condition number:", np.linalg.cond(covariance))
    print("multivariate Gaussian logpdf:", logpdf)


if __name__ == "__main__":
    main()
