import unittest,math
from ccfsm_p26_2_quadratic_projection import moments,quadratic_minimum
from ccfsm_p26_5_optimal_positive_projection import closest_positive_coefficients,limit_target_reconstruction_optimal,project_optimal_positive_quadratic,run_study
from ccfsm_p26_4_positive_target import positive_target_coefficients
class TestP265OptimalPositive(unittest.TestCase):
    def test_edge_case_is_positive_and_closer_than_radial(self):
        a,b,d=closest_positive_coefficients(1.,4.,0.)
        r=positive_target_coefficients(1.,4.,0.)
        self.assertGreaterEqual(1+quadratic_minimum(a,b),-1e-11)
        self.assertLessEqual((a-4)**2+b*b,(r[0]-4)**2+r[1]**2+1e-12)
    def test_interior_vertex_constraint(self):
        a,b,d=closest_positive_coefficients(.2,0.,3.)
        self.assertGreaterEqual(.2+quadratic_minimum(a,b),-1e-11)
        self.assertLess(d["objective"],9.)
    def test_already_positive_is_unchanged(self):
        a,b,d=closest_positive_coefficients(1.,.2,.1)
        self.assertEqual((a,b),(.2,.1)); self.assertEqual(d["objective"],0.)
    def test_zero_mean_forces_zero_modes(self):
        a,b,d=closest_positive_coefficients(0.,.5,1.)
        self.assertEqual((a,b),(0.,0.))
    def test_weights_and_invalid_inputs(self):
        with self.assertRaises(ValueError): closest_positive_coefficients(1.,1.,1.,weights=(1.,0.))
        with self.assertRaises(ValueError): closest_positive_coefficients(-1.,0.,0.)
        with self.assertRaises(ValueError): closest_positive_coefficients(1.,0.,0.,safety=-1.)
    def test_weighted_projection_is_feasible(self):
        for w in ((1.,1.),(4.,.25),(.25,4.)):
            a,b,d=closest_positive_coefficients(.1,2.,-1.,weights=w)
            self.assertGreaterEqual(.1+quadratic_minimum(a,b),-1e-10)
            self.assertTrue(d["converged"])
    def test_cellwise_mass_preserved_and_moments_reported(self):
        edges=(0.,.4,1.); avg=(.2,1.); lin=(0.,4.); quad=(2.,0.)
        old=moments(edges,avg,lin,quad)
        result,diag=limit_target_reconstruction_optimal(edges,avg,lin,quad)
        new=moments(edges,*result)
        self.assertAlmostEqual(old[0],new[0],places=13)
        self.assertEqual(result[0],avg)
        self.assertGreaterEqual(diag["minimum_target_value"],-1e-10)
    def test_transfer_wrapper(self):
        result,diag=project_optimal_positive_quadratic((0.,1.),(1.,),(4.,),(0.,),(0.,.5,1.))
        self.assertGreaterEqual(diag["minimum_target_value"],-1e-10)
        self.assertAlmostEqual(diag["absolute_moment_changes"]["mass"],0.,places=13)
    def test_study_artifacts(self):
        import tempfile,os
        with tempfile.TemporaryDirectory() as d:
            s=run_study(d)
            self.assertEqual(s["cases"],5)
            self.assertTrue(os.path.exists(os.path.join(d,"p26_5_optimal_positive_projection.csv")))
            self.assertGreaterEqual(s["minimum_after"],-1e-10)
if __name__=="__main__": unittest.main()
