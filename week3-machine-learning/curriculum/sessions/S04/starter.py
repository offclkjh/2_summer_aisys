"""S04 starter: entropy, cross-entropy, and KL from explicit distributions."""

from __future__ import annotations

import numpy as np


def entropy(p: np.ndarray) -> float:
    """Return H(p) in bits for a strictly positive probability vector."""
    # raise NotImplementedError("T3: entropy")
    return float(-np.sum(p * np.log2(p)))


def cross_entropy(p: np.ndarray, q: np.ndarray) -> float:
    """Return H(p, q) in bits for aligned positive probability vectors."""
    # raise NotImplementedError("T3: cross_entropy")
    return float(-np.sum(p * np.log2(q)))


def kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    """Return KL(p || q) in bits for aligned positive probability vectors."""
    # raise NotImplementedError("T3: kl_divergence")
    return -entropy(p) + cross_entropy(p, q)


def main() -> None:
    p = np.array([0.50, 0.25, 0.25], dtype=np.float64)
    q = np.array(
        [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0],
        dtype=np.float64,
    )

    print("H(p):", entropy(p))
    print("H(p, q):", cross_entropy(p, q))
    print("KL(p || q):", kl_divergence(p, q))
    print(kl_divergence(p,p))
    print(kl_divergence(q,p))

if __name__ == "__main__":
    main()
