"""CCFSM P10: spatial P9 chemo-poroelastic finite-volume coupling.

Primary state: fluid capacity theta and four silicon inventories (M,O,N,B).
P9 supplies cellwise pore pressure, strain, bridge fraction and permeability.
A single Darcy face flux updates both fluid continuity and mobile M/O advection.
This is a semidiscrete 1D operator; it is not a time integrator or a global
PDE existence/energy theorem.
"""
from __future__ import annotations
import math
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters, p9_field_closure
from ccfsm_p2_chemical_affinity import R_GAS


def _field(values, n, name, positive=False, nonnegative=False):
    if len(values) != n:
        raise ValueError(f"{name} must contain {n} cell values")
    out = tuple(float(v) for v in values)
    if any(not math.isfinite(v) for v in out):
        raise ValueError(f"{name} must be finite")
    if positive and any(v <= 0 for v in out):
        raise ValueError(f"{name} must be positive")
    if nonnegative and any(v < 0 for v in out):
        raise ValueError(f"{name} must be nonnegative")
    return out


def _logmean(x, y):
    if x <= 0 or y <= 0:
        raise ValueError("logarithmic-mean arguments must be positive")
    if x == y:
        return x
    if abs(x-y) <= 1e-8*max(x, y):
        return 0.5*(x+y)
    return (x-y)/(math.log(x)-math.log(y))


def _chemistry_validate(chem):
    cref = float(chem.reference_concentration)
    temp = float(chem.temperature_k)
    rates = tuple(float(v) for v in chem.rate_constants_s)
    eq = tuple(float(v) for v in chem.equilibrium_constants)
    gamma = tuple(float(v) for v in chem.activity_coefficients)
    if not math.isfinite(cref) or cref <= 0 or not math.isfinite(temp) or temp <= 0:
        raise ValueError("reference concentration and temperature must be positive")
    if len(rates) != 3 or any(not math.isfinite(v) or v < 0 for v in rates):
        raise ValueError("three nonnegative reaction rates required")
    if len(eq) != 3 or any(not math.isfinite(v) or v <= 0 for v in eq):
        raise ValueError("three positive equilibrium constants required")
    if len(gamma) != 4 or any(not math.isfinite(v) or v <= 0 for v in gamma):
        raise ValueError("four positive activity coefficients required")
    return cref, R_GAS*temp, rates, eq, gamma


