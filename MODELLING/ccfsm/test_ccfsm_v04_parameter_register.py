"""Structural checks for the CCFSM v0.4 influence-parameter register."""
import csv
from pathlib import Path
import unittest

REGISTER = Path(__file__).with_name("CCFSM_v0.4_INFLUENCE_PARAMETER_REGISTER.csv")
REQUIRED = {
    "symbol", "name", "group", "role", "unit", "status",
    "primary_path", "required_observation", "identifiability_caution",
}


class TestCCFSMV04ParameterRegister(unittest.TestCase):
    def test_register_has_complete_schema_and_unique_symbols(self):
        with REGISTER.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(set(reader.fieldnames or ()), REQUIRED)
            rows = list(reader)
        self.assertGreaterEqual(len(rows), 40)
        self.assertEqual(len({row["symbol"] for row in rows}), len(rows))
        for row in rows:
            for field in REQUIRED:
                self.assertTrue(row[field].strip(), (row["symbol"], field))

    def test_natural_syneresis_scope_is_explicit(self):
        with REGISTER.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        symbols = {row["symbol"] for row in rows}
        self.assertTrue({"pH", "T_g", "D_f", "kappa_eff", "K_eff",
                         "R_c", "L_d", "eta_a", "J_evap"} <= symbols)


if __name__ == "__main__":
    unittest.main()
