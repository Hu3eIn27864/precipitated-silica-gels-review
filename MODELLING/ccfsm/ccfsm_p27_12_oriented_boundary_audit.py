"""P27.12 exact oriented-boundary audit for tetrahedral meshes.

Checks induced boundary-face orientation, closed edge incidence, connected
boundary components, Euler characteristics and exact signed-volume balance.
This does not test boundary self-intersections or physical CCFSM positivity.
"""
from collections import defaultdict, deque
from itertools import combinations
from fractions import Fraction
from ccfsm_p27_11_geometric_embedding_audit import audit_tetra_mesh_embedding


def _sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def _dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def _det(a, b, c):
    return _dot(a, _cross(b, c))


def _tet_six_volume(points):
    a, b, c, d = points
    return _det(_sub(b, a), _sub(c, a), _sub(d, a))


def _face_six_volume(points, face):
    a, b, c = (points[i] for i in face)
    return _det(a, b, c)


def _connected(nodes, adjacency):
    if not nodes:
        return False
    seen = {next(iter(nodes))}
    queue = deque(seen)
    while queue:
        u = queue.popleft()
        for v in adjacency.get(u, ()):
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return seen == set(nodes)


def audit_tetra_mesh_boundary(vertices, tetrahedra, *, min_quality_ratio=0):
    """Run P27.11 and audit the exact oriented boundary chain."""
    embedding = audit_tetra_mesh_embedding(
        vertices, tetrahedra, min_quality_ratio=min_quality_ratio)
    if embedding.get("status") != "geometric_embedding_audited":
        return {"status": "base_audit_failed", "base_audit": embedding,
                "boundary_orientation_certified": False,
                "closed_boundary_certified": False}

    base = embedding["base_link_audit"]["base_incidence_audit"]
    points = base["vertices"]
    tets = base["tetrahedra"]
    oriented_faces = []
    for tet in tets:
        a, b, c, d = tet
        oriented_faces.extend(((b, c, d), (a, d, c), (a, b, d), (a, c, b)))

    face_counts = defaultdict(int)
    for face in oriented_faces:
        face_counts[tuple(sorted(face))] += 1
    boundary = [face for face in oriented_faces
                if face_counts[tuple(sorted(face))] == 1]
    # Every boundary edge of a closed oriented 2-manifold occurs twice,
    # once in each direction.
    edge_directions = defaultdict(list)
    for face in boundary:
        for u, v in ((face[0], face[1]), (face[1], face[2]),
                     (face[2], face[0])):
            key = tuple(sorted((u, v)))
            edge_directions[key].append(1 if (u, v) == key else -1)

    open_edges = tuple(sorted(e for e, inc in edge_directions.items()
                              if len(inc) == 1))
    overfull_edges = tuple(sorted(e for e, inc in edge_directions.items()
                                  if len(inc) > 2))
    orientation_conflicts = tuple(sorted(
        e for e, inc in edge_directions.items()
        if len(inc) == 2 and sum(inc) != 0))
    underfull_edges = tuple(sorted(e for e, inc in edge_directions.items()
                                   if len(inc) == 0))
    closed = not (open_edges or overfull_edges or orientation_conflicts or underfull_edges)

    # Boundary triangles are connected when sharing an edge.
    face_adjacency = defaultdict(set)
    edge_to_faces = defaultdict(list)
    for i, face in enumerate(boundary):
        for edge in combinations(face, 2):
            edge_to_faces[tuple(sorted(edge))].append(i)
    for ids in edge_to_faces.values():
        for i, j in combinations(ids, 2):
            face_adjacency[i].add(j)
            face_adjacency[j].add(i)
    components = []
    seen = set()
    for start in range(len(boundary)):
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        comp = []
        while queue:
            i = queue.popleft()
            comp.append(i)
            for j in face_adjacency[i]:
                if j not in seen:
                    seen.add(j)
                    queue.append(j)
        components.append(tuple(sorted(comp)))

    component_reports = []
    for comp_id, ids in enumerate(components):
        faces = [boundary[i] for i in ids]
        verts = {v for face in faces for v in face}
        edges = {tuple(sorted(e)) for face in faces for e in combinations(face, 2)}
        chi = len(verts) - len(edges) + len(faces)
        six_volume = sum((_face_six_volume(points, f) for f in faces), Fraction(0))
        genus_numerator = 2 - chi
        genus = genus_numerator // 2 if genus_numerator >= 0 and genus_numerator % 2 == 0 else None
        component_reports.append({
            "component_index": comp_id,
            "triangle_count": len(faces),
            "vertex_count": len(verts),
            "edge_count": len(edges),
            "euler_characteristic": chi,
            "orientable_closed_surface_genus_from_euler": genus,
            "signed_volume": six_volume / 6,
            "signed_six_volume": six_volume,
        })

    boundary_six_volume = sum(
        (_face_six_volume(points, face) for face in boundary), Fraction(0))
    tetra_six_volume = sum(
        (_tet_six_volume(tuple(points[i] for i in tet)) for tet in tets),
        Fraction(0))
    volume_balance = boundary_six_volume == tetra_six_volume
    euler_ok = all(r["orientable_closed_surface_genus_from_euler"] is not None
                   for r in component_reports) if closed else False
    orientation_ok = closed and not orientation_conflicts
    consistent = closed and orientation_ok and euler_ok and volume_balance
    return {
        "status": "oriented_boundary_audited" if consistent else "boundary_inconsistent",
        "boundary_triangle_count": len(boundary),
        "boundary_edge_count": len(edge_directions),
        "boundary_component_count": len(components),
        "boundary_components": tuple(component_reports),
        "open_boundary_edges": open_edges,
        "overfull_boundary_edges": overfull_edges,
        "boundary_edge_orientation_conflicts": orientation_conflicts,
        "closed_boundary": closed,
        "boundary_orientation_consistent": orientation_ok,
        "component_euler_checks_passed": euler_ok,
        "boundary_signed_volume": boundary_six_volume / 6,
        "tetrahedron_signed_volume_sum": tetra_six_volume / 6,
        "exact_volume_balance": volume_balance,
        "volume_balance_residual": (boundary_six_volume-tetra_six_volume) / 6,
        "exact_arithmetic": True,
        "boundary_self_intersection_checked": False,
        "lower_dimensional_nonincident_intersections_checked": False,
        "physical_ccfsm_positivity_certified": False,
        "geometric_embedding_audit": embedding,
    }
