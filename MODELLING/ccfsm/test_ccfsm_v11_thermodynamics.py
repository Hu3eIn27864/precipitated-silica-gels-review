"""Structural tests for the CCFSM v1.1 thermodynamic core."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent


class CCFSMv11ThermodynamicsTests(unittest.TestCase):
    def test_energy_core_has_conjugate_variables_and_balance(self):
        text = (ROOT / "CCFSM_v1.1_THERMODYNAMIC_CORE_DE.md").read_text(encoding="utf-8")
        for token in ("\\psi_0", "\\boldsymbol\\sigma=\\partial_\\varepsilon\\psi_0",
                      "p=\\partial_\\zeta\\psi_0", "\\mathbf q=-\\mathbb L_p\\nabla p",
                      "\\frac{d}{dt}\\mathcal F_0", "noch offen"):
            self.assertIn(token, text)

    def test_p0_proof_cancels_biot_coupling(self):
        text = (ROOT / "CCFSM_v1.1_P0_ENERGY_ESTIMATE_DE.md").read_text(encoding="utf-8")
        self.assertIn("heben sich exakt auf", text)
        self.assertIn("Korn-Ungleichung", text)
        self.assertIn("nichtlinearen CCFSM P1–P5", text)

    def test_scope_does_not_overclaim(self):
        text = (ROOT / "CCFSM_v1.1_THERMODYNAMIC_CORE_DE.md").read_text(encoding="utf-8")
        self.assertIn("Kein vollständiger thermodynamischer Abschluss", text)
        self.assertIn("noch kein empirisch belegtes Silica-Kinetikgesetz", text)


if __name__ == "__main__":
    unittest.main()
