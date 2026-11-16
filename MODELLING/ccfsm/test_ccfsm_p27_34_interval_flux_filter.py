import unittest

from ccfsm_p27_34_interval_flux_filter import (
    Interval, classify_flux_interval, enclose_flux,
)


class P2734IntervalFluxFilterTests(unittest.TestCase):
    def test_positive_flux_excludes_zero(self):
        result = classify_flux_interval(lambda t: t*0.0 + 2.0, 0.0, 1.0)
        self.assertEqual(result["status"], "certified_zero_excluded")
        self.assertFalse(result["root_existence_proved"])

    def test_tangential_candidate_remains_unresolved(self):
        result = classify_flux_interval(lambda t: (t-0.5).square(), 0.4, 0.6)
        self.assertEqual(result["status"], "unresolved_zero_inclusion")
        self.assertFalse(result["root_existence_proved"])

    def test_negative_flux_excludes_zero(self):
        result = classify_flux_interval(lambda t: t*0.0 - 3.0, 0.0, 1.0)
        self.assertEqual(result["status"], "certified_zero_excluded")

    def test_outward_rounding_contains_exact_samples(self):
        x = Interval(0.1, 0.2)
        y = x*x + 1.0
        for value in (1.01, 1.04):
            self.assertLessEqual(y.lo, value)
            self.assertGreaterEqual(y.hi, value)

    def test_division_rejects_zero_containing_denominator(self):
        with self.assertRaises(ZeroDivisionError):
            _ = Interval(1.0, 2.0) / Interval(-1.0, 1.0)

    def test_invalid_interval_and_extension_are_rejected(self):
        with self.assertRaises(ValueError):
            Interval(2.0, 1.0)
        with self.assertRaises(ValueError):
            enclose_flux(lambda x: x, 1.0, 1.0)
        with self.assertRaises(TypeError):
            enclose_flux(lambda x: 1.0, 0.0, 1.0)

    def test_nonfinite_interval_result_rejected(self):
        with self.assertRaises(ValueError):
            Interval(0.0, float("inf"))


    def test_arithmetic_enclosures_against_exact_binary_rationals(self):
        """Check endpoint operations against exact values of their float inputs."""
        from fractions import Fraction

        cases = [
            (Interval(-3.0, -1.0), Interval(-2.0, 4.0)),
            (Interval(-3.0, 2.0), Interval(-5.0, -0.5)),
            (Interval(0.25, 1.5), Interval(2.0, 3.0)),
            (Interval(-0.75, 0.125), Interval(-0.5, 0.25)),
        ]
        for a, b in cases:
            add = a + b
            exact_add_lo = Fraction.from_float(a.lo) + Fraction.from_float(b.lo)
            exact_add_hi = Fraction.from_float(a.hi) + Fraction.from_float(b.hi)
            self.assertLessEqual(Fraction.from_float(add.lo), exact_add_lo)
            self.assertGreaterEqual(Fraction.from_float(add.hi), exact_add_hi)

            product = a * b
            exact_products = [
                Fraction.from_float(x) * Fraction.from_float(y)
                for x in (a.lo, a.hi) for y in (b.lo, b.hi)
            ]
            self.assertLessEqual(Fraction.from_float(product.lo), min(exact_products))
            self.assertGreaterEqual(Fraction.from_float(product.hi), max(exact_products))

    def test_reciprocal_and_square_enclosures_against_exact_rationals(self):
        from fractions import Fraction

        for interval in (Interval(0.25, 2.0), Interval(-4.0, -0.5)):
            reciprocal = interval.reciprocal()
            exact_reciprocals = [
                Fraction(1, 1) / Fraction.from_float(x)
                for x in (interval.lo, interval.hi)
            ]
            self.assertLessEqual(Fraction.from_float(reciprocal.lo), min(exact_reciprocals))
            self.assertGreaterEqual(Fraction.from_float(reciprocal.hi), max(exact_reciprocals))

            square = interval.square()
            exact_squares = [Fraction.from_float(x) ** 2 for x in (interval.lo, interval.hi)]
            self.assertLessEqual(Fraction.from_float(square.lo), min(exact_squares))
            self.assertGreaterEqual(Fraction.from_float(square.hi), max(exact_squares))

        crossing = Interval(-2.0, 3.0).square()
        self.assertLessEqual(Fraction.from_float(crossing.lo), Fraction(0))
        self.assertGreaterEqual(
            Fraction.from_float(crossing.hi),
            Fraction.from_float(3.0) ** 2,
        )


    def test_subnormal_underflow_is_still_outward_enclosed(self):
        import math
        from fractions import Fraction

        tiny = math.ulp(0.0)
        result = Interval(tiny) * Interval(tiny)
        exact = Fraction.from_float(tiny) ** 2
        self.assertLessEqual(Fraction.from_float(result.lo), exact)
        self.assertGreaterEqual(Fraction.from_float(result.hi), exact)

    def test_overflow_and_unrepresentable_reciprocal_fail_closed(self):
        import sys

        largest = sys.float_info.max
        with self.assertRaises(ValueError):
            _ = Interval(largest) + Interval(largest)
        with self.assertRaises(ValueError):
            _ = Interval(largest) * Interval(largest)
        with self.assertRaises(ValueError):
            _ = Interval(math.ulp(0.0)).reciprocal()


if __name__ == "__main__":
    unittest.main()
