"""S07 standard NumPy API examples after the direct implementation."""

import numpy as np


def main() -> None:
    counts = np.array([[3, 1, 0], [1, 4, 0]], dtype=np.int64)
    category = 2

    class_totals = counts.sum(axis=1)
    priors = class_totals / class_totals.sum()
    print("priors:", priors)
    for alpha in (0.0, 1.0):
        conditionals = (counts + alpha) / (
            class_totals[:, None] + alpha * counts.shape[1]
        )
        with np.errstate(divide="ignore"):
            log_joint = np.log(priors) + np.log(conditionals[:, category])
        prediction = (
            int(np.argmax(log_joint))
            if np.any(np.isfinite(log_joint))
            else None
        )
        print("alpha:", alpha)
        print("conditionals:\n", conditionals)
        print("log-joint:", log_joint)
        print("prediction:", prediction)


if __name__ == "__main__":
    main()
