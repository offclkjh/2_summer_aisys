"""S09 standard NumPy API examples after the direct implementation."""

import numpy as np


def main() -> None:
    data = np.array([[1.0, 1.0], [2.0, 3.0], [3.0, 2.0]], dtype=np.float64)
    transform = np.array([[1.0, 1.0]], dtype=np.float64)

    mean = data.mean(axis=0)
    centered = data - mean
    first_outer = np.outer(centered[0], centered[0])
    covariance = np.cov(data, rowvar=False, bias=True)
    transformed = data @ transform.T
    transformed_covariance = np.atleast_2d(
        np.cov(transformed, rowvar=False, bias=True)
    )
    formula_covariance = transform @ covariance @ transform.T

    print("mean:", mean)
    print("centered:\n", centered)
    print("first outer product:\n", first_outer)
    print("covariance:\n", covariance)
    print("transformed covariance:\n", transformed_covariance)
    print("A Sigma A.T:\n", formula_covariance)


if __name__ == "__main__":
    main()
