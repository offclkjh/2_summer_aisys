"""S08 starter: one-dimensional Gaussian calculations."""
from __future__ import annotations
import numpy as np

def gaussian_logpdf(x: np.ndarray, mean: float, variance: float) -> np.ndarray:
    """Return elementwise Gaussian log-density."""
    return -0.5*(np.log(2*np.pi*variance)+(x - mean)**2/variance)
    pass

def gaussian_nll(data: np.ndarray, mean: float, variance: float) -> float:
    """Return summed negative log-likelihood."""
    return float(-gaussian_logpdf(data, mean, variance).sum())
    pass

def squared_error_sum(data: np.ndarray, mean: float) -> float:
    """Return sum of squared residuals."""
    return float(((data - mean)**2).sum())
    pass

def gaussian_mean_mle(data: np.ndarray) -> float:
    """Return the Gaussian mean MLE."""
    return float(data.sum()/data.size)
    pass

def gaussian_variance_mle(data: np.ndarray, mean: float) -> float:
    """Return variance MLE with denominator n."""
    return squared_error_sum(data, mean)/data.size
    pass

def main() -> None:
    data = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    print(gaussian_logpdf(data, 1.5, 2.0))
    print(gaussian_nll(data, 1.5, 2.0), squared_error_sum(data, 1.5))
    mean = gaussian_mean_mle(data)
    print(mean, gaussian_variance_mle(data, mean))

if __name__ == "__main__": main()
