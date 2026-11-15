import unittest
from ccfsm_p27_25_snapshot_integrals import reconstruct_p27_25_p24_step


def snap(scale):
    tr = {
        "reaction_dissipation_w_m3_reference": (2.*scale, 1.*scale),
        "darcy_internal_dissipation_w_m2": 3.*scale,
        "mobile_species_onsager_diffusive_dissipation_w_m2": (4.*scale, 5.*scale),
        "reservoir_hydraulic_power_w_m2": 6.*scale,
        "mobile_species_advective_face_fluxes_mol_m2_s": ((1.*scale, 2.*scale, 3.*scale),
                                                            (2.*scale, 3.*scale, 4.*scale)),
        "mobile_species_face_fluxes_mol_m2_s": ((1.5*scale, 2.*scale, 2.5*scale),
                                                 (2.5*scale, 3.*scale, 3.5*scale)),
        "mobile_species_chemical_potential_j_mol": ((10., 11.), (20., 21.)),
        "onsager_reservoir_chemical_potential_left_j_mol": (8., 18.),
        "onsager_reservoir_chemical_potential_right_j_mol": (12., 22.),
    }
    return {"transport_rhs": tr}


class P27_25Tests(unittest.TestCase):
    def test_trapezoidal_integrals(self):
        r = reconstruct_p27_25_p24_step(snap(1.), {
            "converged": True, "pressure_snapshot_matches_accepted_state": True,
            "last_snapshot": snap(3.)}, 2., cell_width_m=.5, reference_area_m2=4.)
        self.assertAlmostEqual(r["integrated_dissipation_j"]["reaction_j"], 24.)
        self.assertAlmostEqual(r["integrated_dissipation_j"]["darcy_j"], 48.)
        self.assertAlmostEqual(r["integrated_dissipation_j"]["onsager_diffusion_j"], 144.)
        self.assertAlmostEqual(r["external_work_j"]["reservoir_hydraulic_j"], 96.)
        self.assertFalse(r["advection_entropy_closure_certified"])
    def test_nonconverged_p24_rejected(self):
        with self.assertRaisesRegex(ValueError, "must be converged"):
            reconstruct_p27_25_p24_step(snap(1.), {"converged": False}, 1.,
                cell_width_m=1., reference_area_m2=1.)
    def test_snapshot_state_consistency_required(self):
        with self.assertRaisesRegex(ValueError, "match accepted state"):
            reconstruct_p27_25_p24_step(snap(1.), {"converged": True,
                "pressure_snapshot_matches_accepted_state": False}, 1.,
                cell_width_m=1., reference_area_m2=1.)
    def test_positive_geometry_and_dt(self):
        with self.assertRaisesRegex(ValueError, "must be positive"):
            reconstruct_p27_25_p24_step(snap(1.), {"converged": True,
                "pressure_snapshot_matches_accepted_state": True,
                "last_snapshot": snap(1.)}, 0., cell_width_m=1., reference_area_m2=1.)
    def test_material_boundary_transfer_reported(self):
        r = reconstruct_p27_25_p24_step(snap(1.), {"converged": True,
            "pressure_snapshot_matches_accepted_state": True,
            "last_snapshot": snap(1.)}, 1., cell_width_m=1., reference_area_m2=2.)
        self.assertEqual(len(r["mobile_species_boundary_transport"]["time_integrated_net_inward_mol"]), 2)


if __name__ == "__main__":
    unittest.main()