def p10_coupled_rhs(fluid_capacity, inventories, grid: P8Grid,
                    mechanical_parameters: P9Parameters, chemistry,
                    diffusivities_m2_s, external_pressure_pa,
                    external_concentrations_left=(0.0, 0.0),
                    external_concentrations_right=(0.0, 0.0)):
    """Return conservative P10 semidiscrete RHS and diagnostic fluxes.

    All inventories are mol Si-equivalent per reference volume; theta is
    reference-volume fluid capacity. q is positive from left to right.
    Reservoir pressure and concentrations are imposed at half-cell distances.
    """
    n, dx = grid.cells, grid.spacing_m
    theta = _field(fluid_capacity, n, "fluid capacity", positive=True)
    if any(v > 1.0 for v in theta):
        raise ValueError("fluid capacity cannot exceed one")
    if len(inventories) != 4:
        raise ValueError("four inventory fields M/O/N/B required")
    fields = tuple(_field(f, n, f"inventory {i}", positive=True)
                   for i, f in enumerate(inventories))
    d = _field(diffusivities_m2_s, 2, "diffusivities", nonnegative=True)
    c_left = _field(external_concentrations_left, 2,
                    "left reservoir concentrations", nonnegative=True)
    c_right = _field(external_concentrations_right, 2,
                     "right reservoir concentrations", nonnegative=True)
    p_ext = float(external_pressure_pa)
    if not math.isfinite(p_ext):
        raise ValueError("external pressure must be finite")
    cref, rt, rates, equilibria, gamma = _chemistry_validate(chemistry)

    mech = p9_field_closure(theta, fields, chemistry, mechanical_parameters)
    pressure = mech["pore_pressure_pa"]
    permeability = mech["intrinsic_permeability_m2_per_pas"]

    # One Darcy flux, computed from P9 pressure and P9 structure-dependent K.
    q = [0.0]*(n+1)
    k_face = [0.0]*(n+1)
    half = 0.5*dx
    k_face[0] = permeability[0]
    k_face[-1] = permeability[-1]
    q[0] = -k_face[0]*(pressure[0]-p_ext)/half
    q[-1] = -k_face[-1]*(p_ext-pressure[-1])/half
    for face in range(1, n):
        kl, kr = permeability[face-1], permeability[face]
        k_face[face] = 2.0*kl*kr/(kl+kr)
        q[face] = -k_face[face]*(pressure[face]-pressure[face-1])/dx

    theta_rhs = [-(q[j+1]-q[j])/dx for j in range(n)]
    mass_rhs = [[0.0]*n for _ in range(4)]
    reaction_dissipation = [0.0]*n
    reaction_rates = [[0.0]*n for _ in range(3)]
    activities_by_cell = []

    # Local reversible chemistry uses P9 total potentials, including
    # mechanical N/B corrections. Log-mean mobility makes r_i*A_i >= 0.
    for j in range(n):
        cell = mech["cells"][j]
        mm, mo, sn, sb = (fields[i][j] for i in range(4))
        activities = (gamma[0]*mm/(theta[j]*cref),
                      gamma[1]*mo/(theta[j]*cref),
                      gamma[2]*sn/cref, gamma[3]*sb/cref)
        mu = cell["total_chemical_potentials_j_mol"]
        activities_by_cell.append(activities)
        rr = []
        for i in range(3):
            affinity = mu[i]-mu[i+1]
            right_activity = activities[i+1]/equilibria[i]
            mobility = rates[i]*cref*_logmean(activities[i], right_activity)
            rate = mobility*affinity/rt
            rr.append(rate)
            reaction_dissipation[j] += rate*affinity
            reaction_rates[i][j] = rate
        r1, r2, r3 = rr
        mass_rhs[0][j] = -r1
        mass_rhs[1][j] = r1-r2
        mass_rhs[2][j] = r2-r3
        mass_rhs[3][j] = r3

    concentrations = tuple(tuple(fields[i][j]/theta[j] for j in range(n))
                           for i in range(2))
    species_boundary_fluxes = []
    diffusion_dissipation = [0.0, 0.0]
    species_face_fluxes = []
    for species in range(2):
        c = concentrations[species]
        flux = [0.0]*(n+1)
        # Advective upwinding and half-cell reservoir diffusion.
        cup_l = c_left[species] if q[0] > 0.0 else c[0]
        cup_r = c[-1] if q[-1] >= 0.0 else c_right[species]
        flux[0] = q[0]*cup_l - theta[0]*d[species]*(c[0]-c_left[species])/half
        flux[-1] = q[-1]*cup_r - theta[-1]*d[species]*(c_right[species]-c[-1])/half
        for face in range(1, n):
            l, r = face-1, face
            cup = c[l] if q[face] >= 0.0 else c[r]
            theta_face = 0.5*(theta[l]+theta[r])
            diffusive = -theta_face*d[species]*(c[r]-c[l])/dx
            flux[face] = q[face]*cup + diffusive
            c_face = _logmean(c[l], c[r])
            diffusion_dissipation[species] += (
                theta_face*d[species]*(c[r]-c[l])**2/(dx*dx*c_face)*dx
            )
        for j in range(n):
            mass_rhs[species][j] -= (flux[j+1]-flux[j])/dx
        species_boundary_fluxes.append((flux[0], flux[-1]))
        species_face_fluxes.append(tuple(flux))

    # Darcy dissipation diagnostic. Boundary reservoir work is reported
    # separately; only internal-face dissipation is included here.
    darcy_dissipation = sum(
        q[f]**2/k_face[f]*dx for f in range(1, n)
    )
    reservoir_hydraulic_power = (
        p_ext*q[-1] - p_ext*q[0]
    )
    return {
        "fluid_capacity_dot_s": tuple(theta_rhs),
        "inventory_dot": tuple(tuple(row) for row in mass_rhs),
        "pore_pressure_pa": pressure,
        "axial_strain": mech["axial_strain"],
        "bridge_fraction": mech["bridge_fraction"],
        "intrinsic_permeability_m2_per_pas": permeability,
        "darcy_flux_faces_m_s": tuple(q),
        "permeability_faces_m2_per_pas": tuple(k_face),
        "mobile_concentrations_mol_m3": concentrations,
        "mobile_species_face_fluxes_mol_m2_s": tuple(species_face_fluxes),
        "mobile_species_boundary_fluxes_mol_m2_s": tuple(species_boundary_fluxes),
        "reaction_rates_mol_m3_s": tuple(tuple(row) for row in reaction_rates),
        "reaction_dissipation_w_m3_reference": tuple(reaction_dissipation),
        "darcy_internal_dissipation_w_m2": darcy_dissipation,
        "diffusion_dissipation_w_m2": tuple(diffusion_dissipation),
        "reservoir_hydraulic_power_w_m2": reservoir_hydraulic_power,
        "cell_mechanics": mech["cells"],
    }


def p10_total_silicon(inventories, grid: P8Grid):
    if len(inventories) != 4 or any(len(f) != grid.cells for f in inventories):
        raise ValueError("four inventory fields matching grid are required")
    return grid.spacing_m*sum(sum(float(v) for v in f) for f in inventories)


def p10_total_fluid_capacity(fluid_capacity, grid: P8Grid):
    theta = _field(fluid_capacity, grid.cells, "fluid capacity", positive=True)
    return grid.spacing_m*sum(theta)
