"""P27.11 exact geometric embedding audit for tetrahedral meshes.

Detects positive-volume intersections of tetrahedron interiors with exact rational
separating-axis tests. Shared-face/edge/vertex contact is allowed. This is not a
complete audit of lower-dimensional intersections between nonincident simplices.
"""
from fractions import Fraction
from itertools import combinations
from ccfsm_p27_10_vertex_edge_link_audit import audit_tetra_mesh_links

def _sub(a,b): return tuple(x-y for x,y in zip(a,b))
def _cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def _dot(a,b): return sum(x*y for x,y in zip(a,b))
def _edges(points):
    return tuple(_sub(points[j],points[i]) for i,j in combinations(range(4),2))
def _face_normals(points):
    return tuple(_cross(_sub(points[j],points[i]),_sub(points[k],points[i]))
                 for i,j,k in combinations(range(4),3))
def _positive_interior_overlap(a,b):
    axes=list(_face_normals(a))+list(_face_normals(b))
    axes.extend(_cross(ea,eb) for ea in _edges(a) for eb in _edges(b))
    for axis in axes:
        if axis==(0,0,0): continue
        pa=tuple(_dot(axis,p) for p in a); pb=tuple(_dot(axis,p) for p in b)
        overlap=min(max(pa),max(pb))-max(min(pa),min(pb))
        if overlap<=0:
            return False
    return True

def audit_tetra_mesh_embedding(vertices,tetrahedra,*,min_quality_ratio=0):
    """Run P27.10, then exact SAT for every pair of tetrahedra."""
    base=audit_tetra_mesh_links(vertices,tetrahedra,min_quality_ratio=min_quality_ratio)
    if base.get("status")!="locally_manifold_audited":
        return {"status":"base_audit_failed","base_audit":base,
                "positive_volume_overlap_pairs":(),"exact_arithmetic":True,
                "geometric_embedding_certified":False}
    points=base["base_incidence_audit"]["vertices"]
    tets=base["base_incidence_audit"]["tetrahedra"]
    used=sorted({v for tet in tets for v in tet})
    aliases=[]
    for i,j in combinations(used,2):
        if points[i]==points[j]: aliases.append((i,j))
    overlaps=[]
    physical=[tuple(points[i] for i in tet) for tet in tets]
    for i,j in combinations(range(len(tets)),2):
        if _positive_interior_overlap(physical[i],physical[j]):
            overlaps.append((i,j))
    status="geometric_embedding_audited"
    if aliases or overlaps: status="geometric_embedding_inconsistent"
    return {
        "status":status,
        "positive_volume_overlap_pairs":tuple(overlaps),
        "coincident_distinct_vertex_pairs":tuple(aliases),
        "tetrahedron_pair_count":len(tets)*(len(tets)-1)//2,
        "tetrahedra_checked":len(tets),
        "exact_arithmetic":True,
        "separating_axis_test":"tetrahedron face normals and cross-products of all edge-direction pairs; strict positive projection overlap on every nonzero axis indicates positive-volume intersection",
        "shared_simplex_contact_allowed":True,
        "lower_dimensional_nonincident_intersections_checked":False,
        "geometric_embedding_certified":not aliases and not overlaps,
        "topological_link_audit_passed":True,
        "physical_ccfsm_positivity_certified":False,
        "base_link_audit":base
    }
