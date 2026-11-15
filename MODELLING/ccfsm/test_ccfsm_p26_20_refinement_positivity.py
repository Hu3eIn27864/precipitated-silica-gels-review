import unittest
from fractions import Fraction

from ccfsm_p26_13_markov_lukacs_socp import certify_cell_nonnegative
from ccfsm_p26_19_exact_profile_restriction import restrict_quadratic_profile
from ccfsm_p26_20_refinement_positivity import (
    verify_cell_certificate, verify_refined_profile_certificates,
)


class TestP2620RefinementPositivity(unittest.TestCase):
    def _certify_children(self, profile):
        certs = []
        for m, a, b in zip(profile["averages"], profile["linear"], profile["quadratic"]):
            # P26.13 accepts exact Fraction inputs; P26.19 exports rational strings.
            cert = certify_cell_nonnegative(*(Fraction(str(v)) for v in (m, a, b)))
            self.assertIsNotNone(cert)
            self.assertTrue(verify_cell_certificate(m, a, b, cert)["verified"])
            certs.append(cert)
        return certs

    def test_positive_parent_remains_certifiable_after_nonuniform_refinement(self):
        profile = restrict_quadratic_profile(
            (0, 1), (2,), (Fraction(1, 5),), (Fraction(1, 10),),
            (0, Fraction(1, 7), Fraction(1, 2), Fraction(5, 6), 1))
        certs = self._certify_children(profile)
        result = verify_refined_profile_certificates(profile, certs)
        self.assertTrue(result["verified"])
        self.assertEqual(len(result["cell_results"]), 4)

    def test_endpoint_touching_profile_survives_refinement(self):
        profile = restrict_quadratic_profile(
            (0, 1), (Fraction(1, 3),), (1,), (1,),
            (0, Fraction(1, 3), Fraction(2, 3), 1))
        certs = self._certify_children(profile)
        self.assertTrue(verify_refined_profile_certificates(profile, certs)["verified"])

    def test_zero_profile_has_exact_child_certificates(self):
        profile = restrict_quadratic_profile(
            (0, 1), (0,), (0,), (0,), (0, Fraction(1, 2), 1))
        certs = self._certify_children(profile)
        self.assertTrue(verify_refined_profile_certificates(profile, certs)["verified"])

    def test_independent_verifier_rejects_tampered_gram_matrix(self):
        cert = certify_cell_nonnegative(2, Fraction(1, 5), Fraction(1, 10))
        bad = dict(cert)
        bad["Q"] = ((Fraction(-1), Fraction(0)), (Fraction(0), Fraction(1)))
        self.assertFalse(verify_cell_certificate(2, Fraction(1, 5),
                                                Fraction(1, 10), bad)["verified"])

    def test_independent_verifier_rejects_nonsymmetric_gram_matrix(self):
        cert = certify_cell_nonnegative(2, Fraction(1, 5), Fraction(1, 10))
        bad = dict(cert)
        bad["Q"] = ((cert["Q"][0][0], Fraction(0)),
                    (Fraction(1, 3), cert["Q"][1][1]))
        self.assertFalse(verify_cell_certificate(2, Fraction(1, 5),
                                                Fraction(1, 10), bad)["verified"])

    def test_independent_verifier_rejects_identity_mismatch(self):
        cert = certify_cell_nonnegative(2, Fraction(1, 5), Fraction(1, 10))
        self.assertFalse(verify_cell_certificate(3, Fraction(1, 5),
                                                Fraction(1, 10), cert)["verified"])

    def test_independent_verifier_rejects_negative_multiplier(self):
        cert = certify_cell_nonnegative(2, 0, 0)
        bad = dict(cert)
        bad["lambda"] = Fraction(-1)
        self.assertFalse(verify_cell_certificate(2, 0, 0, bad)["verified"])

    def test_cell_count_mismatch_is_not_accepted(self):
        profile = restrict_quadratic_profile(
            (0, 1), (2,), (0,), (0,), (0, Fraction(1, 2), 1))
        result = verify_refined_profile_certificates(profile, ())
        self.assertFalse(result["verified"])
        self.assertEqual(result["reason"], "cell_count_mismatch")

    def test_negative_parent_is_not_promoted_to_positive(self):
        self.assertIsNone(certify_cell_nonnegative(Fraction(1, 10), 0, -2))


if __name__ == "__main__":
    unittest.main()
