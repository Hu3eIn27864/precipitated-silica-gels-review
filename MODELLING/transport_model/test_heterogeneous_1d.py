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

    def test_grid_refinement_reduces_analytical_error(self):
        exact = 1.0 - average_degree_of_consolidation(0.025, 1.0, 0.5)
        errors = []
        for n in (20, 40, 80):
            dx = 1.0 / n
            dt = 0.02 * dx * dx
            steps = round(0.025 / dt)
            result = solve_1d_pressure_diffusion([1.0]*n, [1.0]*n,
                                                 1.0, dt, steps)
            errors.append(abs(result["mean_pressure_pa"][-1] - exact))
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])

    def test_time_refinement_reduces_analytical_error(self):
        exact = 1.0 - average_degree_of_consolidation(0.025, 1.0, 0.5)
        errors = []
        for dt in (1e-4, 5e-5, 2.5e-5):
            steps = round(0.025 / dt)
            result = solve_1d_pressure_diffusion([1.0]*40, [1.0]*40,
                                                 1.0, dt, steps)
            errors.append(abs(result["mean_pressure_pa"][-1] - exact))
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])

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

    def test_layer_interface_location_refinement(self):
        # A non-grid-aligned material interface checks convergence when its
        # represented location shifts with cell-centred discretisation.
        # The finest-grid result is a numerical reference, not an exact solution.
        interface_x = 0.37
        final_time = 0.005
        dt = 1.0e-5

        def run(n):
            dx = 1.0 / n
            centers = [(i + 0.5) * dx for i in range(n)]
            mobility = [1.0 if x < interface_x else 0.1 for x in centers]
            result = solve_1d_pressure_diffusion(
                [1.0] * n, mobility, 1.0, dt, round(final_time / dt))
            return result["mean_pressure_pa"][-1]

        reference = run(320)
        errors = [abs(run(n) - reference) for n in (40, 80, 160)]
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])

    def test_global_integrated_outflow_matches_storage_loss(self):
        n = 40
        storage = [1.0] * 24 + [2.0] * 16
        mobility = [1.0] * 24 + [0.15] * 16
        dt, steps, thickness = 1.0e-5, 500, 1.0
        result = solve_1d_pressure_diffusion(
            storage, mobility, thickness, dt, steps)
        dx = thickness / n
        initial_storage = sum(s * dx for s in storage)
        final_storage = sum(
            storage[i] * dx * p
            for i, p in enumerate(result["profiles_pa"][-1]))
        integrated_outflow = dt * sum(result["boundary_outflow_m_s"][1:])
        self.assertAlmostEqual(
            initial_storage - final_storage, integrated_outflow, delta=1e-10)

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
