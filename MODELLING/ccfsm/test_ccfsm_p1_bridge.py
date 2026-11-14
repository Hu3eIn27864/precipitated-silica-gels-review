import math
import unittest

from ccfsm_p1_bridge import bridge_fraction, darcy_mobility


class TestCCFSMP1Bridge(unittest.TestCase):
    def test_bridge_bounds_for_all_endpoint_combinations(self):
        for b0 in (0.0, 0.2, 0.7, 1.0):
            for b_eq in (0.0, 0.3, 0.8, 1.0):
                for t in (0.0, 0.01, 1.0, 100.0):
                    b = bridge_fraction(t, b0, b_eq, 0.4)
                    self.assertGreaterEqual(b, 0.0)
                    self.assertLessEqual(b, 1.0)

    def test_exact_initial_value_and_equilibrium(self):
        self.assertEqual(bridge_fraction(0.0, 0.25, 0.8, 0.7), 0.25)
        self.assertAlmostEqual(bridge_fraction(1e6, 0.25, 0.8, 0.7), 0.8)

    def test_semigroup_property(self):
        first = bridge_fraction(0.4, 0.2, 0.9, 0.3)
        sequential = bridge_fraction(0.6, first, 0.9, 0.3)
        direct = bridge_fraction(1.0, 0.2, 0.9, 0.3)
        self.assertAlmostEqual(sequential, direct, places=14)

    def test_monotonic_relaxation(self):
        increasing = [bridge_fraction(t, 0.1, 0.9, 0.5) for t in (0, 1, 2, 3)]
        decreasing = [bridge_fraction(t, 0.9, 0.1, 0.5) for t in (0, 1, 2, 3)]
        self.assertEqual(increasing, sorted(increasing))
        self.assertEqual(decreasing, sorted(decreasing, reverse=True))

    def test_mobility_interpolation_stays_positive_and_bounded(self):
        for b in (0.0, 0.1, 0.5, 0.9, 1.0):
            value = darcy_mobility(b, 2.0, 5.0)
            self.assertGreaterEqual(value, 2.0)
            self.assertLessEqual(value, 5.0)

    def test_mobility_can_interpolate_in_either_direction(self):
        self.assertAlmostEqual(darcy_mobility(0.25, 8.0, 4.0), 7.0)

    def test_invalid_inputs_rejected(self):
        invalid_bridge = (
            (-1, 0.2, 0.8, 1.0),
            (1, -0.1, 0.8, 1.0),
            (1, 0.2, 1.1, 1.0),
            (1, 0.2, 0.8, 0.0),
            (math.nan, 0.2, 0.8, 1.0),
        )
        for args in invalid_bridge:
            with self.subTest(args=args), self.assertRaises(ValueError):
                bridge_fraction(*args)
        for args in ((-0.1, 1.0, 2.0), (0.5, 0.0, 2.0), (0.5, 1.0, math.inf)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                darcy_mobility(*args)


if __name__ == "__main__":
    unittest.main()
