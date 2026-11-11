import math
import unittest

from geometry_scaling import (
    apparent_radial_diffusivity,
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
