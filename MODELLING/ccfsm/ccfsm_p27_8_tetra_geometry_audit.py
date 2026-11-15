"""P27.8 exact tetrahedral orientation normalization and shape-quality audit.
Uses exact rational determinants and Q=432 det(E)^2/(sum six edge lengths squared)^3.
Q=1 for a regular tetrahedron and Q=0 for a degenerate one.
"""
from fractions import Fraction
from itertools import combinations

def _f(x):
    return x if isinstance(x, Fraction) else Fraction(x)

def _sub(a, b):
    return tuple(x-y for x,y in zip(a,b))

def _norm2(a):
    return sum(x*x for x in a)

def _det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))

def tetrahedron_geometry(vertices, tet):
    p=tuple(vertices[i] for i in tet)
    e=tuple(_sub(p[i],p[0]) for i in (1,2,3))
    det=_det3(*e)
    s=sum(_norm2(_sub(p[i],p[j])) for i,j in combinations(range(4),2))
    q=Fraction(0) if s==0 else Fraction(432)*det*det/(s**3)
    return {"signed_six_volume":det,"quality_ratio":q}

def normalize_and_audit_tetra_mesh(vertices,tetrahedra,*,min_quality_ratio=Fraction(0)):
    try:
        points=tuple(tuple(_f(x) for x in p) for p in vertices)
        tets=tuple(tuple(t) for t in tetrahedra)
        threshold=_f(min_quality_ratio)
        if not points or any(len(p)!=3 for p in points):
            return {"status":"invalid","reason":"vertices_must_be_nonempty_3d"}
        if threshold<0 or threshold>1:
            return {"status":"invalid","reason":"quality_threshold_out_of_range"}
        if not tets or any(len(t)!=4 or len(set(t))!=4 or any(isinstance(i,bool) or not isinstance(i,int) or i<0 or i>=len(points) for i in t) for t in tets):
            return {"status":"invalid","reason":"invalid_tetrahedron_connectivity"}
        normalized=[]; qualities=[]; flips=[]
        for index,tet in enumerate(tets):
            g=tetrahedron_geometry(points,tet); det=g["signed_six_volume"]; q=g["quality_ratio"]
            if det==0:
                return {"status":"invalid","reason":"degenerate_tetrahedron","element_index":index}
            if det<0:
                tet=(tet[0],tet[2],tet[1],tet[3]); flips.append(index)
            g=tetrahedron_geometry(points,tet)
            if g["signed_six_volume"]<=0:
                return {"status":"invalid","reason":"orientation_normalization_failed","element_index":index}
            normalized.append(tet); qualities.append(q)
        qmin=min(qualities)
        if qmin<threshold:
            return {"status":"quality_below_threshold","reason":"minimum_shape_quality_below_requested_limit","minimum_quality_ratio":qmin,"requested_minimum_quality_ratio":threshold,"element_quality_ratios":tuple(qualities),"negative_orientation_flips":tuple(flips)}
        return {"status":"oriented_quality_audited","vertices":points,"tetrahedra":tuple(normalized),"negative_orientation_flips":tuple(flips),"element_signed_six_volumes":tuple(tetrahedron_geometry(points,t)["signed_six_volume"] for t in normalized),"element_quality_ratios":tuple(qualities),"minimum_quality_ratio":qmin,"maximum_quality_ratio":max(qualities),"quality_metric":"432*det(E)^2/(sum_of_six_squared_edge_lengths)^3","quality_metric_regular_tetrahedron":Fraction(1),"quality_metric_degenerate_limit":Fraction(0),"exact_arithmetic":True,"quality_threshold_applied":threshold,"physical_positivity_certified":False}
    except (TypeError,ValueError,ZeroDivisionError,IndexError):
        return {"status":"invalid","reason":"malformed_mesh_or_quality_data"}