import math
import unittest
from ccfsm_p27_18_onsager_audit import reconstruct_onsager_species_flux,audit_onsager_diffusion,audit_p13_onsager_snapshot

def fixture():
    theta=(.8,.7); c=((1.,2.),(2.,3.)); mu=((0.,1.),(1.,2.))
    rt=2.; dx=1.; d=(.5,.25)
    cl=(.5,1.); cr=(3.,4.); mul=(-1.,0.); mur=(2.,3.)
    rec=[reconstruct_onsager_species_flux(c[s],mu[s],theta,d[s],rt,dx,
        cl[s],cr[s],mul[s],mur[s]) for s in range(2)]
    adv=((.2,.3,.4),(-.1,.0,.1))
    total=tuple(tuple(adv[s][f]+rec[s]["diffusive_face_flux"][f] for f in range(3)) for s in range(2))
    diss=tuple(x["dissipation_w_m2"] for x in rec)
    args=(c,mu,theta,d,rt,dx,cl,cr,mul,mur,total,adv,diss)
    return args

class TestP2718(unittest.TestCase):
    def test_independent_flux_and_dissipation(self):
        r=audit_onsager_diffusion(*fixture())
        self.assertTrue(r["overall_pass"],r)
        self.assertEqual(r["status"],"onsager_independent_audit_passed")
        self.assertTrue(all(x["dissipation_nonnegative"] for x in r["species_reports"]))
    def test_detects_stored_flux_perturbation(self):
        a=list(fixture()); total=[list(x) for x in a[10]]; total[0][1]+=.01; a[10]=tuple(tuple(x) for x in total)
        r=audit_onsager_diffusion(*a)
        self.assertFalse(r["overall_pass"])
    def test_detects_stored_dissipation_perturbation(self):
        a=list(fixture()); a[12]=(a[12][0]+.1,a[12][1])
        self.assertFalse(audit_onsager_diffusion(*a)["overall_pass"])
    def test_zero_diffusivity(self):
        r=reconstruct_onsager_species_flux((1.,),(2.,),(.8,),0.,2.,1.,.5,2.,1.,3.)
        self.assertEqual(r["diffusive_face_flux"],(0.,0.))
        self.assertEqual(r["dissipation_w_m2"],0.)
    def test_single_cell_boundary_half_cells(self):
        r=reconstruct_onsager_species_flux((2.,),(1.,),(.9,),.4,3.,.2,1.,4.,0.,2.)
        self.assertEqual(len(r["diffusive_face_flux"]),2)
        self.assertGreaterEqual(r["dissipation_w_m2"],0.)
    def test_equal_concentration_logmean(self):
        r=reconstruct_onsager_species_flux((1.,1.),(0.,0.),(.8,.8),.5,2.,1.,1.,1.,0.,0.)
        self.assertEqual(r["diffusive_face_flux"],(0.,0.,0.))
    def test_bad_positive_domain(self):
        # The low-level reconstruction API raises on malformed input;
        # the aggregate audit API converts the same invalid data to a
        # structured fail-closed status.
        with self.assertRaises(ValueError):
            reconstruct_onsager_species_flux((0.,),(1.,),(.8,),.5,2.,1.,1.,1.,0.,0.)
        result=audit_onsager_diffusion(((0.,),)*2,((0.,),)*2,(.8,),(.5,.5),2.,1.,
            (.5,.5),(.5,.5),(0.,0.),(0.,0.),((0.,0.),)*2,((0.,0.),)*2,(0.,0.))
        self.assertFalse(result["overall_pass"])
        self.assertEqual(result["status"],"invalid_or_malformed_input")
    def test_p13_snapshot_adapter(self):
        a=fixture()
        c,mu,theta,d,rt,dx,cl,cr,mul,mur,total,adv,diss=a
        snap={"mobile_species_concentration_mol_m3":c,
            "mobile_species_chemical_potential_j_mol":mu,"onsager_fluid_capacity":theta,
            "onsager_diffusivities_m2_s":d,"onsager_rt_j_mol":rt,"onsager_grid_spacing_m":dx,
            "onsager_reservoir_concentration_left_mol_m3":cl,
            "onsager_reservoir_concentration_right_mol_m3":cr,
            "onsager_reservoir_chemical_potential_left_j_mol":mul,
            "onsager_reservoir_chemical_potential_right_j_mol":mur,
            "mobile_species_face_fluxes_mol_m2_s":total,
            "mobile_species_advective_face_fluxes_mol_m2_s":adv,
            "mobile_species_onsager_diffusive_dissipation_w_m2":diss}
        self.assertTrue(audit_p13_onsager_snapshot(snap)["overall_pass"])
    def test_no_physical_law_claim(self):
        r=audit_onsager_diffusion(*fixture())
        self.assertFalse(r["physical_onsager_law_certified"])

if __name__=="__main__": unittest.main()
