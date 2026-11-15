import unittest

from ccfsm_p27_26_reference_verification import (
    manufactured_quadrature_report, polynomial_integral, trapezoid_samples,
)


class P27_26ReferenceTests(unittest.TestCase):
    def test_exact_constant_and_linear_reference(self):
        self.assertAlmostEqual(polynomial_integral((3.0,), 0.0, 2.0), 6.0)
        self.assertAlmostEqual(polynomial_integral((1.0, 2.0), 0.0, 2.0), 6.0)

    def test_composite_trapezoid_exact_for_linear_history(self):
        self.assertAlmostEqual(
            trapezoid_samples((0.0, 0.25, 1.0), (2.0, 2.5, 4.0)), 3.0
        )

    def test_quadratic_error_reduces_by_four_on_halving_dt(self):
        coarse = manufactured_quadrature_report((1.0, 2.0, 3.0), 0.0, 1.0, 4)
        fine = manufactured_quadrature_report((1.0, 2.0, 3.0), 0.0, 1.0, 8)
        self.assertAlmostEqual(coarse["absolute_error"] / fine["absolute_error"], 4.0)
        self.assertIsNone(fine["order_claimed"])

    def test_quadrature_independent_of_p27_25_adapter(self):
        # Cubic data also provides an exact reference; no P27.25 function is called.
        report = manufactured_quadrature_report((0.5, -1.0, 0.0, 2.0), -1.0, 1.0, 100)
        self.assertAlmostEqual(report["exact_integral"], 1.0)
        self.assertLess(report["absolute_error"], 1e-3)

    def test_invalid_time_grid_rejected(self):
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            trapezoid_samples((0.0, 1.0, 1.0), (1.0, 2.0, 3.0))


if __name__ == "__main__":
    unittest.main()
