#!/usr/bin/env python3
"""Manufactured-solution verification for smooth heterogeneous S(x), lambda(x)."""
import math
import unittest
from heterogeneous_1d import solve_1d_pressure_diffusion

LENGTH = 1.0
FINAL_TIME = 0.02


def storage(x):
    return 1.0 + 0.4*x


def mobility(x):
    return 1.0 + 0.3*x


def exact_pressure(x, t):
    return math.exp(-t) * math.sin(math.pi*x/LENGTH)


def manufactured_source(x, t):
    """f=S*p_t-(lambda*p_x)_x for S*p_t=(lambda*p_x)_x+f."""
    pi = math.pi
    decay = math.exp(-t)
    phase = pi*x/LENGTH
    p = decay*math.sin(phase)
    px = decay*(pi/LENGTH)*math.cos(phase)
    pxx = -((pi/LENGTH)**2)*p
    lam = mobility(x)
    lam_x = 0.3
    divergence = lam_x*px + lam*pxx
    return -storage(x)*p - divergence


class ManufacturedSolutionTests(unittest.TestCase):
    def run_case(self, n, dt):
        dx = LENGTH/n
        centres = [(i+0.5)*dx for i in range(n)]
        result = solve_1d_pressure_diffusion(
            [storage(x) for x in centres], [mobility(x) for x in centres],
            LENGTH, dt, round(FINAL_TIME/dt),
            initial_pressure_profile_pa=[exact_pressure(x, 0.0) for x in centres],
            source_term_s_inv=manufactured_source)
        numerical = result["profiles_pa"][-1]
        errors = [numerical[i]-exact_pressure(centres[i], FINAL_TIME) for i in range(n)]
        l2 = math.sqrt(sum(e*e for e in errors)/n)
        linf = max(abs(e) for e in errors)
        return result, l2, linf

    def test_spatial_refinement_with_second_order_time_scaling(self):
        errors = []
        for n in (20, 40, 80):
            dx = LENGTH/n
            _, l2, _ = self.run_case(n, 0.05*dx*dx)
            errors.append(l2)
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])
        self.assertGreater(errors[0]/errors[1], 2.5)
        self.assertGreater(errors[1]/errors[2], 2.5)

    def test_time_refinement_at_fixed_grid(self):
        # Compare against a much smaller-dt solution on the same grid, thereby
        # isolating temporal error from the fixed spatial truncation error.
        n = 40
        reference, _, _ = self.run_case(n, 1e-5)
        reference_profile = reference["profiles_pa"][-1]
        errors = []
        for dt in (4e-4, 2e-4, 1e-4):
            result, _, _ = self.run_case(n, dt)
            profile = result["profiles_pa"][-1]
            errors.append(math.sqrt(sum((a-b)**2 for a, b in
                                        zip(profile, reference_profile))/n))
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])
        self.assertGreater(errors[0]/errors[1], 1.8)
        self.assertGreater(errors[1]/errors[2], 1.8)

    def test_manufactured_source_global_balance(self):
        result, _, _ = self.run_case(40, 1e-4)
        self.assertLess(max(abs(v) for v in result["balance_residual_m"][1:]), 2e-12)

    def test_initial_profile_and_boundary_conditions(self):
        result, _, _ = self.run_case(32, 1e-4)
        self.assertEqual(result["profiles_pa"][0][0], exact_pressure(0.5/32, 0.0))
        self.assertTrue(all(math.isfinite(v) for p in result["profiles_pa"] for v in p))
        self.assertTrue(all(v >= 0.0 for p in result["profiles_pa"] for v in p))

    def test_rejects_invalid_initial_profile_and_nonfinite_source(self):
        with self.assertRaises(ValueError):
            solve_1d_pressure_diffusion([1.0]*4, [1.0]*4, 1.0, 0.1, 1,
                                        initial_pressure_profile_pa=[1.0])
        with self.assertRaises(ValueError):
            solve_1d_pressure_diffusion([1.0]*4, [1.0]*4, 1.0, 0.1, 1,
                                        source_term_s_inv=lambda x, t: float('nan'))


if __name__ == "__main__":
    unittest.main()
