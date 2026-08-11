"""S01 starter: one explicit coin-observation case."""

from __future__ import annotations

import numpy as np


def inspect_observations(observations: np.ndarray) -> tuple:
    """Return shape, dtype, first observation, and number of observations."""
    # raise NotImplementedError("T2: inspect_observations")
    validate_coin_observations(observations)

    return (observations.shape, observations.dtype, observations[0], observations.shape[0])

def validate_coin_observations(observations: np.ndarray) -> None:
    """Validate the five input rules stated in PROBLEM.md T3."""
    # raise NotImplementedError("T3: validate_coin_observations")

    if not isinstance(observations, np.ndarray):
        raise TypeError("not numpy array")

    if len(observations.shape) != 1:
        raise ValueError("not dim 1")
    elif observations.shape[0] == 0:
        raise ValueError("no observations")
    elif not np.issubdtype(observations.dtype, np.integer):
        raise TypeError("not int value")
    else:
        for i in observations:
            if i != 0 and i != 1:
                raise ValueError("not bernouill")


def main() -> None:
    observations = np.array([1, 0, 1, 1], dtype=np.int64)
    print(inspect_observations(observations))
    validate_coin_observations(observations)

    # # T5
    # o1 = np.array([], dtype=np.int64)
    # o2 = np.array(1)
    # o3 = 1
    # validate_coin_observations(o3)


if __name__ == "__main__":
    main()
