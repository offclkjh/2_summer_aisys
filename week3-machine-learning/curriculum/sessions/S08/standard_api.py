"""S08 standard NumPy/SciPy API examples after the direct implementation."""

import numpy as np
from scipy.stats import norm


def main() -> None:
    data = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    mean = 1.5
    variance = 2.0

    logpdf = norm.logpdf(data, loc=mean, scale=np.sqrt(variance))
    nll = -logpdf.sum()
    mean_mle = data.mean()
    variance_mle = data.var(ddof=0)
    unbiased_variance = data.var(ddof=1)

    print("logpdf:", logpdf)
    print("NLL:", nll)
    print("mean MLE:", mean_mle)
    print("variance MLE:", variance_mle)
    print("unbiased sample variance:", unbiased_variance)


if __name__ == "__main__":
    main()
