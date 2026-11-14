"""Regression tests for the natural-syneresis two-timescale CCFSM."""
import math
import unittest
from ccfsm_two_stage import (
    TwoTimescaleNaturalSyneresis,
    hydraulic_rate_from_properties_per_hour,
    isotropic_natural_stretch,
    recover_unordered_rate_pair,
)


class TestTwoTimescaleNaturalSyneresis(unittest.TestCase):
    def test_initial_conditions_and_preaged_network(self):
        m = TwoTimescaleNaturalSyneresis(0.5, 0.4, 0.8, 0.2, 0.1, 0.8)
        self.assertAlmostEqual(m.intrinsic_potential(0), 0.2)
        self.assertAlmostEqual(m.shrinkage(0), 0.1)
        self.assertAlmostEqual(m.shrinkage_rate(0), 0.8 * (0.8 * 0.2 - 0.1))

    def test_zero_initial_two_stage_lag(self):
        m = TwoTimescaleNaturalSyneresis(0.4, 2.0, 0.5)
        self.assertAlmostEqual(m.shrinkage(0), 0.0)
        self.assertAlmostEqual(m.shrinkage_rate(0), 0.0)
        self.assertGreater(m.shrinkage(0.1), 0.0)

    def test_equal_rate_limit(self):
        m = TwoTimescaleNaturalSyneresis(0.4, 1.25, 1.25)
        expected = 0.4 * (1.0 - (1.0 + 1.25 * 2.0) * math.exp(-2.5))
        self.assertAlmostEqual(m.shrinkage(2.0), expected, places=14)

    def test_continuity_near_equal_rates(self):
        a = TwoTimescaleNaturalSyneresis(0.4, 1.0, 1.0)
        b = TwoTimescaleNaturalSyneresis(0.4, 1.0, 1.0 + 1e-10)
        self.assertAlmostEqual(a.shrinkage(3.0), b.shrinkage(3.0), places=10)

    def test_monotonicity_and_invariant_region(self):
        m = TwoTimescaleNaturalSyneresis(0.6, 0.17, 0.9, 0.15, 0.04)
        previous = m.shrinkage(0.0)
        for i in range(1, 1001):
            t = i * 0.02
            q, s = m.intrinsic_potential(t), m.shrinkage(t)
            self.assertGreaterEqual(s, -1e-13)
            self.assertLessEqual(s, q + 1e-12)
            self.assertLessEqual(q, m.q_infinity + 1e-12)
            self.assertGreaterEqual(s + 1e-12, previous)
            self.assertGreaterEqual(m.shrinkage_rate(t), -1e-13)
            previous = s

    def test_long_time_limit(self):
        m = TwoTimescaleNaturalSyneresis(0.55, 0.3, 0.8, 0.1, 0.05)
        self.assertAlmostEqual(m.shrinkage(1e4), 0.55, places=12)
        self.assertAlmostEqual(m.intrinsic_potential(1e4), 0.55, places=12)

    def test_accessibility_limits_endpoint(self):
        m = TwoTimescaleNaturalSyneresis(0.7, 0.3, 0.8, 0.1, 0.02, 0.4)
        for i in range(1000):
            t = 0.02 * i
            self.assertLessEqual(m.shrinkage(t), 0.4 * m.intrinsic_potential(t) + 1e-12)
        self.assertAlmostEqual(m.shrinkage(1e4), 0.28, places=12)

    def test_rate_swap_nonidentifiability(self):
        a = TwoTimescaleNaturalSyneresis(0.42, 0.25, 1.8, accessibility=0.7)
        b = TwoTimescaleNaturalSyneresis(0.42, 1.8, 0.25, accessibility=0.7)
        for t in (0.0, 0.1, 0.5, 2.0, 10.0, 100.0):
            self.assertAlmostEqual(a.shrinkage(t), b.shrinkage(t), places=14)

    def test_unordered_rate_recovery(self):
        pair = recover_unordered_rate_pair(2.05, 0.45)
        self.assertAlmostEqual(pair[0], 0.25)
        self.assertAlmostEqual(pair[1], 1.8)

    def test_hydraulic_rate_units_and_length_scaling(self):
        one = hydraulic_rate_from_properties_per_hour(1e-3, 1e-3, 1e-14, 1e4)
        two = hydraulic_rate_from_properties_per_hour(1e-3, 2e-3, 1e-14, 1e4)
        self.assertAlmostEqual(one / two, 4.0)

    def test_exact_finite_kinematics(self):
        q = 0.51
        lam = isotropic_natural_stretch(q)
        self.assertAlmostEqual(lam**3, 1.0 - q, places=14)

    def test_invalid_states_and_properties(self):
        with self.assertRaises(ValueError):
            TwoTimescaleNaturalSyneresis(0.4, 0.0, 1.0)
        with self.assertRaises(ValueError):
            TwoTimescaleNaturalSyneresis(0.4, 1.0, 1.0, 0.2, 0.3)
        with self.assertRaises(ValueError):
            TwoTimescaleNaturalSyneresis(0.4, 1.0, 1.0, 0.2, 0.2, 0.5)
        with self.assertRaises(ValueError):
            TwoTimescaleNaturalSyneresis(0.4, 1.0, 1.0, accessibility=0.0)
        with self.assertRaises(ValueError):
            hydraulic_rate_from_properties_per_hour(1e-3, 0.0, 1e-14, 1e4)
        with self.assertRaises(ValueError):
            recover_unordered_rate_pair(1.0, 2.0)


if __name__ == "__main__":
    unittest.main()
