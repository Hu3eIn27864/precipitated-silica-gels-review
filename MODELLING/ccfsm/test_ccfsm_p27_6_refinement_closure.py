import unittest
from ccfsm_p27_6_refinement_closure import close_tetra_refinement_depths


class TestP276(unittest.TestCase):
    def setUp(self):
        self.tets = ((0, 1, 2, 3), (0, 2, 1, 4), (5, 6, 7, 8))

    def test_one_sided_mark_promotes_face_neighbor(self):
        r = close_tetra_refinement_depths(self.tets, (1, 0, 0))
        self.assertEqual(r["status"], "closed")
        self.assertEqual(r["closed_depths"], (1, 1, 0))
        self.assertEqual(r["promoted_elements"], (1,))
        self.assertEqual(r["predicted_leaf_tetrahedra"], 17)

    def test_connected_chain_closes_to_component_maximum(self):
        tets = ((0, 1, 2, 3), (0, 2, 1, 4), (0, 1, 4, 5))
        r = close_tetra_refinement_depths(tets, (0, 2, 1))
        self.assertEqual(r["status"], "closed")
        self.assertEqual(r["closed_depths"], (2, 2, 2))

    def test_disconnected_component_not_promoted(self):
        r = close_tetra_refinement_depths(self.tets, (2, 0, 1))
        self.assertEqual(r["closed_depths"], (2, 2, 1))

    def test_equal_depths_remain_unchanged(self):
        r = close_tetra_refinement_depths(self.tets[:2], (2, 2))
        self.assertEqual(r["closed_depths"], (2, 2))
        self.assertEqual(r["promoted_elements"], ())

    def test_nonmanifold_rejected(self):
        tets = self.tets[:2] + ((0, 1, 2, 9),)
        r = close_tetra_refinement_depths(tets, (0, 0, 0))
        self.assertEqual(r["status"], "invalid")
        self.assertEqual(r["reason"], "nonmanifold_coarse_face")

    def test_resource_cap_is_unresolved_and_nonmutating(self):
        r = close_tetra_refinement_depths(self.tets[:2], (2, 0), max_total_leaf_tetrahedra=100)
        self.assertEqual(r["status"], "unresolved")
        self.assertFalse(r["mesh_modified"])
        self.assertEqual(r["reason"], "predicted_leaf_element_cap_exceeded")

    def test_depth_cap(self):
        r = close_tetra_refinement_depths(self.tets[:1], (9,))
        self.assertEqual(r["status"], "unresolved")
        self.assertEqual(r["reason"], "requested_depth_exceeds_cap")

    def test_bad_depths_and_connectivity(self):
        self.assertEqual(close_tetra_refinement_depths(self.tets[:1], (-1,))["status"], "invalid")
        self.assertEqual(close_tetra_refinement_depths(((0, 1, 1, 2),), (0,))["status"], "invalid")
        self.assertEqual(close_tetra_refinement_depths(self.tets[:1], (True,))["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
