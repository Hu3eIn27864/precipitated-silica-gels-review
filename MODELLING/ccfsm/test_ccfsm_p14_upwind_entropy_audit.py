import unittest
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p14_upwind_entropy_audit import p14_upwind_entropy_audit

class TestCCFSMP14UpwindEntropy(unittest.TestCase):
 def setUp(self): self.grid=P8Grid(3,0.01)
 def audit(self,q=(0.,1e-6,2e-6,0.),theta=(.2,.3,.4),c=(10.,20.,5.),reservoirs=(7.,8.)):
  return p14_upwind_entropy_audit(theta,tuple(theta[j]*c[j] for j in range(3)),q,self.grid,reservoirs,1.)
 def test_exact_identity(self): self.assertTrue(self.audit()["entropy_balance_identity_verified"])
 def test_production_nonnegative_both_directions(self):
  for q in ((0.,1e-6,2e-6,0.),(0.,-1e-6,-2e-6,0.),(0.,1e-6,-2e-6,0.)):
   self.assertGreaterEqual(self.audit(q=q)["upwind_internal_entropy_production_w_m2"],0.)
 def test_uniform_state_zero_production(self):
  r=self.audit(q=(0.,1e-6,-2e-6,0.),c=(12.,12.,12.),reservoirs=(12.,12.))
  self.assertAlmostEqual(r["upwind_internal_entropy_production_w_m2"],0.)
 def test_closed_no_flow(self):
  r=self.audit(q=(0.,0.,0.,0.)); self.assertEqual(r["mobile_entropy_rate_w_m2"],0.); self.assertEqual(r["advective_boundary_entropy_power_w_m2"],0.)
 def test_variable_capacity(self): self.assertTrue(self.audit(theta=(.1,.5,.8))["entropy_balance_identity_verified"])
 def test_reverse_flow_donor(self):
  r=self.audit(q=(0.,-1e-6,-2e-6,0.)); self.assertTrue(r["entropy_balance_identity_verified"]); self.assertEqual(r["upwind_face_concentrations_mol_m3"][1],20.)
 def test_invalid_inputs(self):
  with self.assertRaises(ValueError): p14_upwind_entropy_audit((.2,.3,.4),(0.,6.,2.),(0.,0.,0.,0.),self.grid)
  with self.assertRaises(ValueError): p14_upwind_entropy_audit((.2,.3,.4),(2.,6.,2.),(0.,0.),self.grid)
if __name__=="__main__": unittest.main()