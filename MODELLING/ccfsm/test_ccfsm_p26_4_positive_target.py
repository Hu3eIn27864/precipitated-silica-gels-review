import unittest
from ccfsm_p26_2_quadratic_projection import moments,quadratic_minimum
from ccfsm_p26_4_positive_target import positive_target_coefficients,limit_target_reconstruction,project_positive_quadratic,run_study
class TestP264PositiveTarget(unittest.TestCase):
    def test_edge_undershoot_removed(self):
        ap,bp,t,before,after=positive_target_coefficients(1.,4.,0.)
        self.assertLess(before,0); self.assertGreaterEqual(after,0); self.assertLess(t,1); self.assertAlmostEqual(ap/4,t); self.assertEqual(bp,0)
    def test_interior_vertex_undershoot_removed(self):
        ap,bp,t,before,after=positive_target_coefficients(.2,0.,2.)
        self.assertLess(before,0); self.assertGreaterEqual(after,0); self.assertGreaterEqual(.2+quadratic_minimum(ap,bp),0)
    def test_positive_polynomial_unchanged(self):
        self.assertEqual(positive_target_coefficients(1.,.2,.1)[:3],(.2,.1,1.))
    def test_zero_mean_forces_zero_modes(self):
        self.assertEqual(positive_target_coefficients(0.,.5,1.)[:3],(0.,0.,0.))
    def test_negative_mean_rejected(self):
        with self.assertRaises(ValueError): positive_target_coefficients(-1e-12,0,0)
    def test_nonfinite_and_bad_safety_rejected(self):
        with self.assertRaises(ValueError): positive_target_coefficients(1,float("nan"),0)
        with self.assertRaises(ValueError): positive_target_coefficients(1,0,0,safety=1.)
    def test_cellwise_mass_preserved_higher_moments_reported(self):
        edges=(0,.4,1); avg=(.2,1.); lin=(0.,4.); quad=(2.,0.)
        before=moments(edges,avg,lin,quad); result,diag=limit_target_reconstruction(edges,avg,lin,quad); after=moments(edges,*result)
        self.assertAlmostEqual(before[0],after[0],places=14); self.assertEqual(result[0],avg)
        self.assertGreaterEqual(diag["minimum_target_value"],0); self.assertGreater(diag["absolute_moment_changes"]["second"],0)
    def test_transfer_wrapper_preserves_mass_and_target_positivity(self):
        se=(0,1); te=(0,.3,.7,1); avg=(1.,); lin=(4.,); quad=(0.,)
        out,diag=project_positive_quadratic(se,avg,lin,quad,te)
        self.assertAlmostEqual(moments(se,avg,lin,quad)[0],moments(te,*out)[0],places=13)
        for m,a,b in zip(*out): self.assertGreaterEqual(m+quadratic_minimum(a,b),0)
        self.assertAlmostEqual(diag["absolute_moment_changes"]["mass"],0.,places=13)
    def test_study_writes_outputs(self):
        import tempfile,os
        with tempfile.TemporaryDirectory() as d:
            s=run_study(d); self.assertEqual(s["cases"],5); self.assertGreater(s["limited_cases"],0)
            self.assertTrue(os.path.exists(os.path.join(d,"p26_4_positive_target_cases.csv")))
            self.assertGreaterEqual(s["minimum_after"],0)
if __name__=="__main__": unittest.main()
