"""CCFSM P20: staggered chemistry/transport to spatial mechanics coupling.
P13/P10 evaluates the existing 1D finite-volume transport RHS and P9 local
constitutive fields. These fields map to P19 FE quadrature points:
bridge fraction -> isotropic chemical eigenstrain; theta-theta_ref -> zeta.
P19 solves spatial quasi-static mechanics. One-way snapshot coupling only.
"""
from ccfsm_p9_mechanical_feedback import p9_field_closure
from ccfsm_p13_onsager_transport import p13_chemical_potential_transport
from ccfsm_p19_spatial_biot_bvp import P19Parameters,p19_solve_spatial_biot_bvp

def _infer_ndof(quadrature):
    first=quadrature[0]["B"]
    if len(first)!=6 or not first or not first[0]: raise ValueError("B must be 6 x ndof")
    n=len(first[0])
    if any(len(row)!=n for row in first): raise ValueError("B must be rectangular")
    for item in quadrature[1:]:
        if len(item["B"])!=6 or any(len(row)!=n for row in item["B"]):
            raise ValueError("all FE B matrices must share ndof")
    return n

def p20_staggered_coupled_snapshot(fluid_capacity,inventories,grid,
    mechanical_parameters,chemistry,diffusivities_m2_s,external_pressure_pa,
    fe_quadrature,dirichlet,boundary_quadrature=(),
    external_concentrations_left=(1e-30,1e-30),
    external_concentrations_right=(1e-30,1e-30),tolerance=1e-9):
    """Map FV chemistry/fluids to P19 quadrature and evaluate P13 transport.
    Each FE point has cell_index, B (6 x ndof), and positive weight.
    P13 fluxes remain based on local P9 closure; FE pressure is diagnostic.
    """
    n=grid.cells
    if len(fluid_capacity)!=n or len(inventories)!=4 or any(len(v)!=n for v in inventories):
        raise ValueError("state fields must match grid and contain M/O/N/B")
    if not fe_quadrature: raise ValueError("FE quadrature cannot be empty")
    local=p9_field_closure(fluid_capacity,inventories,chemistry,mechanical_parameters)
    transport=p13_chemical_potential_transport(
        fluid_capacity,inventories,grid,mechanical_parameters,chemistry,
        diffusivities_m2_s,external_pressure_pa,
        external_concentrations_left,external_concentrations_right)
    mapped=[]; indices=[]
    for item in fe_quadrature:
        idx=item["cell_index"]
        if not isinstance(idx,int) or idx<0 or idx>=n: raise ValueError("invalid FE cell_index")
        cell=local["cells"][idx]
        mapped.append({"B":item["B"],"weight":item["weight"],
          "eigenstrain":cell["chemical_eigenstrain"],
          "fluid_content_increment":float(fluid_capacity[idx])-mechanical_parameters.reference_fluid_capacity})
        indices.append(idx)
    pp=P19Parameters(mechanical_parameters.lame_lambda_pa,
        mechanical_parameters.shear_modulus_pa,mechanical_parameters.biot_modulus_pa,
        mechanical_parameters.biot_coefficient)
    mechanics=p19_solve_spatial_biot_bvp(_infer_ndof(fe_quadrature),mapped,pp,
        dirichlet,boundary_quadrature,tolerance)
    fe_p=mechanics["pore_pressure_pa"]
    local_p=tuple(local["cells"][idx]["pore_pressure_pa"] for idx in indices)
    delta=tuple(fe_p[k]-local_p[k] for k in range(len(indices)))
    scale=max(1.,*(abs(x) for x in fe_p),*(abs(x) for x in local_p))
    return {"transport_rhs":transport,"spatial_mechanics":mechanics,
      "fe_quadrature_cell_indices":tuple(indices),
      "mapped_chemical_eigenstrain":tuple(q["eigenstrain"] for q in mapped),
      "mapped_fluid_content_increment":tuple(q["fluid_content_increment"] for q in mapped),
      "local_p9_pressure_at_fe_points_pa":local_p,
      "spatial_p19_pressure_at_fe_points_pa":tuple(fe_p),
      "spatial_minus_local_pressure_pa":delta,
      "pressure_difference_relative_to_scale":max((abs(x) for x in delta),default=0.)/scale,
      "pressure_comparison_is_not_a_residual":True,
      "mechanics_equilibrium_verified":mechanics["free_dof_equilibrium_verified"],
      "two_way_transport_mechanics_feedback_implemented":False,
      "scope":"P13 FV transport and P9 local fields feed P19 spatial mechanics; FE pressure is compared but not fed back into fluxes."}
