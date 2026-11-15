import unittest
from fractions import Fraction
from ccfsm_p27_11_geometric_embedding_audit import audit_tetra_mesh_embedding

class TestP2711(unittest.TestCase):
    def test_single_tetrahedron(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
        r=audit_tetra_mesh_embedding(v,((0,1,2,3),))
        self.assertEqual(r["status"],"geometric_embedding_audited")
        self.assertEqual(r["tetrahedron_pair_count"],0)
    def test_shared_face_contact_is_allowed(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,0,-1))
        r=audit_tetra_mesh_embedding(v,((0,1,2,3),(1,0,2,4)))
        self.assertEqual(r["status"],"geometric_embedding_audited")
        self.assertEqual(r["positive_volume_overlap_pairs"],())
    def test_disjoint_tetrahedra(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(3,0,0),(4,0,0),(3,1,0),(3,0,1))
        r=audit_tetra_mesh_embedding(v,((0,1,2,3),(4,5,6,7)))
        self.assertEqual(r["status"],"geometric_embedding_audited")
    def test_nested_tetrahedron_overlap_detected(self):
        v=((0,0,0),(2,0,0),(0,2,0),(0,0,2),(Fraction(1,10),Fraction(1,10),Fraction(1,10)),
           (Fraction(2,10),Fraction(1,10),Fraction(1,10)),(Fraction(1,10),Fraction(2,10),Fraction(1,10)),
           (Fraction(1,10),Fraction(1,10),Fraction(2,10)))
        r=audit_tetra_mesh_embedding(v,((0,1,2,3),(4,5,6,7)))
        self.assertEqual(r["status"],"geometric_embedding_inconsistent")
        self.assertEqual(r["positive_volume_overlap_pairs"],((0,1),))
    def test_coincident_distinct_vertices_reported(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,0,0),(-1,0,0),(0,-1,0),(0,0,-1))
        r=audit_tetra_mesh_embedding(v,((0,1,2,3),(4,5,6,7)))
        self.assertEqual(r["status"],"geometric_embedding_inconsistent")
        self.assertIn((0,4),r["coincident_distinct_vertex_pairs"])
    def test_invalid_base_mesh_propagates(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,0,-1),(0,0,2))
        r=audit_tetra_mesh_embedding(v,((0,1,2,3),(1,0,2,4),(0,1,2,5)))
        self.assertEqual(r["status"],"base_audit_failed")

if __name__=="__main__": unittest.main()
