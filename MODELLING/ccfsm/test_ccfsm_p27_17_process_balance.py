import unittest
from ccfsm_p27_17_process_balance import audit_p21_process_balance

def fixture():
    # One cell, unit width. Darcy q=(0,1), M/O total fluxes (0,3)/(0,5).
    # Advective components are (0,2)/(0,3); inferred diffusion is (0,1)/(0,2).
    # Rates r=(4,1,.5) imply reaction sources (-4,3,.5,.5).
    # Therefore RHS: theta=-1, M=-7, O=-2, N=.5, B=.5.
    return {"transport_rhs":{
        "fluid_capacity_dot_s":(-1.,),
        "inventory_dot":((-7.,),(-2.,),(.5,),(.5,)),
        "darcy_flux_faces_m_s":(0.,1.),
        "mobile_species_advective_face_fluxes_mol_m2_s":((0.,2.),(0.,3.)),
        "mobile_species_face_fluxes_mol_m2_s":((0.,3.),(0.,5.)),
        "reaction_rates_mol_m3_s":((4.,),(1.,),(.5,)),
    }}

class TestP2717(unittest.TestCase):
    def test_all_processes_close(self):
        r=audit_p21_process_balance(fixture(),(1.,))
        self.assertTrue(r["overall_pass"],r)
        self.assertEqual(r["status"],"p21_process_balance_audited")
        self.assertTrue(r["rhs_reconstruction"]["pass"])
        self.assertTrue(r["process_reports"]["M_onsager_diffusion"]["global_pass"])
        self.assertTrue(r["process_reports"]["O_advection"]["local_pass"])
    def test_reaction_stoichiometry_cancels_total_silicon(self):
        r=audit_p21_process_balance(fixture(),(1.,))
        src=r["reaction_sources_mol_m3_s"]
        self.assertAlmostEqual(sum(row[0] for row in src),0.)
    def test_detects_wrong_mobile_rhs(self):
        s=fixture(); s["transport_rhs"]["inventory_dot"]=((-6.,),(-2.,),(.5,),(.5,))
        r=audit_p21_process_balance(s,(1.,))
        self.assertFalse(r["overall_pass"])
        self.assertEqual(r["status"],"p21_process_balance_failed")
    def test_detects_flux_rhs_mismatch(self):
        s=fixture(); s["transport_rhs"]["mobile_species_face_fluxes_mol_m2_s"]=((0.,4.),(0.,5.))
        r=audit_p21_process_balance(s,(1.,))
        self.assertFalse(r["overall_pass"])
    def test_nonuniform_widths(self):
        s=fixture()
        # Rebuild a two-cell exact field with q=(0,1,2), constant divergence -1.
        t=s["transport_rhs"]
        t["fluid_capacity_dot_s"]=(-1.,-1.)
        t["darcy_flux_faces_m_s"]=(0.,1.,2.)
        t["inventory_dot"]=((-7.,-7.),(-2.,-2.),(.5,.5),(.5,.5))
        t["mobile_species_advective_face_fluxes_mol_m2_s"]=((0.,2.,4.),(0.,3.,6.))
        t["mobile_species_face_fluxes_mol_m2_s"]=((0.,3.,6.),(0.,5.,10.))
        t["reaction_rates_mol_m3_s"]=((4.,4.),(1.,1.),(.5,.5))
        r=audit_p21_process_balance(s,(.5,1.5))
        self.assertTrue(r["overall_pass"],r)
    def test_requires_process_fluxes(self):
        s=fixture(); del s["transport_rhs"]["mobile_species_advective_face_fluxes_mol_m2_s"]
        self.assertEqual(audit_p21_process_balance(s,(1.,))["status"],"incomplete_p21_process_data")
    def test_reaction_only_n_b_balance(self):
        r=audit_p21_process_balance(fixture(),(1.,))
        self.assertTrue(r["process_reports"]["N_reaction_only"]["global_pass"])
        self.assertTrue(r["process_reports"]["B_reaction_only"]["global_pass"])
    def test_no_physical_completeness_claim(self):
        r=audit_p21_process_balance(fixture(),(1.,))
        self.assertFalse(r["physical_process_completeness_certified"])

if __name__=="__main__": unittest.main()
