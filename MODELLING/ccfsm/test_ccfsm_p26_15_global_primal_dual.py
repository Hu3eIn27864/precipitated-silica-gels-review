import unittest
from fractions import Fraction
from ccfsm_p26_15_global_primal_dual import (
    search_global_dual_separator, assess_global_primal_dual_feasibility,
)


class TestP2615GlobalPrimalDual(unittest.TestCase):
    def test_zero_inventory_nonzero_modes_exactly_infeasible(self):
        r=search_global_dual_separator((0,Fraction(2,5),1),(0,0),(1,0),(0,0),max_direction=4)
        self.assertEqual(r["status"],"certified_infeasible")
        self.assertTrue(r["verified"])
        self.assertGreater(Fraction(r["certificate"]["gap_lower_bound"]),0)

    def test_positive_constant_exact_primal_witness(self):
        r=assess_global_primal_dual_feasibility((0,Fraction(1,2),1),(2,2),(0,0),(0,0),
            max_direction=3,denominators=(1,),offset_radius=0)
        self.assertEqual(r["status"],"feasible_exact_primal_witness")
        self.assertTrue(r["verified"])
        self.assertTrue(r["primal_witness"]["exact_certificate"]["global_moments_exact"])

    def test_zero_modes_not_falsely_certified_infeasible(self):
        r=search_global_dual_separator((0,Fraction(2,5),1),(1,Fraction(7,10)),(0,0),(0,0),max_direction=3)
        self.assertEqual(r["status"],"no_certificate_found")
        self.assertFalse(r["verified"])

    def test_finite_search_failure_is_not_feasibility(self):
        r=assess_global_primal_dual_feasibility((0,Fraction(2,5),1),(0,0),(1,0),(0,0),
            max_direction=1,max_iterations=1,denominators=(),offset_radius=0)
        self.assertIn(r["status"],("certified_infeasible","unresolved"))
        if r["status"]=="unresolved":
            self.assertFalse(r["verified"])
            self.assertIn("No feasibility or infeasibility",r["meaning"])

    def test_invalid_direction_bound_rejected(self):
        with self.assertRaises(ValueError):
            search_global_dual_separator((0,1),(1,),(0,),(0,),max_direction=0)


if __name__=="__main__": unittest.main()
