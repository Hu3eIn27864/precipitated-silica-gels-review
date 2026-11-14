#!/usr/bin/env python3
"""Tests for local identifiability of bulk mobility and contact resistance."""
import math
import unittest
from identifiability import log_rate_sensitivity


class IdentifiabilityTests(unittest.TestCase):
    def setUp(self):
        self.design = {
            "storage": [1.0, 1.0],
            "mobility": [1.0, 1.0],
            "widths": [0.4, 0.6],
            "contact_resistances": [0.08],
        }

    def test_one_modal_rate_cannot_identify_two_parameters(self):
        result = log_rate_sensitivity([self.design], n_modes=1)
        self.assertEqual(result["n_observations"], 1)
        self.assertEqual(result["rank"], 1)
        self.assertTrue(math.isinf(result["condition_number"]))

    def test_multiple_modes_identify_two_synthetic_scales_locally(self):
        result = log_rate_sensitivity([self.design], n_modes=3)
        self.assertEqual(result["rank"], 2)
        self.assertTrue(math.isfinite(result["condition_number"]))
        self.assertGreater(result["singular_values"][1], 0.0)

    def test_nearly_collinear_modes_keep_small_singular_value(self):
        result = log_rate_sensitivity([self.design], n_modes=3, mode_indices=(0, 1))
        self.assertEqual(result["rank"], 2)
        self.assertGreater(result["singular_values"][1], 0.0)
        self.assertGreater(result["condition_number"], 10.0)

    def test_log_finite_difference_step_stability(self):
        coarse = log_rate_sensitivity([self.design], n_modes=3, step=1e-3)
        fine = log_rate_sensitivity([self.design], n_modes=3, step=5e-4)
        for a, b in zip(coarse["jacobian"], fine["jacobian"]):
            for x, y in zip(a, b):
                self.assertAlmostEqual(x, y, delta=2e-5)

    def test_uncertainty_weighting_changes_information_scale(self):
        weighted = dict(self.design, sigma_log_rates=[0.1, 0.2])
        plain = log_rate_sensitivity([self.design], n_modes=2)
        scaled = log_rate_sensitivity([weighted], n_modes=2)
        self.assertGreater(scaled["singular_values"][0],
                           plain["singular_values"][0])

    def test_zero_contact_is_not_replaced_by_epsilon(self):
        zero = dict(self.design, contact_resistances=[0.0])
        with self.assertRaises(ValueError):
            log_rate_sensitivity([zero], n_modes=1)

    def test_invalid_uncertainty_is_rejected(self):
        bad = dict(self.design, sigma_log_rates=[1.0, 0.0])
        with self.assertRaises(ValueError):
            log_rate_sensitivity([bad], n_modes=2)


if __name__ == "__main__":
    unittest.main()
