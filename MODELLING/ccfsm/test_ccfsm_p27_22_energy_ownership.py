import unittest
from types import SimpleNamespace
from ccfsm_p9_mechanical_feedback import P9Parameters,p9_cell_closure
from ccfsm_p19_spatial_biot_bvp import P19Parameters,p19_solve_spatial_biot_bvp
from ccfsm_p27_22_energy_ownership import audit_p9_p19_energy_equivalence

class P27_22Tests(unittest.TestCase):
    def setUp(self):
        self.p9=P9Parameters(2e6,1e6,5e6,.6,.02,.1,.1,.8,0.,1e-18,1.,1.)
        self.p19=P19Parameters(2e6,1e6,5e6,.6)
        chem=SimpleNamespace(temperature_k=298.15,reference_concentration=1000.,
          activity_coefficients=(1.,1.,1.,1.),equilibrium_constants=(1.,1.,1.))
        cell=p9_cell_closure(.82,(.2,.3),(.4,.1),chem,self.p9)
        self.cells=[cell]
        self.q=[{"B":[[1.],[0.],[0.],[0.],[0.],[0.]],"weight":2.5,
          "eigenstrain":cell["chemical_eigenstrain"],
          "fluid_content_increment":cell["fluid_content_increment"]}]
        self.result=p19_solve_spatial_biot_bvp(1,self.q,self.p19,{})
    def audit(self,**kw):
        return audit_p9_p19_energy_equivalence(self.cells,self.p9,self.p19,self.q,
          self.result["displacement_dofs"],self.result,**kw)
    def test_equivalence_and_exclusive_owner(self):
        r=self.audit()
        self.assertEqual(r["status"],"matched_p9_p19_mechanical_energy")
        self.assertTrue(r["mechanical_terms_added_once"])
        self.assertAlmostEqual(r["selected_mechanical_energy_j"],self.result["stored_energy_j"])
        self.assertNotEqual(r["selected_chemical_energy_j"],0.)
    def test_p9_can_own_mechanics(self):
        r=self.audit(mechanical_energy_owner="p9")
        self.assertAlmostEqual(r["selected_mechanical_energy_j"],self.result["stored_energy_j"])
    def test_parameter_mismatch_rejected(self):
        bad=P19Parameters(3e6,1e6,5e6,.6)
        with self.assertRaisesRegex(ValueError,"material mismatch"):
            audit_p9_p19_energy_equivalence(self.cells,self.p9,bad,self.q,
              self.result["displacement_dofs"],self.result)
    def test_state_mismatch_rejected(self):
        q=[dict(self.q[0],eigenstrain=0.)]
        with self.assertRaisesRegex(ValueError,"state mismatch"):
            audit_p9_p19_energy_equivalence(self.cells,self.p9,self.p19,q,
              self.result["displacement_dofs"],self.result)
    def test_invalid_owner_rejected(self):
        with self.assertRaisesRegex(ValueError,"mechanical_energy_owner"):
            self.audit(mechanical_energy_owner="both")

if __name__=="__main__": unittest.main()
