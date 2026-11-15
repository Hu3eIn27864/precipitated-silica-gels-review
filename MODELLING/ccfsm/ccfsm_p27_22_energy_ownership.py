"""P27.22: termwise P9/P19 mechanical-energy equivalence and ownership audit."""
from __future__ import annotations
import math

def _f(x, name):
    x=float(x)
    if not math.isfinite(x): raise ValueError(name+' must be finite')
    return x

def _close(a,b,atol,rtol):
    return abs(a-b) <= atol+rtol*max(abs(a),abs(b))

def audit_p9_p19_energy_equivalence(p9_cells,p9_parameters,p19_parameters,p19_quadrature,p19_displacement_dofs,p19_result,*,mechanical_energy_owner='p19',chemical_energy_owner='p9',atol=1e-8,rtol=1e-8):
    """Compare P9 local densities with independently reconstructed P19 FE quadrature.
    Weights are physical m^3; densities J/m^3; integrated energies J.
    The P9 special kinematics (axial strain only) is enforced.
    """
    if mechanical_energy_owner not in ('p9','p19'): raise ValueError('mechanical_energy_owner must be p9 or p19')
    if chemical_energy_owner not in ('p9','external','none'): raise ValueError('invalid chemical_energy_owner')
    atol,rtol=_f(atol,'atol'),_f(rtol,'rtol')
    if atol<0 or rtol<0: raise ValueError('tolerances must be nonnegative')
    p9_parameters.validate(); p19_parameters.validate()
    for name in ('lame_lambda_pa','shear_modulus_pa','biot_modulus_pa','biot_coefficient'):
        if not _close(_f(getattr(p9_parameters,name),'P9 '+name),_f(getattr(p19_parameters,name),'P19 '+name),atol,rtol): raise ValueError('P9/P19 material mismatch: '+name)
    cells,quad=tuple(p9_cells),tuple(p19_quadrature)
    u=tuple(_f(x,'displacement DOF') for x in p19_displacement_dofs)
    if not cells or len(cells)!=len(quad): raise ValueError('P9 cells and P19 quadrature need equal nonzero length')
    if not u: raise ValueError('P19 displacement vector must be nonempty')
    lam=float(p19_parameters.lame_lambda_pa); G=float(p19_parameters.shear_modulus_pa); M=float(p19_parameters.biot_modulus_pa); alpha=float(p19_parameters.biot_coefficient)
    e19=s19=e9=s9=chemical=0.0; details=[]
    for i,(cell,q) in enumerate(zip(cells,quad)):
        B=q['B']
        if len(B)!=6 or any(len(row)!=len(u) for row in B): raise ValueError('P19 B must be 6 x number of displacement DOFs')
        B=[[_f(x,'B entry') for x in row] for row in B]
        eps=[sum(row[j]*u[j] for j in range(len(u))) for row in B]
        w=_f(q['weight'],'quadrature weight'); c=_f(q['eigenstrain'],'eigenstrain'); z=_f(q['fluid_content_increment'],'fluid increment')
        if w<=0: raise ValueError('quadrature weights must be positive')
        ee=[eps[0]-c,eps[1]-c,eps[2]-c,eps[3],eps[4],eps[5]]
        tr_e=sum(ee[:3]); tr=sum(eps[:3])
        de=0.5*lam*tr_e**2+G*sum(x*x for x in ee); ds=0.5*M*(z-alpha*tr)**2
        pe=_f(cell['elastic_energy_j_m3_reference'],'P9 elastic density'); ps=_f(cell['biot_storage_energy_j_m3_reference'],'P9 storage density')
        state=(_close(eps[0],_f(cell['axial_strain'],'P9 strain'),atol,rtol) and all(_close(eps[k],0.,atol,rtol) for k in (1,2,3,4,5)) and _close(c,_f(cell['chemical_eigenstrain'],'P9 eigenstrain'),atol,rtol) and _close(z,_f(cell['fluid_content_increment'],'P9 fluid increment'),atol,rtol))
        if not state: raise ValueError('P9/P19 state mismatch at quadrature point '+str(i))
        if not _close(de,pe,atol,rtol): raise ValueError('elastic energy mismatch at quadrature point '+str(i))
        if not _close(ds,ps,atol,rtol): raise ValueError('Biot storage mismatch at quadrature point '+str(i))
        e19+=w*de; s19+=w*ds; e9+=w*pe; s9+=w*ps
        if chemical_energy_owner=='p9': chemical+=w*_f(cell['chemical_energy_j_m3_reference'],'P9 chemical density')
        details.append({'index':i,'weight_m3':w,'elastic_p19_j_m3':de,'elastic_p9_j_m3':pe,'storage_p19_j_m3':ds,'storage_p9_j_m3':ps})
    p19_total=_f(p19_result['stored_energy_j'],'P19 stored energy'); reconstructed=e19+s19; p9_integral=e9+s9
    if not _close(p19_total,reconstructed,atol,rtol): raise ValueError('P19 stored energy disagrees with reconstructed quadrature')
    if not _close(p9_integral,reconstructed,atol,rtol): raise ValueError('integrated P9 mechanical energy disagrees with P19')
    mechanical=p19_total if mechanical_energy_owner=='p19' else p9_integral
    return {'status':'matched_p9_p19_mechanical_energy','quadrature_points':len(cells),'p19_elastic_energy_j':e19,'p19_biot_storage_energy_j':s19,'p9_elastic_energy_integral_j':e9,'p9_biot_storage_energy_integral_j':s9,'p19_stored_energy_j':p19_total,'p9_mechanical_energy_integral_j':p9_integral,'mechanical_energy_owner':mechanical_energy_owner,'chemical_energy_owner':chemical_energy_owner,'selected_mechanical_energy_j':mechanical,'selected_chemical_energy_j':chemical,'selected_total_energy_j':mechanical+chemical,'mechanical_terms_added_once':True,'point_reports':tuple(details),'limitations':('Only matched states with zero lateral total strain are compared.','P19 has no chemical term; P9 chemical energy is separate.','External traction potential, Dirichlet reaction work, gradient energies and P10/P13 terms are excluded.','Not a common P10/P13/P19/P21 free-energy proof or physical validation.')}