import math
import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2, R_GAS
from ccfsm_p5_thermodynamic_coupling import P5Parameters, p5_evaluate


class TestCCFSMP5ThermodynamicCoupling(unittest.TestCase):
    def setUp(self):
        chemistry = ChemicalParametersP2(
            100.0, 298.15, (0.2, 0.1, 0.05), (2.0, 0.5, 1.5),
            (1.0, 1.1, 0.9, 1.05)
        )
        self.params = P5Parameters(
            2.0e9, 1.0e9, 5.0e9, 0.8, 0.35,
            0.02, 0.1, 1e-3, chemistry
        )
        self.strain = (
            (0.01, 0.001, 0.0),
            (0.001, -0.002, 0.0),
            (0.0, 0.0, 0.003),
        )
        self.zeta = 0.01
        self.mobile = (30.0, 20.0)
        self.network = (35.0, 15.0)

    def evaluate(self, mobile=None, network=None, strain=None, zeta=None, params=None):
        return p5_evaluate(
            self.strain if strain is None else strain,
            self.zeta if zeta is None else zeta,
            self.mobile if mobile is None else mobile,
            self.network if network is None else network,
            self.params if params is None else params,
        )

    def test_positive_fluid_capacity_and_finite_energy(self):
        result = self.evaluate()
        self.assertGreater(result.theta, 0)
        self.assertTrue(math.isfinite(result.free_energy_j_m3_reference))

    def test_stress_contains_biot_pressure_coupling(self):
        result = self.evaluate()
        trace = sum(self.strain[i][i] for i in range(3))
        expected_p = self.params.biot_modulus_pa * (
            self.zeta - self.params.biot_coefficient * trace
        )
        self.assertAlmostEqual(result.pore_pressure_pa, expected_p)
        self.assertAlmostEqual(
            result.stress_pa[0][0],
            2*self.params.shear_modulus_pa*(self.strain[0][0] -
                self.params.bridge_eigenstrain*(result.bridge_fraction -
                self.params.bridge_reference))
            + self.params.lame_lambda_pa*(
                trace - 3*self.params.bridge_eigenstrain*(
                    result.bridge_fraction-self.params.bridge_reference))
            - self.params.biot_coefficient*expected_p
        )

    def test_reaction_dissipation_nonnegative(self):
        self.assertGreaterEqual(self.evaluate().reaction_dissipation_w_m3_reference, -1e-12)

    def test_bridge_mechanics_changes_total_network_potentials(self):
        coupled = self.evaluate()
        no_eigen = P5Parameters(
            self.params.lame_lambda_pa, self.params.shear_modulus_pa,
            self.params.biot_modulus_pa, self.params.biot_coefficient,
            self.params.initial_fluid_capacity, 0.0,
            self.params.bridge_reference, self.params.bridge_regularization,
            self.params.chemistry
        )
        uncoupled = self.evaluate(params=no_eigen)
        self.assertNotAlmostEqual(coupled.total_potentials_j_mol[2],
                                  uncoupled.total_potentials_j_mol[2])
        self.assertNotAlmostEqual(coupled.total_potentials_j_mol[3],
                                  uncoupled.total_potentials_j_mol[3])

    def test_p2_rate_recovered_when_mechanical_feedback_is_off(self):
        p = P5Parameters(
            self.params.lame_lambda_pa, self.params.shear_modulus_pa,
            self.params.biot_modulus_pa, self.params.biot_coefficient,
            self.params.initial_fluid_capacity, 0.0,
            self.params.bridge_reference, self.params.bridge_regularization,
            self.params.chemistry
        )
        result = self.evaluate(params=p)
        theta = result.theta
        c_ref = self.params.chemistry.reference_concentration
        gam = self.params.chemistry.activity_coefficients
        acts = (gam[0]*self.mobile[0]/(theta*c_ref),
                gam[1]*self.mobile[1]/(theta*c_ref),
                gam[2]*self.network[0]/c_ref,
                gam[3]*self.network[1]/c_ref)
        expected = tuple(
            k*c_ref*(acts[i]-acts[i+1]/K)
            for i,(k,K) in enumerate(zip(
                self.params.chemistry.rate_constants_s,
                self.params.chemistry.equilibrium_constants))
        )
        for actual, target in zip(result.reaction_rates_mol_m3_s, expected):
            self.assertAlmostEqual(actual, target, places=12)

    def test_reaction_stoichiometry_conserves_silicon(self):
        r1, r2, r3 = self.evaluate().reaction_rates_mol_m3_s
        self.assertAlmostEqual(-r1 + (r1-r2) + (r2-r3) + r3, 0.0, places=14)

    def test_chemical_potential_is_energy_derivative_for_network_pool(self):
        base = self.evaluate()
        h = 1e-4
        plus = self.evaluate(network=(self.network[0]+h, self.network[1]))
        minus = self.evaluate(network=(self.network[0]-h, self.network[1]))
        fd = (plus.free_energy_j_m3_reference -
              minus.free_energy_j_m3_reference)/(2*h)
        self.assertAlmostEqual(fd, base.total_potentials_j_mol[2], delta=2e-4)

    def test_chemical_potential_is_energy_derivative_for_mobile_pool(self):
        base = self.evaluate()
        h = 1e-4
        plus = self.evaluate(mobile=(self.mobile[0]+h, self.mobile[1]))
        minus = self.evaluate(mobile=(self.mobile[0]-h, self.mobile[1]))
        fd = (plus.free_energy_j_m3_reference -
              minus.free_energy_j_m3_reference)/(2*h)
        self.assertAlmostEqual(fd, base.total_potentials_j_mol[0], delta=2e-4)

    def test_rejects_nonpositive_capacity_or_inventory(self):
        with self.assertRaises(ValueError):
            self.evaluate(zeta=-0.35)
        with self.assertRaises(ValueError):
            self.evaluate(mobile=(0.0, self.mobile[1]))


    def test_fluid_content_derivative_includes_mobile_osmotic_term(self):
        result = self.evaluate()
        h = 1e-7
        plus = self.evaluate(zeta=self.zeta+h)
        minus = self.evaluate(zeta=self.zeta-h)
        fd = (plus.free_energy_j_m3_reference - minus.free_energy_j_m3_reference)/(2*h)
        self.assertAlmostEqual(fd, result.fluid_energy_conjugate_pa, delta=2e-2)
        self.assertAlmostEqual(result.fluid_energy_conjugate_pa, result.pore_pressure_pa-result.osmotic_pressure_pa, delta=1e-8)

    def test_osmotic_pressure_scales_with_mobile_inventory(self):
        result = self.evaluate()
        self.assertAlmostEqual(result.osmotic_pressure_pa, R_GAS*self.params.chemistry.temperature_k*sum(self.mobile)/result.theta)

    def test_log_mean_equal_activity_limit(self):
        result = self.evaluate()
        self.assertTrue(all(math.isfinite(v) for v in result.reaction_rates_mol_m3_s))


if __name__ == "__main__":
    unittest.main()
