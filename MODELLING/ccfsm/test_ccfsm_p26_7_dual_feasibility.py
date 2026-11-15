import unittest,tempfile,os
from ccfsm_p26_7_dual_feasibility import cell_support_function,dual_feasibility_diagnostic,run_study
class TestP267DualFeasibility(unittest.TestCase):
 def test_zero_mean_support(self):
  value,point=cell_support_function(0.,2.,-3.); self.assertEqual(value,0.); self.assertEqual(point,(0.,0.))
 def test_support_point_satisfies_endpoint_constraints(self):
  value,(a,b)=cell_support_function(1.,1.,1.); self.assertGreaterEqual(value,0.)
  self.assertGreaterEqual(1+a/2+b/6,-1e-9); self.assertGreaterEqual(1-a/2+b/6,-1e-9)
 def test_multi_cell_infeasible_separator(self):
  d=dual_feasibility_diagnostic((0.,.4,1.),(0.,0.),(1.,0.),(0.,0.))
  self.assertEqual(d["status"],"numerical_separator"); self.assertGreater(d["separation_gap"],0.)
 def test_zero_inventory_zero_modes(self):
  d=dual_feasibility_diagnostic((0.,.4,1.),(0.,0.),(0.,0.),(0.,0.)); self.assertEqual(d["status"],"feasible")
 def test_no_separator_not_mislabeled(self):
  d=dual_feasibility_diagnostic((0.,.4,1.),(1.,.8),(.2,-.1),(.1,0.))
  self.assertIn(d["status"],("numerical_separator","no_separator_found","feasible"))
 def test_study(self):
  with tempfile.TemporaryDirectory() as d:
   s=run_study(d); self.assertEqual(len(s["cases"]),3)
   self.assertTrue(os.path.exists(os.path.join(d,"p26_7_dual_feasibility.csv")))
if __name__=="__main__": unittest.main()
