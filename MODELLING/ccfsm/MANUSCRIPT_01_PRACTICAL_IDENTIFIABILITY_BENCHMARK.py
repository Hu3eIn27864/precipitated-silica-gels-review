"""Synthetic identifiability benchmark for manuscript 1.

Requires NumPy and SciPy. This is a numerical illustration only; it does not
fit experimental silica-gel data and does not validate the physical model.
Run: python MANUSCRIPT_01_PRACTICAL_IDENTIFIABILITY_BENCHMARK.py
"""
import numpy as np
from scipy.optimize import least_squares


def response(t, endpoint, rate_a, rate_b):
    """Exact zero-start response; rates may be supplied in either order."""
    scale = max(rate_a, rate_b)
    if abs(rate_a - rate_b) <= 1e-7 * scale:
        rate = 0.5 * (rate_a + rate_b)
        return endpoint * (1.0 - (1.0 + rate * t) * np.exp(-rate * t))
    return endpoint * (
        1.0
        - (
            rate_b * np.exp(-rate_a * t)
            - rate_a * np.exp(-rate_b * t)
        ) / (rate_b - rate_a)
    )


def fit_curve(times, observations):
    """Multi-start nonlinear least squares in log-parameters."""
    def residual(log_parameters):
        endpoint, rate_a, rate_b = np.exp(log_parameters)
        return response(times, endpoint, rate_a, rate_b) - observations

    best = None
    starts = (
        (max(float(np.max(observations)), 0.05), 0.03, 0.30),
        (0.40, 0.08, 0.12),
        (0.40, 0.01, 0.50),
        (0.40, 0.10, 0.10),
    )
    lower = np.log([1e-4, 1e-4, 1e-4])
    upper = np.log([2.0, 5.0, 5.0])
    for start in starts:
        result = least_squares(
            residual, np.log(start), bounds=(lower, upper), max_nfev=4000
        )
        if best is None or np.dot(result.fun, result.fun) < np.dot(best.fun, best.fun):
            best = result
    endpoint, rate_a, rate_b = np.exp(best.x)
    return endpoint, min(rate_a, rate_b), max(rate_a, rate_b)


def main():
    rng = np.random.default_rng(20261115)
    cases = (
        ("near_equal_5pct_dense_long", 0.4, 0.100, 0.105,
         np.linspace(0.0, 100.0, 100), 0.002),
        ("near_equal_5pct_coarse_short", 0.4, 0.100, 0.105,
         np.linspace(0.0, 15.0, 12), 0.002),
        ("separated_dense_long", 0.4, 0.030, 0.300,
         np.linspace(0.0, 180.0, 100), 0.002),
        ("separated_coarse_short", 0.4, 0.030, 0.300,
         np.linspace(0.0, 15.0, 12), 0.002),
    )
    print("case,median_rel_error_endpoint,median_rel_error_slow,")
    print("median_rel_error_fast,q90_rel_error_slow,q90_rel_error_fast")
    for name, endpoint, rate_a, rate_b, times, noise_sd in cases:
        truth = np.array([endpoint, min(rate_a, rate_b), max(rate_a, rate_b)])
        estimates = []
        for _ in range(100):
            clean = response(times, endpoint, rate_a, rate_b)
            noisy = clean + rng.normal(0.0, noise_sd, size=times.size)
            estimates.append(fit_curve(times, noisy))
        estimates = np.asarray(estimates)
        relative = np.abs(estimates - truth) / truth
        median = np.median(relative, axis=0)
        q90_rates = np.quantile(relative[:, 1:], 0.90, axis=0)
        print(
            f"{name},{median[0]:.6f},{median[1]:.6f},{median[2]:.6f},"
            f"{q90_rates[0]:.6f},{q90_rates[1]:.6f}"
        )


if __name__ == "__main__":
    main()
