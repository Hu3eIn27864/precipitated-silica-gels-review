#!/usr/bin/env python3
"""Tests for prescribed time-dependent hydraulic mobility."""
import unittest
from time_dependent_1d import solve_1d_time_dependent_mobility
from heterogeneous_1d import solve_1d_pressure_diffusion


class TimeDependentMobilityTests(unittest.TestCase):
    def test_constant_schedule_recovers_fixed_coefficient_solver(self):
        n, steps = 24, 80
        storage = [1e-5]*n
        mobility = [1e-12]*n
        schedule = [mobility[:] for _ in range(steps)]
        varying = solve_1d_time_dependent_mobility(
            storage, schedule, 1e-3, 0.1)
        fixed = solve_1d_pressure_diffusion(
            storage, mobility, 1e-3, 0.1, steps)
        self.assertAlmostEqual(varying["mean_pressure_pa"][-1],
                               fixed["mean_pressure_pa"][-1], places=12)

    def test_increasing_mobility_accelerates_pressure_relaxation(self):
        n, steps = 30, 100
        storage = [1.0]*n
        low = [0.01]*n
        high = [0.05]*n
        schedule_aging = [low[:] if k < 50 else high[:] for k in range(steps)]
        schedule_low = [low[:] for _ in range(steps)]
        aged = solve_1d_time_dependent_mobility(
            storage, schedule_aging, 1.0, 1e-4)
        constant = solve_1d_time_dependent_mobility(
            storage, schedule_low, 1.0, 1e-4)
        self.assertLess(aged["mean_pressure_pa"][-1],
                        constant["mean_pressure_pa"][-1])

    def test_mass_balance_each_step(self):
        n = 20
        schedule = [[1e-12*(1.0+0.01*k)]*n for k in range(60)]
        result = solve_1d_time_dependent_mobility(
            [2e-5]*n, schedule, 1e-3, 0.2)
        for residual in result["balance_residual_m"][1:]:
            self.assertLess(abs(residual), 1e-14)

    def test_pressure_nonnegative_and_nonincreasing_mean(self):
        schedule = [[1e-12*(1.0+0.02*k)]*16 for k in range(50)]
        result = solve_1d_time_dependent_mobility(
            [1e-5]*16, schedule, 1e-3, 0.1)
        self.assertTrue(all(p >= 0 for row in result["profiles_pa"] for p in row))
        means = result["mean_pressure_pa"]
        self.assertTrue(all(a >= b for a, b in zip(means, means[1:])))

    def test_rejects_bad_schedule(self):
        with self.assertRaises(ValueError):
            solve_1d_time_dependent_mobility([1.0, 1.0], [], 1.0, 0.1)
        with self.assertRaises(ValueError):
            solve_1d_time_dependent_mobility([1.0, 1.0], [[1.0]], 1.0, 0.1)
        with self.assertRaises(ValueError):
            solve_1d_time_dependent_mobility([1.0, 1.0], [[1.0, 0.0]], 1.0, 0.1)


if __name__ == "__main__":
    unittest.main()
