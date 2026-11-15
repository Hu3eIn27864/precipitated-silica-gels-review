import unittest
from fractions import Fraction

from ccfsm_p27_1_tetra_p1_positivity import (
    tetrahedron_signed_six_volume, verify_tetra_p1_mesh,
    verify_tetra_p1_positivity,
)


class TestP271TetraP1Positivity(unittest.TestCase):
    def setUp(self):
        self.tet = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))

    def test_exact_unit_tetrahedron_volume(self):
        self.assertEqual(tetrahedron_signed_six_volume(self.tet), 1)
        result = verify_tetra_p1_positivity(self.tet, (0, 1, 2, 3))
        self.assertTrue(result["verified"])
        self.assertEqual(result["volume"], Fraction(1, 6))

    def test_negative_orientation_is_valid_geometry(self):
        tet = (self.tet[0], self.tet[2], self.tet[1], self.tet[3])
        result = verify_tetra_p1_positivity(tet, (1, 1, 1, 1))
        self.assertTrue(result["verified"])
        self.assertEqual(result["signed_six_volume"], -1)

    def test_zero_vertex_value_is_allowed(self):
        self.assertTrue(verify_tetra_p1_positivity(
            self.tet, (0, Fraction(1, 3), 2, 5))["verified"])

    def test_negative_vertex_value_is_rejected(self):
        result = verify_tetra_p1_positivity(self.tet, (1, 0, -1, 2))
        self.assertFalse(result["verified"])
        self.assertEqual(result["reason"], "negative_vertex_value")

    def test_degenerate_tetrahedron_is_rejected(self):
        flat = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0))
        self.assertEqual(verify_tetra_p1_positivity(
            flat, (1, 1, 1, 1))["reason"], "degenerate_tetrahedron")

    def test_mesh_requires_every_element_to_pass(self):
        nodes = self.tet + ((1, 1, 1),)
        result = verify_tetra_p1_mesh(nodes, (1, 1, 1, 1, -1),
                                      ((0, 1, 2, 3), (1, 2, 3, 4)))
        self.assertFalse(result["verified"])
        self.assertEqual(len(result["cells"]), 2)

    def test_bad_connectivity_is_rejected(self):
        result = verify_tetra_p1_mesh(self.tet, (1, 1, 1, 1), ((0, 1, 1, 3),))
        self.assertFalse(result["verified"])
        self.assertEqual(result["cells"][0]["reason"], "invalid_connectivity")

    def test_rational_geometry_is_exact(self):
        tet = ((0, 0, 0), (Fraction(1, 3), 0, 0),
               (0, Fraction(1, 2), 0), (0, 0, Fraction(1, 4)))
        self.assertEqual(tetrahedron_signed_six_volume(tet), Fraction(1, 24))


if __name__ == "__main__":
    unittest.main()
