import unittest
from ccfsm_p19_spatial_biot_bvp import P19Parameters,p19_solve_spatial_biot_bvp

class TestP19(unittest.TestCase):
 def setUp(self): self.p=P19Parameters(2e6,1e6,1e7,.8)
 def test_bar_patch_with_traction(self):
  B=[[-1.,1.],[0,0],[0,0],[0,0],[0,0],[0,0]]
  q=[{"B":B,"weight":1.,"eigenstrain":0.,"fluid_content_increment":0.}]
  face={"N":[[0.,1.],[0.,0.],[0.,0.]],"traction":[1000.,0.,0.],"weight":1.}
  r=p19_solve_spatial_biot_bvp(2,q,self.p,{0:0.},[face])
  self.assertAlmostEqual(r["displacement_dofs"][1],1000./4e6,delta=1e-12)
  self.assertTrue(r["free_dof_equilibrium_verified"])
 def test_eigenstrain_and_fluid_drive_solution(self):
  B=[[-1.,1.],[0,0],[0,0],[0,0],[0,0],[0,0]]
  q=[{"B":B,"weight":1.,"eigenstrain":.001,"fluid_content_increment":.002}]
  r=p19_solve_spatial_biot_bvp(2,q,self.p,{0:0.})
  self.assertTrue(r["free_dof_equilibrium_verified"])
  self.assertNotEqual(r["displacement_dofs"][1],0.)
  self.assertGreater(r["stored_energy_j"],0.)
 def test_dirichlet_reaction_reported(self):
  B=[[1.],[0],[0],[0],[0],[0]]
  q=[{"B":B,"weight":1.,"eigenstrain":0.,"fluid_content_increment":0.}]
  r=p19_solve_spatial_biot_bvp(1,q,self.p,{0:.002})
  self.assertGreater(r["dirichlet_reaction_residual"],0.)
 def test_singular_system_rejected(self):
  B=[[0.,0.] for _ in range(6)]
  q=[{"B":B,"weight":1.,"eigenstrain":0.,"fluid_content_increment":0.}]
  with self.assertRaises(ValueError): p19_solve_spatial_biot_bvp(2,q,self.p,{})
 def test_bad_weight_rejected(self):
  B=[[1.] for _ in range(6)]
  q=[{"B":B,"weight":0.,"eigenstrain":0.,"fluid_content_increment":0.}]
  with self.assertRaises(ValueError): p19_solve_spatial_biot_bvp(1,q,self.p,{0:0.})
if __name__=="__main__": unittest.main()
