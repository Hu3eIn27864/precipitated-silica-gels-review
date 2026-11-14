import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p7_chemo_transport import P7Grid, p7_rhs, p7_total_silicon

class TestCCFSMP7ChemoTransport(unittest.TestCase):
    def setUp(self):
        self.grid=P7Grid(4,0.01)
        self.chem=ChemicalParametersP2(100.0,298.15,(0.2,0.1,0.05),
            (2.0,0.5,1.5),(1.0,1.1,0.9,1.05))
        self.state=((30.,25.,20.,15.),(20.,22.,24.,26.),
                    (35.,34.,33.,32.),(15.,16.,17.,18.))
    def rhs(self,state=None,q=(0.,0.,0.,0.,0.),d=(0.,0.)):
        return p7_rhs(state or self.state,self.grid,q,d,0.35,self.chem)
    def test_global_silicon_conservation(self):
        rhs=self.rhs(q=(0.,0.03,-0.01,0.02,0.),d=(1e-6,2e-6))
        self.assertAlmostEqual(self.grid.spacing_m*sum(sum(f) for f in rhs),0.,delta=1e-12)
    def test_uniform_state_has_uniform_local_reaction_rhs(self):
        uniform=tuple((f[0],)*4 for f in self.state)
        rhs=self.rhs(uniform)
        for field in rhs:
            for x in field:
                self.assertAlmostEqual(x,field[0])
    def test_diffusion_conserves_each_mobile_pool(self):
        full=self.rhs(d=(1e-6,2e-6)); reaction=self.rhs()
        for i in (0,1):
            self.assertAlmostEqual(sum(full[i])-sum(reaction[i]),0.,delta=1e-10)
    def test_advection_conserves_each_mobile_pool(self):
        q=(0.,0.03,-0.01,0.02,0.)
        full=self.rhs(q=q); reaction=self.rhs()
        for i in (0,1):
            self.assertAlmostEqual(sum(full[i])-sum(reaction[i]),0.,delta=1e-10)
    def test_total_silicon(self):
        self.assertAlmostEqual(p7_total_silicon(self.state,self.grid),
            self.grid.spacing_m*sum(sum(f) for f in self.state))
    def test_rejects_nonzero_boundary_flux(self):
        with self.assertRaises(ValueError): self.rhs(q=(1e-3,0.,0.,0.,0.))
    def test_rejects_negative_inventory_or_diffusivity(self):
        bad=((-1.,1.,1.,1.),*self.state[1:])
        with self.assertRaises(ValueError): self.rhs(state=bad)
        with self.assertRaises(ValueError): self.rhs(d=(-1.,0.))
    def test_rejects_bad_shapes_and_capacity(self):
        with self.assertRaises(ValueError):
            p7_rhs(self.state,self.grid,(0.,)*4,(0.,0.),0.35,self.chem)
        with self.assertRaises(ValueError):
            p7_rhs(self.state,self.grid,(0.,)*5,(0.,0.),0.,self.chem)

if __name__=="__main__": unittest.main()
