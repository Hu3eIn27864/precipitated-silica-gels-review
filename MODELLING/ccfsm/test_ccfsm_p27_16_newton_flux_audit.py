import unittest
from ccfsm_p27_16_newton_flux_audit import limit_newton_direction,audit_fv_flux_balance,audit_p21_flux_balance

class TestP2716(unittest.TestCase):
 def test_unlimited_direction(self):
  r=limit_newton_direction((.4,.6),((1.,1.),)*4,(.01,-.01),((0.,0.),)*4)
  self.assertTrue(r["overall_pass"]); self.assertEqual(r["limiting_factor"],1.)
 def test_one_shared_factor(self):
  r=limit_newton_direction((.95,.5),((.1,1.),)*4,(.2,0.),((-1.,0.),)*4)
  self.assertTrue(r["overall_pass"]); self.assertLess(r["limiting_factor"],1.)
  self.assertTrue(r["all_fields_share_one_factor"])
  self.assertLessEqual(r["fluid_capacity"][0],1.)
  self.assertGreater(min(row[0] for row in r["inventories"]),0.)
 def test_local_and_global_balance(self):
  r=audit_fv_flux_balance(((-1.,-2.),),((0.,1.,3.),),((0.,0.),),(1.,1.))
  self.assertTrue(r["overall_pass"]); self.assertEqual(r["status"],"flux_balance_audited")
  self.assertAlmostEqual(r["fields"][0]["integrated_rhs_minus_source"],-3.)
 def test_nonconservative_rhs_detected(self):
  r=audit_fv_flux_balance(((-1.,-1.),),((0.,1.,3.),),((0.,0.),),(1.,1.))
  self.assertFalse(r["overall_pass"]); self.assertEqual(r["status"],"flux_balance_failed")
 def test_nonuniform_cells(self):
  r=audit_fv_flux_balance(((-2.,-1.),),((0.,2.,3.),),((0.,0.),),(.5,1.))
  self.assertTrue(r["overall_pass"])
 def test_bad_shape(self):
  r=audit_fv_flux_balance(((0.,),),((0.,1.),),((0.,),),(1.,1.))
  self.assertEqual(r["status"],"invalid_or_malformed_input")
 def test_p21_adapter(self):
  snap={"transport_rhs":{"fluid_capacity_dot_s":(-1.,),"inventory_dot":((-2.,),(-3.,),(4.,),(5.,)),
   "darcy_flux_faces_m_s":(0.,1.),"mobile_species_face_fluxes_mol_m2_s":((0.,2.),(0.,3.))}}
  r=audit_p21_flux_balance(snap,(1.,),((0.,),(0.,),(0.,),(4.,),(5.,)))
  self.assertTrue(r["overall_pass"])
 def test_no_physical_claim(self):
  r=audit_fv_flux_balance(((0.,),),((0.,0.),),((0.,),),(1.,))
  self.assertFalse(r["physical_conservation_certified"])
if __name__=="__main__": unittest.main()
