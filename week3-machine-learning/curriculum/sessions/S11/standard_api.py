"""S11 reference check using SciPy Gaussian log-densities after Core work."""

import numpy as np
from scipy.stats import multivariate_normal


def main() -> None:
    mean = np.array([1.0, 2.0], dtype=np.float64)
    covariance = np.array([[4.0, 2.0], [2.0, 2.0]], dtype=np.float64)
    target_indices = np.array([0], dtype=np.int64)
    observed_indices = np.array([1], dtype=np.int64)
    observed_values = np.array([4.0], dtype=np.float64)

    mean_target = mean[target_indices]
    mean_observed = mean[observed_indices]
    covariance_tt = covariance[np.ix_(target_indices, target_indices)]
    covariance_to = covariance[np.ix_(target_indices, observed_indices)]
    covariance_ot = covariance[np.ix_(observed_indices, target_indices)]
    covariance_oo = covariance[np.ix_(observed_indices, observed_indices)]

    conditional_mean = mean_target + covariance_to @ np.linalg.solve(
        covariance_oo,
        observed_values - mean_observed,
    )
    conditional_covariance = covariance_tt - covariance_to @ np.linalg.solve(
        covariance_oo,
        covariance_ot,
    )

    target_candidates = np.array([-1.0, 1.0, 3.0, 5.0], dtype=np.float64)
    conditional_points = target_candidates[:, None]
    joint_points = np.column_stack(
        [
            target_candidates,
            np.full(target_candidates.shape, observed_values[0]),
        ]
    )

    conditional_logpdf = multivariate_normal.logpdf(
        conditional_points,
        mean=conditional_mean,
        cov=conditional_covariance,
    )
    joint_logpdf = multivariate_normal.logpdf(
        joint_points,
        mean=mean,
        cov=covariance,
    )
    observed_logpdf = multivariate_normal.logpdf(
        observed_values,
        mean=mean_observed,
        cov=covariance_oo,
    )
    density_identity_logpdf = joint_logpdf - observed_logpdf

    np.testing.assert_allclose(conditional_logpdf, density_identity_logpdf)

    print("conditional mean:", conditional_mean)
    print("conditional covariance:\n", conditional_covariance)
    print("conditional logpdf:", conditional_logpdf)
    print("joint logpdf - observed marginal logpdf:", density_identity_logpdf)


if __name__ == "__main__":
    main()
