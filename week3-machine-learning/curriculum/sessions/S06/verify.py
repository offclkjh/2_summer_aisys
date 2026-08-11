"""S06 verification: compare learner functions with standard NumPy references."""

from __future__ import annotations

import math

import numpy as np

from starter import (
    categorical_likelihood,
    categorical_mle,
    counts_from_labels,
    multinomial_pmf,
    one_hot,
)


def main() -> None:
    labels = np.array([0, 2, 1, 2, 2], dtype=np.int64)
    theta = np.array([0.2, 0.3, 0.5], dtype=np.float64)
    num_categories = theta.size

    actual_one_hot = one_hot(labels, num_categories)
    actual_counts = counts_from_labels(labels, num_categories)

    # Standard NumPy references introduced in PROBLEM.md.
    standard_one_hot = np.eye(num_categories, dtype=np.float64)[labels]
    standard_counts = np.bincount(labels, minlength=num_categories)

    np.testing.assert_array_equal(actual_one_hot, standard_one_hot)
    print("PASS: one_hot matches np.eye indexing")

    np.testing.assert_array_equal(actual_counts, standard_counts)
    print("PASS: counts match np.bincount")

    np.testing.assert_array_equal(actual_one_hot.sum(axis=0), actual_counts)
    print("PASS: one_hot column sums equal counts")

    sequence = categorical_likelihood(labels, theta)
    count_probability = multinomial_pmf(actual_counts, theta)
    coefficient = math.factorial(labels.size) // math.prod(
        math.factorial(int(count)) for count in actual_counts
    )
    np.testing.assert_allclose(
        count_probability / sequence,
        coefficient,
        rtol=1e-7,
        atol=1e-12,
    )
    print("PASS: count-PMF/sequence ratio equals coefficient")

    permuted_labels = labels[::-1]
    permuted_counts = counts_from_labels(permuted_labels, num_categories)
    np.testing.assert_array_equal(permuted_counts, actual_counts)
    np.testing.assert_allclose(
        categorical_likelihood(permuted_labels, theta),
        sequence,
        rtol=1e-7,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        multinomial_pmf(permuted_counts, theta),
        count_probability,
        rtol=1e-7,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        categorical_mle(permuted_counts),
        categorical_mle(actual_counts),
        rtol=1e-7,
        atol=1e-12,
    )
    print("PASS: permutation preserves counts and probabilities")

    print("\nsummary: 5/5 checks passed")


if __name__ == "__main__":
    main()
