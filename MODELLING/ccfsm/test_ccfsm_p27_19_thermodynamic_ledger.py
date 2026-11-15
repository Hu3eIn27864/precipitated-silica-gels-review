"""Regression tests for P27.19."""
import unittest
from ccfsm_p27_19_thermodynamic_ledger import audit_thermodynamic_ledger


class P2719Tests(unittest.TestCase):
    def test_closed_system_balance(self):
        r = audit_thermodynamic_ledger({"chemical": -2.0, "mechanical": -1.0},
            {"onsager": 2.0, "reaction": 1.0}, {"reservoir": 0.0})
        self.assertTrue(r["overall_pass"])
        self.assertAlmostEqual(r["independent_balance_residual_w_m2"], 0.0)

    def test_open_system_external_power(self):
        r = audit_thermodynamic_ledger({"chemical": 1.0}, {"diffusion": 2.0}, {"reservoir": 3.0})
        self.assertTrue(r["balance_pass"])

    def test_energy_defect_detected(self):
        r = audit_thermodynamic_ledger({"chemical": -2.5}, {"diffusion": 2.0}, {"boundary": 0.0})
        self.assertFalse(r["overall_pass"])
        self.assertFalse(r["balance_pass"])

    def test_negative_dissipation_rejected(self):
        r = audit_thermodynamic_ledger({"e": 0.0}, {"bad": -1.0}, {"p": 0.0})
        self.assertEqual(r["status"], "invalid_or_malformed_input")

    def test_reaction_affinity_sign(self):
        good = audit_thermodynamic_ledger({"e": -1.0}, {"rxn": 1.0}, {"p": 0.0},
            reaction_affinity_rate_pairs=[(2.0, 0.5)])
        bad = audit_thermodynamic_ledger({"e": -1.0}, {"rxn": 1.0}, {"p": 0.0},
            reaction_affinity_rate_pairs=[(-2.0, 0.5)])
        self.assertTrue(good["reaction_dissipation_pass"])
        self.assertFalse(bad["overall_pass"])

    def test_optional_onsager_gate(self):
        good = audit_thermodynamic_ledger({"e": -1.0}, {"d": 1.0}, {"p": 0.0},
            onsager_audit={"overall_pass": True})
        bad = audit_thermodynamic_ledger({"e": -1.0}, {"d": 1.0}, {"p": 0.0},
            onsager_audit={"overall_pass": False})
        self.assertTrue(good["overall_pass"])
        self.assertFalse(bad["overall_pass"])

    def test_darcy_constitutive_identity(self):
        r = audit_thermodynamic_ledger({"e": -1.0}, {"darcy": 1.0}, {"p": 0.0},
            darcy_faces_m_s=(0.0, -2.0, -3.0, 0.0),
            darcy_permeability_faces_m2_per_pas=(1.0, 2.0, 3.0, 1.0),
            pressure_gradient_faces_pa_m=(0.0, 1.0, 1.0, 0.0))
        self.assertTrue(r["darcy_check"]["constitutive_pass"])

    def test_darcy_sign_error_detected(self):
        r = audit_thermodynamic_ledger({"e": -1.0}, {"darcy": 1.0}, {"p": 0.0},
            darcy_faces_m_s=(0.0, 2.0, -3.0, 0.0),
            darcy_permeability_faces_m2_per_pas=(1.0, 2.0, 3.0, 1.0),
            pressure_gradient_faces_pa_m=(0.0, 1.0, 1.0, 0.0))
        self.assertFalse(r["overall_pass"])

    def test_invalid_darcy_lengths(self):
        r = audit_thermodynamic_ledger({"e": 0.0}, {"d": 0.0}, {"p": 0.0},
            darcy_faces_m_s=(0.0, 1.0, 0.0),
            darcy_permeability_faces_m2_per_pas=(1.0, 1.0),
            pressure_gradient_faces_pa_m=(0.0, 1.0, 0.0))
        self.assertEqual(r["status"], "invalid_or_malformed_input")


if __name__ == "__main__":
    unittest.main()
