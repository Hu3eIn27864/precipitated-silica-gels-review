import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p11_energy_time_integration import P11State
from ccfsm_p12_energy_budget_audit import p12_energy_budget_audit


class TestCCFSMP12EnergyBudgetAudit(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(3, 0.01)
        self.chem = ChemicalParametersP2(
            100.0, 298.15, (0.2, 0.1, 0.05), (2.0, 0.5, 1.5),
            (1.0, 1.1, 0.9, 1.05))
        self.mech = P9Parameters(
            lame_lambda_pa=2.0e6, shear_modulus_pa=1.0e6,
            biot_modulus_pa=1.0e7, biot_coefficient=0.8,
            bridge_eigenstrain=0.01, bridge_reference=15.0/51.0,
            bridge_regularization=1.0, reference_fluid_capacity=0.3,
            reference_axial_strain=0.0,
            reference_permeability_m2_per_pas=1.0e-12,
            bridge_permeability_sensitivity=2.0,
            strain_permeability_sensitivity=5.0,
            reference_bridge_fraction=15.0/51.0)
        self.state = P11State(
            (0.30, 0.30, 0.30),
            ((30., 30., 30.), (20., 20., 20.),
             (35., 35., 35.), (15., 15., 15.)), 0.0)

    def audit(self, pressure=0.0, concentrations=(0., 0.)):
        return p12_energy_budget_audit(
            self.state, self.grid, self.mech, self.chem, (0., 0.),
            pressure, concentrations, concentrations)

    def test_closed_zero_flow_case_has_zero_boundary_work(self):
        r = self.audit()
        self.assertTrue(r["complete_energy_identity_established"])
        self.assertAlmostEqual(r["hydraulic_reservoir_power_w_m2"], 0.0)
        self.assertAlmostEqual(r["mobile_silicon_boundary_power_estimate_w_m2"], 0.0)
        self.assertAlmostEqual(r["total_boundary_power_estimate_w_m2"], 0.0)

    def test_open_hydraulic_boundary_is_reported_not_called_complete(self):
        r = self.audit(pressure=1.0e5)
        self.assertFalse(r["complete_energy_identity_established"])
        self.assertNotEqual(r["hydraulic_boundary_fluxes_m_s"], (0.0, 0.0))
        self.assertTrue(r["unclosed_energy_rate_residual_w_m2"] == r["unclosed_energy_rate_residual_w_m2"])

    def test_boundary_chemical_power_is_explicitly_approximate(self):
        r = self.audit(pressure=0.0, concentrations=(0.1, 0.05))
        self.assertFalse(r["boundary_chemical_power_is_exact_discrete_entropy_flux"])
        self.assertEqual(len(r["mobile_silicon_boundary_power_by_species_w_m2"]), 2)

    def test_nonzero_traction_is_flagged_as_incomplete(self):
        from dataclasses import replace
        loaded = replace(self.mech, applied_axial_traction_pa=1000.0)
        r = p12_energy_budget_audit(self.state, self.grid, loaded,
            self.chem, (0., 0.), 0.0)
        self.assertFalse(r["complete_energy_identity_established"])
        self.assertFalse(r["mechanical_work_included"])

    def test_energy_and_dissipation_diagnostics_are_finite(self):
        r = self.audit()
        for key in ("stored_free_energy_j_m2", "stored_free_energy_rate_w_m2",
                    "hydraulic_reservoir_power_w_m2",
                    "mobile_silicon_boundary_power_estimate_w_m2",
                    "unclosed_energy_rate_residual_w_m2",
                    "reaction_dissipation_w_m2"):
            self.assertTrue(abs(r[key]) < float("inf"))


if __name__ == "__main__":
    unittest.main()
