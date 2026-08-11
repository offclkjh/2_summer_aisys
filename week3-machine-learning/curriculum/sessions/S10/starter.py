"""S10 starter: stable multivariate Gaussian log-density."""
from __future__ import annotations
import numpy as np

def mahalanobis_squared(x: np.ndarray, mean: np.ndarray, covariance: np.ndarray) -> float:
    """Return (x-mean)^T covariance^-1 (x-mean) using solve."""
    pass

def multivariate_gaussian_logpdf(observations: np.ndarray, mean: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    """Return one log-density per observation without explicit inverse/determinant."""
    pass

def main() -> None:
    mean = np.array([0.0, 0.0], dtype=np.float64)
    covariance = np.array([[2.0, 1.0], [1.0, 2.0]], dtype=np.float64)
    observations = np.array([[1.0, 0.0], [0.0, 2.0]], dtype=np.float64)
    print(mahalanobis_squared(observations[0], mean, covariance))
    print(multivariate_gaussian_logpdf(observations, mean, covariance))

if __name__ == "__main__": main()
