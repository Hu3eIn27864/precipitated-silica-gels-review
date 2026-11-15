import unittest
from fractions import Fraction
from ccfsm_p26_11_all_pair_exact_witness import exact_two_coordinate_correction, find_exact_positive_witness_all_pairs, _modal_columns, _solve_pair_exact


class TestP2611AllPairExactWitness(unittest.TestCase):
    def test_general_pair_solves_exact_global_moments(self):
        target=(Fraction(2),Fraction(1),Fraction(4,3))
        r=exact_two_coordinate_correction((0,Fraction(1,2),1),(2,2),(.2,-.2),(.2,.2),
            target,pivot_coordinates=(0,2),significant_digits=10)
        self.assertTrue(r["global_moments_exact"])
        self.assertEqual(r["moment_residuals_exact"],["0","0","0"])
        self.assertEqual(r["pivot_coordinates"],[0,2])

    def test_singular_pair_reported(self):
        r=exact_two_coordinate_correction((0,1),(1,),(0,),(0,),pivot_coordinates=(0,0))
        self.assertEqual(r["status"],"singular_pivot_pair")

    def test_invalid_pivots_rejected(self):
        with self.assertRaises(ValueError):
            exact_two_coordinate_correction((0,1),(1,),(0,),(0,),pivot_coordinates=(0,2))

    def test_all_pairs_search_returns_exact_witness(self):
        r=find_exact_positive_witness_all_pairs((0,Fraction(1,2),1),(2,2),(0,0),(0,0),digit_choices=(17,12))
        self.assertEqual(r["status"],"feasible_exact_primal_witness")
        self.assertTrue(r["verified"])
        self.assertGreater(r["search"]["coordinate_pairs_tested"],0)

    def test_zero_inventory_is_not_misreported_feasible(self):
        r=find_exact_positive_witness_all_pairs((0,Fraction(1,2),1),(0,0),(1,0),(0,0),digit_choices=(17,12))
        self.assertEqual(r["status"],"no_exact_positive_witness_found")

    def test_pair_matrix(self):
        cols=_modal_columns((Fraction(0),Fraction(1,2),Fraction(1)))
        self.assertIsNone(_solve_pair_exact(cols[1],cols[3],(Fraction(1),Fraction(1))))


if __name__=="__main__": unittest.main()
