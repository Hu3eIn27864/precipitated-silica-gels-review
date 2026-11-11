#!/usr/bin/env python3
"""Tests for the conservative heterogeneous 1-D pressure solver."""
import math
import unittest
from heterogeneous_1d import solve_1d_pressure_diffusion
from syneresis_1d import average_degree_of_consolidation


class HeterogeneousPressureTests(unittest.TestCase):
    def test_initial_and_long_time_limits(self):
        result = solve_1d_pressure_diffusion([1e-5]*20, [1e-12]*20, 1e-3, 1.0, 1)
        self.assertEqual(result["mean_pressure_pa"][0], 1.0)
        late = solve_1d_pressure_diffusion([1e-5]*20, [1e-12]*20, 1e-3, 100.0, 1000)
        self.assertLess(late["mean_pressure_pa"][-1], 1e-8)

    def test_constant_coefficient_recovers_analytical_solution(self):
        n, thickness, storage, mobility = 80, 1.0, 1.0, 1.0
        dt, steps = 2.0e-5, 1250
        result = solve_1d_pressure_diffusion([storage]*n, [mobility]*n,
                                             thickness, dt, steps)
        cv = mobility / storage
        expected = 1.0 - average_degree_of_consolidation(
            dt*steps, cv, thickness/2.0)
        self.assertAlmostEqual(result["mean_pressure_pa"][-1], expected, delta=0.012)

    def test_mass_balance_each_step(self):
        result = solve_1d_pressure_diffusion([1e-5]*30, [1e-12]*30, 1e-3, 0.5, 40)
        for residual in result["balance_residual_m"][1:]:
            self.assertLess(abs(residual), 1e-15)

    def test_pressure_nonnegative_and_mean_decreases(self):
        result = solve_1d_pressure_diffusion([1e-5]*25, [1e-12]*25, 1e-3, 0.2, 100)
        means = result["mean_pressure_pa"]
        self.assertTrue(all(p >= 0.0 for profile in result["profiles_pa"] for p in profile))
        self.assertTrue(all(a >= b for a, b in zip(means, means[1:])))

    def test_piecewise_coefficients(self):
        result = solve_1d_pressure_diffusion([1e-5]*10+[2e-5]*10,
                                             [1e-12]*10+[5e-13]*10, 1e-3, 0.1, 20)
        self.assertEqual(len(result["profiles_pa"]), 21)
        self.assertTrue(all(math.isfinite(p) for profile in result["profiles_pa"] for p in profile))

    def test_rejects_invalid_inputs(self):
        bad = [
            ([], [], 1.0, 1.0, 1),
            ([1.0], [1.0, 2.0], 1.0, 1.0, 1),
            ([0.0], [1.0], 1.0, 1.0, 1),
            ([1.0], [1.0], 1.0, 0.0, 1),
            ([1.0], [1.0], 1.0, 1.0, 0),
        ]
        for args in bad:
            with self.subTest(args=args), self.assertRaises(ValueError):
                solve_1d_pressure_diffusion(*args)


if __name__ == "__main__":
    unittest.main()
