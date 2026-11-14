#!/usr/bin/env python3
"""Synthetic recovery tests; no experimental silica data are used."""
import math
import unittest
from multilayer_reference import multilayer_eigenvalues
from synthetic_inverse import recover_common_scales


class SyntheticInverseTests(unittest.TestCase):
    def setUp(self):
        self.designs = [
            {"storage": [1.0, 1.0], "mobility": [1.0, 0.7],
             "widths": [0.4, 0.6], "contact_resistances": [0.08]},
            {"storage": [1.2, 0.8], "mobility": [0.6, 1.4],
             "widths": [0.65, 0.35], "contact_resistances": [0.12]},
        ]

    def records(self, m, r, n=3):
        result = []
        for d in self.designs:
            rates = multilayer_eigenvalues(
                d["storage"], [v*m for v in d["mobility"]], d["widths"], n,
                [v*r for v in d["contact_resistances"]])
            result.append(dict(d, log_rates=[math.log(v) for v in rates]))
        return result

    def test_exact_synthetic_parameter_recovery(self):
        result = recover_common_scales(self.records(1.7, 2.3), n_modes=3)
        self.assertTrue(result["converged"])
        self.assertAlmostEqual(result["mobility_scale"], 1.7, places=7)
        self.assertAlmostEqual(result["contact_resistance_scale"], 2.3, places=7)
        self.assertLess(result["weighted_residual_norm"], 1e-8)

    def test_recovery_from_displaced_initial_guess(self):
        result = recover_common_scales(
            self.records(0.65, 3.1), n_modes=3, initial=(0.5, -0.4))
        self.assertAlmostEqual(result["mobility_scale"], 0.65, places=6)
        self.assertAlmostEqual(result["contact_resistance_scale"], 3.1, places=6)

    def test_one_mode_single_design_is_rejected(self):
        with self.assertRaises(ValueError):
            recover_common_scales(self.records(1.2, 1.4, n=1)[:1], n_modes=1)

    def test_invalid_observation_uncertainty_is_rejected(self):
        records = self.records(1.2, 1.4)
        records[0]["sigma_log_rates"] = [1.0, 0.0, 1.0]
        with self.assertRaises(ValueError):
            recover_common_scales(records, n_modes=3)


if __name__ == "__main__":
    unittest.main()
