"""P27.5 exact conformity audit for adaptively subdivided tetrahedral meshes."""
from fractions import Fraction as F
from collections import defaultdict
from itertools import combinations

EDGES=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
IDENTITY=tuple(tuple(F(int(i==j)) for j in range(4)) for i in range(4))

def _f(x): return x if isinstance(x,F) else F(x)
def _mid(a,b): return tuple((x+y)/2 for x,y in zip(a,b))
def _children(v):
    m={e:_mid(v[e[0]],v[e[1]]) for e in EDGES}
    return ((v[0],m[0,1],m[0,2],m[0,3]),(v[1],m[0,1],m[1,2],m[1,3]),
            (v[2],m[0,2],m[1,2],m[2,3]),(v[3],m[0,3],m[1,3],m[2,3]),
            (m[0,1],m[0,2],m[0,3],m[2,3]),(m[0,1],m[0,3],m[1,3],m[2,3]),
            (m[0,1],m[1,3],m[1,2],m[2,3]),(m[0,1],m[1,2],m[0,2],m[2,3]))
def _point(vertices,bary):
    return tuple(sum(_f(bary[i])*_f(vertices[i][d]) for i in range(4)) for d in range(3))
def _face_key(indices): return tuple(sorted(indices))
def _triangle_key(points): return tuple(sorted(tuple(_f(x) for x in p) for p in points))

def audit_tetra_mesh_face_conformity(vertices,tetrahedra,certificates):
    """Compare exact induced triangulations on every shared coarse face.
    certificates maps element index to complete P27.3 results with leaf_records.
    """
    try:
        points=tuple(tuple(_f(x) for x in p) for p in vertices)
        if any(len(p)!=3 for p in points): return {"status":"invalid","reason":"vertices_must_be_3d"}
        tets=tuple(tuple(int(i) for i in t) for t in tetrahedra)
        if any(len(t)!=4 or len(set(t))!=4 or min(t)<0 or max(t)>=len(points) for t in tets):
            return {"status":"invalid","reason":"invalid_tetrahedron_connectivity"}
        owners=defaultdict(list)
        for ei,tet in enumerate(tets):
            for face in combinations(tet,3): owners[_face_key(face)].append(ei)
        nonmanifold=tuple(f for f,o in owners.items() if len(o)>2)
        if nonmanifold: return {"status":"invalid","reason":"nonmanifold_coarse_face","faces":nonmanifold}
        induced={}
        for ei,tet in enumerate(tets):
            cert=certificates[ei]
            if cert.get("status") not in ("certified_nonnegative","unresolved"):
                return {"status":"invalid","reason":"certificate_has_no_complete_leaf_partition","element":ei}
            records=cert.get("leaf_records")
            if not isinstance(records,(tuple,list)) or not records:
                return {"status":"invalid","reason":"missing_leaf_geometry","element":ei}
            physical=tuple(points[i] for i in tet)
            for lf in combinations(range(4),3):
                gf=_face_key(tuple(tet[i] for i in lf))
                if len(owners[gf])!=2: continue
                opposite=next(i for i in range(4) if i not in lf)
                tris=[]
                for rec in records:
                    bary=rec.get("barycentric_vertices")
                    if not isinstance(bary,(tuple,list)) or len(bary)!=4:
                        return {"status":"invalid","reason":"malformed_leaf_geometry","element":ei}
                    p=tuple(_point(physical,v) for v in bary)
                    for leaf_face in combinations(range(4),3):
                        if all(_f(bary[i][opposite])==0 for i in leaf_face):
                            tris.append(_triangle_key(tuple(p[i] for i in leaf_face)))
                if not tris: return {"status":"invalid","reason":"no_induced_face_triangles","element":ei,"face":gf}
                induced[(ei,gf)]=tuple(sorted(tris))
        mismatches=[]; checked=0
        for face,adj in owners.items():
            if len(adj)!=2: continue
            a,b=adj; ta=induced.get((a,face)); tb=induced.get((b,face))
            if ta is None or tb is None:
                return {"status":"invalid","reason":"missing_neighbor_face_partition","face":face}
            checked+=1
            if ta!=tb: mismatches.append({"face":face,"element_a":a,"element_b":b,"triangles_a":ta,"triangles_b":tb})
        if mismatches: return {"status":"nonconforming","checked_shared_faces":checked,"mismatch_count":len(mismatches),"mismatches":tuple(mismatches)}
        return {"status":"conforming","checked_shared_faces":checked,"mismatch_count":0}
    except (KeyError,TypeError,ValueError,ZeroDivisionError,IndexError):
        return {"status":"invalid","reason":"malformed_mesh_or_certificate"}