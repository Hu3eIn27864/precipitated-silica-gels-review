import unittest
from fractions import Fraction
from ccfsm_p26_9_primal_dual_feasibility import _poly_min_exact, verify_primal_witness, assess_primal_dual_feasibility


class TestP269PrimalDual(unittest.TestCase):
    def test_exact_polynomial_minimum(self):
        self.assertEqual(_poly_min_exact(Fraction(1),Fraction(0),Fraction(0)),1)
        self.assertEqual(_poly_min_exact(Fraction(0),Fraction(1),Fraction(0)),Fraction(-1,2))
        self.assertEqual(_poly_min_exact(Fraction(1),Fraction(0),Fraction(2)),Fraction(5,6))

    def test_primal_witness_exact_positive_and_zero_residual(self):
        v=verify_primal_witness((0,1),(1,),(0,),(0,),(1,Fraction(1,2),Fraction(1,3)))
        self.assertTrue(v["verified"]); self.assertTrue(v["cellwise_nonnegative_exact"])

    def test_primal_witness_rejects_negative_polynomial(self):
        v=verify_primal_witness((0,1),(0,),(1,),(0,),(0,0,0))
        self.assertFalse(v["verified"]); self.assertFalse(v["cellwise_nonnegative_exact"])

    def test_dual_certificate_has_priority(self):
        r=assess_primal_dual_feasibility((0.,.4,1.),(0.,0.),(1.,0.),(0.,0.),max_direction=4)
        self.assertEqual(r["status"],"certified_infeasible"); self.assertFalse(r["primal_attempted"])

    def test_already_positive_case_has_primal_witness(self):
        r=assess_primal_dual_feasibility((0.,.4,1.),(1.,.8),(0.,0.),(0.,0.))
        self.assertEqual(r["status"],"feasible_verified_primal_witness")
        self.assertTrue(r["primal_witness"]["verification"]["verified"])

    def test_bad_lengths_rejected(self):
        with self.assertRaises(ValueError):
            verify_primal_witness((0,1),(1,),(),(0,),(1,0,0))


if __name__=="__main__": unittest.main()
