"""Unit tests for the natural-syneresis reduced CCFSM module."""
import math
import unittest

from ccfsm_reduced import (
    NaturalSyneresisFit,
    apparent_rate_per_hour,
    exact_relaxation_step,
    hydraulic_relaxation_time_seconds,
    initial_shrinkage_rate_per_hour,
    log_volume_contraction,
    shrinkage,
    shrinkage_rate,
    solid_volume_fraction,
)


class TestNaturalSyneresisFit(unittest.TestCase):
    def setUp(self):
        self.fit = NaturalSyneresisFit(amplitude=0.4, tau_hours=2.0)

    def test_initial_condition(self):
        self.assertEqual(shrinkage(0.0, self.fit), 0.0)
        self.assertAlmostEqual(shrinkage_rate(0.0, self.fit), 0.2)

    def test_monotone_and_bounded(self):
        values = [shrinkage(t, self.fit) for t in (0.0, 0.1, 1.0, 2.0, 10.0)]
        self.assertTrue(all(0.0 <= x < self.fit.amplitude for x in values))
        self.assertEqual(values, sorted(values))

    def test_asymptote(self):
        self.assertAlmostEqual(shrinkage(100.0, self.fit), 0.4, places=10)

    def test_exact_step_semigroup(self):
        one_step = exact_relaxation_step(0.0, 3.0, self.fit)
        two_steps = exact_relaxation_step(
            exact_relaxation_step(0.0, 1.25, self.fit), 1.75, self.fit
        )
        self.assertAlmostEqual(one_step, two_steps, places=14)
        self.assertAlmostEqual(one_step, shrinkage(3.0, self.fit), places=14)

    def test_exact_step_preserves_interval(self):
        s = 0.15
        for _ in range(100):
            s = exact_relaxation_step(s, 0.5, self.fit)
            self.assertGreaterEqual(s, 0.0)
            self.assertLessEqual(s, self.fit.amplitude)

    def test_solid_volume_balance(self):
        self.assertAlmostEqual(solid_volume_fraction(0.2, 0.5), 0.4)
        with self.assertRaises(ValueError):
            solid_volume_fraction(0.8, 0.5)

    def test_hydraulic_time_scale_dimensions_and_value(self):
        # 1 Pa s * (1 m)^2 / (1 * 1e-12 m^2 * 1e6 Pa) = 1e6 s
        value = hydraulic_relaxation_time_seconds(
            1.0, 1.0, 1e-12, 1e6, 1.0
        )
        self.assertAlmostEqual(value, 1e6)

    def test_derived_coefficients(self):
        self.assertAlmostEqual(apparent_rate_per_hour(self.fit), 0.5)
        self.assertAlmostEqual(initial_shrinkage_rate_per_hour(self.fit), 0.2)

    def test_log_contraction(self):
        self.assertAlmostEqual(log_volume_contraction(0.5), math.log(2.0))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            NaturalSyneresisFit(amplitude=1.0, tau_hours=2.0)
        with self.assertRaises(ValueError):
            NaturalSyneresisFit(amplitude=0.2, tau_hours=0.0)
        with self.assertRaises(ValueError):
            shrinkage(-0.1, self.fit)
        with self.assertRaises(ValueError):
            exact_relaxation_step(0.5, 1.0, self.fit)


if __name__ == "__main__":
    unittest.main()
