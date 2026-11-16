import unittest

from ccfsm_p27_28_time_dependent_boundary import (
    audit_p27_28_time_dependent_boundary_case,
)


class P27_28TimeDependentBoundaryTests(unittest.TestCase):
    def test_exact_polynomial_reference_and_separate_budgets(self):
        report = audit_p27_28_time_dependent_boundary_case()
        self.assertAlmostEqual(report["exact"]["material_M_mol"], 2.9)
        self.assertAlmostEqual(report["exact"]["chemical_boundary_work_j"], 18.24)
        self.assertAlmostEqual(report["exact"]["hydraulic_boundary_work_j"], 7.9)
        self.assertEqual(set(report["material_error_budget_mol"]), {"M", "O"})
        self.assertEqual(set(report["energy_error_budget_j"]),
                         {"chemical_boundary", "hydraulic_boundary"})

    def test_quadrature_errors_are_reported_separately(self):
        report = audit_p27_28_time_dependent_boundary_case()
        self.assertGreater(report["absolute_error"]["material_M_mol"], 0.0)
        self.assertGreater(report["absolute_error"]["chemical_boundary_work_j"], 0.0)
        self.assertGreater(report["absolute_error"]["hydraulic_boundary_work_j"], 0.0)
        self.assertFalse(report["within_tolerance"])

    def test_linear_rate_trapezoid_is_exact_by_polynomial_identity(self):
        # Independently verifies the reference integration identity for degree 1.
        from ccfsm_p27_28_time_dependent_boundary import _poly_integral, _poly_value
        duration = 3.0
        coeff = (2.0, -0.5)
        exact = _poly_integral(coeff, duration)
        trapezoid = 0.5 * duration * (
            _poly_value(coeff, 0.0) + _poly_value(coeff, duration))
        self.assertAlmostEqual(exact, trapezoid)

    def test_invalid_parameters_rejected(self):
        with self.assertRaisesRegex(ValueError, "must be positive"):
            audit_p27_28_time_dependent_boundary_case(duration_s=0.0)


if __name__ == "__main__":
    unittest.main()
