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


if __name__ == "__main__":
    unittest.main()
