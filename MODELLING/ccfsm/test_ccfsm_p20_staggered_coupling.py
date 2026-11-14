import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p20_staggered_coupling import p20_staggered_coupled_snapshot

class TestP20(unittest.TestCase):
 def setUp(self):
  self.grid=P8Grid(1,1.)
  self.chem=ChemicalParametersP2(1000.,298.15,(.01,.01,.01),(1.,1.,1.))
  self.mech=P9Parameters(2e6,1e6,1e7,.8,.01,.2,1e-12,.5,0.,1e-12,0.,0.,.2,0.)
  self.theta=[.51]; self.inv=[[100.],[80.],[300.],[100.]]
 def quadrature(self):
  return [{"cell_index":0,"B":[[-1.,1.],[0.,0.],[0.,0.],[0.,0.],[0.,0.],[0.,0.]],"weight":1.}]
 def run_model(self,q=None):
  return p20_staggered_coupled_snapshot(self.theta,self.inv,self.grid,
   self.mech,self.chem,(0.,0.),0.,self.quadrature() if q is None else q,{0:0.})
 def test_maps_bridge_and_fluid_state(self):
  r=self.run_model()
  self.assertAlmostEqual(r["mapped_fluid_content_increment"][0],.01)
  b=self.inv[3][0]/(self.inv[2][0]+self.inv[3][0]+self.mech.bridge_regularization)
  self.assertAlmostEqual(r["mapped_chemical_eigenstrain"][0],.01*(b-.2))
  self.assertTrue(r["mechanics_equilibrium_verified"])
  self.assertEqual(len(r["transport_rhs"]["inventory_dot"]),4)
 def test_pressure_comparison_is_diagnostic(self):
  r=self.run_model()
  self.assertEqual(len(r["spatial_minus_local_pressure_pa"]),1)
  self.assertTrue(r["pressure_comparison_is_not_a_residual"])
  self.assertFalse(r["two_way_transport_mechanics_feedback_implemented"])
 def test_rejects_bad_cell_mapping(self):
  q=self.quadrature(); q[0]["cell_index"]=2
  with self.assertRaises(ValueError): self.run_model(q)
 def test_rejects_inconsistent_fe_dofs(self):
  q=self.quadrature(); q.append({"cell_index":0,"B":[[-1.],[0.],[0.],[0.],[0.],[0.]],"weight":1.})
  with self.assertRaises(ValueError): self.run_model(q)
if __name__=="__main__": unittest.main()
