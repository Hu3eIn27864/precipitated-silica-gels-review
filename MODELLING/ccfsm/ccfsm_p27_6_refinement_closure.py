"""P27.6 conservative face-connected refinement-depth closure.

This computes a compatible target depth field; it does NOT generate tetrahedra.
All tetrahedra in a face-connected component are promoted to that component's
maximum requested depth. P27.5 remains the independent geometric audit.
"""
from collections import defaultdict
from itertools import combinations


def close_tetra_refinement_depths(
    tetrahedra,
    requested_depths,
    *,
    max_refinement_depth=8,
    max_total_leaf_tetrahedra=1_000_000,
):
    """Return a conservative face-neighbour closure of requested red depths."""
    try:
        tets = tuple(tuple(t) for t in tetrahedra)
        depths = tuple(requested_depths)
        if not tets or len(depths) != len(tets):
            return {"status": "invalid", "reason": "mesh_and_depths_must_be_nonempty_and_aligned"}
        if isinstance(max_refinement_depth, bool) or not isinstance(max_refinement_depth, int) or max_refinement_depth < 0:
            return {"status": "invalid", "reason": "invalid_max_refinement_depth"}
        if isinstance(max_total_leaf_tetrahedra, bool) or not isinstance(max_total_leaf_tetrahedra, int) or max_total_leaf_tetrahedra < 1:
            return {"status": "invalid", "reason": "invalid_leaf_element_cap"}
        clean = []
        for tet in tets:
            if len(tet) != 4 or len(set(tet)) != 4:
                return {"status": "invalid", "reason": "invalid_tetrahedron_connectivity"}
            if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in tet):
                return {"status": "invalid", "reason": "vertex_indices_must_be_nonnegative_integers"}
            clean.append(tet)
        clean_depths = []
        for d in depths:
            if isinstance(d, bool) or not isinstance(d, int) or d < 0:
                return {"status": "invalid", "reason": "requested_depths_must_be_nonnegative_integers"}
            if d > max_refinement_depth:
                return {"status": "unresolved", "reason": "requested_depth_exceeds_cap", "requested_depth": d, "max_refinement_depth": max_refinement_depth}
            clean_depths.append(d)
        face_owners = defaultdict(list)
        for ei, tet in enumerate(clean):
            for face in combinations(tet, 3):
                face_owners[tuple(sorted(face))].append(ei)
        nonmanifold = tuple(face for face, owners in face_owners.items() if len(owners) > 2)
        if nonmanifold:
            return {"status": "invalid", "reason": "nonmanifold_coarse_face", "faces": nonmanifold}
        adjacency = [set() for _ in clean]
        for owners in face_owners.values():
            if len(owners) == 2:
                a, b = owners
                adjacency[a].add(b)
                adjacency[b].add(a)
        components = []
        seen = set()
        for root in range(len(clean)):
            if root in seen:
                continue
            stack = [root]
            seen.add(root)
            component = []
            while stack:
                node = stack.pop()
                component.append(node)
                for nxt in sorted(adjacency[node], reverse=True):
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            components.append(tuple(sorted(component)))
        closed = list(clean_depths)
        component_records = []
        for component in components:
            target = max(clean_depths[i] for i in component)
            for i in component:
                closed[i] = target
            component_records.append({
                "elements": component,
                "target_depth": target,
                "promoted_elements": tuple(i for i in component if clean_depths[i] < target),
            })
        predicted = sum(8 ** d for d in closed)
        if predicted > max_total_leaf_tetrahedra:
            return {
                "status": "unresolved",
                "reason": "predicted_leaf_element_cap_exceeded",
                "predicted_leaf_tetrahedra": predicted,
                "max_total_leaf_tetrahedra": max_total_leaf_tetrahedra,
                "closed_depths": tuple(closed),
                "components": tuple(component_records),
                "mesh_modified": False,
            }
        promoted = tuple(i for i, (old, new) in enumerate(zip(clean_depths, closed)) if new > old)
        shared_faces = sum(1 for owners in face_owners.values() if len(owners) == 2)
        return {
            "status": "closed",
            "closure_scope": "uniform_maximum_depth_per_face_connected_component",
            "requested_depths": tuple(clean_depths),
            "closed_depths": tuple(closed),
            "promoted_elements": promoted,
            "components": tuple(component_records),
            "shared_coarse_faces": shared_faces,
            "predicted_leaf_tetrahedra": predicted,
            "mesh_modified": False,
            "requires_p27_5_post_refinement_audit": True,
        }
    except (TypeError, ValueError):
        return {"status": "invalid", "reason": "malformed_mesh_or_depth_data"}
