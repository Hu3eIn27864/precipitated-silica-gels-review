import math
import unittest

from radial_consolidation import (
    analytical_radial_average,
    solve_radial_average,
)


class RadialConsolidationTests(unittest.TestCase):
    def test_initial_and_long_time_limits(self):
        for geometry in ("cylinder", "sphere"):
            values = solve_radial_average(
                geometry, [0.0, 0.1, 2.0], n_cells=80,
                max_fourier_step=0.005)
            self.assertEqual(values[0], 1.0)
            self.assertGreater(values[1], values[2])
            self.assertGreater(values[2], 0.0)
            self.assertLess(values[2], 1e-5)

    def test_matches_independent_eigenfunction_series(self):
        for geometry in ("cylinder", "sphere"):
            for fo in (0.02, 0.1, 0.5):
                numerical = solve_radial_average(
                    geometry, [fo], n_cells=120,
                    max_fourier_step=0.002)[0]
                analytical = analytical_radial_average(
                    geometry, fo, terms=10)
                self.assertAlmostEqual(numerical, analytical, delta=0.012)

    def test_refinement_converges_for_both_radial_geometries(self):
        fo = 0.1
        for geometry in ("cylinder", "sphere"):
            exact = analytical_radial_average(geometry, fo, terms=10)
            errors = []
            for n_cells, dt in ((30, 0.02), (60, 0.005), (120, 0.001)):
                value = solve_radial_average(
                    geometry, [fo], n_cells=n_cells,
                    max_fourier_step=dt)[0]
                errors.append(abs(value - exact))
            self.assertGreater(errors[0], errors[1])
            self.assertGreater(errors[1], errors[2])
            self.assertLess(errors[2], 0.002)

    def test_time_step_refinement_at_fixed_grid(self):
        fo = 0.1
        for geometry in ("cylinder", "sphere"):
            exact = analytical_radial_average(geometry, fo, terms=10)
            errors = []
            for dt in (0.02, 0.005, 0.001):
                value = solve_radial_average(
                    geometry, [fo], n_cells=120,
                    max_fourier_step=dt)[0]
                errors.append(abs(value - exact))
            self.assertGreater(errors[0], errors[1])
            self.assertGreater(errors[1], errors[2])

    def test_grid_and_time_refinement_reduce_error(self):
        fo = 0.1
        exact = analytical_radial_average("sphere", fo, terms=10)
        coarse = solve_radial_average(
            "sphere", [fo], n_cells=30, max_fourier_step=0.02)[0]
        fine = solve_radial_average(
            "sphere", [fo], n_cells=120, max_fourier_step=0.002)[0]
        self.assertLess(abs(fine - exact), abs(coarse - exact))

    def test_monotonicity_and_bounds(self):
        times = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2]
        for geometry in ("cylinder", "sphere"):
            values = solve_radial_average(
                geometry, times, n_cells=80, max_fourier_step=0.002)
            self.assertTrue(all(0.0 <= v <= 1.0 for v in values))
            self.assertTrue(all(values[i] >= values[i + 1]
                                for i in range(len(values) - 1)))

    def test_invalid_inputs(self):
        for geometry in ("cylindrical", "plane"):
            with self.assertRaises(ValueError):
                solve_radial_average(geometry, [0.1])
        for times in ([-0.1], [math.nan], [0.2, 0.1]):
            with self.assertRaises(ValueError):
                solve_radial_average("sphere", times)
        with self.assertRaises(ValueError):
            solve_radial_average("sphere", [0.1], n_cells=2)
        with self.assertRaises(ValueError):
            analytical_radial_average("cylinder", 0.1, terms=0)


if __name__ == "__main__":
    unittest.main()
