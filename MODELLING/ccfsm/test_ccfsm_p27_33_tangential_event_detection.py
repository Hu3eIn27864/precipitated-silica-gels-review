import unittest

from ccfsm_p27_33_tangential_event_detection import (
    quadratic_tangency_candidates,
    audit_p27_33_tangential_event_detection,
)


class P27_33TangentialEventDetectionTests(unittest.TestCase):
    def test_even_multiplicity_root_without_sign_change(self):
        report = audit_p27_33_tangential_event_detection()
        self.assertTrue(report["tangential_candidate_found"])
        self.assertAlmostEqual(
            report["tangential_candidates"][0]["time_s"], 0.37, places=8)
        self.assertLess(
            report["maximum_tangential_candidate_error_s"], 1e-8)

    def test_original_flux_is_evaluated_at_candidate(self):
        # A deliberately inconsistent callable rejects a spurious quadratic fit.
        times = (0.0, 0.5, 1.0)
        values = (0.25, 0.0, 0.25)
        candidates = quadratic_tangency_candidates(
            times, values, lambda t: 1.0, flux_tolerance=1e-8)
        self.assertEqual(candidates, ())

    def test_nonuniform_sample_times(self):
        f = lambda t: (t-0.4)**2
        candidates = quadratic_tangency_candidates(
            (0.0, 0.2, 0.9), tuple(f(t) for t in (0.0, 0.2, 0.9)),
            f, flux_tolerance=1e-12)
        self.assertEqual(len(candidates), 1)
        self.assertAlmostEqual(candidates[0]["time_s"], 0.4, places=12)

    def test_sign_change_roots_are_still_refined(self):
        report = audit_p27_33_tangential_event_detection()
        roots = report["refined_sign_change_roots"]
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0]["root_s"], 0.23, places=8)
        self.assertAlmostEqual(roots[1]["root_s"], 0.81, places=8)

    def test_invalid_samples_rejected(self):
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            quadratic_tangency_candidates(
                (0.0, 0.5, 0.5), (1.0, 0.0, 1.0), lambda t: 0.0)

    def test_nonfinite_original_flux_rejected(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            quadratic_tangency_candidates(
                (0.0, 0.5, 1.0), (1.0, 0.0, 1.0),
                lambda t: float("nan"))


if __name__ == "__main__":
    unittest.main()
