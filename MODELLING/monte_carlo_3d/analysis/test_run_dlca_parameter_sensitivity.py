import math
import unittest

from run_dlca_parameter_sensitivity import (
    VARIANTS, validate_target_q, validate_variant,
)


class ParameterSensitivityTests(unittest.TestCase):
    def test_matrix_changes_one_parameter_at_a_time(self):
        self.assertEqual(len(VARIANTS), 7)
        baseline = (1.0, 0.2, 1.0)
        self.assertEqual(VARIANTS[0], ("baseline", *baseline))
        for name, contact, step, mobility in VARIANTS:
            values = (contact, step, mobility)
            self.assertEqual(sum(a != b for a, b in zip(values, baseline)),
                             0 if name == "baseline" else 1, name)
            validate_variant(*values)

    def test_target_q_must_be_finite_and_nonnegative(self):
        validate_target_q(0.0)
        validate_target_q(2000.0)
        for value in (-1.0, float("nan"), float("inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_target_q(value)

    def test_rejects_contact_step_violation(self):
        with self.assertRaises(ValueError):
            validate_variant(1.0, 0.3, 1.0)

    def test_rejects_non_finite_and_invalid_values(self):
        for values in ((float("nan"), 0.1, 1.0),
                       (1.0, float("inf"), 1.0),
                       (1.0, 0.1, -0.1)):
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    validate_variant(*values)


if __name__ == "__main__":
    unittest.main()
