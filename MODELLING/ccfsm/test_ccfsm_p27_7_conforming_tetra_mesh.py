import unittest
from fractions import Fraction as F

from ccfsm_p27_7_conforming_tetra_mesh import generate_conforming_red_refined_mesh


class TestP277(unittest.TestCase):
    def setUp(self):
        self.vertices = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1))
        self.tets = ((0, 1, 2, 3), (0, 2, 1, 4))

    def test_unrefined_mesh(self):
        r = generate_conforming_red_refined_mesh(self.vertices, self.tets, (0, 0))
        self.assertEqual(r["status"], "generated_conforming_mesh")
        self.assertEqual(r["generated_tetrahedron_count"], 2)
        self.assertEqual(r["conformity_audit"]["status"], "conforming")

    def test_one_sided_request_is_closed_and_generated(self):
        r = generate_conforming_red_refined_mesh(self.vertices, self.tets, (1, 0))
        self.assertEqual(r["status"], "generated_conforming_mesh")
        self.assertEqual(r["closed_refinement_depths"], (1, 1))
        self.assertEqual(r["generated_tetrahedron_count"], 16)
        self.assertEqual(r["conformity_audit"]["checked_shared_faces"], 1)

    def test_two_level_refinement(self):
        r = generate_conforming_red_refined_mesh(self.vertices, self.tets, (2, 0))
        self.assertEqual(r["status"], "generated_conforming_mesh")
        self.assertEqual(r["closed_refinement_depths"], (2, 2))
        self.assertEqual(r["generated_tetrahedron_count"], 128)

    def test_disconnected_component_can_have_different_depth(self):
        vertices = self.vertices + ((3, 0, 0), (4, 0, 0), (3, 1, 0), (3, 0, 1))
        tets = self.tets + ((5, 6, 7, 8),)
        r = generate_conforming_red_refined_mesh(vertices, tets, (1, 0, 0))
        self.assertEqual(r["status"], "generated_conforming_mesh")
        self.assertEqual(r["closed_refinement_depths"], (1, 1, 0))
        self.assertEqual(r["generated_tetrahedron_count"], 17)

    def test_resource_limit_returns_no_mesh(self):
        r = generate_conforming_red_refined_mesh(self.vertices, self.tets, (2, 0), max_total_leaf_tetrahedra=100)
        self.assertEqual(r["status"], "unresolved")
        self.assertNotIn("tetrahedra", r)

    def test_nonmanifold_rejected(self):
        vertices = self.vertices + ((0, 0, 2),)
        tets = self.tets + ((0, 1, 2, 5),)
        r = generate_conforming_red_refined_mesh(vertices, tets, (0, 0, 0))
        self.assertEqual(r["status"], "invalid")

    def test_exact_rational_coordinates(self):
        r = generate_conforming_red_refined_mesh(self.vertices, self.tets, (1, 0))
        self.assertEqual(r["status"], "generated_conforming_mesh")
        self.assertTrue(all(isinstance(x, F) for p in r["vertices"] for x in p))

    def test_bad_connectivity_and_depths(self):
        self.assertEqual(generate_conforming_red_refined_mesh(self.vertices, ((0, 1, 1, 3),), (0,))["status"], "invalid")
        self.assertEqual(generate_conforming_red_refined_mesh(self.vertices, self.tets, (-1, 0))["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
