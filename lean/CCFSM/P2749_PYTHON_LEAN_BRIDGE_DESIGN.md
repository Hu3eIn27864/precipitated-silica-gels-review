# P27.49 — Python producer / Lean checker bridge

## Current implementation facts

The current Python P27.37 producer
`MODELLING/ccfsm/ccfsm_p27_37_adaptive_polynomial_root_isolation.py` accepts
binary64 coefficients in **descending-power order** and partitions a binary64
interval. Its leaf claims are conditional on the P27.34/P27.35 interval
enclosure contracts. It deliberately leaves unresolved cases unresolved,
including tangential roots and roots on subdivision boundaries.

The Lean P27.49 polynomial core stores exact rational coefficients in
**ascending-degree order**. This difference in coefficient order must be
handled by an explicit, tested adapter; it must never be inferred from a
schema default.

## Canonical serialized representation

Proposed schema identifier: `ccfsm.root-isolation-certificate.v1`.

- Rational values are objects with decimal-string `num` and `den` fields.
- Denominator is strictly positive.
- Numerator and denominator are coprime.
- Zero is encoded uniquely as `0/1`.
- No JSON floating-point numbers appear in a proof-bearing field.
- Coefficient order is declared as `ascending_degree` in the Lean-facing
  canonical payload.
- The Python-facing adapter reads the current descending-power input and
  reverses the exact rational coefficient vector once.
- Every interval endpoint is serialized as an exact rational pair.
- Shared split points are represented by identical canonical rational pairs
  in both children and by one midpoint-evidence object in the parent node.

For an existing Python binary64 input, the producer obtains the exact dyadic
rational represented by the float via `float.as_integer_ratio()`. It must
not use `str(float)`, decimal formatting, or a rounded display value to
reconstruct the rational. This certifies the polynomial whose coefficients
are those exact binary64 values; it does not certify an unknown pre-rounded
decimal or measured coefficient.

## Tree payload

Each node records:

- exact rational `left` and `right` endpoints;
- either a leaf certificate or a split with exact rational midpoint;
- for a split, exactly one midpoint state: `root`, `no_root`, or
  `unresolved`;
- child nodes whose endpoints exactly match the parent endpoints and
  midpoint.

Leaf certificates may claim only:
- `no_root`, backed by an exact rational interval enclosure excluding zero;
- `unique_root`, backed by a derivative interval enclosure with a strict
  sign and endpoint polynomial enclosures of opposite strict signs;
- `unresolved`, which makes no count claim.

Endpoint root/no-root evidence at the outer interval bounds follows P27.48.
A midpoint root is owned by the parent split and must not also be counted as
an interior root of either child. This ownership rule is checked structurally.

## Independent checker responsibilities

The Lean checker must ignore producer-supplied conclusions and recompute:

1. rational normalization and denominator positivity;
2. coefficient-order conversion;
3. polynomial and derivative coefficients;
4. exact rational interval addition and four-corner multiplication;
5. interval Horner enclosures for the polynomial and derivative;
6. strict sign and endpoint sign-opposition conditions;
7. split coverage, midpoint identity, and endpoint ownership;
8. root/no-root/unresolved soundness and aggregate count completeness.

The checker must reject malformed quotient/remainder data once the Sturm
certificate layer is added. The P27.49 polynomial arithmetic module alone is
not yet a Sturm checker.

## Why the checker should recompute exact rational enclosures

The existing Python path uses outward-rounded binary64 interval operations.
A separate exact-rational checker can avoid trusting those operations: it
interprets the input floats as exact dyadic rationals and recomputes interval
Horner bounds over `ℚ`. If the exact enclosure is too wide to decide a leaf,
the checker returns unresolved; it must never weaken a sign condition to
force acceptance.

This is a soundness-first bridge. It may certify fewer leaves than the
floating-point producer suggests, but it cannot promote an unsupported
producer claim to a proof.

## Trust boundary and limitations

- The certificate proves a statement about the exact rational polynomial and
  exact rational interval endpoints serialized in the payload.
- It does not prove that those coefficients represent the physical silica
  constitutive model accurately.
- It does not prove a measurement-to-coefficient calibration map.
- It does not prove binary64 arithmetic refines the exact rational model.
- It does not prove the Python search algorithm is complete; completeness
  comes only from a fully resolved, coverage-certified tree.
- It does not count roots for an uncertain coefficient set. That requires a
  quantified family semantics, not a point-polynomial certificate.

## Acceptance tests

- Round-trip descending Python coefficients to ascending Lean coefficients.
- Exact binary64 dyadic conversion for positive, negative, subnormal, and
  signed-zero inputs (signed-zero payload semantics remain explicitly
  separate; rational zero canonicalizes to `0/1`).
- Reject zero or negative denominators, unreduced fractions, duplicate JSON
  keys, unknown schema versions, and JSON floating-point proof values.
- Mutate a leaf status, derivative enclosure, endpoint sign, coefficient
  order, split midpoint, and shared child endpoint; each mutation must be
  rejected or downgraded to unresolved.
- Include a simple root, two simple roots, a tangential root, a root at an
  outer endpoint, and a root exactly at an internal split point.
- Keep a valid certificate that is mathematically sound even if the
  producer's original float interval claim was wider; the checker recomputes
  the exact rational result rather than comparing untrusted display floats.

## Current status

Design only. The Python P27.37 producer is not yet a serializer for this
schema, and Lean P27.49 does not yet parse or verify these payloads.
