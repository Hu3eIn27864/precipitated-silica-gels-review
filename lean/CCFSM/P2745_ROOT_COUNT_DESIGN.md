# P27.45 — explicit root witnesses and count certificates

## Implemented first layer

P27.37 now uses a Type-level `UniqueRootEvidence` structure with:
- a concrete witness coordinate;
- proof that the coordinate is an interior root;
- proof that every other interior root equals that witness.

P27.45 defines:
- `splitPointWitnesses`: a midpoint contributes only when its evidence is `root`;
- `certifiedRootWitnesses`: recursively collects witnesses from unique leaves and certified midpoint roots; unresolved/no-root nodes contribute none;
- `splitPointWitnesses_sound`: each midpoint witness equals that midpoint and is a root;
- `certifiedRootWitnesses_sound`: every collected witness is a root in the open parent interval.

The parent-domain proof explicitly requires transitivity of the strict order:
`lt_transitive : ∀ {a b c}, a < b → b < c → a < c`.
This is a mathematical contract, not an assumption silently inferred from the bare `LT` typeclass.

## Not yet proved

The list collector establishes validity of every emitted witness, but it does not yet prove pairwise distinctness. In particular, list length must not yet be interpreted as a root count.

The next theorem must prove:
1. every left-subtree witness is strictly below the split point;
2. every right-subtree witness is strictly above it;
3. a certified midpoint appears once at the split node and never in either child;
4. each child collector has no duplicates by induction;
5. therefore the concatenated collector has no duplicates.

Only then is its length a sound lower bound on the number of distinct roots.

A finite upper bound requires still stronger evidence: every outer endpoint and every split point must have root/no-root evidence; unique leaves must exclude endpoint roots; no unresolved nodes may remain. P27.44's `FullyResolved` is currently only structural and is not sufficient by itself.

## Tangencies

Strict-derivative monotonicity appropriately leaves intervals containing derivative zeros unresolved. Tangential/even-multiplicity roots need a complementary exact method. A rational Sturm-sequence certificate is under evaluation for rational/dyadic polynomial coefficients, with explicit endpoint-root handling.

## Verification state

P27.45 now contains the explicit Type-level unique-root witness, recursive midpoint/leaf witness collector, a theorem that every collected witness is a root in the open parent interval, and a custom duplicate-free list predicate with a recursive proof that the collector has no duplicate coordinates. The Lean build for this collector and distinctness theorem passed (run 43795801299). A further theorem packages the collector length as a lower bound on the number of distinct interior roots; its Lean run is pending and is not yet claimed as compiled.

This module certifies mathematical polynomial roots only. It does not validate noisy measurements, physical input enclosures, or CCFSM constitutive laws.
