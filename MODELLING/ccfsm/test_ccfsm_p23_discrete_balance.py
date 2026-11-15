import unittest
from unittest.mock import patch

from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p11_energy_time_integration import P11State
from ccfsm_p23_discrete_balance import p23_audit_accepted_step


class TestP23DiscreteBalance(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(2, 0.5)
        self.initial = P11State(
            (0.5, 0.5),
            ((1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)), 0.0)
        # Total Si change = 0.1 mol/m2. Boundary influx = dt*(0.3-0.1).
        self.accepted = P11State(
            (0.5, 0.5),
            ((1.1, 1.1), (2.0, 2.0), (3.0, 3.0), (4.0, 4.0)), 0.5)
        self.result = {
            "converged": True, "accepted_dt_s": 0.5,
            "state": self.accepted,
            "last_snapshot": {
                "transport_rhs": {
                    "mobile_species_face_fluxes_mol_m2_s": (
                        (0.2, 9.0, 0.1), (0.1, -3.0, 0.0)),
                },
                "spatial_mechanics": {
                    "stored_energy_j": 12.0,
                    "boundary_traction_work_j": 2.0,
                    "dirichlet_reaction_residual": 1e-12,
                    "free_dof_equilibrium_verified": True,
                },
            },
        }
        self.parameters = object()
        self.chemistry = object()

    @patch("ccfsm_p23_discrete_balance.p11_total_free_energy")
    def test_closed_boundary_silicon_conservation(self, energy):
        self.result["last_snapshot"]["transport_rhs"][
            "mobile_species_face_fluxes_mol_m2_s"] = (
                (0.0, 9.0, 0.0), (0.0, -3.0, 0.0))
        energy.side_effect = [1.0, 1.2]
        out = p23_audit_accepted_step(
            self.initial, self.result, self.grid,
            self.parameters, self.chemistry)
        self.assertTrue(out["silicon_balance_verified"])
        self.assertAlmostEqual(out["silicon_balance_residual_mol_m2"], 0.0)
        self.assertAlmostEqual(out["p9_local_free_energy_change_j_m2"], 0.2)

    @patch("ccfsm_p23_discrete_balance.p11_total_free_energy")
    def test_open_boundary_fluxes_enter_balance(self, energy):
        energy.side_effect = [1.0, 1.0]
        out = p23_audit_accepted_step(
            self.initial, self.result, self.grid,
            self.parameters, self.chemistry)
        self.assertAlmostEqual(out["open_boundary_silicon_influx_mol_m2"], 0.1)
        self.assertTrue(out["silicon_balance_verified"])

    def test_rejects_unaccepted_p22_step(self):
        bad = dict(self.result, converged=False)
        with self.assertRaises(ValueError):
            p23_audit_accepted_step(
                self.initial, bad, self.grid, self.parameters, self.chemistry)

    def test_does_not_claim_global_energy_closure(self):
        with patch("ccfsm_p23_discrete_balance.p11_total_free_energy",
                   side_effect=[1.0, 1.0]):
            out = p23_audit_accepted_step(
                self.initial, self.result, self.grid,
                self.parameters, self.chemistry)
        self.assertFalse(out["global_energy_balance_residual_available"])
        self.assertFalse(out["energy_monotonicity_claimed"])
        self.assertFalse(out["mechanical_energy_change_available"])


if __name__ == "__main__":
    unittest.main()
