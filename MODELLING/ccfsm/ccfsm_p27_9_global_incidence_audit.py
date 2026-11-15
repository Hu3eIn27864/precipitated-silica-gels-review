"""P27.9 global tetrahedral mesh incidence audit (exact orientation via P27.8)."""
from collections import defaultdict, deque
from itertools import combinations
from ccfsm_p27_8_tetra_geometry_audit import normalize_and_audit_tetra_mesh

def _parity_to_sorted(face):
    inv=sum(face[i]>face[j] for i in range(3) for j in range(i+1,3))
    return -1 if inv%2 else 1

def audit_global_tetra_mesh(vertices, tetrahedra, *, min_quality_ratio=0):
    """Audit face/edge/vertex incidence; deliberately not a full link-manifold proof."""
    try:
        raw=tuple(tuple(t) for t in tetrahedra)
        if not raw:
            return {"status":"invalid","reason":"tetrahedra_must_be_nonempty"}
        canonical=[tuple(sorted(t)) for t in raw if len(t)==4]
        if len(canonical)!=len(raw):
            return {"status":"invalid","reason":"invalid_tetrahedron_connectivity"}
        if len(set(canonical))!=len(canonical):
            return {"status":"invalid","reason":"duplicate_tetrahedron"}
        geom=normalize_and_audit_tetra_mesh(vertices,raw,min_quality_ratio=min_quality_ratio)
        if geom["status"]!="oriented_quality_audited":
            return {"status":geom["status"],"reason":geom.get("reason"),"element_index":geom.get("element_index"),"geometry_audit":geom}
        tets=geom["tetrahedra"]
        faces=defaultdict(list); edges=defaultdict(set); used=set()
        for ti,(a,b,c,d) in enumerate(tets):
            used.update((a,b,c,d))
            # Boundary orientation induced by the positive tetrahedron orientation.
            oriented=((b,c,d),(a,d,c),(a,b,d),(a,c,b))
            for face in oriented:
                key=tuple(sorted(face))
                faces[key].append((ti,_parity_to_sorted(face)))
            for edge in combinations((a,b,c,d),2):
                edges[tuple(sorted(edge))].add(ti)
        overfull=tuple(sorted(f for f,inc in faces.items() if len(inc)>2))
        boundary=tuple(sorted(f for f,inc in faces.items() if len(inc)==1))
        interior=tuple(sorted(f for f,inc in faces.items() if len(inc)==2))
        orientation_conflicts=tuple(sorted(f for f,inc in faces.items() if len(inc)==2 and inc[0][1]==inc[1][1]))
        adjacency=[set() for _ in tets]
        for face,inc in faces.items():
            if len(inc)==2:
                i,j=inc[0][0],inc[1][0]; adjacency[i].add(j); adjacency[j].add(i)
        components=[]; seen=set()
        for start in range(len(tets)):
            if start in seen: continue
            q=deque([start]); seen.add(start); comp=[]
            while q:
                i=q.popleft(); comp.append(i)
                for j in sorted(adjacency[i]):
                    if j not in seen: seen.add(j); q.append(j)
            components.append(tuple(sorted(comp)))
        edge_face_counts=defaultdict(int)
        for f in faces:
            for e in combinations(f,2): edge_face_counts[tuple(sorted(e))]+=1
        isolated=tuple(i for i in range(len(geom["vertices"])) if i not in used)
        status="incidence_audited"
        if overfull or orientation_conflicts:
            status="incidence_inconsistent"
        return {
            "status":status,"vertices":geom["vertices"],"tetrahedra":tets,
            "boundary_faces":boundary,"interior_faces":interior,
            "face_incidence_counts":tuple(sorted((f,len(inc)) for f,inc in faces.items())),
            "nonmanifold_face_candidates":overfull,
            "interior_face_orientation_conflicts":orientation_conflicts,
            "edge_tetrahedron_incidence_counts":tuple(sorted((e,len(inc)) for e,inc in edges.items())),
            "edge_face_incidence_counts":tuple(sorted(edge_face_counts.items())),
            "vertex_tetrahedron_incidence_counts":tuple(sorted((v,sum(v in t for t in tets)) for v in used)),
            "isolated_vertex_indices":isolated,
            "face_connected_components":tuple(components),
            "component_count":len(components),
            "boundary_face_count":len(boundary),"interior_face_count":len(interior),
            "exact_geometry_audit":True,"full_topological_manifold_certified":False,
            "vertex_and_edge_link_tests_performed":False,
            "physical_ccfsm_positivity_certified":False
        }
    except (TypeError,ValueError,KeyError,IndexError):
        return {"status":"invalid","reason":"malformed_mesh_data"}
