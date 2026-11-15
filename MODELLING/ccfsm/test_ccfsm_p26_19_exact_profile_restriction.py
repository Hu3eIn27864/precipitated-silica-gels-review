import unittest
from fractions import Fraction
from ccfsm_p26_19_exact_profile_restriction import (
    restrict_quadratic_profile, coarsen_quadratic_profile, round_trip_profile)

class TestP2619ExactProfileRestriction(unittest.TestCase):
    def test_nonuniform_refinement_round_trip_exact(self):
        result=round_trip_profile((0,1),(2,),(Fraction(1,5),),(Fraction(1,10),),
                                  (0,Fraction(1,4),Fraction(3,4),1))
        self.assertTrue(result["round_trip_exact"])
        self.assertEqual(result["coarsening"]["averages"],("2",))
        self.assertEqual(result["coarsening"]["linear"],("1/5",))
        self.assertEqual(result["coarsening"]["quadratic"],("1/10",))

    def test_piecewise_parent_cells_refined_independently(self):
        result=round_trip_profile((0,Fraction(1,2),1),(2,3),(0,Fraction(1,7)),
                                  (Fraction(1,10),Fraction(1,8)),
                                  (0,Fraction(1,4),Fraction(1,2),Fraction(3,4),1))
        self.assertTrue(result["round_trip_exact"])
        self.assertEqual(result["restriction"]["parent_cell"],(0,0,1,1))

    def test_non_nested_mesh_rejected(self):
        with self.assertRaises(ValueError):
            restrict_quadratic_profile((0,Fraction(1,2),1),(2,2),(0,0),(0,0),
                                       (0,Fraction(1,3),1))

    def test_fine_profile_not_exact_restriction_detected(self):
        restricted=restrict_quadratic_profile((0,1),(2,),(0,),(0,),(0,Fraction(1,2),1))
        altered=dict(restricted); altered["linear"]=("1/10","-1/10")
        result=coarsen_quadratic_profile((0,1),altered["edges"],altered["averages"],
                                         altered["linear"],altered["quadratic"])
        self.assertFalse(result["exact_local_restriction"])

    def test_global_moments_preserved_by_restriction(self):
        parent=(0,1); fine=(0,Fraction(1,3),1)
        restricted=restrict_quadratic_profile(parent,(2,),(Fraction(1,5),),
                                               (Fraction(1,10),),fine)
        from ccfsm_p26_19_exact_profile_restriction import _raw_moments
        coarse=_raw_moments(tuple(map(Fraction,parent)),(Fraction(2),),
                            (Fraction(1,5),),(Fraction(1,10),))
        refined=_raw_moments(tuple(map(Fraction,fine)),
            tuple(map(Fraction,restricted["averages"])),
            tuple(map(Fraction,restricted["linear"])),
            tuple(map(Fraction,restricted["quadratic"])))
        self.assertEqual(coarse,refined)

if __name__=="__main__": unittest.main()
