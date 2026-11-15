import unittest
from ccfsm_p27_23_thermodynamic_ledger import build_p27_23_thermodynamic_ledger

class P27_23Tests(unittest.TestCase):
    def setUp(self):
        self.cells=[
          {"elastic_energy_j_m3_reference":2.0,"biot_storage_energy_j_m3_reference":3.0,
           "chemical_energy_j_m3_reference":5.0,"axial_strain":0.01,"applied_axial_traction_pa":100.0},
          {"elastic_energy_j_m3_reference":1.0,"biot_storage_energy_j_m3_reference":2.0,
           "chemical_energy_j_m3_reference":4.0,"axial_strain":0.02,"applied_axial_traction_pa":100.0},
        ]
        self.volumes=[2.0,3.0]
        self.p13={"reaction_dissipation_w_m3_reference":(2.0,1.0),
          "darcy_internal_dissipation_w_m2":4.0,
          "mobile_species_onsager_diffusive_dissipation_w_m2":(3.0,2.0)}
    def ledger(self,**kw):
        return build_p27_23_thermodynamic_ledger(self.cells,self.volumes,self.p13,
          reference_area_m2=2.0,energy_rate_w=-1.0,**kw)
    def test_energy_and_dissipation_units(self):
        r=self.ledger()
        self.assertAlmostEqual(r["p9_mechanical_energy_integral_j"],20.0)
        self.assertAlmostEqual(r["selected_chemical_energy_j"],22.0)
        self.assertAlmostEqual(r["reaction_dissipation_w"],7.0)
        self.assertAlmostEqual(r["darcy_internal_dissipation_w"],8.0)
        self.assertAlmostEqual(r["onsager_diffusion_dissipation_w"],10.0)
        self.assertAlmostEqual(r["total_dissipation_w"],25.0)
    def test_balance_residual_and_external_power(self):
        r=build_p27_23_thermodynamic_ledger(self.cells,self.volumes,self.p13,
          reference_area_m2=2.0,energy_rate_w=-20.0,
          external_power_terms_w={"reservoirs":5.0})
        self.assertAlmostEqual(r["predicted_energy_rate_w"],-20.0)
        self.assertTrue(r["balance_within_tolerance"])
    def test_p19_replaces_not_adds_p9_mechanics(self):
        audit={"status":"matched_p9_p19_mechanical_energy","p19_elastic_energy_j":7.0,
          "p19_biot_storage_energy_j":13.0,"p19_stored_energy_j":20.0,
          "point_reports":({"weight_m3":2.0},{"weight_m3":3.0})}
        r=self.ledger(mechanical_energy_owner="p19",p19_energy_audit=audit)
        self.assertEqual(r["selected_mechanical_energy_j"],20.0)
        self.assertTrue(r["mechanical_energy_counted_once"])
        self.assertEqual(r["selected_total_potential_j"],42.0)
    def test_p19_volume_mismatch_rejected(self):
        audit={"status":"matched_p9_p19_mechanical_energy","p19_elastic_energy_j":7.0,
          "p19_biot_storage_energy_j":13.0,"p19_stored_energy_j":20.0,
          "point_reports":({"weight_m3":4.0},)}
        with self.assertRaisesRegex(ValueError,"volume"):
            self.ledger(mechanical_energy_owner="p19",p19_energy_audit=audit)
    def test_negative_dissipation_rejected(self):
        bad=dict(self.p13,reaction_dissipation_w_m3_reference=(2.0,-0.1))
        with self.assertRaisesRegex(ValueError,"negative reaction"):
            build_p27_23_thermodynamic_ledger(self.cells,self.volumes,bad,
              reference_area_m2=2.0,energy_rate_w=0.0)
    def test_dead_load_potential_is_explicit(self):
        r=self.ledger(potential_convention="dead_load_total")
        self.assertAlmostEqual(r["dead_load_potential_j"],-8.0)
        self.assertAlmostEqual(r["selected_total_potential_j"],34.0)
    def test_dead_load_requires_uniform_traction(self):
        cells=[dict(self.cells[0]),dict(self.cells[1],applied_axial_traction_pa=101.)]
        with self.assertRaisesRegex(ValueError,"uniform applied traction"):
            build_p27_23_thermodynamic_ledger(cells,self.volumes,self.p13,
              reference_area_m2=2.0,energy_rate_w=0.0,potential_convention="dead_load_total")

if __name__=="__main__": unittest.main()
