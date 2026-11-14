import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p8a_hydraulic_pressure import P8aHydraulicParameters
from ccfsm_p8b_open_drainage import (
    p8b_hydraulic_rhs,p8b_coupled_rhs,p8b_pressure_dissipation
)


class TestCCFSMP8bOpenDrainage(unittest.TestCase):
    def setUp(self):
        self.grid=P8Grid(3,0.01)
        self.params=P8aHydraulicParameters(
            (1e-8,)*3,(1e-12,)*3,(0.3,)*3,1e5)
        self.chem=ChemicalParametersP2(
            100.,298.15,(0.,0.,0.),(2.,.5,1.5),(1.,1.,1.,1.))
        self.state=((30.,25.,20.),(20.,22.,24.),
                    (35.,34.,33.),(15.,16.,17.))

    def test_pressure_above_reservoir_drains_at_both_ends(self):
        _,_,_,q=p8b_hydraulic_rhs((1.1e5,1.1e5,1.1e5),self.grid,
                                   self.params,1e5)
        self.assertLess(q[0],0.)
        self.assertGreater(q[-1],0.)

    def test_pressure_below_reservoir_causes_inflow(self):
        _,_,_,q=p8b_hydraulic_rhs((0.9e5,)*3,self.grid,self.params,1e5)
        self.assertGreater(q[0],0.)
        self.assertLess(q[-1],0.)

    def test_equal_pressure_zero_flux(self):
        _,pdot,tdot,q=p8b_hydraulic_rhs((1e5,)*3,self.grid,self.params,1e5)
        self.assertTrue(all(x==0. for x in q))
        self.assertTrue(all(x==0. for x in pdot))
        self.assertTrue(all(x==0. for x in tdot))

    def test_fluid_volume_balance_matches_boundary_flux(self):
        _,_,tdot,q=p8b_hydraulic_rhs((1.1e5,1.05e5,1.02e5),
                                      self.grid,self.params,1e5)
        self.assertAlmostEqual(sum(tdot)*self.grid.spacing_m,
                               q[0]-q[-1],delta=1e-15)

    def test_pressure_dissipation_nonnegative(self):
        self.assertGreaterEqual(
            p8b_pressure_dissipation((1.1e5,1.05e5,1.02e5),
                                     self.grid,self.params,1e5),0.)

    def test_si_boundary_balance_matches_rhs(self):
        out=p8b_coupled_rhs(self.state,(1.1e5,1.05e5,1.02e5),
                            self.grid,self.params,(0.,0.),self.chem,1e5)
        total_rate=sum(sum(f) for f in out["inventory_dot"])*self.grid.spacing_m
        self.assertAlmostEqual(total_rate,
                               -out["net_outward_mobile_si_flux_mol_m2_s"],
                               delta=1e-10)

    def test_immobilized_pools_have_no_boundary_advection(self):
        out=p8b_coupled_rhs(self.state,(1.1e5,1.05e5,1.02e5),
                            self.grid,self.params,(0.,0.),self.chem,1e5)
        # Reaction rates are disabled, so N/B remain exactly stationary.
        self.assertTrue(all(x==0. for x in out["inventory_dot"][2]))
        self.assertTrue(all(x==0. for x in out["inventory_dot"][3]))

    def test_inflow_uses_external_mobile_concentration(self):
        # Left boundary has inward q; with zero diffusion, M inflow is q*c_ext.
        p=(0.9e5,)*3
        out=p8b_coupled_rhs(self.state,p,self.grid,self.params,(0.,0.),
                            self.chem,1e5,(7.,11.),(0.,0.))
        ql=out["darcy_flux_faces_m_s"][0]
        fl=out["mobile_species_boundary_fluxes_mol_m2_s"][0][0]
        self.assertAlmostEqual(fl,ql*7.)

    def test_outflow_uses_gel_concentration(self):
        p=(1.1e5,)*3
        out=p8b_coupled_rhs(self.state,p,self.grid,self.params,(0.,0.),
                            self.chem,1e5)
        ql=out["darcy_flux_faces_m_s"][0]
        cM=self.state[0][0]/out["fluid_capacity"][0]
        fl=out["mobile_species_boundary_fluxes_mol_m2_s"][0][0]
        self.assertAlmostEqual(fl,ql*cM)

    def test_rejects_negative_external_concentration(self):
        with self.assertRaises(ValueError):
            p8b_coupled_rhs(self.state,(1.1e5,)*3,self.grid,self.params,
                            (0.,0.),self.chem,1e5,(-1.,0.),(0.,0.))


if __name__=="__main__":
    unittest.main()
