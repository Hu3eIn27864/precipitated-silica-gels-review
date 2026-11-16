import math
import unittest
from fractions import Fraction

from ccfsm_p27_43_rational_interval_certificate import (
    CERTIFICATE_SCHEMA,
    CertificateError,
    verify_interval_certificate,
)


def _fraction(value):
    return Fraction.from_float(float(value))


def _outward_pair(lower, upper):
    """Create a deliberately widened binary64 pair for exact test rationals."""
    return [
        math.nextafter(float(lower), -math.inf),
        math.nextafter(float(upper), math.inf),
    ]


def _certificate(operation, lhs, rhs, result):
    return {
        "schema": CERTIFICATE_SCHEMA,
        "operation": operation,
        "lhs": list(lhs),
        "rhs": list(rhs),
        "result": list(result),
    }


class P2743RationalCertificateTests(unittest.TestCase):
    def test_addition_certificate_is_checked_exactly(self):
        lhs, rhs = (0.1, 0.2), (0.3, 0.4)
        exact_lo = _fraction(lhs[0]) + _fraction(rhs[0])
        exact_hi = _fraction(lhs[1]) + _fraction(rhs[1])
        report = verify_interval_certificate(
            _certificate("add", lhs, rhs, _outward_pair(exact_lo, exact_hi))
        )
        self.assertTrue(report["valid"])
        self.assertEqual(Fraction(report["exact_lower"]), exact_lo)
        self.assertEqual(Fraction(report["exact_upper"]), exact_hi)

    def test_multiplication_all_sign_patterns_and_zero_crossings(self):
        cases = [
            ((1.0, 2.0), (3.0, 4.0)),
            ((-2.0, -1.0), (3.0, 4.0)),
            ((1.0, 2.0), (-4.0, -3.0)),
            ((-2.0, -1.0), (-4.0, -3.0)),
            ((-2.0, 3.0), (4.0, 5.0)),
            ((-2.0, 3.0), (-5.0, -4.0)),
            ((-2.0, 3.0), (-5.0, 4.0)),
            ((0.0, 2.0), (-3.0, 4.0)),
        ]
        for lhs, rhs in cases:
            with self.subTest(lhs=lhs, rhs=rhs):
                a, b = map(_fraction, lhs)
                c, d = map(_fraction, rhs)
                corners = (a * c, a * d, b * c, b * d)
                report = verify_interval_certificate(
                    _certificate(
                        "mul", lhs, rhs,
                        _outward_pair(min(corners), max(corners))
                    )
                )
                self.assertTrue(report["valid"])
                self.assertTrue(report["lower_enclosed"])
                self.assertTrue(report["upper_enclosed"])

    def test_checker_rejects_too_high_lower_endpoint(self):
        report = verify_interval_certificate(
            _certificate("mul", (1.0, 2.0), (3.0, 4.0), (4.0, 8.0))
        )
        self.assertFalse(report["valid"])
        self.assertFalse(report["lower_enclosed"])
        self.assertTrue(report["upper_enclosed"])

    def test_checker_rejects_too_low_upper_endpoint(self):
        report = verify_interval_certificate(
            _certificate("mul", (1.0, 2.0), (3.0, 4.0), (3.0, 7.0))
        )
        self.assertFalse(report["valid"])
        self.assertTrue(report["lower_enclosed"])
        self.assertFalse(report["upper_enclosed"])

    def test_subnormal_underflow_certificate(self):
        least_subnormal = math.ulp(0.0)
        exact = _fraction(least_subnormal) * Fraction(1, 2)
        result = [
            math.nextafter(0.0, -math.inf),
            math.nextafter(0.0, math.inf),
        ]
        report = verify_interval_certificate(
            _certificate(
                "mul", (least_subnormal, least_subnormal), (0.5, 0.5), result
            )
        )
        self.assertTrue(report["valid"])
        self.assertEqual(Fraction(report["exact_lower"]), exact)

    def test_division_positive_and_negative_denominator_intervals(self):
        for lhs, rhs in [
            ((1.0, 2.0), (3.0, 4.0)),
            ((-2.0, 1.0), (-4.0, -2.0)),
        ]:
            a, b = map(_fraction, lhs)
            c, d = map(_fraction, rhs)
            corners = (a / c, a / d, b / c, b / d)
            report = verify_interval_certificate(
                _certificate(
                    "div", lhs, rhs,
                    _outward_pair(min(corners), max(corners))
                )
            )
            self.assertTrue(report["valid"])

    def test_division_rejects_zero_containing_denominator(self):
        with self.assertRaises(CertificateError):
            verify_interval_certificate(
                _certificate("div", (1.0, 2.0), (-1.0, 1.0), (-2.0, 2.0))
            )

    def test_finite_binary64_result_cannot_enclose_overflowing_exact_product(self):
        largest = float.fromhex("0x1.fffffffffffffp+1023")
        report = verify_interval_certificate(
            _certificate(
                "mul", (largest, largest), (2.0, 2.0), (-largest, largest)
            )
        )
        self.assertFalse(report["valid"])

    def test_malformed_and_nonfinite_certificates_are_rejected(self):
        with self.assertRaises(CertificateError):
            verify_interval_certificate({})
        with self.assertRaises(CertificateError):
            verify_interval_certificate(
                _certificate(
                    "mul", (1.0, 2.0), (3.0, 4.0), (float("nan"), 8.0)
                )
            )
        with self.assertRaises(CertificateError):
            verify_interval_certificate(
                _certificate("mul", (True, 2.0), (3.0, 4.0), (3.0, 8.0))
            )
        with self.assertRaises(CertificateError):
            verify_interval_certificate(
                {
                    **_certificate("mul", (1.0, 2.0), (3.0, 4.0), (3.0, 8.0)),
                    "untrusted_extra": "must not be silently ignored",
                }
            )


if __name__ == "__main__":
    unittest.main()
