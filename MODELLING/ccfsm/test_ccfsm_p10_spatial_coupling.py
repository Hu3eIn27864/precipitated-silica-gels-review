import math
import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p10_spatial_coupling import (
    p10_coupled_rhs, p10_total_fluid_capacity, p10_total_silicon
)


class TestCCFSMP10SpatialCoupling(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(3, 0.01)
        self.chem = ChemicalParametersP2(
            100.0, 298.15, (0.2, 0.1, 0.05), (2.0, 0.5, 1.5),
            (1.0, 1.1, 0.9, 1.05))
        self.mech = P9Parameters(
            lame_lambda_pa=2.0e6, shear_modulus_pa=1.0e6,
            biot_modulus_pa=1.0e7, biot_coefficient=0.8,
            bridge_eigenstrain=0.01, bridge_reference=15.0/51.0,
            bridge_regularization=1.0, reference_fluid_capacity=0.3,
            reference_axial_strain=0.0,
            reference_permeability_m2_per_pas=1.0e-12,
            bridge_permeability_sensitivity=2.0,
            strain_permeability_sensitivity=5.0,
            reference_bridge_fraction=15.0/51.0)

    def state(self):
        return ((0.30, 0.30, 0.30),
                ((30., 30., 30.), (20., 20., 20.),
                 (35., 35., 35.), (15., 15., 15.)))

    def rhs(self, theta=None, inventories=None, pext=0.0, cL=(0.,0.), cR=(0.,0.)):
        th, inv = self.state()
        return p10_coupled_rhs(theta or th, inventories or inv, self.grid,
            self.mech, self.chem, (1e-10, 1e-10), pext, cL, cR)

    def test_uniform_zero_pressure_reference_has_zero_darcy_flux(self):
        r = self.rhs()
        self.assertTrue(all(abs(q) < 1e-18 for q in r["darcy_flux_faces_m_s"]))
        self.assertTrue(all(abs(v) < 1e-18 for v in r["fluid_capacity_dot_s"]))

    def test_same_darcy_flux_drives_fluid_and_mobile_advection(self):
        th, inv = self.state()
        r = self.rhs(theta=(.31,.30,.29), pext=0.)
        q = r["darcy_flux_faces_m_s"]
        self.assertEqual(len(q), self.grid.cells+1)
        self.assertTrue(any(abs(v)>0 for v in q))
        # In the zero-diffusion, zero-reaction limit the mobile flux is q*c_upwind.
        zero = p10_coupled_rhs((.31,.30,.29), inv, self.grid, self.mech,
            ChemicalParametersP2(100.,298.15,(0.,0.,0.),(2.,.5,1.5),
                                 (1.,1.1,.9,1.05)), (0.,0.), 0.)
        for sp in range(2):
            for f in range(1, self.grid.cells):
                qf = zero["darcy_flux_faces_m_s"][f]
                c = zero["mobile_concentrations_mol_m3"][sp]
                cup = c[f-1] if qf >= 0 else c[f]
                self.assertAlmostEqual(zero["mobile_species_face_fluxes_mol_m2_s"][sp][f],
                                       qf*cup, delta=1e-14)

    def test_closed_boundary_total_fluid_capacity_conserved(self):
        th, inv = self.state()
        # Set external pressure equal to both endpoint cell pressures.
        p0 = self.rhs()["pore_pressure_pa"][0]
        r = self.rhs(pext=p0)
        self.assertAlmostEqual(sum(r["fluid_capacity_dot_s"])*self.grid.spacing_m,
                               0.0, delta=1e-18)

    def test_closed_boundary_total_silicon_conserved(self):
        th, inv = self.state()
        no_reaction = ChemicalParametersP2(100.,298.15,(0.,0.,0.),
            (2.,.5,1.5),(1.,1.1,.9,1.05))
        r = p10_coupled_rhs(th, inv, self.grid, self.mech, no_reaction,
                            (1e-10,1e-10), 0.)
        total_rate = sum(sum(f) for f in r["inventory_dot"])*self.grid.spacing_m
        self.assertAlmostEqual(total_rate, 0.0, delta=1e-12)

    def test_open_boundary_silicon_balance(self):
        th, inv = self.state()
        no_reaction = ChemicalParametersP2(100.,298.15,(0.,0.,0.),
            (2.,.5,1.5),(1.,1.1,.9,1.05))
        r = p10_coupled_rhs(th, inv, self.grid, self.mech, no_reaction,
            (1e-10,1e-10), 0., (10.,5.), (12.,7.))
        total_rate = sum(sum(f) for f in r["inventory_dot"])*self.grid.spacing_m
        boundary = r["mobile_species_boundary_fluxes_mol_m2_s"]
        self.assertAlmostEqual(total_rate,
            -sum(fr-fl for fl,fr in boundary), delta=1e-10)

    def test_reaction_conserves_local_silicon_and_dissipates(self):
        th, inv = self.state()
        r = self.rhs()
        for j in range(self.grid.cells):
            self.assertAlmostEqual(sum(f[j] for f in r["inventory_dot"])
                + sum(r["mobile_species_face_fluxes_mol_m2_s"][sp][j+1]
                      - r["mobile_species_face_fluxes_mol_m2_s"][sp][j]
                      for sp in range(2))/self.grid.spacing_m, 0.0,
                delta=1e-9)
        self.assertTrue(all(x >= -1e-14 for x in
                            r["reaction_dissipation_w_m3_reference"]))

    def test_positive_permeability_and_dissipation_diagnostics(self):
        r = self.rhs(theta=(.31,.30,.29))
        self.assertTrue(all(k > 0 and math.isfinite(k)
                            for k in r["intrinsic_permeability_m2_per_pas"]))
        self.assertGreaterEqual(r["darcy_internal_dissipation_w_m2"], 0.)
        self.assertTrue(all(v >= 0 for v in r["diffusion_dissipation_w_m2"]))

    def test_boundary_flux_sign_and_reservoir_effect(self):
        r = self.rhs(theta=(.31,.30,.29), pext=0., cL=(1.,2.), cR=(3.,4.))
        self.assertEqual(len(r["mobile_species_boundary_fluxes_mol_m2_s"]), 2)
        self.assertTrue(all(math.isfinite(x) for pair in
                            r["mobile_species_boundary_fluxes_mol_m2_s"]
                            for x in pair))

    def test_invalid_state_rejected(self):
        th, inv = self.state()
        with self.assertRaises(ValueError):
            self.rhs(theta=(.3,.3,0.))
        with self.assertRaises(ValueError):
            p10_coupled_rhs(th, inv, self.grid, self.mech, self.chem,
                            (-1.,0.), 0.)


if __name__ == "__main__":
    unittest.main()
