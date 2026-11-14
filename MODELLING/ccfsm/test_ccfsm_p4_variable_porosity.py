import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p4_variable_porosity import P4Grid, p4_rhs, p4_total_silicon


class TestCCFSMP4VariablePorosity(unittest.TestCase):
    def setUp(self):
        self.grid = P4Grid((3, 2), (2e-6, 3e-6))
        self.theta = (0.25, 0.28, 0.31, 0.27, 0.30, 0.33)
        self.fields = (
            (80., 70., 60., 50., 40., 30.),
            (15., 16., 17., 18., 19., 20.),
            (4., 5., 6., 7., 8., 9.),
            (1., 1.5, 2., 2.5, 3., 3.5),
        )
        self.params = ChemicalParametersP2(
            100.0, 298.15, (0.0, 0.0, 0.0), (2.0, 0.5, 1.5)
        )
        self.q = ((1e-8, -2e-8, 3e-8, 1e-8), (2e-8, -1e-8, 3e-8))

    def test_fluid_capacity_balance_is_conservative(self):
        _, theta_rhs = p4_rhs(self.fields, self.theta, self.grid, (1e-10,)*4,
                              self.q, self.params)
        self.assertAlmostEqual(sum(theta_rhs), 0.0, delta=1e-16)

    def test_global_si_inventory_conserved(self):
        dc, dtheta = p4_rhs(self.fields, self.theta, self.grid, (1e-10,)*4,
                            self.q, self.params)
        derivative = self.grid.cell_volume * sum(
            dtheta[k] * sum(self.fields[s][k] for s in range(4))
            + self.theta[k] * sum(dc[s][k] for s in range(4))
            for k in range(self.grid.cell_count)
        )
        self.assertAlmostEqual(derivative, 0.0, places=18)

    def test_each_species_conserved_without_reaction(self):
        dc, dtheta = p4_rhs(self.fields, self.theta, self.grid, (1e-10,)*4,
                            self.q, self.params)
        for s in range(4):
            derivative = sum(
                dtheta[k] * self.fields[s][k] + self.theta[k] * dc[s][k]
                for k in range(self.grid.cell_count)
            )
            self.assertAlmostEqual(derivative, 0.0, places=12)

    def test_uniform_concentration_is_carried_with_fluid(self):
        uniform = tuple((v,) * self.grid.cell_count for v in (80., 15., 4., 1.))
        dc, _ = p4_rhs(uniform, self.theta, self.grid, (1e-10,)*4,
                       self.q, self.params)
        for field in dc:
            for value in field:
                self.assertAlmostEqual(value, 0.0, places=10)

    def test_zero_flux_reduces_to_diffusive_transport(self):
        zeros = tuple((0.0,) * n for n in self.grid.face_counts())
        dc, dtheta = p4_rhs(self.fields, self.theta, self.grid, (1e-10,)*4,
                            zeros, self.params)
        self.assertTrue(all(v == 0.0 for v in dtheta))
        self.assertTrue(any(abs(v) > 0 for field in dc for v in field))

    def test_total_silicon_helper(self):
        value = p4_total_silicon(self.fields, self.theta, self.grid)
        expected = self.grid.cell_volume * sum(
            self.theta[k] * sum(self.fields[s][k] for s in range(4))
            for k in range(self.grid.cell_count)
        )
        self.assertAlmostEqual(value, expected)

    def test_rejects_bad_theta_or_face_flux_shape(self):
        with self.assertRaises(ValueError):
            p4_rhs(self.fields, (0.0,) + self.theta[1:], self.grid,
                   (1e-10,)*4, self.q, self.params)
        with self.assertRaises(ValueError):
            p4_rhs(self.fields, self.theta, self.grid, (1e-10,)*4,
                   ((1e-8,), self.q[1]), self.params)


if __name__ == "__main__":
    unittest.main()
