from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent
PROOF = ROOT / "CCFSM_v1.2_P0_GALERKIN_EXISTENCE_DE.md"


class TestCCFSMP0GalerkinProof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PROOF.read_text(encoding="utf-8")

    def test_proof_artifact_and_scope(self):
        self.assertIn("Satz (schwache P0-Existenz)", self.text)
        self.assertIn("Eindeutigkeit", self.text)
        self.assertIn("P1–P5", self.text)
        self.assertIn("kein", self.text.lower())

    def test_function_spaces_and_boundary_conditions(self):
        for token in ("H^1_0", "H^1(\\Omega)", "L^2(0,T;Q')",
                      "No-Flow", "Korn"):
            self.assertIn(token, self.text)

    def test_schur_complement_and_energy(self):
        for token in ("m(p,r)", "a(Tp,Tr)", "Darcy-Dissipation",
                      "E-P0", "p(0)=p_0"):
            self.assertIn(token, self.text)

    def test_no_claim_of_full_model_proof(self):
        self.assertIn("nicht für das nichtlineare CCFSM P1–P5", self.text)
        self.assertIn("keinen globalen Regularitätssatz", self.text)


if __name__ == "__main__":
    unittest.main()
