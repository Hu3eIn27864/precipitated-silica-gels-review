import unittest, tempfile, os
from ccfsm_p26_2_quadratic_projection import moments, quadratic_minimum
from ccfsm_p26_6_global_positive_projection import globally_coupled_positive_projection, assess_global_feasibility, run_study

class TestP266GlobalPositive(unittest.TestCase):
    def test_global_moments_mass_and_positivity(self):
        edges=(0.,.3,.7,1.); u=(1.,.8,1.2); a=(3.,-2.,2.5); b=(0.,2.5,0.)
        old=moments(edges,u,a,b)
        result,d=globally_coupled_positive_projection(edges,u,a,b,tolerance=1e-10)
        new=moments(edges,*result)
        for x,y in zip(old,new): self.assertAlmostEqual(x,y,places=8)
        for j,m in enumerate(u):
            self.assertGreaterEqual(m+quadratic_minimum(result[1][j],result[2][j]),-1e-8)
        self.assertTrue(d["converged"])
    def test_already_feasible_is_unchanged(self):
        edges=(0.,.5,1.); u=(1.,1.); a=(.1,-.1); b=(.1,.1)
        result,d=globally_coupled_positive_projection(edges,u,a,b)
        for x,y in zip(result[1],a): self.assertAlmostEqual(x,y,places=9)
        for x,y in zip(result[2],b): self.assertAlmostEqual(x,y,places=9)
    def test_negative_average_rejected(self):
        with self.assertRaises(ValueError):
            globally_coupled_positive_projection((0.,1.),(-.1,),(0.,),(0.,))
    def test_single_cell_infeasibility_is_certified(self):
        report=assess_global_feasibility((0.,1.),(.1,),(1.,),(0.,))
        self.assertEqual(report["status"],"certified_infeasible")
        self.assertLess(report["minimum_cell_value"],0.)
    def test_single_cell_feasible_case_is_certified(self):
        report=assess_global_feasibility((0.,1.),(1.,),(.2,),(.1,))
        self.assertEqual(report["status"],"feasible")
    def test_study_artifacts(self):
        with tempfile.TemporaryDirectory() as d:
            s=run_study(d)
            self.assertTrue(s["converged"])
            self.assertTrue(os.path.exists(os.path.join(d,"p26_6_global_positive_projection.csv")))
if __name__=="__main__": unittest.main()
