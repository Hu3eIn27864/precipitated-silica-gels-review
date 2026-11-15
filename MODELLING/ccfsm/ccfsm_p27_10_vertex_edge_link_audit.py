"""P27.10 local vertex- and edge-link manifold audit for tetrahedral meshes."""
from collections import defaultdict, deque
from itertools import combinations
from ccfsm_p27_9_global_incidence_audit import audit_global_tetra_mesh

def _connected(nodes, adjacency):
    if not nodes:
        return False
    seen={next(iter(nodes))}
    q=deque(seen)
    while q:
        u=q.popleft()
        for v in adjacency.get(u,()):
            if v not in seen:
                seen.add(v); q.append(v)
    return seen==set(nodes)

def _edge_link_report(edge, tets, boundary_edges):
    a,b=edge
    graph=defaultdict(set); nodes=set()
    for tet in tets:
        if a in tet and b in tet:
            opp=tuple(v for v in tet if v not in edge)
            if len(opp)!=2:
                return {"status":"invalid_link","reason":"tetrahedron_edge_opposite_pair_invalid"}
            x,y=opp; nodes.update((x,y)); graph[x].add(y); graph[y].add(x)
    if not nodes:
        return {"status":"invalid_link","reason":"empty_edge_link"}
    degrees={v:len(graph[v]) for v in nodes}
    connected=_connected(nodes,graph)
    boundary=edge in boundary_edges
    if boundary:
        valid=connected and sum(d==1 for d in degrees.values())==2 and all(d in (1,2) for d in degrees.values())
        expected="path"
    else:
        valid=connected and all(d==2 for d in degrees.values())
        expected="cycle"
    return {"status":"link_ok" if valid else "link_inconsistent",
            "kind":"boundary" if boundary else "interior",
            "expected_link":expected,"link_vertex_count":len(nodes),
            "link_edge_count":sum(degrees.values())//2,
            "degree_sequence":tuple(sorted(degrees.values())),
            "connected":connected}

def _vertex_link_report(vertex, tets, boundary_vertex):
    triangles=[]
    for tet in tets:
        if vertex in tet:
            tri=tuple(v for v in tet if v!=vertex)
            if len(tri)!=3:
                return {"status":"invalid_link","reason":"tetrahedron_vertex_opposite_face_invalid"}
            triangles.append(tuple(sorted(tri)))
    if not triangles or len(set(triangles))!=len(triangles):
        return {"status":"invalid_link","reason":"empty_or_duplicate_link_triangle"}
    edge_counts=defaultdict(int); adjacency=defaultdict(set); link_vertices=set()
    for tri in triangles:
        link_vertices.update(tri)
        for e in combinations(tri,2):
            edge=tuple(sorted(e)); edge_counts[edge]+=1
    bad=tuple(sorted(e for e,n in edge_counts.items() if n>2 or n<1))
    for i,t1 in enumerate(triangles):
        for j in range(i+1,len(triangles)):
            if len(set(t1).intersection(triangles[j]))==2:
                adjacency[i].add(j); adjacency[j].add(i)
    seen=set()
    if triangles:
        seen={0}; q=deque([0])
        while q:
            i=q.popleft()
            for j in adjacency[i]:
                if j not in seen: seen.add(j); q.append(j)
    connected=len(seen)==len(triangles)
    boundary_edges=tuple(sorted(e for e,n in edge_counts.items() if n==1))
    boundary_graph=defaultdict(set)
    for x,y in boundary_edges:
        boundary_graph[x].add(y); boundary_graph[y].add(x)
    boundary_connected=(not boundary_edges) or _connected(set(boundary_graph),boundary_graph)
    boundary_cycle=(bool(boundary_edges) and boundary_connected and
                    all(len(boundary_graph[v])==2 for v in boundary_graph))
    chi=len(link_vertices)-len(edge_counts)+len(triangles)
    if boundary_vertex:
        valid=(connected and not bad and boundary_cycle and chi==1)
        expected="triangulated_disk"
    else:
        valid=(connected and not bad and not boundary_edges and chi==2)
        expected="triangulated_sphere"
    return {"status":"link_ok" if valid else "link_inconsistent",
            "kind":"boundary" if boundary_vertex else "interior",
            "expected_link":expected,"link_vertex_count":len(link_vertices),
            "link_edge_count":len(edge_counts),"link_triangle_count":len(triangles),
            "euler_characteristic":chi,"boundary_link_edge_count":len(boundary_edges),
            "boundary_is_single_cycle":boundary_cycle if boundary_edges else False,
            "triangle_edge_connected":connected,"edge_incidence_counts":tuple(sorted(edge_counts.items())),
            "invalid_link_edges":bad}

def audit_tetra_mesh_links(vertices, tetrahedra, *, min_quality_ratio=0):
    """Run P27.9 then check every vertex link (disk/sphere) and edge link (path/cycle)."""
    base=audit_global_tetra_mesh(vertices,tetrahedra,min_quality_ratio=min_quality_ratio)
    if base.get("status")!="incidence_audited":
        return {"status":"base_audit_failed","base_audit":base,
                "full_topological_manifold_certified":False}
    tets=base["tetrahedra"]
    boundary_faces=set(base["boundary_faces"])
    boundary_edges=set()
    boundary_vertices=set()
    for face in boundary_faces:
        boundary_vertices.update(face)
        boundary_edges.update(tuple(sorted(e)) for e in combinations(face,2))
    used=sorted({v for tet in tets for v in tet})
    all_edges=sorted({tuple(sorted(e)) for tet in tets for e in combinations(tet,2)})
    vertex_links={v:_vertex_link_report(v,tets,v in boundary_vertices) for v in used}
    edge_links={e:_edge_link_report(e,tets,boundary_edges) for e in all_edges}
    bad_vertices=tuple(v for v,r in vertex_links.items() if r["status"]!="link_ok")
    bad_edges=tuple(e for e,r in edge_links.items() if r["status"]!="link_ok")
    status="locally_manifold_audited" if not bad_vertices and not bad_edges else "link_inconsistent"
    return {"status":status,"vertex_link_reports":vertex_links,"edge_link_reports":edge_links,
            "invalid_vertex_links":bad_vertices,"invalid_edge_links":bad_edges,
            "vertex_count_checked":len(used),"edge_count_checked":len(all_edges),
            "base_incidence_audit":base,
            "vertex_link_criterion":"connected triangulated 2-sphere (interior) or 2-disk (boundary), edge incidences <=2 and Euler characteristic 2 or 1",
            "edge_link_criterion":"connected cycle (interior) or path (boundary)",
            "link_tests_performed":True,
            "local_topological_manifold_conditions_passed":not bad_vertices and not bad_edges,
            "full_topological_manifold_certified":False,
            "physical_ccfsm_positivity_certified":False}
