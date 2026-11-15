import unittest
from fractions import Fraction
from ccfsm_p26_10_exact_moment_witness import exact_moment_correction, find_exact_positive_witness, assess_exact_moment_feasibility


class TestP2610ExactMomentWitness(unittest.TestCase):
    def test_one_cell_exact_witness(self):
        r=exact_moment_correction((0,1),(1,),(0,),(0,),(1,Fraction(1,2),Fraction(1,3)))
        self.assertTrue(r["verified"]); self.assertTrue(r["global_moments_exact"])
        self.assertTrue(r["cellwise_nonnegative_exact"])

    def test_correction_restores_exact_moments(self):
        r=exact_moment_correction((0,1),(1,),(0.1,),(0.2,),(1,Fraction(1,2),Fraction(1,3)))
        self.assertTrue(r["verified"]); self.assertEqual(r["moment_residuals_exact"],["0","0","0"])

    def test_negative_exact_polynomial_rejected(self):
        r=exact_moment_correction((0,1),(0,),(1,),(0,),(0,Fraction(1,12),Fraction(1,24)))
        self.assertFalse(r["verified"]); self.assertFalse(r["cellwise_nonnegative_exact"])

    def test_exact_original_positive_case(self):
        r=find_exact_positive_witness((0,1),(1,),(0,),(0,))
        self.assertTrue(r["verified"]); self.assertIn("already satisfy",r["method"])

    def test_dual_infeasibility_priority(self):
        r=assess_exact_moment_feasibility((0.,.4,1.),(0.,0.),(1.,0.),(0.,0.),max_direction=4)
        self.assertEqual(r["status"],"certified_infeasible")

    def test_already_positive_global_case(self):
        r=assess_exact_moment_feasibility((0.,.4,1.),(1.,.8),(0.,0.),(0.,0.))
        self.assertEqual(r["status"],"feasible_exact_primal_witness")

    def test_invalid_pivot(self):
        with self.assertRaises(ValueError):
            exact_moment_correction((0,1),(1,),(0,),(0,),pivot_cell=1)


if __name__=="__main__": unittest.main()
