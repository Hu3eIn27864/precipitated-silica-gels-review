import unittest
from ccfsm_p27_9_global_incidence_audit import audit_global_tetra_mesh

class TestP279(unittest.TestCase):
    def setUp(self):
        self.v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,0,-1),(1,1,1))
    def test_single_tetra_boundary(self):
        r=audit_global_tetra_mesh(self.v[:4],((0,1,2,3),))
        self.assertEqual(r["status"],"incidence_audited")
        self.assertEqual(r["boundary_face_count"],4)
        self.assertEqual(r["interior_face_count"],0)
    def test_two_tets_share_one_face_and_orientation(self):
        r=audit_global_tetra_mesh(self.v[:5],((0,1,2,3),(1,0,2,4)))
        self.assertEqual(r["status"],"incidence_audited")
        self.assertEqual(r["interior_face_count"],1)
        self.assertEqual(r["boundary_face_count"],6)
        self.assertEqual(r["interior_face_orientation_conflicts"],())
        self.assertEqual(r["component_count"],1)
    def test_three_tets_on_one_face_rejected(self):
        v=self.v[:5]+((0,0,2),)
        r=audit_global_tetra_mesh(v,((0,1,2,3),(1,0,2,4),(0,1,2,5)))
        self.assertEqual(r["status"],"incidence_inconsistent")
        self.assertEqual(len(r["nonmanifold_face_candidates"]),1)
    def test_duplicate_tetrahedron_rejected(self):
        r=audit_global_tetra_mesh(self.v[:4],((0,1,2,3),(3,2,1,0)))
        self.assertEqual(r["reason"],"duplicate_tetrahedron")
    def test_isolated_vertex_reported(self):
        r=audit_global_tetra_mesh(self.v,((0,1,2,3),))
        self.assertEqual(r["isolated_vertex_indices"],(4,5))
    def test_disconnected_components(self):
        v=self.v[:4]+((3,0,0),(3,1,0),(3,0,1),(3,0,2))
        r=audit_global_tetra_mesh(v,((0,1,2,3),(4,5,6,7)))
        self.assertEqual(r["component_count"],2)
    def test_bad_connectivity_and_degenerate(self):
        self.assertEqual(audit_global_tetra_mesh(self.v[:4],((0,1,1,3),))["status"],"invalid")
        flat=((0,0,0),(1,0,0),(0,1,0),(1,1,0))
        self.assertEqual(audit_global_tetra_mesh(flat,((0,1,2,3),))["status"],"invalid")
    def test_inverted_element_normalized(self):
        r=audit_global_tetra_mesh(self.v[:4],((0,2,1,3),))
        self.assertEqual(r["status"],"incidence_audited")
        self.assertEqual(r["tetrahedra"],((0,1,2,3),))

if __name__=="__main__": unittest.main()
