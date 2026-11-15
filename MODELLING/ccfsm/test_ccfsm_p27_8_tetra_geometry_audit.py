import unittest
from fractions import Fraction as F
from ccfsm_p27_8_tetra_geometry_audit import normalize_and_audit_tetra_mesh,tetrahedron_geometry

class TestP278(unittest.TestCase):
    def setUp(self):
        self.simple=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
    def test_right_unit_tetrahedron_quality_is_exact(self):
        self.assertEqual(tetrahedron_geometry(self.simple,(0,1,2,3))["quality_ratio"],F(16,27))
    def test_positive_orientation(self):
        r=normalize_and_audit_tetra_mesh(self.simple,((0,1,2,3),))
        self.assertEqual(r["status"],"oriented_quality_audited"); self.assertGreater(r["element_signed_six_volumes"][0],0)
    def test_negative_orientation_normalized(self):
        r=normalize_and_audit_tetra_mesh(self.simple,((0,2,1,3),))
        self.assertEqual(r["status"],"oriented_quality_audited"); self.assertEqual(r["negative_orientation_flips"],(0,)); self.assertEqual(r["tetrahedra"],((0,1,2,3),))
    def test_scale_invariance(self):
        scaled=tuple(tuple(7*x for x in p) for p in self.simple)
        self.assertEqual(tetrahedron_geometry(self.simple,(0,1,2,3))["quality_ratio"],tetrahedron_geometry(scaled,(0,1,2,3))["quality_ratio"])
    def test_quality_threshold_rejects_without_mesh(self):
        r=normalize_and_audit_tetra_mesh(self.simple,((0,1,2,3),),min_quality_ratio=F(9,10))
        self.assertEqual(r["status"],"quality_below_threshold"); self.assertNotIn("tetrahedra",r)
    def test_degenerate_rejected(self):
        flat=((0,0,0),(1,0,0),(0,1,0),(1,1,0))
        r=normalize_and_audit_tetra_mesh(flat,((0,1,2,3),))
        self.assertEqual(r["reason"],"degenerate_tetrahedron")
    def test_bad_threshold_and_connectivity(self):
        self.assertEqual(normalize_and_audit_tetra_mesh(self.simple,((0,1,2,3),),min_quality_ratio=2)["status"],"invalid")
        self.assertEqual(normalize_and_audit_tetra_mesh(self.simple,((0,1,1,3),))["status"],"invalid")
    def test_mixed_orientation_batch(self):
        r=normalize_and_audit_tetra_mesh(self.simple+((0,0,-1),),((0,1,2,3),(1,0,2,4)))
        self.assertEqual(r["status"],"oriented_quality_audited"); self.assertTrue(all(v>0 for v in r["element_signed_six_volumes"]))

if __name__=="__main__": unittest.main()