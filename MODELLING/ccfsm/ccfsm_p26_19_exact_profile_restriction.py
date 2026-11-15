"""P26.19 exact restriction/coarsening of piecewise-quadratic cell profiles."""
from __future__ import annotations
from fractions import Fraction

def _F(value):
    if isinstance(value, Fraction): return value
    if isinstance(value, bool): raise ValueError("boolean is not a rational profile value")
    return Fraction(str(value))

def _mesh(edges, name):
    values=tuple(_F(v) for v in edges)
    if len(values)<2 or any(b<=a for a,b in zip(values,values[1:])):
        raise ValueError("%s must be strictly increasing with at least two edges" % name)
    return values

def _validate_profile(edges, means, linear, quadratic):
    e=_mesh(edges,"profile edges")
    m=tuple(_F(v) for v in means); a=tuple(_F(v) for v in linear); b=tuple(_F(v) for v in quadratic)
    n=len(e)-1
    if not (len(m)==len(a)==len(b)==n): raise ValueError("profile coefficient counts must match cells")
    return e,m,a,b

def _nested_parent_map(parent_edges, fine_edges):
    p=_mesh(parent_edges,"parent edges"); f=_mesh(fine_edges,"fine edges")
    if f[0]!=p[0] or f[-1]!=p[-1]: raise ValueError("fine mesh must cover exactly the parent domain")
    if not set(p).issubset(set(f)): raise ValueError("fine mesh must contain every parent edge")
    result=[]; j=0
    for left,right in zip(f,f[1:]):
        while j<len(p)-2 and left>=p[j+1]: j+=1
        if left<p[j] or right>p[j+1]: raise ValueError("fine cell crosses a parent-cell boundary")
        result.append(j)
    return p,f,tuple(result)

def restrict_quadratic_profile(parent_edges, means, linear, quadratic, fine_edges):
    """Restrict u=m+a*xi+b*(xi**2-1/12), xi in [-1/2,1/2], exactly."""
    p,m,a,b=_validate_profile(parent_edges,means,linear,quadratic)
    p,f,parent_of_fine=_nested_parent_map(p,fine_edges)
    fm=[]; fa=[]; fb=[]
    for left,right,j in zip(f,f[1:],parent_of_fine):
        H=p[j+1]-p[j]; h=right-left; c=(p[j]+p[j+1])/2
        d=((left+right)/2-c)/H; r=h/H
        fm.append(m[j]+a[j]*d+b[j]*(d*d+r*r/Fraction(12)-Fraction(1,12)))
        fa.append(r*(a[j]+2*b[j]*d)); fb.append(b[j]*r*r)
    return {"edges":tuple(map(str,f)),"averages":tuple(map(str,fm)),
            "linear":tuple(map(str,fa)),"quadratic":tuple(map(str,fb)),
            "parent_cell":parent_of_fine}

def _raw_moments(edges, means, linear, quadratic):
    mass=first=second=Fraction(0)
    for left,right,m,a,b in zip(edges,edges[1:],means,linear,quadratic):
        h=right-left; c=(left+right)/2
        mass+=m*h; first+=m*h*c+a*h*h/12
        second+=m*h*(c*c+h*h/12)+a*c*h*h/6+b*h**3/180
    return mass,first,second

def coarsen_quadratic_profile(parent_edges, fine_edges, fine_means, fine_linear, fine_quadratic):
    """Recover parent coefficients from child moments and test exact local restriction."""
    f,m,a,b=_validate_profile(fine_edges,fine_means,fine_linear,fine_quadratic)
    p,f,parent_of_fine=_nested_parent_map(parent_edges,f)
    n=len(p)-1; pm=[]; pa=[]; pb=[]
    for j in range(n):
        indices=[k for k,parent in enumerate(parent_of_fine) if parent==j]
        if not indices: raise ValueError("every parent cell must contain at least one fine cell")
        lo,hi=indices[0],indices[-1]+1
        if indices!=list(range(lo,hi)): raise ValueError("fine-to-parent map is not contiguous")
        M0,M1,M2=_raw_moments(f[lo:hi+1],m[lo:hi],a[lo:hi],b[lo:hi])
        H=p[j+1]-p[j]; c=(p[j]+p[j+1])/2
        mean=M0/H; lin=12*(M1-c*M0)/(H*H)
        centered_second=M2-2*c*M1+c*c*M0
        quad=180*(centered_second-M0*H*H/12)/(H**3)
        pm.append(mean); pa.append(lin); pb.append(quad)
    recovered=restrict_quadratic_profile(p,pm,pa,pb,f)
    exact=(tuple(map(str,m))==recovered["averages"] and
           tuple(map(str,a))==recovered["linear"] and tuple(map(str,b))==recovered["quadratic"])
    return {"edges":tuple(map(str,p)),"averages":tuple(map(str,pm)),
            "linear":tuple(map(str,pa)),"quadratic":tuple(map(str,pb)),
            "exact_local_restriction":exact,
            "global_moments":tuple(map(str,_raw_moments(f,m,a,b)))}

def round_trip_profile(parent_edges, means, linear, quadratic, fine_edges):
    restricted=restrict_quadratic_profile(parent_edges,means,linear,quadratic,fine_edges)
    coarsened=coarsen_quadratic_profile(parent_edges,restricted["edges"],restricted["averages"],
        restricted["linear"],restricted["quadratic"])
    original=(tuple(map(str,map(_F,means))),tuple(map(str,map(_F,linear))),tuple(map(str,map(_F,quadratic))))
    recovered=(coarsened["averages"],coarsened["linear"],coarsened["quadratic"])
    return {"restriction":restricted,"coarsening":coarsened,
            "round_trip_exact":coarsened["exact_local_restriction"] and recovered==original}
