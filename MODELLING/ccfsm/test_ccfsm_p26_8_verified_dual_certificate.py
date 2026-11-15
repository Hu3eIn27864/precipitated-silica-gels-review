import unittest
from fractions import Fraction
from ccfsm_p26_8_verified_dual_certificate import cell_support_upper,verify_dual_certificate,search_dual_certificate,_sqrt_upper

class TestP268VerifiedDual(unittest.TestCase):
 def test_sqrt_upper_is_exact_upper_bound(self):
  x=Fraction(2,3); u=_sqrt_upper(x,20); self.assertGreaterEqual(u*u,x)
 def test_cell_support_known_directions(self):
  self.assertEqual(cell_support_upper(0,3,2),0)
  self.assertEqual(cell_support_upper(1,0,1),Fraction(12))
  self.assertGreaterEqual(cell_support_upper(1,1,0),Fraction(0))
 def test_zero_inventory_nonzero_mode_certificate(self):
  r=search_dual_certificate((0.,.4,1.),(0.,0.),(1.,0.),(0.,0.),max_direction=4)
  self.assertEqual(r["status"],"certified_infeasible")
  self.assertTrue(r["certificate"]["verified"])
  self.assertGreater(Fraction(r["certificate"]["gap_lower_bound"]),0)
 def test_certificate_recomputes(self):
  r=verify_dual_certificate((0.,.4,1.),(0.,0.),(1.,0.),(0.,0.),(1,0))
  self.assertTrue(r["verified"])
  self.assertEqual(Fraction(r["gap_lower_bound"]),Fraction(r["gap_lower_numerator"],r["gap_lower_denominator"]))
 def test_zero_modes_no_false_certificate(self):
  r=search_dual_certificate((0.,.4,1.),(1.,.7),(0.,0.),(0.,0.),max_direction=4)
  self.assertFalse(r["verified"])
  self.assertEqual(r["status"],"no_certificate_found")
 def test_direction_must_be_nonzero(self):
  with self.assertRaises(ValueError):
   verify_dual_certificate((0.,1.),(1.,),(0.,),(0.,),(0,0))
if __name__=="__main__": unittest.main()
