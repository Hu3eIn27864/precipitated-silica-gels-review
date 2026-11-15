import unittest
from ccfsm_p26_3_refinement_study import profile_value, source_projection, run_study
from ccfsm_p26_2_quadratic_projection import moments, project_quadratic_moments
class TestP263RefinementStudy(unittest.TestCase):
    def test_profiles_are_finite_nonnegative(self):
        for name in ("smooth_gaussian","steep_front","local_extrema","near_zero_inventory"):
            self.assertTrue(all(profile_value(name,i/100)>=0 for i in range(101)))
    def test_source_projection_shapes_and_positive_means(self):
        edges=(0,.1,.35,.7,1); av,a,b=source_projection(edges,"smooth_gaussian")
        self.assertEqual(len(av),len(edges)-1); self.assertTrue(all(v>0 for v in av))
    def test_projection_conserves_reconstructed_source_moments(self):
        edges=(0,.1,.35,.7,1); target=(0,.17,.42,.81,1); src=source_projection(edges,"local_extrema")
        dst=project_quadratic_moments(edges,*src,target)
        for x,y in zip(moments(edges,*src),moments(target,*dst)): self.assertAlmostEqual(x,y,places=11)
    def test_small_study_writes_metrics_and_has_four_profiles(self):
        import tempfile,os
        with tempfile.TemporaryDirectory() as d:
            result=run_study(d,cells=(8,))
            self.assertEqual(result["cases"],8); self.assertEqual(len(result["by_profile"]),4)
            self.assertTrue(os.path.exists(os.path.join(d,"p26_3_refinement_metrics.csv")))
            self.assertLess(result["max_relative_moment_residual"],1e-10)
if __name__=="__main__": unittest.main()
