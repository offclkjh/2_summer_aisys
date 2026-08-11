"""S02 starter: probabilities from one 2x2 detector count table."""

from __future__ import annotations

import numpy as np


def normalize_joint(counts: np.ndarray) -> np.ndarray:
    """Return the float64 joint probability table."""
    # raise NotImplementedError("T3: normalize_joint")
    return counts.astype(np.float64) / counts.sum()


def compute_marginals(joint: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return p(A) and p(Y), in that order."""
    # raise NotImplementedError("T3: compute_marginals")
    norm = normalize_joint(joint)
    return norm.sum(axis=1), norm.sum(axis=0)


def compute_alarm_posterior(joint: np.ndarray) -> tuple[float, float]:
    """Return p(A=1|Y=1) by the direct definition and by Bayes rule."""
    # raise NotImplementedError("T4: compute_alarm_posterior")
    pa, py = compute_marginals(joint)
    pa1, py1 = pa[1]/pa.sum(), py[1]/py.sum()
    pa1y1 = joint[1, 1]/joint.sum()
    likelihood = pa1y1/pa1
    return pa1y1/py1, likelihood*pa1/py1


def main() -> None:
    counts = np.array([[72, 8], [6, 14]], dtype=np.int64)
    joint = normalize_joint(counts)
    p_a, p_y = compute_marginals(joint)
    posterior_direct, posterior_bayes = compute_alarm_posterior(joint)

    print("joint:\n", joint)
    print("p(A):", p_a)
    print("p(Y):", p_y)
    print("p(A=1|Y=1), direct:", posterior_direct)
    print("p(A=1|Y=1), Bayes:", posterior_bayes)


if __name__ == "__main__":
    main()
