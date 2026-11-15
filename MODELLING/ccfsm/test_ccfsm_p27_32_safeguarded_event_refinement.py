import unittest

from ccfsm_p27_32_safeguarded_event_refinement import (
    refine_flux_root_bisection,
    audit_p27_32_safeguarded_event_refinement,
)


class P27_32SafeguardedEventRefinementTests(unittest.TestCase):
    def test_hidden_pair_is_refined_to_narrow_brackets(self):
        report = audit_p27_32_safeguarded_event_refinement()
        roots = report["refined_roots_by_flux"][0]
        self.assertEqual(len(roots), 2)
        self.assertAlmostEqual(roots[0]["root_s"], 0.35, places=8)
        self.assertAlmostEqual(roots[1]["root_s"], 0.75, places=8)
        self.assertTrue(report["all_brackets_converged"])
        self.assertLessEqual(report["maximum_final_bracket_width_s"], 1e-10)

    def test_linear_roots(self):
        report = audit_p27_32_safeguarded_event_refinement()
        self.assertAlmostEqual(report["refined_roots_by_flux"][1][0]["root_s"], 1.0)
        self.assertAlmostEqual(report["refined_roots_by_flux"][2][0]["root_s"], 1.5)

    def test_endpoint_root(self):
        r = refine_flux_root_bisection(lambda t: t, 0.0, 1.0)
        self.assertEqual(r["root_s"], 0.0)
        self.assertTrue(r["converged"])

    def test_rejects_non_bracket(self):
        with self.assertRaisesRegex(ValueError, "sign-changing"):
            refine_flux_root_bisection(lambda t: t*t+1, 0.0, 1.0)

    def test_rejects_nonfinite_flux(self):
        with self.assertRaisesRegex(ValueError, "finite"):
            refine_flux_root_bisection(lambda t: float("nan"), 0.0, 1.0)

    def test_iteration_limit_is_reported(self):
        r = refine_flux_root_bisection(
            lambda t: t*t-0.1234567, 0.0, 1.0,
            time_tolerance=1e-30, flux_tolerance=0.0, max_iterations=2)
        self.assertFalse(r["converged"])
        self.assertEqual(r["termination"], "iteration_limit")


if __name__ == "__main__":
    unittest.main()
