"""S06 standard API reference after completing the direct implementation."""

import numpy as np
from scipy.stats import multinomial


def main() -> None:
    labels = np.array([0, 2, 1, 2, 2], dtype=np.int64)
    theta = np.array([0.2, 0.3, 0.5], dtype=np.float64)
    num_categories = theta.size

    # One-hot encoding and category counts with standard NumPy APIs.
    one_hot = np.eye(num_categories, dtype=np.float64)[labels]
    counts = np.bincount(labels, minlength=num_categories)

    # An ordered Categorical sequence is selected by indexing and multiplied.
    sequence_likelihood = np.prod(theta[labels])

    # A Multinomial count probability is available as a completed SciPy PMF.
    count_pmf = multinomial.pmf(
        counts,
        n=labels.size,
        p=theta,
    )

    # The Categorical MLE is the normalized count vector.
    mle = counts / counts.sum()

    print("one_hot:\n", one_hot)
    print("counts:", counts)
    print("sequence likelihood:", sequence_likelihood)
    print("multinomial PMF:", count_pmf)
    print("MLE:", mle)

    print("\nT4 relationships")
    print("one_hot column sums:", one_hot.sum(axis=0))
    print("count-PMF / sequence:", count_pmf / sequence_likelihood)

    permuted_labels = labels[::-1]
    permuted_counts = np.bincount(
        permuted_labels,
        minlength=num_categories,
    )
    print("permuted counts:", permuted_counts)
    print("permuted sequence likelihood:", np.prod(theta[permuted_labels]))
    print(
        "permuted multinomial PMF:",
        multinomial.pmf(permuted_counts, n=permuted_labels.size, p=theta),
    )
    print("permuted MLE:", permuted_counts / permuted_counts.sum())


if __name__ == "__main__":
    main()
