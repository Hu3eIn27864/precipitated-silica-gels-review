import unittest

from ccfsm_p27_27_boundary_reference import audit_p27_27_boundary_reference_cases


class P27_27BoundaryReferenceTests(unittest.TestCase):
    def test_closed_boundaries_have_zero_transfer_and_boundary_work(self):
        report = audit_p27_27_boundary_reference_cases()
        self.assertAlmostEqual(report["observed"]["closed_chemical_j"], 0.0)
        self.assertAlmostEqual(report["observed"]["closed_hydraulic_j"], 0.0)
        self.assertAlmostEqual(report["observed"]["closed_M_transfer_mol"], 0.0)
        self.assertAlmostEqual(report["observed"]["closed_O_transfer_mol"], 0.0)

    def test_open_case_matches_independent_chemical_work_reference(self):
        report = audit_p27_27_boundary_reference_cases()
        self.assertAlmostEqual(report["expected"]["open_chemical_j"], 49.5)
        self.assertAlmostEqual(report["observed"]["open_chemical_j"], 49.5)

    def test_open_case_matches_hydraulic_work_reference(self):
        report = audit_p27_27_boundary_reference_cases()
        self.assertAlmostEqual(report["observed"]["open_hydraulic_j"], 24.0)

    def test_open_case_matches_species_material_transfer(self):
        report = audit_p27_27_boundary_reference_cases()
        self.assertAlmostEqual(report["observed"]["open_M_transfer_mol"], 10.5)
        self.assertAlmostEqual(report["observed"]["open_O_transfer_mol"], 0.0)

    def test_audit_reports_separate_error_budget_and_scope(self):
        report = audit_p27_27_boundary_reference_cases()
        self.assertTrue(report["passed"])
        self.assertTrue(all(value <= report["tolerance"]
                            for value in report["absolute_errors"].values()))
        self.assertIn("full upwind entropy chain rule", report["not_certified"])

    def test_invalid_tolerance_rejected(self):
        with self.assertRaisesRegex(ValueError, "tolerance must be positive"):
            audit_p27_27_boundary_reference_cases(0.0)


if __name__ == "__main__":
    unittest.main()
