import unittest
from fractions import Fraction
from ccfsm_p26_16_dual_search_stability import (
    audit_sqrt_enclosure, audit_fixed_direction, audit_direction_radii,
    support_gap_error_bound,
)

class TestP2616DualSearchStability(unittest.TestCase):
    def test_sqrt_upper_bounds_are_nested(self):
        r = audit_sqrt_enclosure(Fraction(7,12), (2,4,8,16))
        values = [Fraction(row["upper"]) for row in r["rows"]]
        self.assertTrue(all(a >= b for a,b in zip(values,values[1:])))
        for d, value in zip((2,4,8,16), values):
            self.assertGreaterEqual(value*value, Fraction(7,12))
            self.assertLess((value - Fraction(1,10**d))**2, Fraction(7,12))

    def test_fixed_direction_gap_is_monotone(self):
        r = audit_fixed_direction((0,Fraction(2,5),1),(0,0),(1,0),(0,0),(1,0),(2,4,8,16))
        gaps = [Fraction(row["gap_lower_bound"]) for row in r["rows"]]
        self.assertTrue(all(a <= b for a,b in zip(gaps,gaps[1:])))
        self.assertTrue(all(row["verified"] for row in r["rows"]))

    def test_nested_direction_search_retains_certificate(self):
        r = audit_direction_radii((0,Fraction(2,5),1),(0,0),(1,0),(0,0),(1,2,4,8),24)
        self.assertTrue(all(row["verified"] for row in r["rows"]))
        self.assertTrue(all(row["first_certifying_shell"] == 1 for row in r["rows"]))
        self.assertTrue(all(a["directions_checked"] <= b["directions_checked"]
                            for a,b in zip(r["rows"],r["rows"][1:])))

    def test_support_error_bound(self):
        self.assertEqual(support_gap_error_bound((1,Fraction(1,2)),10), Fraction(9,10**10))

    def test_invalid_levels_rejected(self):
        with self.assertRaises(ValueError): audit_sqrt_enclosure(Fraction(2),(8,4))

if __name__ == "__main__": unittest.main()
