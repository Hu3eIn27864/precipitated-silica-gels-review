import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import (
    P8Grid, p8_rhs, p8_total_silicon, p8_total_fluid_capacity
)


class TestCCFSMP8VariableCapacity(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(4, 0.01)
        self.chem = ChemicalParametersP2(
            100.0, 298.15, (0.2, 0.1, 0.05),
            (2.0, 0.5, 1.5), (1.0, 1.1, 0.9, 1.05)
        )
        self.theta = (0.30, 0.32, 0.35, 0.33)
        self.state = (
            (30., 25., 20., 15.), (20., 22., 24., 26.),
            (35., 34., 33., 32.), (15., 16., 17., 18.)
        )

    def rhs(self, state=None, theta=None, q=(0., 0., 0., 0., 0.), d=(0., 0.)):
        return p8_rhs(state or self.state, theta or self.theta, self.grid,
                      q, d, self.chem)

    def test_fluid_capacity_is_conserved(self):
        _, dtheta = self.rhs(q=(0., 0.03, -0.01, 0.02, 0.))
        self.assertAlmostEqual(sum(dtheta) * self.grid.spacing_m, 0., delta=1e-15)

    def test_global_silicon_is_conserved(self):
        dm, _ = self.rhs(q=(0., 0.03, -0.01, 0.02, 0.), d=(1e-6, 2e-6))
        self.assertAlmostEqual(
            self.grid.spacing_m * sum(sum(field) for field in dm),
            0.0, delta=1e-12
        )

    def test_species_conserved_without_reaction(self):
        chemistry = ChemicalParametersP2(
            100.0, 298.15, (0., 0., 0.), (2., 0.5, 1.5),
            (1., 1., 1., 1.)
        )
        dm, _ = p8_rhs(self.state, self.theta, self.grid,
                       (0., 0.03, -0.01, 0.02, 0.), (1e-6, 2e-6), chemistry)
        for field in dm:
            self.assertAlmostEqual(sum(field), 0.0, delta=1e-10)

    def test_uniform_concentration_tracks_fluid_capacity(self):
        concentrations = (80., 15.)
        state = (
            tuple(concentrations[0] * t for t in self.theta),
            tuple(concentrations[1] * t for t in self.theta),
            self.state[2], self.state[3]
        )
        # Disable reactions so only the conservative transport is tested.
        chemistry = ChemicalParametersP2(
            100., 298.15, (0., 0., 0.), (2., 0.5, 1.5), (1., 1., 1., 1.)
        )
        dm, dt = p8_rhs(state, self.theta, self.grid,
                        (0., 0.03, -0.01, 0.02, 0.), (0., 0.), chemistry)
        for species, c0 in enumerate(concentrations):
            for j in range(self.grid.cells):
                self.assertAlmostEqual(dm[species][j], c0 * dt[j], places=12)

    def test_zero_flow_zero_diffusion_has_no_transport_rhs(self):
        dm, dt = self.rhs(d=(0., 0.))
        self.assertTrue(all(abs(x) < 1e-14 for field in dm for x in field))
        self.assertTrue(all(x == 0. for x in dt))

    def test_total_inventory_helpers(self):
        self.assertAlmostEqual(
            p8_total_silicon(self.state, self.grid),
            self.grid.spacing_m * sum(sum(f) for f in self.state)
        )
        self.assertAlmostEqual(
            p8_total_fluid_capacity(self.theta, self.grid),
            self.grid.spacing_m * sum(self.theta)
        )

    def test_rejects_invalid_capacity_flux_or_inventory(self):
        with self.assertRaises(ValueError):
            self.rhs(theta=(0., *self.theta[1:]))
        with self.assertRaises(ValueError):
            self.rhs(q=(1e-3, 0., 0., 0., 0.))
        bad = ((-1., 1., 1., 1.), *self.state[1:])
        with self.assertRaises(ValueError):
            self.rhs(state=bad)

    def test_rejects_bad_shapes_and_diffusivity(self):
        with self.assertRaises(ValueError):
            p8_rhs(self.state, self.theta, self.grid, (0.,)*4, (0., 0.), self.chem)
        with self.assertRaises(ValueError):
            self.rhs(d=(-1e-8, 0.))


if __name__ == "__main__":
    unittest.main()
