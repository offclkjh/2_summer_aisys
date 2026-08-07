"""S04 starter: entropy, cross-entropy, and KL from explicit distributions."""

from __future__ import annotations

import numpy as np


def entropy(p: np.ndarray) -> float:
    """Return H(p) in bits for a strictly positive probability vector."""
    raise NotImplementedError("T3: entropy")


def cross_entropy(p: np.ndarray, q: np.ndarray) -> float:
    """Return H(p, q) in bits for aligned positive probability vectors."""
    raise NotImplementedError("T3: cross_entropy")


def kl_divergence(p: np.ndarray, q: np.ndarray) -> float:
    """Return KL(p || q) in bits for aligned positive probability vectors."""
    raise NotImplementedError("T3: kl_divergence")


def main() -> None:
    p = np.array([0.50, 0.25, 0.25], dtype=np.float64)
    q = np.array(
        [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0],
        dtype=np.float64,
    )

    print("H(p):", entropy(p))
    print("H(p, q):", cross_entropy(p, q))
    print("KL(p || q):", kl_divergence(p, q))


if __name__ == "__main__":
    main()
