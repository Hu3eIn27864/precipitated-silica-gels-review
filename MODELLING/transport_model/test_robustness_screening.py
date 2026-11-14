"""Tests for deterministic geometry/storage/mode robustness screening."""
import math
import unittest
from robustness_screening import screen_robustness


class RobustnessScreeningTests(unittest.TestCase):
    def setUp(self):
        self.design = {"storage": [1.0, 1.2], "mobility": [1.0, 0.65],
                       "widths": [0.4, 0.6], "contact_resistances": [0.08]}

    def test_scenario_count_and_rank_summary(self):
        result = screen_robustness(
            self.design, 0.4, interface_offsets=(-0.05, 0.0, 0.05),
            storage_scale_scenarios=((1.0, 1.0), (0.9, 1.1)),
            mode_scenarios=((0, 1, 2), (0, 2)))
        self.assertEqual(result["summary"]["scenario_count"], 12)
        self.assertIn(result["summary"]["minimum_rank"], (1, 2))
        self.assertGreaterEqual(result["summary"]["rank_two_fraction"], 0.0)
        self.assertLessEqual(result["summary"]["rank_two_fraction"], 1.0)

    def test_single_mode_assignment_is_rank_deficient(self):
        result = screen_robustness(self.design, 0.4,
                                   mode_scenarios=((1,),), n_modes=3)
        self.assertEqual(result["summary"]["minimum_rank"], 1)
        self.assertTrue(math.isinf(result["scenarios"][0]["condition_number"]))

    def test_invalid_perturbed_interface_rejected(self):
        with self.assertRaises(ValueError):
            screen_robustness(self.design, 0.4, interface_offsets=(0.7,))

    def test_invalid_storage_scale_rejected(self):
        with self.assertRaises(ValueError):
            screen_robustness(self.design, 0.4,
                              storage_scale_scenarios=((1.0, 0.0),))


if __name__ == "__main__":
    unittest.main()
