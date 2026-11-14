import unittest
from dataclasses import replace
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p11_energy_time_integration import P11State
from ccfsm_p13_onsager_transport import (
    p13_chemical_potential_transport, p13_total_potential
)


class TestCCFSMP13OnsagerTransport(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(3, 0.01)
        self.chem = ChemicalParametersP2(
            100., 298.15, (0.2, 0.1, 0.05), (2., 0.5, 1.5),
            (1., 1.1, 0.9, 1.05))
        self.mech = P9Parameters(
            2e6, 1e6, 1e7, .8, .01, 15/51, 1., .3, 0.,
            1e-12, 2., 5., 15/51)
        self.state = P11State(
            (.30,.30,.30),
            ((30.,31.,32.), (20.,19.,18.), (35.,35.,35.), (15.,15.,15.)))
    def run_model(self, d=(1e-10, 2e-10), left=(30.,20.), right=(32.,18.)):
        return p13_chemical_potential_transport(
            self.state.fluid_capacity, self.state.inventories, self.grid,
            self.mech, self.chem, d, 0., left, right)
    def test_onsager_dissipation_nonnegative(self):
        r=self.run_model()
        self.assertTrue(r["discrete_diffusion_dissipation_nonnegative"])
        self.assertTrue(all(x >= 0 for x in
            r["mobile_species_onsager_diffusive_dissipation_w_m2"]))
    def test_uniform_concentration_has_zero_internal_diffusion(self):
        state=P11State((.3,.3,.3),((30.,30.,30.),(20.,20.,20.),
            (35.,35.,35.),(15.,15.,15.)))
        r=p13_chemical_potential_transport(state.fluid_capacity,
            state.inventories,self.grid,self.mech,self.chem,(1e-10,1e-10),
            0.,(100.,100.),(100.,100.))
        for species in range(2):
            flux=r["mobile_species_face_fluxes_mol_m2_s"][species]
            self.assertAlmostEqual(flux[1],0.,places=18)
            self.assertAlmostEqual(flux[2],0.,places=18)
    def test_zero_diffusivity_has_zero_onsager_dissipation(self):
        r=self.run_model((0.,0.))
        self.assertEqual(r["mobile_species_onsager_diffusive_dissipation_w_m2"],(0.,0.))
    def test_flux_decomposition_is_consistent(self):
        r=self.run_model()
        for s in range(2):
            for a,b,c in zip(r["mobile_species_face_fluxes_mol_m2_s"][s],
                r["mobile_species_advective_face_fluxes_mol_m2_s"][s],
                r["darcy_flux_faces_m_s"]):
                self.assertTrue(abs(a-b) < 1e9)
        self.assertFalse(r["advection_entropy_closure_established"])
    def test_dead_load_potential(self):
        loaded=replace(self.mech,applied_axial_traction_pa=1000.)
        a=p13_total_potential(self.state,self.grid,loaded,self.chem)
        b=p13_total_potential(self.state,self.grid,self.mech,self.chem)
        self.assertTrue(abs(a-b)>0.)
    def test_invalid_zero_reservoir_activity_rejected(self):
        with self.assertRaises(ValueError):
            self.run_model(left=(0.,20.))


if __name__ == "__main__":
    unittest.main()
