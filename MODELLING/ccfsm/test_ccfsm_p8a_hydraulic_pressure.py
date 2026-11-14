import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p8a_hydraulic_pressure import (
    P8aHydraulicParameters, p8a_hydraulic_rhs, p8a_coupled_rhs,
    p8a_pressure_dissipation
)


class TestCCFSMP8aHydraulicPressure(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(4, 0.01)
        self.params = P8aHydraulicParameters(
            (2e-9,)*4, (1e-12, 2e-12, 1e-12, 4e-12),
            (0.3,)*4, 1e5
        )
        self.pressure = (1.04e5, 1.02e5, 0.99e5, 0.95e5)
        self.chem = ChemicalParametersP2(
            100., 298.15, (0.2, 0.1, 0.05), (2., .5, 1.5),
            (1., 1.1, .9, 1.05)
        )
        self.state = (
            (30., 25., 20., 15.), (20., 22., 24., 26.),
            (35., 34., 33., 32.), (15., 16., 17., 18.)
        )

    def test_capacity_pressure_closure(self):
        theta, _, _, _ = p8a_hydraulic_rhs(self.pressure, self.grid, self.params)
        for j in range(4):
            self.assertAlmostEqual(theta[j], .3 + 2e-9*(self.pressure[j]-1e5))

    def test_closed_boundary_fluxes(self):
        _, _, _, q = p8a_hydraulic_rhs(self.pressure, self.grid, self.params)
        self.assertEqual(q[0], 0.)
        self.assertEqual(q[-1], 0.)

    def test_darcy_flux_sign(self):
        _, _, _, q = p8a_hydraulic_rhs((4., 3., 2., 1.), self.grid,
                                        P8aHydraulicParameters(
                                            (1e-3,)*4, (1.,)*4, (.3,)*4, 0.))
        self.assertTrue(all(x > 0 for x in q[1:-1]))

    def test_harmonic_mean_resistance(self):
        # Face flux for a unit pressure drop over dx=1 with K=(1,3).
        grid = P8Grid(2, 1.)
        params = P8aHydraulicParameters((1.,1.), (1.,3.), (.5,.5), 0.)
        _, _, _, q = p8a_hydraulic_rhs((1.,0.), grid, params)
        self.assertAlmostEqual(q[1], 1.5)

    def test_fluid_capacity_rate_conserves_closed_volume(self):
        _, _, dtheta, _ = p8a_hydraulic_rhs(self.pressure, self.grid, self.params)
        self.assertAlmostEqual(sum(dtheta)*self.grid.spacing_m, 0., delta=1e-15)

    def test_pressure_mean_rate_zero_for_constant_storage(self):
        _, pdot, _, _ = p8a_hydraulic_rhs(self.pressure, self.grid, self.params)
        self.assertAlmostEqual(sum(pdot), 0., delta=1e-12)

    def test_pressure_dissipation_is_nonnegative(self):
        self.assertGreaterEqual(
            p8a_pressure_dissipation(self.pressure, self.grid, self.params), 0.
        )

    def test_constant_pressure_is_stationary(self):
        theta, pdot, dtheta, q = p8a_hydraulic_rhs(
            (1e5,)*4, self.grid, self.params)
        self.assertTrue(all(abs(x) < 1e-20 for x in pdot))
        self.assertTrue(all(x == 0. for x in dtheta))
        self.assertTrue(all(x == 0. for x in q))

    def test_coupled_rhs_uses_same_hydraulic_flux(self):
        result = p8a_coupled_rhs(
            self.state, self.pressure, self.grid, self.params,
            (1e-6, 2e-6), self.chem
        )
        self.assertEqual(result["darcy_flux_faces_m_s"][0], 0.)
        self.assertEqual(result["darcy_flux_faces_m_s"][-1], 0.)
        self.assertEqual(len(result["inventory_dot"]), 4)

    def test_rejects_nonpositive_capacity_and_bad_parameters(self):
        bad = P8aHydraulicParameters((1e-9,)*4, (1e-12,)*4,
                                     (.00001,)*4, 1e5)
        with self.assertRaises(ValueError):
            p8a_hydraulic_rhs((0.,)*4, self.grid, bad)
        with self.assertRaises(ValueError):
            P8aHydraulicParameters((0.,)*4, (1e-12,)*4, (.3,)*4, 0.).validate(4)
        with self.assertRaises(ValueError):
            P8aHydraulicParameters((1.,)*4, (0.,)*4, (.3,)*4, 0.).validate(4)


if __name__ == "__main__":
    unittest.main()
