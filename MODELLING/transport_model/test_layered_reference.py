#!/usr/bin/env python3
"""Independent verification tests for the fixed-interface two-layer slab."""
import math
import unittest

from heterogeneous_1d import solve_1d_pressure_diffusion
from layered_reference import two_layer_eigenvalues, two_layer_mean_pressure_ratio


class FixedInterfaceLayeredReferenceTests(unittest.TestCase):
    # Interface is fixed at x=0.375 m and exactly coincides with a cell face
    # for all tested grids. Coefficients are discontinuous across that face.
    L = 1.0
    A = 0.375
    S1, LAMBDA1 = 1.0, 1.0
    S2, LAMBDA2 = 2.0, 0.15
    FINAL_TIME = 0.005

    def arrays(self, n):
        n_left = round(n * self.A / self.L)
        self.assertEqual(n_left * self.L / n, self.A)
        return ([self.S1] * n_left + [self.S2] * (n - n_left),
                [self.LAMBDA1] * n_left + [self.LAMBDA2] * (n - n_left))

    def exact(self, time_s):
        return two_layer_mean_pressure_ratio(
            time_s, self.S1, self.LAMBDA1, self.S2, self.LAMBDA2,
            self.L, self.A, n_modes=120)

    def test_eigenvalues_are_ordered_and_first_mode_regression(self):
        rates = two_layer_eigenvalues(
            self.S1, self.LAMBDA1, self.S2, self.LAMBDA2,
            self.L, self.A, n_modes=8)
        self.assertTrue(all(b > a for a, b in zip(rates, rates[1:])))
        self.assertAlmostEqual(rates[0], 1.580701502541381, places=9)

    def test_uniform_initial_condition_and_positive_modal_reference(self):
        self.assertEqual(self.exact(0.0), 1.0)
        values = [self.exact(t) for t in (0.001, 0.005, 0.02, 0.1)]
        self.assertTrue(all(0.0 < p < 1.0 for p in values))
        self.assertTrue(all(a > b for a, b in zip(values, values[1:])))

    def test_fixed_interface_fv_converges_to_independent_eigenfunction(self):
        errors = []
        for n in (40, 80, 160):
            storage, mobility = self.arrays(n)
            dt = 2.0e-6
            steps = round(self.FINAL_TIME / dt)
            result = solve_1d_pressure_diffusion(
                storage, mobility, self.L, dt, steps)
            errors.append(abs(result["mean_pressure_pa"][-1]
                               - self.exact(self.FINAL_TIME)))
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])
        self.assertLess(errors[-1], 3.0e-4)

    def test_time_refinement_against_fixed_interface_reference(self):
        n = 160
        storage, mobility = self.arrays(n)
        errors = []
        for dt in (8.0e-6, 4.0e-6, 2.0e-6):
            steps = round(self.FINAL_TIME / dt)
            result = solve_1d_pressure_diffusion(
                storage, mobility, self.L, dt, steps)
            errors.append(abs(result["mean_pressure_pa"][-1]
                               - self.exact(self.FINAL_TIME)))
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])

    def test_independently_reconstructed_boundary_flux_matches_storage_loss(self):
        n, dt, steps = 80, 2.0e-6, 2500
        storage, mobility = self.arrays(n)
        result = solve_1d_pressure_diffusion(
            storage, mobility, self.L, dt, steps)
        dx = self.L / n
        initial_storage = sum(s * dx for s in storage)
        final_storage = sum(storage[i] * dx * p
                            for i, p in enumerate(result["profiles_pa"][-1]))

        # Reconstruct Darcy boundary gradients directly from p=0 at each
        # boundary and the adjacent cell-centre pressure, without using the
        # solver's reported boundary_outflow_m_s array.
        integrated_flux = 0.0
        for profile in result["profiles_pa"][1:]:
            left_flux = mobility[0] * profile[0] / (0.5 * dx)
            right_flux = mobility[-1] * profile[-1] / (0.5 * dx)
            integrated_flux += dt * (left_flux + right_flux)
        storage_loss = initial_storage - final_storage
        self.assertAlmostEqual(storage_loss, integrated_flux, delta=5.0e-11)

    def test_reference_rejects_invalid_interface(self):
        with self.assertRaises(ValueError):
            two_layer_eigenvalues(1.0, 1.0, 2.0, 0.15, 1.0, 1.0, 5)


    def test_nonzero_interface_flux_eigenmode_converges(self):
        # Exact first eigenmode has nonzero interface gradient. Its amplitude
        # is chosen for pressure continuity; the characteristic equation
        # enforces continuity of lambda * dp/dx at x=A.
        sigma = two_layer_eigenvalues(
            self.S1, self.LAMBDA1, self.S2, self.LAMBDA2,
            self.L, self.A, n_modes=1)[0]
        k1 = math.sqrt(sigma * self.S1 / self.LAMBDA1)
        k2 = math.sqrt(sigma * self.S2 / self.LAMBDA2)
        b = self.L - self.A
        amplitude_right = math.sin(k1*self.A) / math.sin(k2*b)

        pressure_left_at_interface = math.sin(k1*self.A)
        pressure_right_at_interface = amplitude_right * math.sin(k2*b)
        flux_left = self.LAMBDA1 * k1 * math.cos(k1*self.A)
        flux_right = -self.LAMBDA2 * amplitude_right * k2 * math.cos(k2*b)
        self.assertAlmostEqual(pressure_left_at_interface,
                               pressure_right_at_interface, places=12)
        self.assertAlmostEqual(flux_left, flux_right, places=11)
        self.assertGreater(abs(flux_left), 0.1)  # not the trivial zero-flux case

        errors = []
        final_time = 0.05
        for n in (40, 80, 160):
            storage, mobility = self.arrays(n)
            dx = self.L / n
            centres = [(i+0.5)*dx for i in range(n)]
            initial_mode = [
                math.sin(k1*x) if x < self.A
                else amplitude_right*math.sin(k2*(self.L-x))
                for x in centres
            ]
            dt = 0.05*dx*dx
            result = solve_1d_pressure_diffusion(
                storage, mobility, self.L, dt, round(final_time/dt),
                initial_pressure_profile_pa=initial_mode)
            exact = [math.exp(-sigma*final_time)*v for v in initial_mode]
            numerical = result["profiles_pa"][-1]
            errors.append(math.sqrt(sum((u-v)**2 for u, v in
                                        zip(numerical, exact))/n))
        self.assertLess(errors[1], errors[0])
        self.assertLess(errors[2], errors[1])
        self.assertGreater(errors[0]/errors[1], 3.5)
        self.assertGreater(errors[1]/errors[2], 3.5)


if __name__ == "__main__":
    unittest.main()
