import unittest

from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p11_energy_time_integration import P11State
from ccfsm_p22_iterated_implicit_coupling import p22_iterated_implicit_step


class TestP22(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(2, 1.0)
        self.chem = ChemicalParametersP2(1000., 298.15, (.01,.01,.01), (1.,1.,1.))
        self.mech = P9Parameters(2e6,1e6,1e7,.8,.01,.2,1e-12,.5,0.,
                                 1e-12,.0,.0,.2,0.)
        self.state = P11State((.51,.52),
            ((100.,110.),(80.,85.),(300.,310.),(100.,105.)),0.)
        self.quad = [
            {"cell_index":0,"B":[[-1.,1.,0.],[0.,0.,0.],[0.,0.,0.],
                                  [0.,0.,0.],[0.,0.,0.],[0.,0.,0.]],"weight":.5},
            {"cell_index":1,"B":[[0.,-1.,1.],[0.,0.,0.],[0.,0.,0.],
                                  [0.,0.,0.],[0.,0.,0.],[0.,0.,0.]],"weight":.5},
        ]

    def run_model(self, **kwargs):
        return p22_iterated_implicit_step(
            self.state,1e-12,self.grid,self.mech,self.chem,(0.,0.),0.,
            self.quad,{0:0.},**kwargs)

    def test_converged_step_is_positive_and_advances_time(self):
        r=self.run_model(state_tolerance=1e-7,pressure_tolerance=1e-7)
        self.assertTrue(r["converged"],r.get("failure"))
        self.assertTrue(r["positivity_verified"])
        self.assertAlmostEqual(r["state"].time_s,1e-12)
        self.assertTrue(all(0 < x <= 1 for x in r["state"].fluid_capacity))
        self.assertTrue(all(x > 0 for row in r["state"].inventories for x in row))

    def test_nonconvergence_is_not_accepted(self):
        r=self.run_model(max_iterations=1)
        self.assertFalse(r["converged"])
        self.assertIsNone(r["state"])
        self.assertEqual(r["failure"],"picard_iteration_limit_reached")

    def test_invalid_relaxation_rejected(self):
        with self.assertRaises(ValueError):
            self.run_model(relaxation=0.)

    def test_pressure_residual_is_reported(self):
        r=self.run_model(state_tolerance=1e-7,pressure_tolerance=1e-7)
        self.assertIn("pressure_relative_residual",r)
        self.assertLessEqual(r["pressure_relative_residual"],1e-7)


if __name__ == "__main__":
    unittest.main()
