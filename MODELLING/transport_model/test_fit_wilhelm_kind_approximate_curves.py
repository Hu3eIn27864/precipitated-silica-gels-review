"""Numerical regression tests for the empirical syneresis curve fitter.

Synthetic tests verify the implementation only; they do not validate chart readings
or establish a physical interpretation of fitted parameters.
"""
import math
import unittest

from fit_wilhelm_kind_approximate_curves import fit_one_exponential


class SingleExponentialFitTests(unittest.TestCase):
    def test_recovers_noise_free_synthetic_parameters(self):
        expected_a = 0.42
        expected_tau = 0.73
        times = [0.0, 0.05, 0.1, 0.2, 0.4, 0.8, 1.2, 2.0, 3.0]
        points = [
            (t, expected_a * (1.0 - math.exp(-t / expected_tau)))
            for t in times
        ]
        amplitude, tau, r2, rmse = fit_one_exponential(points)
        self.assertAlmostEqual(amplitude, expected_a, places=7)
        self.assertAlmostEqual(tau, expected_tau, places=6)
        self.assertAlmostEqual(r2, 1.0, places=12)
        self.assertLess(rmse, 1e-9)

    def test_zero_origin_does_not_change_fit(self):
        expected_a = 0.31
        expected_tau = 1.4
        times = [0.1, 0.2, 0.5, 1.0, 2.0, 4.0]
        points = [
            (t, expected_a * (1.0 - math.exp(-t / expected_tau)))
            for t in times
        ]
        without_origin = fit_one_exponential(points)
        with_origin = fit_one_exponential([(0.0, 0.0)] + points)
        for left, right in zip(without_origin, with_origin):
            self.assertAlmostEqual(left, right, places=9)

    def test_fit_returns_finite_diagnostics(self):
        points = [(t, y) for t, y in [
            (0.0, 0.0), (0.2, 0.08), (0.5, 0.17),
            (1.0, 0.25), (2.0, 0.31), (4.0, 0.35)
        ]]
        amplitude, tau, r2, rmse = fit_one_exponential(points)
        for value in (amplitude, tau, r2, rmse):
            self.assertTrue(math.isfinite(value))
        self.assertGreater(amplitude, 0.0)
        self.assertGreater(tau, 0.0)
        self.assertGreaterEqual(rmse, 0.0)


if __name__ == "__main__":
    unittest.main()
