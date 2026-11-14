import math
import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2, R_GAS
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p8a_hydraulic_pressure import P8aHydraulicParameters
from ccfsm_p8c_thermodynamic_closure import (
    p8c_cell_thermodynamics,p8c_coupled_rhs
)


class TestCCFSMP8cThermodynamicClosure(unittest.TestCase):
    def setUp(self):
        self.chem=ChemicalParametersP2(
            100.,298.15,(0.2,0.1,0.05),(2.,0.5,1.5),(1.,1.1,0.9,1.05))
        self.grid=P8Grid(3,0.01)
        self.hyd=P8aHydraulicParameters(
            (2e-9,)*3,(1e-12,)*3,(0.3,)*3,1e5)

    def data(self,theta=0.3,mm=30.,mo=20.):
        return p8c_cell_thermodynamics(theta,1e5+(theta-0.3)/2e-9,(mm,mo),(35.,15.),
            self.chem,0.3,1e5,2e-9)

    def test_osmotic_pressure_and_fluid_conjugate(self):
        r=self.data()
        expected=R_GAS*298.15*50./0.3
        self.assertAlmostEqual(r["osmotic_pressure_pa"],expected)
        self.assertAlmostEqual(r["fluid_energy_conjugate_pa"],1e5-expected)

    def test_theta_derivative_is_pressure_minus_osmotic(self):
        theta=.3; h=1e-6
        plus=self.data(theta+h)["free_energy_j_m3_reference"]
        minus=self.data(theta-h)["free_energy_j_m3_reference"]
        numeric=(plus-minus)/(2*h)
        self.assertAlmostEqual(numeric,self.data()["fluid_energy_conjugate_pa"],
                               delta=2e-3)

    def test_mobile_inventory_derivative_is_chemical_potential(self):
        h=1e-4
        base=self.data()["free_energy_j_m3_reference"]
        plus=p8c_cell_thermodynamics(.3,1e5,(30.+h,20.),(35.,15.),
             self.chem,.3,1e5,2e-9)["free_energy_j_m3_reference"]
        numeric=(plus-base)/h
        self.assertAlmostEqual(numeric,
            self.data()["chemical_potentials_j_mol"][0],delta=1e-2)

    def test_reaction_dissipation_nonnegative(self):
        state=((30.,25.,20.),(20.,22.,24.),
               (35.,34.,33.),(15.,16.,17.))
        result=p8c_coupled_rhs(state,(1.01e5,)*3,self.grid,self.hyd,
            (0.,0.),self.chem,1e5)
        self.assertTrue(all(v>=-1e-18 for v in
                            result["reaction_dissipation_w_m3_reference"]))

    def test_reactions_conserve_local_total_silicon(self):
        state=((30.,25.,20.),(20.,22.,24.),
               (35.,34.,33.),(15.,16.,17.))
        result=p8c_coupled_rhs(state,(1e5,)*3,self.grid,self.hyd,
            (0.,0.),self.chem,1e5)
        for j in range(3):
            self.assertAlmostEqual(sum(f[j] for f in result["inventory_dot"]),
                                   0.,delta=1e-12)

    def test_darcy_uses_mechanical_pressure(self):
        state=((30.,25.,20.),(20.,22.,24.),
               (35.,34.,33.),(15.,16.,17.))
        p=(1.03e5,1.02e5,1.01e5)
        result=p8c_coupled_rhs(state,p,self.grid,self.hyd,(0.,0.),
                               self.chem,1e5)
        expected=-1e-12*(p[1]-p[0])/self.grid.spacing_m
        self.assertAlmostEqual(result["darcy_flux_faces_m_s"][1],expected)
        self.assertNotEqual(result["cell_thermodynamics"][0]
                            ["fluid_energy_conjugate_pa"],
                            result["cell_thermodynamics"][0]["pore_pressure_pa"])

    def test_open_boundary_si_balance(self):
        state=((30.,25.,20.),(20.,22.,24.),
               (35.,34.,33.),(15.,16.,17.))
        result=p8c_coupled_rhs(state,(1.03e5,1.02e5,1.01e5),self.grid,
            self.hyd,(0.,0.),self.chem,1e5)
        total_rate=sum(sum(f) for f in result["inventory_dot"])*self.grid.spacing_m
        b=result["mobile_species_boundary_fluxes_mol_m2_s"]
        self.assertAlmostEqual(total_rate,-sum(fr-fl for fl,fr in b),
                               delta=1e-9)

    def test_energy_finite_and_positive_capacity_required(self):
        self.assertTrue(math.isfinite(self.data()["free_energy_j_m3_reference"]))
        with self.assertRaises(ValueError):
            self.data(theta=0.0)


if __name__=="__main__":
    unittest.main()
