# CCFSM Lean proof kernel

This is an isolated Lean 4 project pinned to Lean **v4.35.0**. It does not change the Python implementation or the CCFSM version line.

## Formal modules

### P27.34 — outward-rounded interval addition contract

- Proves endpoint ordering and enclosure for interval addition from lower/upper scalar rounding contracts and monotonicity of exact addition.
- Provides an adapter for combining the proved addition operation with separately certified multiplication.
- The actual IEEE-754 `nextafter` functions are **not** verified by this abstract contract.

### P27.35 — Horner interval enclosure

- Coefficients are stored in descending degree order (highest degree first), matching the Python implementation.
- Proves that exact polynomial evaluation at any point in the input interval is enclosed by interval Horner evaluation, conditional on sound addition and multiplication.

### P27.36 — monotone-root theorem contract

- Proves uniqueness of an interior root from strict monotonicity.
- Existence still requires a justified intermediate-value argument; derivative-sign-to-strict-monotonicity is separate.

### P27.37 — proof-carrying root-isolation certificates

- No-root leaves carry a closed-interval exclusion proof.
- Unique-root leaves carry existence and uniqueness on the open interval.
- Unresolved leaves make no root-count claim.
- Subdivision lemmas cover the parent interval and handle split-point roots explicitly.

### P27.38 — certified interval-multiplication interface

- Introduces `SoundIntervalMultiplication`: a multiplication operation is admissible only together with a theorem enclosing every product of points from its input intervals.
- `assemble` composes this contract with P27.34 outward addition into the `IntervalArithmetic` interface consumed by P27.35.
- Separate the proof of the interface from the proof of any concrete endpoint algorithm. In particular, this module does **not** yet prove the familiar four-corner formula or its floating-point implementation.

### P27.39 — exact interval product in the nonnegative quadrant

- Proves the endpoint-product enclosure for intervals whose lower endpoints are nonnegative.
- The proof uses an explicit order-compatible multiplication law (`mul_mono_nonneg`) and proves both lower and upper enclosure bounds, plus endpoint ordering.
- This is an exact algebraic result, independent of floating-point rounding.
- It is **not** yet the full four-sign-case theorem: intervals crossing zero and intervals with negative endpoints remain open. The current result must not be applied outside its stated quadrant.

## Roadmap: P27.40–P27.42

1. **P27.40 — full four-sign-case product.** Prove the general endpoint-extremum result, including negative and zero-crossing intervals, with explicit sign cases and no floating-point assumptions.
2. **P27.41 — IEEE-754 refinement boundary.** Specify finite binary floating-point values, directed rounding, subnormal behavior, signed zero, and overflow/fail-closed behavior. Choose between a bit-level proof of `nextafter` and a verified refinement to exact rational bounds; tests alone are not a proof.
3. **P27.42 — certificate pipeline.** Connect polynomial and derivative enclosures to P27.36 root criteria, then define/export a certificate format and prove the checker sound. Algorithmic completeness and Python-to-Lean certificate extraction remain separate obligations.

## Open obligations and scope

- Extend P27.39 from the nonnegative quadrant to all sign combinations, including intervals crossing zero.
- Instantiate multiplication with a concrete endpoint implementation and prove its enclosure contract.
- Prove outward rounding for the actual Python `nextafter` implementation, including finite-input and overflow conditions. Underflow/subnormal and signed-zero cases need explicit treatment.
- Connect P27.35 polynomial/derivative bounds to P27.36 and P27.37 certificate construction.
- Prove algorithm-to-certificate extraction and search completeness.
- The Lean results are mathematical/software-verification results only. They do not validate the physical constitutive equations or material parameters of CCFSM.

## Build

From this directory run `lake update` once if no `lake-manifest.json` is present, then `lake build`. The dedicated GitHub Actions workflow performs both commands.
