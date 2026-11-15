import unittest

from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p11_energy_time_integration import P11State
from ccfsm_p22_iterated_implicit_coupling import p22_iterated_implicit_step
from ccfsm_p24_newton_reference import (
    p24_newton_reference_step, p24_compare_with_p22,
)


class TestP24NewtonReference(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(2, 1.0)
        self.chem = ChemicalParametersP2(
            1000., 298.15, (.01, .01, .01), (1., 1., 1.))
        self.mech = P9Parameters(
            2e6, 1e6, 1e7, .8, .01, .2, 1e-12, .5, 0.,
            1e-12, .0, .0, .2, 0.)
        self.state = P11State(
            (.51, .52),
            ((100., 110.), (80., 85.), (300., 310.), (100., 105.)), 0.)
        self.quad = [
            {"cell_index": 0, "B": [
                [-1., 1., 0.], [0., 0., 0.], [0., 0., 0.],
                [0., 0., 0.], [0., 0., 0.], [0., 0., 0.]], "weight": .5},
            {"cell_index": 1, "B": [
                [0., -1., 1.], [0., 0., 0.], [0., 0., 0.],
                [0., 0., 0.], [0., 0., 0.], [0., 0., 0.]], "weight": .5},
        ]

    def solve_newton(self, **kwargs):
        return p24_newton_reference_step(
            self.state, 1e-12, self.grid, self.mech, self.chem, (0., 0.),
            0., self.quad, {0: 0.}, **kwargs)

    def solve_picard(self):
        return p22_iterated_implicit_step(
            self.state, 1e-12, self.grid, self.mech, self.chem, (0., 0.),
            0., self.quad, {0: 0.},
            state_tolerance=1e-7, pressure_tolerance=1e-7)

    def test_newton_reference_converges_and_preserves_admissibility(self):
        result = self.solve_newton()
        self.assertTrue(result["converged"], result.get("failure"))
        self.assertLessEqual(result["scaled_residual_inf"], 1e-10)
        self.assertTrue(result["positivity_verified"])
        self.assertTrue(result["pressure_snapshot_matches_accepted_state"])
        self.assertTrue(result["shared_invariant_limiter_used"])
        self.assertAlmostEqual(result["state"].time_s, 1e-12)

    def test_newton_and_picard_solve_same_discrete_step(self):
        p22 = self.solve_picard()
        p24 = self.solve_newton()
        self.assertTrue(p22["converged"], p22.get("failure"))
        self.assertTrue(p24["converged"], p24.get("failure"))
        comparison = p24_compare_with_p22(p22, p24, self.grid)
        self.assertTrue(comparison["same_accepted_time"])
        self.assertLess(comparison["state_relative_difference_inf"], 1e-6)
        self.assertLess(
            comparison["projected_pressure_relative_difference_inf"], 1e-6)

    def test_iteration_limit_does_not_accept_state(self):
        result = self.solve_newton(max_iterations=1, tolerance=1e-30)
        self.assertFalse(result["converged"])
        self.assertIsNone(result["state"])
        self.assertEqual(result["failure"], "newton_iteration_limit_reached")

    def test_comparison_rejects_nonconverged_input(self):
        with self.assertRaises(ValueError):
            p24_compare_with_p22({"converged": False},
                                 {"converged": False}, self.grid)


if __name__ == "__main__":
    unittest.main()
