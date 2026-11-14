"""Tests for CCFSM v0.4 chemical submodel."""
import unittest

from ccfsm_chemical_v04 import (
    ChemicalEnvironment, ChemicalParameters, ChemicalState,
    acid_base_activity_factors, arrhenius_rate, chemical_rhs,
    evaluate_chemical_rates, simulate_chemical_network,
)


def parameters(**overrides):
    values = dict(
        reference_silica_concentration_mol_m3=100.0,
        pKa_monomer=9.5,
        oligomerization_rate_ref_s=1e-4,
        network_growth_rate_ref_s=2e-4,
        dissolution_rate_ref_s=1e-6,
        bridge_formation_rate_ref_s=1e-3,
        bridge_hydrolysis_rate_ref_s=1e-5,
        acid_catalysis_weight=1.0,
        silanolate_pair_weight=0.2,
        base_catalysis_weight=1.0,
        ionic_strength_exponent=0.2,
        load_bearing_fraction=0.7,
    )
    values.update(overrides)
    return ChemicalParameters(**values)


def environment(**overrides):
    values = dict(pH=8.0, temperature_k=298.15,
                  ionic_strength_mol_kg=0.1,
                  silica_solubility_mol_m3=10.0, pKw=14.0)
    values.update(overrides)
    return ChemicalEnvironment(**values)


class TestCCFSMChemicalV04(unittest.TestCase):
    def test_silicon_transfer_rates_conserve_total_silicon(self):
        state = ChemicalState(0.0, 100.0, 20.0, 30.0, 0.4)
        d = chemical_rhs(state, environment(), parameters())
        self.assertAlmostEqual(sum(d[:3]), 0.0, places=12)

    def test_effective_bridges_are_bounded_by_load_bearing_network_silicon(self):
        state = ChemicalState(0.0, 100.0, 20.0, 30.0, 0.4)
        p = parameters()
        rates = evaluate_chemical_rates(state, environment(), p)
        self.assertAlmostEqual(rates.effective_bridge_density_mol_m3,
                               0.7*30.0*0.4)
        self.assertLessEqual(rates.effective_bridge_density_mol_m3,
                             p.load_bearing_fraction*30.0)

    def test_acid_channel_increases_toward_lower_ph(self):
        p = parameters(silanolate_pair_weight=0.0, base_catalysis_weight=0.0)
        low = acid_base_activity_factors(environment(pH=1.0), p)[0]
        high = acid_base_activity_factors(environment(pH=3.0), p)[0]
        self.assertGreater(low, high)

    def test_base_channel_increases_toward_higher_ph(self):
        p = parameters(acid_catalysis_weight=0.0, silanolate_pair_weight=0.0)
        low = acid_base_activity_factors(environment(pH=8.0), p)[2]
        high = acid_base_activity_factors(environment(pH=10.0), p)[2]
        self.assertGreater(high, low)

    def test_silanolate_pair_proxy_peaks_at_pka(self):
        p = parameters(acid_catalysis_weight=0.0, base_catalysis_weight=0.0,
                       silanolate_pair_weight=1.0)
        at_pka = acid_base_activity_factors(environment(pH=9.5), p)[1]
        away = acid_base_activity_factors(environment(pH=7.5), p)[1]
        self.assertAlmostEqual(at_pka, 1.0)
        self.assertGreater(at_pka, away)

    def test_no_net_oligomerization_below_supplied_solubility(self):
        state = ChemicalState(0.0, 5.0, 0.0, 0.0, 0.0)
        rates = evaluate_chemical_rates(
            state, environment(silica_solubility_mol_m3=10.0), parameters())
        self.assertEqual(rates.oligomerization_mol_m3_s, 0.0)

    def test_arrhenius_rate_has_correct_temperature_direction(self):
        k_ref = arrhenius_rate(1.0, 30000.0, 298.15)
        k_hot = arrhenius_rate(1.0, 30000.0, 323.15)
        self.assertAlmostEqual(k_ref, 1.0)
        self.assertGreater(k_hot, k_ref)

    def test_integrator_conserves_silicon_and_keeps_states_admissible(self):
        p = parameters()
        env = environment()
        result = simulate_chemical_network(
            p, env, duration_s=1000.0, time_step_s=0.5,
            initial_monomeric_silica_mol_m3=100.0,
            initial_soluble_oligomer_silica_mol_m3=10.0,
            initial_network_silicon_mol_m3=5.0,
            initial_bridge_fraction=0.2)
        total0 = 115.0
        for state in result:
            total = (state.monomeric_silica_mol_m3
                     + state.soluble_oligomer_silica_mol_m3
                     + state.network_silicon_mol_m3)
            self.assertAlmostEqual(total, total0, places=8)
            self.assertGreaterEqual(state.bridge_fraction, 0.0)
            self.assertLessEqual(state.bridge_fraction, 1.0)

    def test_bad_environment_and_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            environment(temperature_k=0.0)
        with self.assertRaises(ValueError):
            parameters(load_bearing_fraction=1.2)


if __name__ == "__main__":
    unittest.main()
