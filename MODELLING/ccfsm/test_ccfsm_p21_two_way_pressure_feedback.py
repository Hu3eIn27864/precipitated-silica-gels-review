import unittest

from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p21_two_way_pressure_feedback import p21_two_way_pressure_feedback


class TestP21(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(2, 1.0)
        self.chem = ChemicalParametersP2(1000., 298.15, (.01,.01,.01), (1.,1.,1.))
        self.mech = P9Parameters(2e6,1e6,1e7,.8,.01,.2,1e-12,.5,0.,
                                 1e-12,.0,.0,.2,0.)
        self.theta = [.51,.52]
        self.inv = [[100.,110.],[80.,85.],[300.,310.],[100.,105.]]
        self.quad = [
            {"cell_index":0,"B":[[-1.,1.,0.],[0.,0.,0.],[0.,0.,0.],
                                  [0.,0.,0.],[0.,0.,0.],[0.,0.,0.]],"weight":.5},
            {"cell_index":1,"B":[[0.,-1.,1.],[0.,0.,0.],[0.,0.,0.],
                                  [0.,0.,0.],[0.,0.,0.],[0.,0.,0.]],"weight":.5},
        ]

    def run_model(self, quadrature=None, external_pressure=0.):
        return p21_two_way_pressure_feedback(
            self.theta,self.inv,self.grid,self.mech,self.chem,(0.,0.),
            external_pressure,self.quad if quadrature is None else quadrature,
            {0:0.})

    def test_feedback_uses_projected_p19_pressure(self):
        r = self.run_model()
        self.assertEqual(len(r["projected_spatial_pressure_cell_pa"]),2)
        self.assertTrue(r["pressure_feedback_used_for_darcy_and_mobile_advection"])
        self.assertTrue(r["same_darcy_flux_used_for_fluid_and_mobile_advection"])
        self.assertTrue(r["mechanics_equilibrium_verified"])

    def test_species_fluxes_are_conservative(self):
        r = self.run_model()
        tr = r["transport_rhs"]
        for s in range(2):
            expected = -(tr["mobile_species_face_fluxes_mol_m2_s"][s][-1]
                         - tr["mobile_species_face_fluxes_mol_m2_s"][s][0])
            actual = self.grid.spacing_m * sum(tr["inventory_dot"][s])
            rates = tr["reaction_rates_mol_m3_s"]
            reaction = ([-rates[0][j] for j in range(2)] if s == 0
                        else [rates[0][j] - rates[1][j] for j in range(2)])
            expected += self.grid.spacing_m * sum(reaction)
            self.assertAlmostEqual(actual, expected, places=10)

    def test_closed_boundary_fluid_balance(self):
        r = self.run_model()
        tr = r["transport_rhs"]
        self.assertAlmostEqual(self.grid.spacing_m*sum(tr["fluid_capacity_dot_s"]),
                               tr["darcy_flux_faces_m_s"][0] -
                               tr["darcy_flux_faces_m_s"][-1], places=12)

    def test_requires_fe_pressure_sample_for_every_cell(self):
        with self.assertRaises(ValueError):
            self.run_model(self.quad[:1])

    def test_rejects_nonpositive_quadrature_weight(self):
        q = [dict(x) for x in self.quad]
        q[0]["weight"] = 0.
        with self.assertRaises(ValueError):
            self.run_model(q)


if __name__ == "__main__":
    unittest.main()
