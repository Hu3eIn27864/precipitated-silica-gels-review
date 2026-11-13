#!/usr/bin/env python3
"""Manufactured transient-coefficient test using an exact time transformation."""
import math
import unittest
from time_dependent_1d import solve_1d_time_dependent_mobility
from layered_reference import two_layer_mean_pressure_ratio


class TimeDependentCoefficientReferenceTests(unittest.TestCase):
    def test_uniform_time_varying_mobility_against_exact_time_transform(self):
        # For spatially uniform lambda(t), S*p_t=lambda(t)*p_xx is the
        # constant-coefficient problem under theta=int(lambda/S dt).
        # Uniform initial pressure therefore has the known slab eigenseries.
        n, final_time = 64, 0.02
        exact_theta = final_time + 0.25*final_time**2  # lambda(t)=1+0.5t, S=1
        exact = two_layer_mean_pressure_ratio(
            exact_theta, 1.0, 1.0, 1.0, 1.0, 1.0, 0.4, n_modes=180)
        errors = []
        for dt in (2e-4, 1e-4, 5e-5):
            steps = round(final_time/dt)
            schedule = []
            for step in range(1, steps+1):
                t_new = step*dt
                lam = 1.0+0.5*t_new
                schedule.append([lam]*n)
            result = solve_1d_time_dependent_mobility(
                [1.0]*n, schedule, 1.0, dt)
            errors.append(abs(result["mean_pressure_pa"][-1]-exact))
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])

    def test_time_varying_mobility_conserves_storage_each_step(self):
        schedule = [[1.0+0.02*k]*24 for k in range(1, 41)]
        result = solve_1d_time_dependent_mobility(
            [1.5]*24, schedule, 1.0, 1e-4)
        self.assertLess(max(abs(v) for v in result["balance_residual_m"][1:]), 1e-12)
        self.assertTrue(all(p >= 0 for row in result["profiles_pa"] for p in row))


if __name__ == "__main__":
    unittest.main()
