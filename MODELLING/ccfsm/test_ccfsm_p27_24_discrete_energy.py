import unittest
from ccfsm_p27_24_discrete_energy import audit_p24_discrete_energy_step


class P27_24Tests(unittest.TestCase):
    def setUp(self):
        self.a = [{"elastic_energy_j_m3_reference": 2., "biot_storage_energy_j_m3_reference": 3.,
                   "chemical_energy_j_m3_reference": 4., "axial_strain": .01,
                   "applied_axial_traction_pa": 100.}]
        self.b = [{"elastic_energy_j_m3_reference": 1., "biot_storage_energy_j_m3_reference": 2.,
                   "chemical_energy_j_m3_reference": 3., "axial_strain": .02,
                   "applied_axial_traction_pa": 100.}]
        self.d = {"reaction_j": 1., "darcy_j": 2., "onsager_diffusion_j": 1.}
    def run_audit(self, **kw):
        diss = kw.pop("integrated_dissipation_j", self.d)
        work = kw.pop("external_work_j", {"reservoir": 1.})
        return audit_p24_discrete_energy_step(self.a, self.b, [2.], 0.5,
            integrated_dissipation_j=diss, external_work_j=work, **kw)
    def test_exact_manufactured_balance(self):
        r = self.run_audit()
        self.assertAlmostEqual(r["energy_change_j"], -6.)
        self.assertAlmostEqual(r["predicted_energy_change_j"], -3.)
        self.assertAlmostEqual(r["discrete_energy_residual_j"], -3.)
        self.assertFalse(r["residual_within_tolerance"])
    def test_closing_balance(self):
        r = audit_p24_discrete_energy_step(self.a, self.b, [2.], 0.5,\n            integrated_dissipation_j=self.d, external_work_j={"reservoir": -2.})
        self.assertAlmostEqual(r["discrete_energy_residual_j"], 0.)
        self.assertTrue(r["residual_within_tolerance"])
    def test_nonnegative_integrated_dissipation(self):
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            self.run_audit(integrated_dissipation_j={**self.d, "darcy_j": -1.})
    def test_fixed_geometry_required(self):
        with self.assertRaisesRegex(ValueError, "equal nonzero"):
            audit_p24_discrete_energy_step(self.a, self.b*2, [2.], .5,
                integrated_dissipation_j=self.d)
    def test_dt_positive(self):
        with self.assertRaisesRegex(ValueError, "dt must be positive"):
            audit_p24_discrete_energy_step(self.a, self.b, [2.], 0.,
                integrated_dissipation_j=self.d)
    def test_p19_owner_replaces_p9(self):
        audit0 = {"status":"matched_p9_p19_mechanical_energy", "p19_elastic_energy_j":4.,
                  "p19_biot_storage_energy_j":6., "p19_stored_energy_j":10.,
                  "point_reports":({"weight_m3":2.},)}
        audit1 = {"status":"matched_p9_p19_mechanical_energy", "p19_elastic_energy_j":2.,
                  "p19_biot_storage_energy_j":4., "p19_stored_energy_j":6.,
                  "point_reports":({"weight_m3":2.},)}
        r = self.run_audit(mechanical_energy_owner="p19",
                           p19_initial_audit=audit0, p19_final_audit=audit1)
        self.assertAlmostEqual(r["energy_change_j"], -6.)
        self.assertTrue(r["mechanical_energy_counted_once"])
    def test_p19_requires_both_states(self):
        with self.assertRaisesRegex(ValueError, "both states"):
            self.run_audit(mechanical_energy_owner="p19", p19_initial_audit={})
    def test_advection_closure_is_explicit(self):
        r = self.run_audit(unclosed_energy_terms=())
        self.assertFalse(r["full_energy_closure_certified"])\n        self.assertTrue(r["caller_declared_all_energy_terms_closed"])
        self.assertNotIn("advection_j", r["integrated_dissipation_terms_j"])
        r2 = self.run_audit(integrated_dissipation_j={**self.d, "advection_j": .5})
        self.assertIn("advection_j", r2["integrated_dissipation_terms_j"])
        self.assertFalse(r2["full_energy_closure_certified"])


if __name__ == "__main__":
    unittest.main()
