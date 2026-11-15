import unittest
from fractions import Fraction as F

from ccfsm_p27_3_tetra_p2_subdivision import certify_tetra_p2_by_subdivision


class TestP273AdaptiveSubdivision(unittest.TestCase):
    def setUp(self):
        self.tet = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))


    def test_eight_children_have_exact_equal_volumes(self):
        from ccfsm_p27_1_tetra_p1_positivity import tetrahedron_signed_six_volume
        from ccfsm_p27_3_tetra_p2_subdivision import _IDENTITY, _child_tetrahedra
        children = _child_tetrahedra(_IDENTITY)
        self.assertEqual(len(children), 8)
        volumes = []
        for child in children:
            physical = tuple(tuple(sum(child[i][k] * self.tet[k][axis] for k in range(4))
                                   for axis in range(3)) for i in range(4))
            volumes.append(abs(tetrahedron_signed_six_volume(physical)) / 6)
        self.assertEqual(set(volumes), {F(1, 48)})
        self.assertEqual(sum(volumes), F(1, 6))

    def test_positive_constant_certified_without_refinement(self):
        r = certify_tetra_p2_by_subdivision(self.tet, (2, 2, 2, 2), (2, 2, 2, 2, 2, 2), 0)
        self.assertEqual(r["status"], "certified_nonnegative")
        self.assertEqual(r["leaf_count"], 1)

    def test_positive_polynomial_with_negative_initial_bernstein_coefficient_resolves(self):
        # u=(lambda0-lambda1)^2 + 1/16 is strictly positive.
        # Its original b01=-15/16, but midpoint subdivision resolves it.
        vertex = (F(17, 16), F(17, 16), F(1, 16), F(1, 16))
        edge = (F(1, 16), F(5, 16), F(5, 16),
                F(5, 16), F(5, 16), F(1, 16))
        r = certify_tetra_p2_by_subdivision(self.tet, vertex, edge, 4)
        self.assertEqual(r["status"], "certified_nonnegative")
        self.assertGreater(r["visited_cells"], 1)

    def test_negative_polynomial_returns_exact_point_witness(self):
        # u=lambda0-1/2 has a negative value at vertex 1.
        vertex = (F(1, 2), F(-1, 2), F(-1, 2), F(-1, 2))
        edge = tuple((vertex[i] + vertex[j]) / 2 for i, j in
                     ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)))
        r = certify_tetra_p2_by_subdivision(self.tet, vertex, edge, 2)
        self.assertEqual(r["status"], "certified_negative_point")
        self.assertLess(r["value"], 0)

    def test_zero_polynomial_is_certified(self):
        r = certify_tetra_p2_by_subdivision(self.tet, (0, 0, 0, 0), (0, 0, 0, 0, 0, 0), 3)
        self.assertEqual(r["status"], "certified_nonnegative")

    def test_max_depth_zero_keeps_inconclusive_result(self):
        vertex = (F(17, 16), F(17, 16), F(1, 16), F(1, 16))
        edge = (F(1, 16), F(5, 16), F(5, 16),
                F(5, 16), F(5, 16), F(1, 16))
        r = certify_tetra_p2_by_subdivision(self.tet, vertex, edge, 0)
        self.assertEqual(r["status"], "unresolved")

    def test_degenerate_geometry_and_bad_depth_are_unresolved(self):
        flat = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0))
        self.assertEqual(certify_tetra_p2_by_subdivision(
            flat, (1, 1, 1, 1), (1, 1, 1, 1, 1, 1))["status"], "unresolved")
        self.assertEqual(certify_tetra_p2_by_subdivision(
            self.tet, (1, 1, 1, 1), (1, 1, 1, 1, 1, 1), -1)["reason"],
            "invalid_max_depth")


if __name__ == "__main__":
    unittest.main()
