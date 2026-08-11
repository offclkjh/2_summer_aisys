"""S05 starter: Bernoulli/Binomial probabilities, likelihood, and MLE."""

from __future__ import annotations

import numpy as np


def bernoulli_pmf(x: int, theta: float) -> float:
    """Return the Bernoulli PMF at x for success probability theta."""
    raise NotImplementedError("T3: bernoulli_pmf")


def bernoulli_likelihood(data: np.ndarray, theta: float) -> float:
    """Return the likelihood of an ordered 1D binary observation array."""
    raise NotImplementedError("T3: bernoulli_likelihood")


def bernoulli_log_likelihood(data: np.ndarray, theta: float) -> float:
    """Return the natural-log likelihood of an ordered binary array."""
    raise NotImplementedError("T3: bernoulli_log_likelihood")


def binomial_pmf(k: int, n: int, theta: float) -> float:
    """Return the probability of k successes in n Bernoulli trials."""
    raise NotImplementedError("T3: binomial_pmf")


def bernoulli_mle(data: np.ndarray) -> float:
    """Return the maximum-likelihood estimate of theta."""
    raise NotImplementedError("T3: bernoulli_mle")


def main() -> None:
    data = np.array([1, 0, 1, 1, 0], dtype=np.int64)
    theta = 0.4

    print("Bernoulli PMF for x=1:", bernoulli_pmf(1, theta))
    print("ordered-data likelihood:", bernoulli_likelihood(data, theta))
    print("ordered-data log-likelihood:", bernoulli_log_likelihood(data, theta))
    print("count probability:", binomial_pmf(int(data.sum()), data.size, theta))
    print("MLE:", bernoulli_mle(data))


if __name__ == "__main__":
    main()
