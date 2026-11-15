import unittest
from fractions import Fraction
from ccfsm_p26_12_exact_affine_parameterization import (
    build_exact_affine_parameterization, evaluate_exact_affine_parameterization,
    verify_affine_candidate, search_rational_positive_witness,
)


class TestP2612ExactAffineParameterization(unittest.TestCase):
    def test_dimension_and_exact_reconstruction(self):
        edges=(0,Fraction(1,2),1); means=(2,2)
        a=(Fraction(1,10),Fraction(-1,10)); b=(Fraction(1,10),Fraction(1,10))
        from ccfsm_p26_10_exact_moment_witness import _targets
        target,_=_targets(edges,means,a,b)
        chart=build_exact_affine_parameterization(edges,means,target)
        self.assertEqual(chart["dimension"],2)
        free=tuple((a+bv) for a,bv in zip(
            (a[0],b[0]), (b[0],a[1])))
        linear,quadratic=evaluate_exact_affine_parameterization(chart,free)
        self.assertTrue(verify_affine_candidate(chart,linear,quadratic)["global_moments_exact"])

    def test_arbitrary_free_coordinates_satisfy_moments_exactly(self):
        edges=(0,Fraction(1,3),1); means=(1,2)
        target=(Fraction(5,3),Fraction(7,6),Fraction(11,9))
        chart=build_exact_affine_parameterization(edges,means,target)
        a,b=evaluate_exact_affine_parameterization(chart,(Fraction(3,7),Fraction(-2,9)))
        result=verify_affine_candidate(chart,a,b)
        self.assertTrue(result["global_moments_exact"])
        self.assertEqual(result["moment_residuals_exact"],(0,0,0))

    def test_one_cell_has_zero_dimensional_affine_space(self):
        edges=(0,1); means=(2,)
        target=(Fraction(2),Fraction(1),Fraction(1,3))
        chart=build_exact_affine_parameterization(edges,means,target)
        self.assertEqual(chart["dimension"],0)
        a,b=evaluate_exact_affine_parameterization(chart,())
        self.assertTrue(verify_affine_candidate(chart,a,b)["global_moments_exact"])

    def test_incompatible_mass_rejected(self):
        with self.assertRaises(ValueError):
            build_exact_affine_parameterization((0,1),(1,),(Fraction(2),Fraction(0),Fraction(0)))

    def test_dependent_pivots_rejected(self):
        target=(Fraction(2),Fraction(1),Fraction(1,3))
        with self.assertRaises(ValueError):
            build_exact_affine_parameterization((0,Fraction(1,2),1),(2,2),target,(1,3))

    def test_rational_grid_finds_interior_witness(self):
        edges=(0,Fraction(1,2),1); means=(2,2)
        a=(Fraction(1,10),Fraction(-1,10)); b=(Fraction(1,10),Fraction(1,10))
        from ccfsm_p26_10_exact_moment_witness import _targets
        target,_=_targets(edges,means,a,b)
        r=search_rational_positive_witness(edges,means,a,b,target,denominators=(1,2),offset_radius=1)
        self.assertEqual(r["status"],"feasible_exact_primal_witness")
        self.assertTrue(r["verified"])

    def test_zero_inventory_failure_is_unresolved(self):
        r=search_rational_positive_witness((0,Fraction(1,2),1),(0,0),(1,0),(0,0),
            denominators=(1,2),offset_radius=1,max_candidates=100)
        self.assertEqual(r["status"],"unresolved")
        self.assertFalse(r["verified"])


if __name__=="__main__": unittest.main()
