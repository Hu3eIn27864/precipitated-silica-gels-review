import unittest

from ccfsm_p27_36_monotone_polynomial_root import (
    classify_monotone_polynomial_root,
    polynomial_derivative_coefficients,
)


class P2736MonotonePolynomialRootTests(unittest.TestCase):
    def test_increasing_linear_polynomial_has_one_root(self):
        result = classify_monotone_polynomial_root([1.0, -0.25], 0.0, 0.5)
        self.assertEqual(result["status"], "certified_unique_root")
        self.assertEqual(result["root_count"], 1)
        self.assertEqual(result["monotonicity"], "strictly_increasing")

    def test_decreasing_linear_polynomial_has_one_root(self):
        result = classify_monotone_polynomial_root([-2.0, 0.5], 0.0, 1.0)
        self.assertEqual(result["status"], "certified_unique_root")
        self.assertEqual(result["monotonicity"], "strictly_decreasing")

    def test_monotone_positive_polynomial_has_no_root(self):
        result = classify_monotone_polynomial_root([1.0, 2.0], -1.0, 1.0)
        self.assertEqual(result["status"], "certified_no_root")
        self.assertEqual(result["root_count"], 0)

    def test_monotone_negative_polynomial_has_no_root(self):
        result = classify_monotone_polynomial_root([-1.0, -2.0], -1.0, 1.0)
        self.assertEqual(result["status"], "certified_no_root")

    def test_derivative_zero_inclusion_remains_unresolved(self):
        result = classify_monotone_polynomial_root([1.0, -1.0, 0.25], 0.4, 0.6)
        self.assertEqual(result["status"], "unresolved_derivative_contains_zero")
        self.assertIsNone(result["root_count"])

    def test_endpoint_root_is_not_misreported_as_interior_unique_root(self):
        result = classify_monotone_polynomial_root([1.0, 0.0], 0.0, 1.0)
        self.assertEqual(result["status"], "unresolved_endpoint_sign")

    def test_derivative_coefficients(self):
        self.assertEqual(polynomial_derivative_coefficients([3.0, -2.0, 5.0]), (6.0, -2.0))
        self.assertEqual(polynomial_derivative_coefficients([4.0]), (0.0,))

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            classify_monotone_polynomial_root([], 0.0, 1.0)
        with self.assertRaises(ValueError):
            classify_monotone_polynomial_root([float("inf"), 1.0], 0.0, 1.0)
        with self.assertRaises(ValueError):
            classify_monotone_polynomial_root([1.0, 0.0], 1.0, 1.0)


if __name__ == "__main__":
    unittest.main()
