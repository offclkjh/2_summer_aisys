"""S08 starter: one-dimensional Gaussian calculations."""
from __future__ import annotations
import numpy as np

def gaussian_logpdf(x: np.ndarray, mean: float, variance: float) -> np.ndarray:
    """Return elementwise Gaussian log-density."""
    pass

def gaussian_nll(data: np.ndarray, mean: float, variance: float) -> float:
    """Return summed negative log-likelihood."""
    pass

def squared_error_sum(data: np.ndarray, mean: float) -> float:
    """Return sum of squared residuals."""
    pass

def gaussian_mean_mle(data: np.ndarray) -> float:
    """Return the Gaussian mean MLE."""
    pass

def gaussian_variance_mle(data: np.ndarray, mean: float) -> float:
    """Return variance MLE with denominator n."""
    pass

def main() -> None:
    data = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    print(gaussian_logpdf(data, 1.5, 2.0))
    print(gaussian_nll(data, 1.5, 2.0), squared_error_sum(data, 1.5))
    mean = gaussian_mean_mle(data)
    print(mean, gaussian_variance_mle(data, mean))

if __name__ == "__main__": main()
