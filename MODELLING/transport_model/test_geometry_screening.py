#!/usr/bin/env python3
"""Geometry-design screening tests; all cases are synthetic."""
import unittest
from geometry_screening import screen_geometries


class GeometryScreeningTests(unittest.TestCase):
    def test_returns_all_requested_designs_ranked(self):
        rows = screen_geometries(
            [0.5, 1.0, 2.0], [0.25, 0.5, 0.75],
            [1.0, 1.2], [1.0, 0.65], 0.08, n_modes=3)
        self.assertEqual(len(rows), 9)
        self.assertTrue(all(row["rank"] in (1, 2) for row in rows))
        self.assertTrue(all(row["smallest_singular_value"] >= 0 for row in rows))

    def test_uncertainty_weighting_changes_information_scale(self):
        precise = screen_geometries(
            [1.0], [0.4], [1.0, 1.2], [1.0, 0.65], 0.08,
            n_modes=3, sigma_log_rates=[0.01, 0.01, 0.01])[0]
        noisy = screen_geometries(
            [1.0], [0.4], [1.0, 1.2], [1.0, 0.65], 0.08,
            n_modes=3, sigma_log_rates=[0.1, 0.1, 0.1])[0]
        self.assertAlmostEqual(
            precise["smallest_singular_value"] / noisy["smallest_singular_value"], 10.0,
            places=5)

    def test_invalid_geometry_is_rejected(self):
        with self.assertRaises(ValueError):
            screen_geometries([1.0], [1.0], [1.0, 1.0], [1.0, 1.0], 0.1)


if __name__ == "__main__":
    unittest.main()
