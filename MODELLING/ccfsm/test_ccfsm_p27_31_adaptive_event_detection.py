import unittest

from ccfsm_p27_31_adaptive_event_detection import (
    adaptive_flux_samples,
    audit_p27_31_adaptive_event_detection,
)


class P27_31AdaptiveEventDetectionTests(unittest.TestCase):
    def test_hidden_two_root_pair_is_detected(self):
        report = audit_p27_31_adaptive_event_detection()
        roots = report["detected_roots_by_flux_s"][0]
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0], 0.35, places=6)
        self.assertAlmostEqual(roots[1], 0.75, places=6)

    def test_linear_boundary_events_are_retained(self):
        report = audit_p27_31_adaptive_event_detection()
        self.assertAlmostEqual(report["detected_roots_by_flux_s"][1][0], 1.0)
        self.assertAlmostEqual(report["detected_roots_by_flux_s"][2][0], 1.5)

    def test_adaptive_grid_refines_coarse_interval(self):
        report = audit_p27_31_adaptive_event_detection()
        self.assertGreater(report["sampled"]["evaluations"], 2)

    def test_same_sign_without_curvature_does_not_refine(self):
        sampled = adaptive_flux_samples(
            (lambda t: 2.0,), 0.0, 1.0, initial_intervals=1,
            curvature_atol=1e-8, curvature_rtol=1e-8)
        self.assertEqual(sampled["sample_times_s"], (0.0, 1.0))

    def test_invalid_settings_and_nonfinite_flux_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid interval"):
            adaptive_flux_samples((lambda t: t,), 1.0, 0.0)
        with self.assertRaisesRegex(ValueError, "finite"):
            adaptive_flux_samples((lambda t: float("nan"),), 0.0, 1.0)

    def test_refinement_depth_is_bounded(self):
        sampled = adaptive_flux_samples(
            (lambda t: (t - 0.31) * (t - 0.72),), 0.0, 1.0,
            curvature_atol=0.0, curvature_rtol=0.0, max_depth=4)
        self.assertLessEqual(sampled["evaluations"], 2 ** 4 + 1)


if __name__ == "__main__":
    unittest.main()
