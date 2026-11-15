import unittest
from copy import deepcopy
from fractions import Fraction as F

from ccfsm_p27_3_tetra_p2_subdivision import certify_tetra_p2_by_subdivision
from ccfsm_p27_4_tetra_p2_certificate_verifier import verify_p27_3_certificate


class TestP274IndependentVerifier(unittest.TestCase):
    def setUp(self):
        self.tet = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
        self.v = (F(17,16), F(17,16), F(1,16), F(1,16))
        self.e = (F(1,16), F(5,16), F(5,16), F(5,16), F(5,16), F(1,16))
        self.cert = certify_tetra_p2_by_subdivision(self.tet, self.v, self.e, 4)

    def test_independently_replays_positive_tree(self):
        r = verify_p27_3_certificate(self.tet, self.v, self.e, self.cert)
        self.assertTrue(r["verified"])
        self.assertEqual(r["status"], "certified_nonnegative")

    def test_rejects_mutated_leaf_coefficient(self):
        c = deepcopy(self.cert)
        rec = dict(c["leaf_records"][0])
        rec["bernstein_coefficients"] = tuple(rec["bernstein_coefficients"][:-1]) + (F(999),)
        c["leaf_records"] = (rec,) + tuple(c["leaf_records"][1:])
        self.assertFalse(verify_p27_3_certificate(self.tet, self.v, self.e, c)["verified"])

    def test_rejects_missing_leaf(self):
        c = deepcopy(self.cert)
        c["leaf_records"] = tuple(c["leaf_records"][:-1])
        self.assertFalse(verify_p27_3_certificate(self.tet, self.v, self.e, c)["verified"])

    def test_rejects_duplicate_leaf(self):
        c = deepcopy(self.cert)
        c["leaf_records"] = tuple(c["leaf_records"]) + (c["leaf_records"][0],)
        self.assertFalse(verify_p27_3_certificate(self.tet, self.v, self.e, c)["verified"])

    def test_rejects_wrong_root_polynomial(self):
        altered = tuple(x + 1 for x in self.v)
        self.assertFalse(verify_p27_3_certificate(self.tet, altered, self.e, self.cert)["verified"])

    def test_verifies_exact_negative_point(self):
        v = (F(1,2), F(-1,2), F(-1,2), F(-1,2))
        e = tuple((v[i]+v[j])/2 for i,j in ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3)))
        cert = certify_tetra_p2_by_subdivision(self.tet, v, e, 2)
        self.assertTrue(verify_p27_3_certificate(self.tet, v, e, cert)["verified"])
        c = dict(cert)
        c["value"] = F(123)
        self.assertFalse(verify_p27_3_certificate(self.tet, v, e, c)["verified"])

    def test_unresolved_is_verified_as_unresolved(self):
        cert = certify_tetra_p2_by_subdivision(self.tet, self.v, self.e, 0)
        r = verify_p27_3_certificate(self.tet, self.v, self.e, cert)
        self.assertTrue(r["verified"])
        self.assertEqual(r["status"], "unresolved")


if __name__ == "__main__":
    unittest.main()
