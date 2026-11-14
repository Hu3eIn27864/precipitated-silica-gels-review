import unittest
from ccfsm_v03 import (
    CCFSMV03Parameters,
    simulate_natural_syneresis_v03,
)

def params(**overrides):
    values = dict(
        bridge_density_infinity_mol_m3=100.0,
        bridge_formation_rate_h=0.4,
        fractal_dimension_initial=1.8,
        fractal_dimension_increment=0.5,
        contact_number_initial=2.0,
        contact_number_increment=2.0,
        morphology_rate_h=0.3,
        bridge_contraction_volume_m3_mol=1.0e-4,
        stress_relaxation_rate_h=0.7,
        hydraulic_rate_h=0.8,
        natural_accessibility=0.75,
    )
    values.update(overrides)
    return CCFSMV03Parameters(**values)

class TestStructuralIdentifiability(unittest.TestCase):
    def test_bridge_scale_symmetry_leaves_shrinkage_unchanged(self):
        p1 = params()
        p2 = params(
            bridge_density_infinity_mol_m3=1000.0,
            bridge_contraction_volume_m3_mol=1.0e-5,
        )
        a = simulate_natural_syneresis_v03(
            p1, 5.0, 0.002, initial_bridge_density_mol_m3=20.0
        )
        b = simulate_natural_syneresis_v03(
            p2, 5.0, 0.002, initial_bridge_density_mol_m3=200.0
        )
        for sa, sb in zip(a, b):
            self.assertAlmostEqual(sa.observed_shrinkage, sb.observed_shrinkage, places=10)
            self.assertAlmostEqual(sa.intrinsic_shrinkage_potential, sb.intrinsic_shrinkage_potential, places=10)
            self.assertAlmostEqual(sa.fractal_dimension, sb.fractal_dimension, places=10)
            self.assertAlmostEqual(sa.contact_number, sb.contact_number, places=10)
            self.assertAlmostEqual(sb.bridge_density_mol_m3, 10.0 * sa.bridge_density_mol_m3, places=8)

    def test_stress_relaxation_rate_is_invisible_to_shrinkage_output(self):
        a = simulate_natural_syneresis_v03(params(stress_relaxation_rate_h=0.15), 5.0, 0.002)
        b = simulate_natural_syneresis_v03(params(stress_relaxation_rate_h=2.5), 5.0, 0.002)
        for sa, sb in zip(a, b):
            self.assertAlmostEqual(sa.observed_shrinkage, sb.observed_shrinkage, places=10)
            self.assertAlmostEqual(sa.intrinsic_shrinkage_potential, sb.intrinsic_shrinkage_potential, places=10)
        self.assertNotAlmostEqual(
            a[-1].residual_eigenstress_contraction,
            b[-1].residual_eigenstress_contraction,
            places=7,
        )

    def test_morphology_parameters_are_invisible_to_shrinkage_output(self):
        a = simulate_natural_syneresis_v03(params(), 5.0, 0.002)
        b = simulate_natural_syneresis_v03(
            params(
                fractal_dimension_initial=2.1,
                fractal_dimension_increment=0.2,
                contact_number_initial=3.0,
                contact_number_increment=1.0,
                morphology_rate_h=1.7,
            ),
            5.0,
            0.002,
        )
        for sa, sb in zip(a, b):
            self.assertAlmostEqual(sa.observed_shrinkage, sb.observed_shrinkage, places=10)
            self.assertAlmostEqual(sa.intrinsic_shrinkage_potential, sb.intrinsic_shrinkage_potential, places=10)
        self.assertNotAlmostEqual(a[-1].fractal_dimension, b[-1].fractal_dimension, places=5)
        self.assertNotAlmostEqual(a[-1].contact_number, b[-1].contact_number, places=5)

if __name__ == "__main__":
    unittest.main()
