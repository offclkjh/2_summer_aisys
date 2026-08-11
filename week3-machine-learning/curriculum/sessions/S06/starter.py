"""S06 starter: categorical labels and multinomial counts."""
from __future__ import annotations
import math
import numpy as np

def one_hot(labels: np.ndarray, num_categories: int) -> np.ndarray:
    """Return shape (n, K) float64 one-hot rows."""
    pass

def counts_from_labels(labels: np.ndarray, num_categories: int) -> np.ndarray:
    """Return shape (K,) int64 category counts."""
    pass

def categorical_likelihood(labels: np.ndarray, theta: np.ndarray) -> float:
    """Return the likelihood of one ordered label sequence."""
    pass

def multinomial_pmf(counts: np.ndarray, theta: np.ndarray) -> float:
    """Return the multinomial probability of a count vector."""
    pass

def categorical_mle(counts: np.ndarray) -> np.ndarray:
    """Return the simplex MLE counts / total."""
    pass

def main() -> None:
    labels = np.array([0, 2, 1, 2, 2], dtype=np.int64)
    theta = np.array([0.2, 0.3, 0.5], dtype=np.float64)
    counts = counts_from_labels(labels, theta.size)
    print(one_hot(labels, theta.size))
    print(counts)
    print(categorical_likelihood(labels, theta))
    print(multinomial_pmf(counts, theta))
    print(categorical_mle(counts))

if __name__ == "__main__":
    main()
