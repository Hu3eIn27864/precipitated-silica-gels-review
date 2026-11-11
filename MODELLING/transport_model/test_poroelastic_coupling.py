import unittest

from poroelastic_coupling import (
    effective_diffusivity_from_hydraulic_conductivity,
    effective_diffusivity_from_intrinsic_permeability,
    hydraulic_conductivity_from_diffusivity,
    intrinsic_permeability_from_diffusivity,
)


class PoroelasticCouplingTests(unittest.TestCase):
    def test_hydraulic_conductivity_identity_and_inverse(self):
        conductivity, modulus, gamma = 2e-10, 4e7, 9810.0
        cv = effective_diffusivity_from_hydraulic_conductivity(
            conductivity, modulus, gamma)
        recovered = hydraulic_conductivity_from_diffusivity(
            cv, modulus, gamma)
        self.assertAlmostEqual(recovered / conductivity, 1.0, places=14)

    def test_intrinsic_permeability_identity_and_inverse(self):
        kappa, modulus, viscosity = 2e-18, 4e7, 1e-3
        cv = effective_diffusivity_from_intrinsic_permeability(
            kappa, modulus, viscosity)
        recovered = intrinsic_permeability_from_diffusivity(
            cv, modulus, viscosity)
        self.assertAlmostEqual(recovered / kappa, 1.0, places=14)

    def test_mechanical_and_hydraulic_inputs_remain_separate(self):
        baseline = effective_diffusivity_from_hydraulic_conductivity(1e-10, 1e7)
        doubled_k = effective_diffusivity_from_hydraulic_conductivity(2e-10, 1e7)
        doubled_m = effective_diffusivity_from_hydraulic_conductivity(1e-10, 2e7)
        self.assertAlmostEqual(doubled_k / baseline, 2.0, places=14)
        self.assertAlmostEqual(doubled_m / baseline, 2.0, places=14)

    def test_invalid_inputs_rejected(self):
        for bad in (0.0, -1.0, float("nan"), float("inf")):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    effective_diffusivity_from_hydraulic_conductivity(bad, 1e7)
                with self.assertRaises(ValueError):
                    effective_diffusivity_from_hydraulic_conductivity(1e-10, bad)
                with self.assertRaises(ValueError):
                    effective_diffusivity_from_intrinsic_permeability(
                        1e-18, 1e7, bad)


if __name__ == "__main__":
    unittest.main()
