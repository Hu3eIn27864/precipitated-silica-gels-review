#!/usr/bin/env python3
"""Unit tests for the analytical 1-D consolidation baseline."""
import unittest
from syneresis_1d import average_degree_of_consolidation


class ConsolidationTests(unittest.TestCase):
    def test_initial_condition(self):
        self.assertEqual(average_degree_of_consolidation(0.0, 1e-10, 1e-3), 0.0)

    def test_long_time_limit(self):
        value = average_degree_of_consolidation(1e9, 1e-10, 1e-3)
        self.assertAlmostEqual(value, 1.0, places=8)

    def test_monotonic_time(self):
        values = [average_degree_of_consolidation(t, 1e-10, 1e-3)
                  for t in (1.0, 10.0, 100.0, 1000.0)]
        self.assertEqual(values, sorted(values))

    def test_rejects_non_finite_inputs(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    average_degree_of_consolidation(value, 1e-10, 1e-3)
                with self.assertRaises(ValueError):
                    average_degree_of_consolidation(1.0, value, 1e-3)
                with self.assertRaises(ValueError):
                    average_degree_of_consolidation(1.0, 1e-10, value)

    def test_series_truncation_convergence(self):
        # At this dimensionless time, 1000 terms are already converged
        # to substantially better than 1e-10 relative to a 5000-term reference.
        reference = average_degree_of_consolidation(1e-4, 1.0, 1.0, terms=5000)
        value = average_degree_of_consolidation(1e-4, 1.0, 1.0, terms=1000)
        self.assertAlmostEqual(value, reference, places=12)

    def test_corrected_reference_table(self):
        references = (
            (0.001, 0.035682482323055424),
            (0.01, 0.11283791670955123),
            (0.05, 0.2523132521777547),
            (0.2, 0.5040878202025485),
            (0.5, 0.7639503307438488),
            (1.0, 0.9312596784633337),
            (2.0, 0.9941704789261604),
        )
        for tv, expected in references:
            with self.subTest(tv=tv):
                value = average_degree_of_consolidation(tv, 1.0, 1.0)
                self.assertAlmostEqual(value, expected, places=12)

    def test_reference_value_checks_eigenvalue_factor(self):
        # Independent series evaluation at Tv=0.1 for a double-drained slab.
        value = average_degree_of_consolidation(0.1, 1.0, 1.0)
        self.assertAlmostEqual(value, 0.3568234004524541, places=12)

    def test_short_time_asymptotic_is_term_independent(self):
        # At Tv << 1, the Poisson-transformed solution is
        # U ~ 2*sqrt(Tv/pi), with exponentially small corrections.
        tv = 1e-6
        expected = 2.0 * (tv / 3.141592653589793) ** 0.5
        a = average_degree_of_consolidation(tv, 1.0, 1.0, terms=1)
        b = average_degree_of_consolidation(tv, 1.0, 1.0, terms=1000)
        self.assertAlmostEqual(a, expected, places=14)
        self.assertEqual(a, b)

    def test_short_time_square_root_scaling(self):
        u1 = average_degree_of_consolidation(1e-6, 1.0, 1.0)
        u2 = average_degree_of_consolidation(4e-6, 1.0, 1.0)
        self.assertAlmostEqual(u2 / u1, 2.0, places=12)

    def test_short_time_to_series_transition_is_continuous(self):
        below = average_degree_of_consolidation(0.01 * (1.0 - 1e-8), 1.0, 1.0)
        above = average_degree_of_consolidation(0.01 * (1.0 + 1e-8), 1.0, 1.0)
        self.assertLess(abs(above - below), 1e-7)

    def test_dimensionless_scaling(self):
        # Equal cv*t/Hd^2 must produce the same average consolidation.
        u1 = average_degree_of_consolidation(100.0, 1e-10, 1e-3)
        u2 = average_degree_of_consolidation(400.0, 1e-10, 2e-3)
        self.assertAlmostEqual(u1, u2, places=12)


if __name__ == "__main__":
    unittest.main()
