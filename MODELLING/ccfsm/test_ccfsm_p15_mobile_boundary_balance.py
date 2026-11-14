import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p11_energy_time_integration import P11State
from ccfsm_p15_mobile_boundary_balance import p15_mobile_boundary_balance


class TestCCFSMP15MobileBoundaryBalance(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(3, 0.01)
        self.chem = ChemicalParametersP2(
            100., 298.15, (0.2, 0.1, 0.05), (2., 0.5, 1.5),
            (1., 1.1, 0.9, 1.05))
        self.mech = P9Parameters(
            2e6, 1e6, 1e7, .8, .01, 15/51, 1., .3, 0.,
            1e-12, 2., 5., 15/51)
        self.state = P11State(
            (.30,.30,.30),
            ((30.,31.,32.), (20.,19.,18.), (35.,35.,35.), (15.,15.,15.)))

    def audit(self, d=(1e-10, 2e-10), left=(30.,20.), right=(32.,18.)):
        return p15_mobile_boundary_balance(
            self.state.fluid_capacity, self.state.inventories, self.grid,
            self.mech, self.chem, d, 0., left, right)

    def test_combined_identity(self):
        result = self.audit()
        self.assertTrue(result["all_mobile_species_balance_identities_verified"])
        for item in result["species_balances"]:
            self.assertAlmostEqual(item["balance_residual_w_m2"], 0., delta=1e-9)

    def test_zero_diffusion_reduces_to_upwind_component(self):
        result = self.audit((0., 0.))
        for item in result["species_balances"]:
            self.assertEqual(item["onsager_internal_dissipation_w_m2"], 0.)
            self.assertEqual(item["onsager_reservoir_interface_dissipation_w_m2"], 0.)
            self.assertEqual(item["reservoir_diffusive_chemical_power_w_m2"], 0.)
            self.assertTrue(item["balance_identity_verified"])

    def test_zero_advection_still_closes_diffusion_balance(self):
        # Equal external pressure and the reference mechanical state give
        # no flow for this homogeneous theta/inventory state.
        state = P11State((.30,.30,.30),
            ((30.,30.,30.), (20.,20.,20.), (35.,35.,35.), (15.,15.,15.)))
        result = p15_mobile_boundary_balance(
            state.fluid_capacity, state.inventories, self.grid, self.mech,
            self.chem, (1e-10, 2e-10), 0., (10.,15.), (40.,25.))
        self.assertTrue(result["all_mobile_species_balance_identities_verified"])

    def test_reverse_and_mixed_flow_balance(self):
        # Test the identity with flow directions determined by the coupled
        # Darcy field; no direction is assumed by the audit.
        result = self.audit(left=(100., 80.), right=(1., 2.))
        self.assertTrue(result["all_mobile_species_balance_identities_verified"])

    def test_invalid_reservoir_concentration(self):
        with self.assertRaises(ValueError):
            self.audit(left=(0., 20.))


if __name__ == "__main__":
    unittest.main()
