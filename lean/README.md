# CCFSM Lean proof kernel

This is an isolated Lean 4 project pinned to Lean **v4.35.0**. It does not change the Python implementation or the CCFSM version line.

## What is proved

### P27.34 — outward-rounded interval addition contract

- Define lower/upper scalar rounding operations and state their enclosure obligations.
- Prove that endpoint-wise interval addition preserves endpoint ordering and encloses every sum of points from the input intervals, assuming monotonicity of exact addition.
- The actual IEEE-754 `nextafter` functions are **not** verified by this abstract contract; proving their finite-input rounding properties and overflow policy remains open.


### P27.35 — Horner interval enclosure contract

- Coefficient lists are explicitly stored in descending degree order (highest-degree coefficient first), matching the Python P27.35 implementation.
- Exact scalar Horner evaluation and interval Horner evaluation are defined using `x * rest + coefficient`.
- The theorem `CCFSM.P2735.hornerInterval_sound` proves that, for every point contained in the input interval, the exact polynomial value is contained in the interval-Horner result.
- The theorem is conditional only on the soundness contracts of interval addition and multiplication supplied by an `IntervalArithmetic` implementation.

**Important boundary:** this proves the generic enclosure theorem, not the soundness of a concrete endpoint implementation. Concrete lower/upper endpoint formulas, IEEE-754 outward rounding, and the Python one-ULP widening still require separate proofs and tests. The current theorem must not be cited as a verification of floating-point arithmetic.

### P27.36 — monotone-root theorem contract

- Formalize strict monotonicity on an open interval and prove that two roots in that interval must coincide.
- The theorem is the uniqueness half of P27.36. Existence still requires a separately justified intermediate-value argument; derivative-sign-to-strict-monotonicity is also a separate obligation.

### P27.37 — proof-carrying root-isolation certificates

- A no-root leaf certificate carries a proof that the predicate has no root anywhere on its closed interval.
- A unique-root leaf certificate carries an existence-and-uniqueness proof for exactly one root in the open interval.
- An unresolved leaf carries no root-count claim.
- The subdivision lemmas prove closed-child coverage and explicitly identify a root at the split point as a boundary case, rather than counting it as an interior root of both children.

## Remaining proof obligations

- Instantiate interval addition and multiplication with concrete endpoint arithmetic and prove their enclosure contracts.
- Prove outward rounding for the actual floating-point implementation (P27.34); the Python one-ULP widening is not assumed correct by the Lean kernel.
- Connect P27.35 interval bounds to the derivative/endpoint criteria in P27.36 and then to certificate construction in P27.37.
- Prove algorithm-to-certificate extraction and completeness of the Python search.
- Physical validity of CCFSM constitutive equations remains a separate empirical question and is not implied by these formal proofs.

## Build

From this directory run `lake update` once if no `lake-manifest.json` is present, then `lake build`. The dedicated GitHub Actions workflow performs both commands.
