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

### P27.40 — signed scalar monotonicity

- Proves the sign split for multiplication by a fixed scalar over an ordered interval: nonnegative factors are monotone and nonpositive factors are antitone.
- Provides separate left- and right-factor lemmas. The scalar dichotomy is exhaustive, including zero; equality of endpoint products at zero additionally needs the concrete multiplication's zero-annihilation law.
- The order-compatible multiplication laws remain explicit assumptions to be instantiated for a concrete ordered ring.
- This is the signed-order foundation for the four-corner theorem, **not** yet the full four-corner min/max enclosure theorem.

### P27.41 — four-corner product envelope

- Proves that every common lower bound of the four endpoint products is a lower bound for every interior product, and every common upper bound is an upper bound for every interior product.
- Derives the enclosure by applying signed scalar monotonicity successively in each interval coordinate.
- Avoids assuming a particular min/max implementation. A concrete `min4`/`max4` routine still needs separate proofs that its outputs bound all four corners.
- Uses explicit order transitivity and signed multiplication laws; no IEEE-754 or physical-model claim is made.

## Roadmap: P27.42–P27.43

1. **P27.41 — full four-corner product.** Combine signed scalar monotonicity with an explicit min/max construction to prove the global endpoint-extremum theorem, including intervals crossing zero.
2. **P27.42 — IEEE-754 refinement boundary.** Specify finite binary floating-point values, directed rounding, subnormal behavior, signed zero, and overflow/fail-closed behavior. Choose between a bit-level proof of `nextafter` and a verified refinement to exact rational bounds; tests alone are not a proof.
3. **P27.43 — certificate pipeline.** Connect polynomial and derivative enclosures to P27.36 root criteria, then define/export a certificate format and prove the checker sound. Algorithmic completeness and Python-to-Lean certificate extraction remain separate obligations.

## Open obligations and scope

- Extend P27.39 from the nonnegative quadrant to all sign combinations, including intervals crossing zero.
- Instantiate multiplication with a concrete endpoint implementation and prove its enclosure contract.
- Prove outward rounding for the actual Python `nextafter` implementation, including finite-input and overflow conditions. Underflow/subnormal and signed-zero cases need explicit treatment.
- Connect P27.35 polynomial/derivative bounds to P27.36 and P27.37 certificate construction.
- Prove algorithm-to-certificate extraction and search completeness.
- The Lean results are mathematical/software-verification results only. They do not validate the physical constitutive equations or material parameters of CCFSM.

## Build

From this directory run `lake update` once if no `lake-manifest.json` is present, then `lake build`. The dedicated GitHub Actions workflow performs both commands.
