"""S09 starter: covariance matrices and linear transforms."""
from __future__ import annotations
import numpy as np

def center_data(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return column mean and centered data."""
    pass

def outer_product(vector: np.ndarray) -> np.ndarray:
    """Return vector times its transpose."""
    pass

def covariance_matrix_mle(data: np.ndarray) -> np.ndarray:
    """Return covariance matrix with denominator n."""
    pass

def transform_covariance(matrix: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    """Return covariance after y = matrix @ x."""
    pass

def main() -> None:
    data = np.array([[1.0, 1.0], [2.0, 3.0], [3.0, 2.0]], dtype=np.float64)
    mean, centered = center_data(data)
    covariance = covariance_matrix_mle(data)
    print(mean, centered, outer_product(centered[0]), covariance)
    print(transform_covariance(np.array([[1.0, 1.0]], dtype=np.float64), covariance))

if __name__ == "__main__": main()
