"""Structural checks for the CCFSM v1.0 research specification.
These validate document/register completeness only, not physics or PDE theorems.
Run: python -m unittest MODELLING/ccfsm/test_ccfsm_v10_specification.py
"""
from pathlib import Path
import csv
import unittest

ROOT = Path(__file__).resolve().parent


class CCFSMv10SpecificationTests(unittest.TestCase):
    def test_pde_specification_contains_required_blocks(self):
        text = (ROOT / "CCFSM_v1.0_3D_PDE_SYSTEM_DE.md").read_text(encoding="utf-8")
        for token in ("Phasenbilanz", "Darcy-Fluss", "Mechanisches Gleichgewicht",
                      "Netzwerkbildung", "Morphologie", "Chemischer Speziestransport",
                      "Thermodynamische Struktur", "Rand- und Anfangsbedingungen",
                      "**keine** vollständig abgeleitete freie Energie"):
            self.assertIn(token, text)

    def test_mathematical_programme_separates_proof_goals(self):
        text = (ROOT / "CCFSM_v1.0_MATHEMATICAL_PROGRAMME_DE.md").read_text(encoding="utf-8")
        for token in ("P0", "P5", "schwache Existenz", "Eindeutigkeit",
                      "Funktionsräume", "a-priori-Abschätzungen",
                      "nicht als Beweis", "kein vollständig ausgeführter Beweis"):
            self.assertIn(token, text)

    def test_equation_register_schema_and_blocks(self):
        with (ROOT / "CCFSM_v1.0_EQUATION_REGISTER.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 8)
        self.assertEqual(set(rows[0]), {
            "block", "equation_or_relation", "unknowns", "required_closure",
            "status", "verification_target", "notes"
        })
        blocks = {row["block"] for row in rows}
        self.assertTrue({"phase_mass", "darcy", "mechanics", "bridges",
                         "morphology", "contraction", "species", "energy",
                         "boundary"}.issubset(blocks))
        self.assertEqual(len(blocks), len(rows))

    def test_no_claim_of_full_model_proof(self):
        text = (ROOT / "CCFSM_v1.0_3D_PDE_SYSTEM_DE.md").read_text(encoding="utf-8")
        self.assertIn("Noch keine", text)
        self.assertIn("keinen globalen Regularitätsbeweis", text)


if __name__ == "__main__":
    unittest.main()
