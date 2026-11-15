import unittest
from ccfsm_p27_10_vertex_edge_link_audit import audit_tetra_mesh_links

class TestP2710(unittest.TestCase):
    def test_single_tetrahedron_is_closed_ball_locally(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
        r=audit_tetra_mesh_links(v,((0,1,2,3),))
        self.assertEqual(r["status"],"locally_manifold_audited")
        self.assertEqual(r["vertex_count_checked"],4)
        self.assertEqual(r["edge_count_checked"],6)
        self.assertTrue(all(x["expected_link"]=="triangulated_disk" for x in r["vertex_link_reports"].values()))
        self.assertTrue(all(x["expected_link"]=="path" for x in r["edge_link_reports"].values()))

    def test_two_tetrahedra_sharing_face_pass(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,0,-1))
        r=audit_tetra_mesh_links(v,((0,1,2,3),(1,0,2,4)))
        self.assertEqual(r["status"],"locally_manifold_audited")
        self.assertEqual(r["invalid_vertex_links"],())
        self.assertEqual(r["invalid_edge_links"],())

    def test_interior_edge_has_cycle_link(self):
        # Four tetrahedra around the z-axis edge (0,1), with a cyclic link.
        v=((0,0,-1),(0,0,1),(1,0,0),(0,1,0),(-1,0,0),(0,-1,0))
        t=((0,1,2,3),(0,1,3,4),(0,1,4,5),(0,1,5,2))
        r=audit_tetra_mesh_links(v,t)
        self.assertEqual(r["status"],"locally_manifold_audited")
        self.assertEqual(r["edge_link_reports"][(0,1)]["expected_link"],"cycle")
        self.assertEqual(r["edge_link_reports"][(0,1)]["degree_sequence"],(2,2,2,2))

    def test_disconnected_edge_link_rejected(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,-1,0),(0,0,-1))
        r=audit_tetra_mesh_links(v,((0,1,2,3),(0,1,4,5)))
        self.assertEqual(r["status"],"link_inconsistent")
        self.assertIn((0,1),r["invalid_edge_links"])
        self.assertFalse(r["edge_link_reports"][(0,1)]["connected"])

    def test_base_nonmanifold_failure_propagates(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,0,-1),(0,0,2))
        r=audit_tetra_mesh_links(v,((0,1,2,3),(1,0,2,4),(0,1,2,5)))
        self.assertEqual(r["status"],"base_audit_failed")

    def test_unused_coordinate_vertex_is_reported_outside_mesh_complex(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(2,2,2))
        r=audit_tetra_mesh_links(v,((0,1,2,3),))
        self.assertEqual(r["status"],"locally_manifold_audited")
        self.assertEqual(r["vertex_count_checked"],4)
        self.assertEqual(r["base_incidence_audit"]["isolated_vertex_indices"],(4,))


    def test_vertex_with_disconnected_link_is_rejected(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1))
        r=audit_tetra_mesh_links(v,((0,1,2,3),(0,4,5,6)))
        self.assertEqual(r["status"],"link_inconsistent")
        self.assertIn(0,r["invalid_vertex_links"])
        self.assertFalse(r["vertex_link_reports"][0]["triangle_edge_connected"])

if __name__=="__main__": unittest.main()
