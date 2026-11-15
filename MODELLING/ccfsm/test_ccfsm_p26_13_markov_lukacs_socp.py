import unittest
from fractions import Fraction

from ccfsm_p26_13_markov_lukacs_socp import (
    certify_cell_nonnegative, verify_global_candidate, verify_free_coordinates,
)
from ccfsm_p26_12_exact_affine_parameterization import build_exact_affine_parameterization


class TestP2613MarkovLukacs(unittest.TestCase):
    def test_strictly_positive_constant(self):
        c = certify_cell_nonnegative(Fraction(2), Fraction(0), Fraction(0))
        self.assertIsNotNone(c)
        self.assertTrue(c["psd_exact"])

    def test_nonnegative_endpoint_touch(self):
        # q(x)=(x+1/2)^2 on [-1/2,1/2]
        m, a, b = Fraction(1,4), Fraction(1), Fraction(1)
        c = certify_cell_nonnegative(m, a, b)
        self.assertIsNotNone(c)
        self.assertEqual(c["minimum_exact"], 0)

    def test_zero_polynomial(self):
        self.assertIsNotNone(certify_cell_nonnegative(0, 0, 0))

    def test_negative_constant_rejected(self):
        self.assertIsNone(certify_cell_nonnegative(-1, 0, 0))

    def test_negative_interior_rejected(self):
        self.assertIsNone(certify_cell_nonnegative(Fraction(1,10), 0, -2))

    def test_certificate_matches_exact_minimum_on_rational_grid(self):
        values = [Fraction(k, 4) for k in range(-8, 9)]
        for m in (Fraction(0), Fraction(1,4), Fraction(1), Fraction(3)):
            for a in values:
                for b in values:
                    c = certify_cell_nonnegative(m, a, b)
                    # The exact polynomial minimum is the independent oracle.
                    from ccfsm_p26_9_primal_dual_feasibility import _poly_min_exact
                    expected = _poly_min_exact(m, a, b) >= 0
                    self.assertEqual(c is not None, expected, (m, a, b))

    def test_global_candidate_uses_exact_sos_per_cell(self):
        edges=(0, Fraction(1,2), 1)
        means=(2,2)
        # Constant field has exact moments (mass, first, second)=(2,1,2/3).
        target=(Fraction(2), Fraction(1), Fraction(2,3))
        chart=build_exact_affine_parameterization(edges, means, target)
        result=verify_free_coordinates(chart, (Fraction(0), Fraction(0)))
        self.assertTrue(result["verified"])
        self.assertEqual(len(result["cell_certificates"]), 2)

    def test_negative_candidate_has_no_cell_certificate(self):
        self.assertIsNone(certify_cell_nonnegative(0, 1, 0))


if __name__ == "__main__":
    unittest.main()
