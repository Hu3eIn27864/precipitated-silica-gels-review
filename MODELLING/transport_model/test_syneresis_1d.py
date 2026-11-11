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

    def test_dimensionless_scaling(self):
        # Equal cv*t/Hd^2 must produce the same average consolidation.
        u1 = average_degree_of_consolidation(100.0, 1e-10, 1e-3)
        u2 = average_degree_of_consolidation(400.0, 1e-10, 2e-3)
        self.assertAlmostEqual(u1, u2, places=12)


if __name__ == "__main__":
    unittest.main()
