import unittest
from ccfsm_p27_15_coupled_invariant_domain import audit_coupled_fv_invariant_domain,audit_p21_rhs_step

class TestP2715(unittest.TestCase):
 def setUp(self):
  self.theta=(.5,.8); self.fields=((1.,2.),(2.,3.),(3.,4.),(4.,5.)); self.zero=((0.,0.),)*4
 def test_full_step(self):
  r=audit_coupled_fv_invariant_domain(self.theta,self.fields,(.01,-.01),self.zero,1.)
  self.assertTrue(r["overall_pass"]); self.assertEqual(r["limiting_factor"],1.)
 def test_inventory_limited(self):
  rhs=((-2.,0.),(0.,0.),(0.,0.),(0.,0.))
  r=audit_coupled_fv_invariant_domain(self.theta,self.fields,(0.,0.),rhs,1.)
  self.assertTrue(r["overall_pass"]); self.assertLess(r["limiting_factor"],1.)
  self.assertGreater(r["inventories"][0][0],0.)
 def test_theta_upper_bound(self):
  r=audit_coupled_fv_invariant_domain(self.theta,self.fields,(2.,0.),self.zero,1.)
  self.assertTrue(r["overall_pass"]); self.assertLessEqual(r["fluid_capacity"][0],1.)
 def test_bad_initial_state(self):
  r=audit_coupled_fv_invariant_domain((0.,.8),self.fields,(0.,0.),self.zero,1.)
  self.assertEqual(r["status"],"initial_state_outside_invariant_domain")
 def test_bad_controls(self):
  r=audit_coupled_fv_invariant_domain(self.theta,self.fields,(0.,0.),self.zero,0.)
  self.assertEqual(r["status"],"invalid_controls")
 def test_bad_shape(self):
  r=audit_coupled_fv_invariant_domain(self.theta,self.fields[:3],(0.,0.),self.zero,1.)
  self.assertEqual(r["status"],"invalid_or_malformed_input")
 def test_p21_adapter(self):
  snap={"transport_rhs":{"fluid_capacity_dot_s":(0.,0.),"inventory_dot":self.zero}}
  self.assertTrue(audit_p21_rhs_step(snap,self.theta,self.fields,.1)["overall_pass"])
 def test_no_physical_claim(self):
  r=audit_coupled_fv_invariant_domain(self.theta,self.fields,(0.,0.),self.zero,1.)
  self.assertFalse(r["implicit_residual_converged"]); self.assertFalse(r["physical_ccfsm_positivity_certified"])

if __name__=="__main__": unittest.main()
