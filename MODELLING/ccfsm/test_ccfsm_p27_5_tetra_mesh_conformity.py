import unittest
from ccfsm_p27_5_tetra_mesh_conformity import IDENTITY,_children,audit_tetra_mesh_face_conformity
class TestP275(unittest.TestCase):
 def setUp(self):
  self.vertices=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,0,-1))
  self.tets=((0,1,2,3),(0,2,1,4))
 def cert(self,leaves): return {"status":"certified_nonnegative","leaf_records":tuple({"barycentric_vertices":v} for v in leaves)}
 def test_matching_unrefined(self):
  r=audit_tetra_mesh_face_conformity(self.vertices,self.tets,{0:self.cert((IDENTITY,)),1:self.cert((IDENTITY,))})
  self.assertEqual(r["status"],"conforming"); self.assertEqual(r["checked_shared_faces"],1)
 def test_detects_hanging_face(self):
  r=audit_tetra_mesh_face_conformity(self.vertices,self.tets,{0:self.cert((IDENTITY,)),1:self.cert(_children(IDENTITY))})
  self.assertEqual(r["status"],"nonconforming"); self.assertEqual(r["mismatch_count"],1)
 def test_matching_refined(self):
  c=self.cert(_children(IDENTITY))
  r=audit_tetra_mesh_face_conformity(self.vertices,self.tets,{0:c,1:c})
  self.assertEqual(r["status"],"conforming")
 def test_rejects_negative_early_exit(self):
  r=audit_tetra_mesh_face_conformity(self.vertices,self.tets,{0:{"status":"certified_negative_point"},1:self.cert((IDENTITY,))})
  self.assertEqual(r["status"],"invalid")
 def test_rejects_nonmanifold(self):
  v=self.vertices+((0,0,2),); t=self.tets+((0,1,2,5),); c={i:self.cert((IDENTITY,)) for i in range(3)}
  self.assertEqual(audit_tetra_mesh_face_conformity(v,t,c)["reason"],"nonmanifold_coarse_face")
 def test_rejects_bad_connectivity(self):
  self.assertEqual(audit_tetra_mesh_face_conformity(self.vertices,((0,1,1,3),),{})["status"],"invalid")
if __name__=="__main__": unittest.main()