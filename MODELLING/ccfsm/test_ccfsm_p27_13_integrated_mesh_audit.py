import unittest
from fractions import Fraction
from ccfsm_p27_13_integrated_mesh_audit import audit_tetra_mesh_3d


class TestP2713(unittest.TestCase):
    def test_single_tetrahedron_all_gates_pass(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
        r=audit_tetra_mesh_3d(v,((0,1,2,3),))
        self.assertEqual(r["status"],"integrated_mesh_audited")
        self.assertTrue(r["overall_pass"])
        self.assertEqual(set(r["gate_results"].values()), {
            "passed","incidence_audited","locally_manifold_audited",
            "geometric_embedding_audited","oriented_boundary_audited"})
        self.assertEqual(r["mesh_summary"]["boundary_signed_volume"],Fraction(1,6))
        self.assertFalse(r["physical_ccfsm_positivity_certified"])

    def test_shared_face_two_tetrahedra(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,0,-1))
        r=audit_tetra_mesh_3d(v,((0,1,2,3),(1,0,2,4)))
        self.assertTrue(r["overall_pass"])
        self.assertEqual(r["mesh_summary"]["boundary_triangle_count"],6)
        self.assertEqual(r["mesh_summary"]["boundary_component_count"],1)

    def test_disconnected_valid_mesh_reports_components(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),
           (3,0,0),(4,0,0),(3,1,0),(3,0,1))
        r=audit_tetra_mesh_3d(v,((0,1,2,3),(4,5,6,7)))
        self.assertTrue(r["overall_pass"])
        self.assertEqual(r["mesh_summary"]["boundary_component_count"],2)

    def test_quality_gate_stops_pipeline(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
        r=audit_tetra_mesh_3d(v,((0,1,2,3),),min_quality_ratio=Fraction(1))
        self.assertFalse(r["overall_pass"])
        self.assertEqual(r["gate_results"]["P27.8_geometry_quality"],
                         "quality_below_threshold")
        self.assertEqual(r["gate_results"]["P27.11_geometric_embedding"],"not_run")

    def test_invalid_mesh_stops_pipeline(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
        r=audit_tetra_mesh_3d(v,((0,1,2,3),(0,1,2,3)))
        self.assertFalse(r["overall_pass"])
        self.assertEqual(r["status"],"integrated_mesh_audit_failed")
        self.assertFalse(r["all_required_gates_passed"])


if __name__=="__main__":
    unittest.main()
