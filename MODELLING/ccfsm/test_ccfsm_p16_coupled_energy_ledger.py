import unittest
from dataclasses import replace

from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p16_coupled_energy_ledger import p16_coupled_energy_ledger


class TestCCFSMP16CoupledEnergyLedger(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(3, 0.01)
        self.chem = ChemicalParametersP2(
            100., 298.15, (0.2, 0.1, 0.05), (2., 0.5, 1.5),
            (1., 1.1, 0.9, 1.05))
        self.mech = P9Parameters(
            2e6, 1e6, 1e7, .8, .01, 15/51, 1., .3, 0.,
            1e-12, 2., 5., 15/51)
        self.theta = (.30, .30, .30)
        self.fields = (
            (30., 31., 32.), (20., 19., 18.),
            (35., 35., 35.), (15., 15., 15.))

    def audit(self, pressure=0., left=(30.,20.), right=(32.,18.),
              d=(1e-10,2e-10), mech=None, fields=None):
        return p16_coupled_energy_ledger(
            self.theta, fields or self.fields, self.grid, mech or self.mech,
            self.chem, d, pressure, left, right)

    def test_declared_chain_rule_decomposition_closes(self):
        r = self.audit()
        self.assertTrue(r["declared_conjugate_chain_rule_decomposition_verified"])
        self.assertAlmostEqual(r["chain_rule_decomposition_residual_w_m2"], 0., delta=1e-8)
        self.assertTrue(r["mobile_transport_component_verified"])
        self.assertTrue(r["reaction_dissipation_nonnegative"])

    def test_hydraulic_boundary_power_and_all_face_dissipation(self):
        r = self.audit(pressure=2e4)
        self.assertTrue(r["hydraulic_pressure_work_identity_verified"])
        self.assertGreaterEqual(r["darcy_dissipation_all_faces_w_m2"], 0.)
        self.assertAlmostEqual(r["hydraulic_balance_residual_w_m2"], 0., delta=1e-7)

    def test_reaction_power_is_negative_dissipation(self):
        r = self.audit()
        self.assertAlmostEqual(
            r["reaction_chemical_power_w_m2"],
            -r["reaction_dissipation_w_m2"], delta=1e-8)

    def test_mechanical_variational_closure_is_verified(self):
        changed = (
            (30.,31.,32.), (20.,19.,18.),
            (34.,35.,36.), (16.,15.,14.))
        r = self.audit(fields=changed)
        self.assertTrue(r["p9_mechanical_variational_closure_verified"])
        self.assertFalse(r["complete_thermodynamic_energy_theorem_established"])

    def test_nonzero_traction_not_claimed_closed(self):
        loaded = replace(self.mech, applied_axial_traction_pa=1000.)
        r = self.audit(mech=loaded)
        self.assertFalse(r["mechanical_boundary_work_included"])
        self.assertFalse(r["complete_thermodynamic_energy_theorem_established"])

    def test_zero_diffusivity_limit(self):
        r = self.audit(d=(0.,0.))
        self.assertTrue(r["declared_conjugate_chain_rule_decomposition_verified"])


if __name__ == "__main__":
    unittest.main()
