import math
import unittest

from geometry_scaling import (
    apparent_radial_diffusivity,
    finite_cylinder_first_mode_time_constant,
    radial_first_mode_time_constant,
)


class RadialGeometryScalingTests(unittest.TestCase):
    def test_cylinder_first_mode_relation_and_inverse(self):
        radius, diffusivity = 0.006, 2.5e-10
        tau = radial_first_mode_time_constant("cylinder", radius, diffusivity)
        recovered = apparent_radial_diffusivity("cylinder", radius, tau)
        self.assertAlmostEqual(recovered / diffusivity, 1.0, places=14)

    def test_sphere_first_mode_relation_and_inverse(self):
        radius, diffusivity = 0.0015, 8.0e-11
        tau = radial_first_mode_time_constant("sphere", radius, diffusivity)
        expected = radius**2 / (math.pi**2 * diffusivity)
        self.assertAlmostEqual(tau / expected, 1.0, places=14)
        self.assertAlmostEqual(
            apparent_radial_diffusivity("sphere", radius, tau) / diffusivity,
            1.0, places=14)

    def test_time_constant_scales_with_radius_squared(self):
        tau1 = radial_first_mode_time_constant("sphere", 1e-3, 1e-10)
        tau2 = radial_first_mode_time_constant("sphere", 2e-3, 1e-10)
        self.assertAlmostEqual(tau2 / tau1, 4.0, places=14)

    def test_finite_cylinder_drained_ends_accelerate_first_mode(self):
        radius, height, diffusivity = 0.006, 0.020, 1e-10
        radial_only = radial_first_mode_time_constant("cylinder", radius, diffusivity)
        finite_drained = finite_cylinder_first_mode_time_constant(
            radius, height, diffusivity, end_boundary="drained")
        finite_sealed = finite_cylinder_first_mode_time_constant(
            radius, height, diffusivity, end_boundary="sealed")
        self.assertLess(finite_drained, radial_only)
        self.assertAlmostEqual(finite_sealed / radial_only, 1.0, places=14)

    def test_finite_cylinder_height_and_radius_scaling(self):
        base = finite_cylinder_first_mode_time_constant(0.006, 0.020, 1e-10)
        taller = finite_cylinder_first_mode_time_constant(0.006, 0.040, 1e-10)
        wider = finite_cylinder_first_mode_time_constant(0.012, 0.020, 1e-10)
        self.assertGreater(taller, base)
        self.assertGreater(wider, base)

    def test_finite_cylinder_validates_boundary_and_dimensions(self):
        with self.assertRaises(ValueError):
            finite_cylinder_first_mode_time_constant(1, 1, 1, "mixed")
        for values in ((0, 1, 1), (1, -1, 1), (1, 1, float("nan"))):
            with self.assertRaises(ValueError):
                finite_cylinder_first_mode_time_constant(*values)

    def test_rejects_invalid_geometry_and_non_finite_values(self):
        with self.assertRaises(ValueError):
            radial_first_mode_time_constant("slab", 1.0, 1.0)
        for invalid in (0.0, -1.0, float("nan"), float("inf")):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    radial_first_mode_time_constant("sphere", invalid, 1.0)
                with self.assertRaises(ValueError):
                    apparent_radial_diffusivity("cylinder", 1.0, invalid)


if __name__ == "__main__":
    unittest.main()
