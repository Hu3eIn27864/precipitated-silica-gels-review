"""CCFSM P13: chemical-potential finite-volume transport and traction potential.

P13 replaces concentration-gradient diffusion by an Onsager flux driven by
the discrete gradient of the P9 total chemical potential. The logarithmic
mean mobility is chosen so that, for ideal activities, this is algebraically
identical to theta*D*grad(c), while exposing an exact nonnegative discrete
diffusion dissipation. Upwind advection remains the P10 operator and is
reported separately: P13 does not claim a complete open-boundary entropy
theorem for that term.
"""
from __future__ import annotations
import math

from ccfsm_p2_chemical_affinity import R_GAS
from ccfsm_p9_mechanical_feedback import p9_field_closure
from ccfsm_p10_spatial_coupling import (
    _field, _logmean, _chemistry_validate, p10_coupled_rhs
)


def _mu0(chemistry):
    rt = R_GAS * float(chemistry.temperature_k)
    out = [0.0]
    for k in chemistry.equilibrium_constants:
        out.append(out[-1] - rt * math.log(float(k)))
    return tuple(out)


def p13_chemical_potential_transport(
    fluid_capacity, inventories, grid, mechanical_parameters, chemistry,
    diffusivities_m2_s, external_pressure_pa,
    external_concentrations_left=(1e-30, 1e-30),
    external_concentrations_right=(1e-30, 1e-30),
):
    """P10 RHS with mobile diffusion represented by Onsager chemical fluxes.

    Mobile advection and Darcy flow are retained from P10. Diffusion uses
    J_diff=-L grad(mu), L=theta_face*D*Lambda(cL,cR)/(R*T), where Lambda is
    the logarithmic mean. Reservoir half-cell faces use the same construction.
    """
    n, dx = grid.cells, grid.spacing_m
    theta = _field(fluid_capacity, n, "fluid capacity", positive=True)
    fields = tuple(_field(f, n, f"inventory {i}", positive=True)
                   for i, f in enumerate(inventories))
    d = _field(diffusivities_m2_s, 2, "diffusivities", nonnegative=True)
    c_left = _field(external_concentrations_left, 2,
                    "left reservoir concentrations", positive=True)
    c_right = _field(external_concentrations_right, 2,
                     "right reservoir concentrations", positive=True)
    cref, rt, _, _, gamma = _chemistry_validate(chemistry)

    base = p10_coupled_rhs(theta, fields, grid, mechanical_parameters,
        chemistry, d, external_pressure_pa, c_left, c_right)
    mech = p9_field_closure(theta, fields, chemistry, mechanical_parameters)
    mu0 = _mu0(chemistry)
    concentrations = tuple(tuple(fields[i][j]/theta[j] for j in range(n))
                           for i in range(2))
    new_rhs = [list(row) for row in base["inventory_dot"]]
    face_fluxes, dissipation, advective_fluxes = [], [], []

    for species in range(2):
        c = concentrations[species]
        mu = tuple(mu0[species] + rt*math.log(
            gamma[species]*v/cref) for v in c)
        q = base["darcy_flux_faces_m_s"]
        adv = [0.0]*(n+1)
        adv[0] = q[0]*(c_left[species] if q[0] > 0 else c[0])
        adv[-1] = q[-1]*(c[-1] if q[-1] >= 0 else c_right[species])
        for f in range(1,n):
            adv[f] = q[f]*(c[f-1] if q[f] >= 0 else c[f])

        diff = [0.0]*(n+1)
        diss = 0.0
        # Half-cell reservoir interfaces.
        for face, c_res, mu_res, cell in (
            (0, c_left[species], mu0[species] + rt*math.log(
                gamma[species]*c_left[species]/cref), 0),
            (n, c_right[species], mu0[species] + rt*math.log(
                gamma[species]*c_right[species]/cref), n-1),
        ):
            if d[species] > 0:
                cbar = _logmean(c_res, c[cell])
                theta_face = theta[cell]
                mobility = theta_face*d[species]*cbar/rt
                delta = (mu[cell]-mu_res) if face == 0 else (mu_res-mu[cell])
                diff[face] = -mobility*delta/(0.5*dx)
                diss += mobility*(delta/(0.5*dx))**2*(0.5*dx)

        for f in range(1,n):
            if d[species] > 0:
                cbar = _logmean(c[f-1], c[f])
                theta_face = 0.5*(theta[f-1]+theta[f])
                mobility = theta_face*d[species]*cbar/rt
                grad_mu = (mu[f]-mu[f-1])/dx
                diff[f] = -mobility*grad_mu
                diss += mobility*grad_mu**2*dx

        # Replace P10 concentration-Fick diffusion by this chemical-potential
        # flux, preserving its upwind advective part exactly.
        old_total = base["mobile_species_face_fluxes_mol_m2_s"][species]
        for j in range(n):
            new_rhs[species][j] += (
                (old_total[j+1] - (adv[j+1] + diff[j+1])) -
                (old_total[j] - (adv[j] + diff[j]))
            )/dx
        total = tuple(adv[f]+diff[f] for f in range(n+1))
        face_fluxes.append(total)
        advective_fluxes.append(tuple(adv))
        dissipation.append(diss)

    return {
        **base,
        "inventory_dot": tuple(tuple(row) for row in new_rhs),
        "mobile_species_face_fluxes_mol_m2_s": tuple(face_fluxes),
        "mobile_species_advective_face_fluxes_mol_m2_s": tuple(advective_fluxes),
        "mobile_species_onsager_diffusive_dissipation_w_m2": tuple(dissipation),
        "diffusion_flux_form": "J_diff = -theta_face*D*logmean(cL,cR)/(R*T) * grad(mu)",
        "discrete_diffusion_dissipation_nonnegative": all(v >= 0 for v in dissipation),
        "advection_entropy_closure_established": False,
    }


def p13_total_potential(state, grid, mechanical_parameters, chemistry):
    """Stored free energy minus dead-load potential traction*axial strain."""
    from ccfsm_p11_energy_time_integration import _validate_state
    theta, fields = _validate_state(state, grid.cells)
    mech = p9_field_closure(theta, fields, chemistry, mechanical_parameters)
    traction = float(mechanical_parameters.applied_axial_traction_pa)
    return grid.spacing_m*sum(
        cell["free_energy_j_m3_reference"] -
        traction*cell["axial_strain"] for cell in mech["cells"]
    )
