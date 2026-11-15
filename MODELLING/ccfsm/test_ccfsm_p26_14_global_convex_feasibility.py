import unittest
from fractions import Fraction
from ccfsm_p26_14_global_convex_feasibility import solve_global_convex_feasibility


class TestP2614GlobalConvexFeasibility(unittest.TestCase):
    def test_exact_feasible_two_cell_constant(self):
        r=solve_global_convex_feasibility((0,Fraction(1,2),1),(2,2),(0,0),(0,0),
                                          denominators=(1,),offset_radius=0)
        self.assertEqual(r["status"],"feasible_exact_primal_witness")
        self.assertTrue(r["verified"])
        self.assertTrue(r["exact_certificate"]["cellwise_nonnegative_exact"])
        self.assertTrue(r["exact_certificate"]["global_moments_exact"])

    def test_negative_single_cell_is_not_mislabelled_infeasible(self):
        r=solve_global_convex_feasibility((0,1),(Fraction(1,10),),(1,),(0,),
                                          denominators=(1,),offset_radius=0,max_iterations=25)
        self.assertEqual(r["status"],"unresolved")
        self.assertFalse(r["verified"])

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            solve_global_convex_feasibility((0,1),(1,1),(0,),(0,))


if __name__=="__main__":
    unittest.main()
