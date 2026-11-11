import math
import unittest

from poroelastic_coupling import (
    effective_consolidation_diffusivity,
    permeability_from_diffusivity,
)


class PoroelasticCouplingTests(unittest.TestCase):
    def test_classical_identity_and_inverse(self):
        k, modulus, gamma = 2e-18, 4e7, 9810.0
        cv = effective_consolidation_diffusivity(k, modulus, gamma)
        self.assertAlmostEqual(
            permeability_from_diffusivity(cv, modulus, gamma) / k,
            1.0, places=14)

    def test_permeability_and_modulus_are_separate_inputs(self):
        baseline = effective_consolidation_diffusivity(1e-18, 1e7)
        doubled_k = effective_consolidation_diffusivity(2e-18, 1e7)
        doubled_m = effective_consolidation_diffusivity(1e-18, 2e7)
        self.assertAlmostEqual(doubled_k / baseline, 2.0, places=14)
        self.assertAlmostEqual(doubled_m / baseline, 2.0, places=14)

    def test_invalid_inputs_rejected(self):
        for bad in (0.0, -1.0, float("nan"), float("inf")):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    effective_consolidation_diffusivity(bad, 1e7)
                with self.assertRaises(ValueError):
                    effective_consolidation_diffusivity(1e-18, bad)
                with self.assertRaises(ValueError):
                    permeability_from_diffusivity(1e-10, 1e7, bad)


if __name__ == "__main__":
    unittest.main()
