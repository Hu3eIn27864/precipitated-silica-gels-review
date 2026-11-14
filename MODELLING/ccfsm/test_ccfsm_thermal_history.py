import math
import unittest

from ccfsm_thermal_history import (
    RateSegment,
    arrhenius_rate_per_hour,
    exact_segment_update,
    simulate_piecewise_constant_rates,
)
from ccfsm_two_stage import TwoTimescaleNaturalSyneresis


class TestThermalHistory(unittest.TestCase):
    def test_single_segment_recovers_v02(self):
        model = TwoTimescaleNaturalSyneresis(0.42, 0.35, 0.8, 0.1, 0.02, 0.75)
        q, s = exact_segment_update(
            0.1, 0.02, 0.42, 0.75, RateSegment(2.5, 0.35, 0.8)
        )
        self.assertAlmostEqual(q, model.intrinsic_potential(2.5), places=14)
        self.assertAlmostEqual(s, model.shrinkage(2.5), places=14)

    def test_two_equal_segments_semigroup(self):
        one = simulate_piecewise_constant_rates(
            [RateSegment(2.0, 0.4, 0.7)], 0.5, 0.8
        )[-1]
        two = simulate_piecewise_constant_rates(
            [RateSegment(0.75, 0.4, 0.7), RateSegment(1.25, 0.4, 0.7)],
            0.5, 0.8,
        )[-1]
        self.assertAlmostEqual(one.intrinsic_potential, two.intrinsic_potential, places=14)
        self.assertAlmostEqual(one.observed_shrinkage, two.observed_shrinkage, places=14)

    def test_temperature_switch_is_history_dependent(self):
        staged = simulate_piecewise_constant_rates(
            [RateSegment(1.0 / 3.0, 0.1, 0.15), RateSegment(2.0, 0.45, 0.8)],
            0.5,
        )[-1]
        instant = simulate_piecewise_constant_rates(
            [RateSegment(7.0 / 3.0, 0.45, 0.8)], 0.5
        )[-1]
        self.assertNotAlmostEqual(staged.observed_shrinkage, instant.observed_shrinkage, places=5)
        self.assertNotAlmostEqual(staged.intrinsic_potential, instant.intrinsic_potential, places=5)

    def test_invariant_region_across_many_segments(self):
        segments = [
            RateSegment(0.03 + i * 0.001, 0.05 + i * 0.02, 0.08 + i * 0.03)
            for i in range(20)
        ]
        states = simulate_piecewise_constant_rates(segments, 0.7, 0.65, 0.1, 0.03)
        for state in states:
            self.assertGreaterEqual(state.intrinsic_potential, 0.0)
            self.assertLessEqual(state.intrinsic_potential, 0.7 + 1e-13)
            self.assertGreaterEqual(state.observed_shrinkage, 0.0)
            self.assertLessEqual(state.observed_shrinkage, 0.65 * state.intrinsic_potential + 1e-12)
        self.assertTrue(all(
            states[i + 1].observed_shrinkage >= states[i].observed_shrinkage - 1e-13
            for i in range(len(states) - 1)
        ))

    def test_equal_rate_segment_limit(self):
        q, s = exact_segment_update(0.0, 0.0, 0.4, 1.0, RateSegment(2.0, 0.7, 0.7))
        expected = 0.4 * (1.0 - (1.0 + 0.7 * 2.0) * math.exp(-1.4))
        self.assertAlmostEqual(s, expected, places=14)
        self.assertAlmostEqual(q, 0.4 * (1.0 - math.exp(-1.4)), places=14)

    def test_arrhenius_reference_and_temperature_direction(self):
        kref = arrhenius_rate_per_hour(0.2, 50000.0, 300.0, 300.0)
        khot = arrhenius_rate_per_hour(0.2, 50000.0, 330.0, 300.0)
        self.assertAlmostEqual(kref, 0.2)
        self.assertGreater(khot, kref)

    def test_zero_duration_and_invalid_inputs(self):
        q, s = exact_segment_update(0.1, 0.05, 0.5, 1.0, RateSegment(0.0, 0.3, 0.4))
        self.assertAlmostEqual(q, 0.1)
        self.assertAlmostEqual(s, 0.05)
        with self.assertRaises(ValueError):
            RateSegment(-0.1, 0.3, 0.4)
        with self.assertRaises(ValueError):
            RateSegment(1.0, 0.0, 0.4)
        with self.assertRaises(ValueError):
            arrhenius_rate_per_hour(0.2, 40000.0, 0.0, 300.0)
        with self.assertRaises(ValueError):
            simulate_piecewise_constant_rates([], 0.5, q_initial=0.1, shrinkage_initial=0.2)


if __name__ == "__main__":
    unittest.main()
