import unittest

from ccfsm_p27_34_interval_flux_filter import Interval
from ccfsm_p27_35_polynomial_enclosure_audit import (
    polynomial_interval, classify_polynomial_interval,
)


class P2735PolynomialEnclosureAuditTests(unittest.TestCase):
    def test_constant_positive_polynomial_excludes_zero(self):
        result = classify_polynomial_interval([2.0], -1.0, 1.0)
        self.assertEqual(result["status"], "certified_zero_excluded")

    def test_linear_root_interval_remains_unresolved(self):
        result = classify_polynomial_interval([1.0, -0.25], 0.0, 0.5)
        self.assertEqual(result["status"], "unresolved_zero_inclusion")

    def test_tangential_root_interval_remains_unresolved(self):
        result = classify_polynomial_interval([1.0, -1.0, 0.25], 0.4, 0.6)
        self.assertEqual(result["status"], "unresolved_zero_inclusion")

    def test_enclosure_contains_dense_polynomial_samples(self):
        cases = [
            ([1.0, -0.7, 0.1], Interval(-0.4, 0.8)),
            ([2.0, -1.0, 0.5, -0.2], Interval(-1.0, 0.5)),
            ([1.0, 0.0, -0.25], Interval(-0.3, 0.7)),
        ]
        for coeffs, domain in cases:
            enclosure = polynomial_interval(coeffs, domain)
            for i in range(1001):
                x = domain.lo + (domain.hi-domain.lo)*i/1000
                exact = 0.0
                for c in coeffs:
                    exact = exact*x+c
                self.assertLessEqual(enclosure.lo, exact)
                self.assertGreaterEqual(enclosure.hi, exact)

    def test_subdivision_tightens_positive_polynomial_enclosure(self):
        whole = polynomial_interval([1.0, 2.0], Interval(-1.0, 1.0))
        left = polynomial_interval([1.0, 2.0], Interval(-1.0, 0.0))
        right = polynomial_interval([1.0, 2.0], Interval(0.0, 1.0))
        self.assertGreater(whole.hi-whole.lo, left.hi-left.lo)
        self.assertGreater(whole.hi-whole.lo, right.hi-right.lo)
        self.assertGreater(left.lo, 0.0)
        self.assertGreater(right.lo, 0.0)

    def test_invalid_coefficients_and_domain_rejected(self):
        with self.assertRaises(ValueError):
            polynomial_interval([], Interval(0.0, 1.0))
        with self.assertRaises(ValueError):
            polynomial_interval([float("nan")], Interval(0.0, 1.0))
        with self.assertRaises(TypeError):
            polynomial_interval([1.0], (0.0, 1.0))

    def test_zero_polynomial_never_claims_root_existence(self):
        result = classify_polynomial_interval([0.0], -1.0, 1.0)
        self.assertEqual(result["status"], "unresolved_zero_inclusion")
        self.assertFalse(result["root_existence_proved"])


if __name__ == "__main__":
    unittest.main()
