"""S01 starter: one explicit coin-observation case."""

from __future__ import annotations

import numpy as np


def inspect_observations(observations: np.ndarray) -> tuple:
    """Return shape, dtype, first observation, and number of observations."""
    raise NotImplementedError("T2: inspect_observations")


def validate_coin_observations(observations: np.ndarray) -> None:
    """Validate the five input rules stated in PROBLEM.md T3."""
    raise NotImplementedError("T3: validate_coin_observations")


def main() -> None:
    observations = np.array([1, 0, 1, 1], dtype=np.int64)
    print(inspect_observations(observations))
    validate_coin_observations(observations)


if __name__ == "__main__":
    main()
