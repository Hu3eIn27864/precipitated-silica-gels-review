import unittest
from fractions import Fraction

from ccfsm_p27_2_tetra_p2_bernstein import (
    quadratic_tetra_bernstein_coefficients,
    verify_tetra_p2_bernstein_positivity,
)


class TestP272TetraP2Bernstein(unittest.TestCase):
    def setUp(self):
        self.tet = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))

    def test_constant_positive_polynomial_is_certified(self):
        result = verify_tetra_p2_bernstein_positivity(
            self.tet, (2, 2, 2, 2), (2, 2, 2, 2, 2, 2))
        self.assertTrue(result["certified"])
        self.assertEqual(result["minimum_bernstein_coefficient"], 2)

    def test_exact_rational_bernstein_coefficients(self):
        coeffs = quadratic_tetra_bernstein_coefficients(
            (1, 1, 0, 0),
            (0, Fraction(1, 4), Fraction(1, 4),
             Fraction(1, 4), Fraction(1, 4), 0))
        self.assertEqual(coeffs, (Fraction(1), Fraction(1), Fraction(0),
                                  Fraction(0), Fraction(-1), Fraction(0),
                                  Fraction(0), Fraction(0), Fraction(0),
                                  Fraction(0)))

    def test_nonnegative_polynomial_may_fail_sufficient_certificate(self):
        # (lambda_0-lambda_1)^2 >= 0, but its edge-01 Bernstein coefficient is -1.
        result = verify_tetra_p2_bernstein_positivity(
            self.tet, (1, 1, 0, 0),
            (0, Fraction(1, 4), Fraction(1, 4),
             Fraction(1, 4), Fraction(1, 4), 0))
        self.assertFalse(result["certified"])
        self.assertEqual(result["reason"],
                         "negative_bernstein_coefficient_not_certified")
        self.assertIn(4, result["negative_coefficient_indices"])

    def test_negative_polynomial_not_certified(self):
        result = verify_tetra_p2_bernstein_positivity(
            self.tet, (-1, 0, 0, 0),
            (Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2),
             0, 0, 0))
        self.assertFalse(result["certified"])

    def test_degenerate_tetrahedron_rejected(self):
        flat = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0))
        result = verify_tetra_p2_bernstein_positivity(
            flat, (1, 1, 1, 1), (1, 1, 1, 1, 1, 1))
        self.assertEqual(result["reason"], "degenerate_tetrahedron")

    def test_bad_coefficient_count_rejected(self):
        result = verify_tetra_p2_bernstein_positivity(
            self.tet, (1, 1, 1, 1), (1, 1, 1, 1, 1))
        self.assertEqual(result["reason"], "malformed_p2_tetrahedron_data")


if __name__ == "__main__":
    unittest.main()
