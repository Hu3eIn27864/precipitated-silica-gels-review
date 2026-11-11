"""Tests for dimensional poroelastic scaling (not physical silica validation)."""
import math
import unittest

from poroelastic_scaling import (
    characteristic_time_s,
    consolidation_diffusivity_m2_s,
    dimensionless_time,
    permeability_for_characteristic_time_m2,
)


class PoroelasticScalingTests(unittest.TestCase):
    def test_diffusivity_has_expected_scaling(self):
        cv = consolidation_diffusivity_m2_s(2.0e-18, 5.0e5, 1.0e-3)
        self.assertAlmostEqual(cv, 1.0e-9, places=20)
        self.assertAlmostEqual(
            consolidation_diffusivity_m2_s(4.0e-18, 5.0e5, 1.0e-3) / cv,
            2.0,
        )
        self.assertAlmostEqual(
            consolidation_diffusivity_m2_s(2.0e-18, 1.0e6, 1.0e-3) / cv,
            2.0,
        )

    def test_characteristic_time_and_inverse_are_consistent(self):
        target = 3600.0
        length = 1.0e-3
        modulus = 2.0e5
        viscosity = 1.0e-3
        permeability = permeability_for_characteristic_time_m2(
            target, length, modulus, viscosity
        )
        recovered = characteristic_time_s(
            length, permeability, modulus, viscosity
        )
        self.assertAlmostEqual(recovered, target, places=8)

    def test_dimensionless_time_is_dimensionless_scaling(self):
        values = (1.0e-18, 1.0e5, 1.0e-3)
        tv = dimensionless_time(100.0, 1.0e-3, *values)
        self.assertTrue(math.isfinite(tv))
        self.assertGreater(tv, 0.0)

    def test_rejects_nonphysical_inputs(self):
        for args in [
            (0.0, 1.0e5, 1.0e-3),
            (-1.0, 1.0e5, 1.0e-3),
            (1.0e-18, float("nan"), 1.0e-3),
        ]:
            with self.assertRaises(ValueError):
                consolidation_diffusivity_m2_s(*args)


if __name__ == "__main__":
    unittest.main()
