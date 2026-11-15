"""Regression tests for the P27.21 P9 variational audit."""
import unittest
from types import SimpleNamespace
from dataclasses import replace
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p27_21_variational_audit import audit_p9_free_energy_variations


class P2721Tests(unittest.TestCase):
    def setUp(self):
        self.chem = SimpleNamespace(
            temperature_k=298.15, reference_concentration=1000.0,
            activity_coefficients=(1.0, 1.0, 1.0, 1.0),
            equilibrium_constants=(1.0, 1.0, 1.0))
        self.params = P9Parameters(
            lame_lambda_pa=1.0e7, shear_modulus_pa=8.0e6,
            biot_modulus_pa=2.0e8, biot_coefficient=0.7,
            bridge_eigenstrain=0.01, bridge_reference=0.2,
            bridge_regularization=1.0e-4,
            reference_fluid_capacity=0.35, reference_axial_strain=0.0,
            reference_permeability_m2_per_pas=1.0e-18,
            bridge_permeability_sensitivity=1.0,
            strain_permeability_sensitivity=1.0,
            reference_bridge_fraction=0.2, applied_axial_traction_pa=0.0)

    def test_zero_load_variational_derivatives(self):
        r = audit_p9_free_energy_variations(0.4, (120.0, 90.0, 40.0, 20.0),
                                            self.chem, self.params)
        self.assertTrue(r["overall_pass"], r)
        self.assertEqual(r["status"], "p9_variational_derivatives_consistent")

    def test_energy_decomposition_is_explicit(self):
        r = audit_p9_free_energy_variations(0.4, (120.0, 90.0, 40.0, 20.0),
                                            self.chem, self.params)
        self.assertAlmostEqual(r["decomposition_sum_defect_j_m3"], 0.0, places=8)
        self.assertEqual(set(r["energy_decomposition_j_m3_reference"]),
                         {"elastic", "biot_storage", "chemical"})

    def test_nonzero_traction_warns_about_external_potential(self):
        loaded = replace(self.params, applied_axial_traction_pa=1.0e5)
        r = audit_p9_free_energy_variations(0.4, (120.0, 90.0, 40.0, 20.0),
                                            self.chem, loaded)
        self.assertIsNotNone(r["traction_potential_warning"])
        self.assertFalse(r["external_traction_potential_included_in_reported_energy"])

    def test_invalid_inventory_rejected(self):
        r = audit_p9_free_energy_variations(0.4, (120.0, 90.0, 40.0, 0.0),
                                            self.chem, self.params)
        self.assertFalse(r["overall_pass"])

    def test_theta_domain_rejected(self):
        r = audit_p9_free_energy_variations(1.1, (120.0, 90.0, 40.0, 20.0),
                                            self.chem, self.params)
        self.assertFalse(r["overall_pass"])


if __name__ == "__main__":
    unittest.main()
