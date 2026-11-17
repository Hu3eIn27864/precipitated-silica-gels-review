import json
import math
import unittest
from fractions import Fraction

from ccfsm_p27_49_rational_certificate import (
    SCHEMA,
    binary64_fraction,
    descending_binary64_to_ascending_payload,
    loads_certificate_json,
    parse_rational_payload,
    polynomial_payload,
    rational_payload,
    validate_polynomial_payload,
)


class P2749RationalCertificateTests(unittest.TestCase):
    def test_binary64_conversion_is_exact_dyadic(self):
        self.assertEqual(binary64_fraction(0.5), Fraction(1, 2))
        self.assertEqual(binary64_fraction(-0.125), Fraction(-1, 8))
        self.assertEqual(
            binary64_fraction(math.nextafter(0.0, 1.0)),
            Fraction(1, 2**1074),
        )

    def test_descending_python_order_is_reversed_for_lean(self):
        payload = descending_binary64_to_ascending_payload([1.0, -0.3, 0.0])
        self.assertEqual(
            tuple(parse_rational_payload(item) for item in payload),
            (Fraction(0), binary64_fraction(-0.3), Fraction(1)),
        )

    def test_negative_zero_has_canonical_rational_zero(self):
        self.assertEqual(rational_payload(binary64_fraction(-0.0)), {"num": "0", "den": "1"})

    def test_payload_round_trip(self):
        payload = polynomial_payload([1.0, -0.3], 0.0, 1.0)
        self.assertEqual(payload["schema"], SCHEMA)
        coeffs, left, right = validate_polynomial_payload(payload)
        self.assertEqual(coeffs, (binary64_fraction(-0.3), Fraction(1)))
        self.assertEqual((left, right), (Fraction(0), Fraction(1)))

    def test_rejects_boolean_and_nonfinite_binary64(self):
        for value in (True, float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    binary64_fraction(value)

    def test_rejects_noncanonical_rationals(self):
        for payload in (
            {"num": "2", "den": "4"},
            {"num": "0", "den": "7"},
            {"num": "1", "den": "0"},
            {"num": "1", "den": "-2"},
            {"num": "01", "den": "1"},
            {"num": "-0", "den": "1"},
            {"num": 1, "den": "2"},
            {"num": "1", "den": "2", "extra": "x"},
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(ValueError):
                    parse_rational_payload(payload)

    def test_rejects_duplicate_json_keys(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            loads_certificate_json('{"schema":"a","schema":"b"}')

    def test_rejects_unknown_schema_and_wrong_order(self):
        payload = polynomial_payload([1.0, -0.3], 0.0, 1.0)
        bad = dict(payload, schema="future.version")
        with self.assertRaises(ValueError):
            validate_polynomial_payload(bad)
        bad = dict(payload, coefficient_order="descending_power")
        with self.assertRaises(ValueError):
            validate_polynomial_payload(bad)

    def test_rejects_float_proof_values_and_invalid_domain(self):
        payload = polynomial_payload([1.0, -0.3], 0.0, 1.0)
        bad = dict(payload)
        bad["coefficients"] = [0.1, payload["coefficients"][1]]
        with self.assertRaises(ValueError):
            validate_polynomial_payload(bad)
        with self.assertRaises(ValueError):
            polynomial_payload([1.0], 1.0, 1.0)
        zero = polynomial_payload([0.0], 0.0, 1.0)
        with self.assertRaises(ValueError):
            validate_polynomial_payload(zero)
        noncanonical = polynomial_payload([1.0, 0.0], 0.0, 1.0)
        noncanonical["coefficients"] = [rational_payload(Fraction(1)), rational_payload(Fraction(0))]
        with self.assertRaises(ValueError):
            validate_polynomial_payload(noncanonical)

    def test_payload_is_json_serializable_without_float_values(self):
        payload = polynomial_payload([1.0, -0.3], 0.0, 1.0)
        encoded = json.dumps(payload, sort_keys=True)
        decoded = loads_certificate_json(encoded)
        validate_polynomial_payload(decoded)


if __name__ == "__main__":
    unittest.main()
