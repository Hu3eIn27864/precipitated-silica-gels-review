import unittest

from ccfsm_p27_30_event_aware_time_support import (
    audit_p27_30_event_aware_time_support,
    detect_zero_crossings,
)


class P27_30EventAwareTimeSupportTests(unittest.TestCase):
    def test_zero_crossings_are_interpolated(self):
        roots = detect_zero_crossings(
            (0.0, 1.0, 2.0),
            ((-1.0, 0.0, 1.0), (1.5, 0.5, -0.5)),
        )
        self.assertEqual(roots, ((1.0,), (1.5,)))

    def test_no_sign_change_has_no_interior_event(self):
        self.assertEqual(detect_zero_crossings(
            (0.0, 1.0, 2.0), ((1.0, 2.0, 3.0),)), ((),))

    def test_event_grid_inserts_both_upwind_switches(self):
        report = audit_p27_30_event_aware_time_support()
        self.assertEqual(report["inserted_event_times_s"], (1.0, 1.5))
        event = report["comparisons"][1]
        self.assertIn(1.0, event["support_times_s"])
        self.assertIn(1.5, event["support_times_s"])
        self.assertGreater(event["time_support_points"],
                           report["comparisons"][0]["time_support_points"])

    def test_event_alignment_reduces_branch_quadrature_error(self):
        report = audit_p27_30_event_aware_time_support()
        uniform, event = report["comparisons"]
        self.assertLess(event["chemical_abs_error_j"],
                        uniform["chemical_abs_error_j"])

    def test_material_error_is_reported_separately(self):
        report = audit_p27_30_event_aware_time_support()
        for item in report["comparisons"]:
            self.assertGreaterEqual(item["material_abs_error_mol"], 0.0)
            self.assertGreaterEqual(item["chemical_abs_error_j"], 0.0)

    def test_multiple_roots_and_invalid_inputs(self):
        roots = detect_zero_crossings(
            (0.0, 1.0, 2.0, 3.0), ((-1.0, 1.0, -1.0, 1.0),))
        self.assertEqual(roots, ((0.5, 1.5, 2.5),))
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            detect_zero_crossings((0.0, 0.0), ((-1.0, 1.0),))


if __name__ == "__main__":
    unittest.main()
