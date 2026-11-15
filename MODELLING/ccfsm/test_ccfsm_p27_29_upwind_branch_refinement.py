import unittest

from ccfsm_p27_29_upwind_branch_refinement import (
    audit_p27_29_upwind_branch_refinement,
)


class P27_29UpwindBranchRefinementTests(unittest.TestCase):
    def test_exact_piecewise_reference_and_sign_switches(self):
        report = audit_p27_29_upwind_branch_refinement()
        self.assertAlmostEqual(report["exact"]["chemical_left_j"], -2.25)
        self.assertAlmostEqual(report["exact"]["chemical_right_j"], 3.75)
        self.assertAlmostEqual(report["exact"]["chemical_total_j"], 1.5)
        self.assertAlmostEqual(report["exact"]["material_total_mol"], 1.5)
        self.assertEqual(report["branch_switches_s"], {"left": 1.0, "right": 1.5})

    def test_aligned_support_points_remove_branch_kink_error(self):
        report = audit_p27_29_upwind_branch_refinement()
        by_n = {x["subintervals"]: x for x in report["refinements"]}
        self.assertTrue(by_n[4]["left_switch_is_support_point"])
        self.assertTrue(by_n[4]["right_switch_is_support_point"])
        self.assertLess(by_n[4]["chemical_abs_error_j"],
                        by_n[3]["chemical_abs_error_j"])

    def test_refinement_reports_separate_material_and_energy_errors(self):
        report = audit_p27_29_upwind_branch_refinement(support_counts=(1, 2, 4, 8, 16))
        for row in report["refinements"]:
            self.assertIn("chemical_abs_error_j", row)
            self.assertIn("material_abs_error_mol", row)
            self.assertGreaterEqual(row["chemical_abs_error_j"], 0.0)
            self.assertGreaterEqual(row["material_abs_error_mol"], 0.0)
        self.assertLess(report["refinements"][-1]["chemical_abs_error_j"],
                        report["refinements"][0]["chemical_abs_error_j"])

    def test_invalid_supports_rejected(self):
        with self.assertRaisesRegex(ValueError, "distinct positive"):
            audit_p27_29_upwind_branch_refinement(support_counts=(1, 1))


if __name__ == "__main__":
    unittest.main()
