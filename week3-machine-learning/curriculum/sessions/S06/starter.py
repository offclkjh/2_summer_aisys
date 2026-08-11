"""S06 starter: categorical labels and multinomial counts."""
from __future__ import annotations
import math
import numpy as np

def one_hot(labels: np.ndarray, num_categories: int) -> np.ndarray:
    """Return shape (n, K) float64 one-hot rows."""
    size = np.size(labels)
    mat = np.zeros((size, num_categories), dtype=np.float64)
    for i in range(size):
        mat[i][labels[i]] = 1
    return mat

def counts_from_labels(labels: np.ndarray, num_categories: int) -> np.ndarray:
    """Return shape (K,) int64 category counts."""
    size = np.size(labels)
    mat = np.zeros(num_categories, dtype=np.int64)
    for i in range(size):
        mat[labels[i]] += 1
    return mat

def categorical_likelihood(labels: np.ndarray, theta: np.ndarray) -> float:
    """Return the likelihood of one ordered label sequence."""
    return float(np.prod(theta[labels]))

def multinomial_pmf(counts: np.ndarray, theta: np.ndarray) -> float:
    """Return the multinomial probability of a count vector."""
    size = np.size(counts)
    pmf = math.factorial(np.sum(counts))
    for i in range(size):
        pmf /= math.factorial(counts[i])
        pmf *= theta[i] ** counts[i]
    return float(pmf)

def categorical_mle(counts: np.ndarray) -> np.ndarray:
    """Return the simplex MLE counts / total."""
    return counts / np.sum(counts)

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
