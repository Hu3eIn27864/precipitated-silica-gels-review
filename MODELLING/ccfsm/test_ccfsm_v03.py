import unittest
from ccfsm_v03 import CCFSMV03Parameters, simulate_natural_syneresis_v03, hydraulic_rate_from_measured_properties_h

def make(**kw):
    d=dict(bridge_density_infinity_mol_m3=100.,bridge_formation_rate_h=.4,
      fractal_dimension_initial=1.8,fractal_dimension_increment=.5,
      contact_number_initial=2.,contact_number_increment=2.,morphology_rate_h=.3,
      bridge_contraction_volume_m3_mol=1e-4,stress_relaxation_rate_h=.7,
      hydraulic_rate_h=.8,natural_accessibility=.75)
    d.update(kw); return CCFSMV03Parameters(**d)

class TestV03(unittest.TestCase):
    def test_initial_state(self):
        x=simulate_natural_syneresis_v03(make(),0,.01)
        self.assertEqual(len(x),1); self.assertEqual(x[0].observed_shrinkage,0)
    def test_bridge_bounds_and_monotonicity(self):
        x=simulate_natural_syneresis_v03(make(),10,.01); b=[s.bridge_density_mol_m3 for s in x]
        self.assertTrue(all(0<=v<=100 for v in b))
        self.assertTrue(all(b[i+1]>=b[i] for i in range(len(b)-1)))
    def test_morphology_ageing(self):
        s=simulate_natural_syneresis_v03(make(),1,.005)[-1]
        self.assertTrue(1.8<s.fractal_dimension<2.3); self.assertTrue(2<s.contact_number<4)
    def test_stress_relaxation_conserves_contraction_inventory(self):
        s=simulate_natural_syneresis_v03(make(),5,.002)[-1]
        self.assertAlmostEqual(s.residual_eigenstress_contraction+s.relaxed_contraction,1e-4*s.bridge_density_mol_m3,places=9)
        self.assertGreater(s.relaxed_contraction,0)
    def test_natural_shrinkage_monotone_and_bounded(self):
        x=simulate_natural_syneresis_v03(make(),10,.01)
        for i,s in enumerate(x):
            self.assertGreaterEqual(s.observed_shrinkage,-1e-12)
            self.assertLessEqual(s.observed_shrinkage,.75*s.intrinsic_shrinkage_potential+1e-9)
            if i: self.assertGreaterEqual(s.observed_shrinkage+1e-12,x[i-1].observed_shrinkage)
    def test_relaxation_changes_partition_not_total_q(self):
        a=simulate_natural_syneresis_v03(make(stress_relaxation_rate_h=2),5,.002)[-1]
        b=simulate_natural_syneresis_v03(make(stress_relaxation_rate_h=.2),5,.002)[-1]
        self.assertAlmostEqual(a.intrinsic_shrinkage_potential,b.intrinsic_shrinkage_potential,places=8)
        self.assertNotAlmostEqual(a.residual_eigenstress_contraction,b.residual_eigenstress_contraction,places=4)
    def test_hydraulic_length_squared_scaling(self):
        a=hydraulic_rate_from_measured_properties_h(.001,.001,1e-15,1000)
        b=hydraulic_rate_from_measured_properties_h(.001,.002,1e-15,1000)
        self.assertAlmostEqual(a/b,4)
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): make(bridge_formation_rate_h=-1)
        with self.assertRaises(ValueError): make(natural_accessibility=0)
        with self.assertRaises(ValueError): simulate_natural_syneresis_v03(make(),1,-.1)
    def test_preaged_initial_network(self):
        s=simulate_natural_syneresis_v03(make(),1,.01,initial_bridge_density_mol_m3=20,
            initial_fractal_dimension=1.9,initial_contact_number=2.2)[-1]
        self.assertGreater(s.bridge_density_mol_m3,20)
