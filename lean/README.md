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

### P27.42 — concrete four-corner extrema

- Defines a dependency-light comparison tree `min4`/`max4` for the four endpoint products.
- Proves that the computed minimum is below all four corners and the computed maximum is above all four corners.
- Combines those lemmas with P27.41 to prove a concrete exact-arithmetic interval-product enclosure for arbitrary sign combinations, including zero-crossing intervals.
- Adds an exactIntervalMultiply operation on the P27.35 interval type and an adapter that packages its enclosure proof as the P27.38 SoundIntervalMultiplication contract. Membership in both input intervals supplies the required endpoint-order proofs.\n- Requires a decidable total order and transitive order relation. This adapter is exact algebra on the abstract endpoint type; it does **not** establish IEEE-754 directed rounding.

## P27.43 — exact-rational interval certificate prototype\n\n### P27.43 — IEEE-754 boundary and rational certificate prototype

- The design obligations for finite binary64 values, nextafter, signed zero, subnormals, and overflow are recorded in CCFSM/P2743_IEEE754_DESIGN.md.
- A Python-side independent checker now verifies add, mul, and div interval certificates by recomputing the exact real range from the supplied binary64 endpoints as dyadic rationals.
- This is an exact-rational software checker, not yet a Lean proof of Python/IEEE-754 refinement. It does not verify expression provenance, external input soundness, or signed-zero bit semantics.
- Ten focused unit tests exercise sign combinations, zero crossings, subnormal products, division domains, malformed certificates, and rejection of unsound enclosures. An integration test runs the current P27.34 interval operations through the independent checker.\n\n### P27.44 — proof-carrying root-partition tree

- Formal module: CCFSM/P2744.lean. It defines a dependent tree indexed by exact closed interval endpoints, with proof-carrying leaf certificates and separate midpoint evidence (no-root, root, unresolved).
- Proves closed-domain coverage: every point in the parent interval follows a certified left or right child path. Proves recursively that all leaf and midpoint claims satisfy their declared logical contracts.
- FullyResolved is only a structural flag excluding unresolved nodes. Aggregate root-count bounds, outer-endpoint ownership, serialized certificates and a producer-to-checker provenance link remain open.
- Detailed design and acceptance gates: CCFSM/P2744_CERTIFICATE_PIPELINE_DESIGN.md.

### P27.45 — explicit root witnesses and count bounds

- Design note: CCFSM/P2745_ROOT_COUNT_DESIGN.md.
- Next formal step is to make unique-root witnesses explicit Type-level data, collect them through the P27.44 tree, prove pairwise distinctness, and derive sound lower and finite upper root-count bounds.
- Tangencies and even-multiplicity roots remain unresolved by strict-derivative monotonicity; compare an exact rational Sturm-sequence certificate as a complementary method.

## Roadmap: P27.44

1. **P27.43 — IEEE-754 refinement boundary.** Specify finite binary floating-point values, directed rounding, subnormal behavior, signed zero, and overflow/fail-closed behavior. Choose between a bit-level proof of `nextafter` and a verified refinement to exact rational bounds; tests alone are not a proof.
2. **P27.44 — certificate pipeline.** Connect polynomial and derivative enclosures to P27.36 root criteria, then define/export a certificate format and prove the checker sound. Algorithmic completeness and Python-to-Lean certificate extraction remain separate obligations.

### P27.45 — explicit root witnesses and count certificates

- Implementation: `CCFSM/P2745.lean`; design and proof obligations: `CCFSM/P2745_ROOT_COUNT_DESIGN.md`.
- Proved: every collected witness is a genuine root in the parent open interval, and the collector is duplicate-free by strict child-interval separation plus unique midpoint ownership (Lean run 43795801299).
- Added: `HasAtLeastDistinctInteriorRoots` and a lower-bound theorem equating the number of collected witnesses with an explicit lower bound. This extra packaging is awaiting its latest Lean CI run.
- Finite upper bounds additionally require outer endpoint and split-point evidence and no unresolved nodes.

## Open obligations and scope

- Connect the exact comparison-tree operation to a concrete numeric representation and instantiate its order and multiplication laws.
- Prove outward rounding for the actual floating-point endpoint operations.
- Prove outward rounding for the actual Python `nextafter` implementation, including finite-input and overflow conditions. Underflow/subnormal and signed-zero cases need explicit treatment.
- Connect P27.35 polynomial/derivative bounds to P27.36 and P27.37 certificate construction.
- Prove algorithm-to-certificate extraction and search completeness.
- The Lean results are mathematical/software-verification results only. They do not validate the physical constitutive equations or material parameters of CCFSM.

## Build

From this directory run `lake update` once if no `lake-manifest.json` is present, then `lake build`. The dedicated GitHub Actions workflow performs both commands.

### P27.45 — explicit root witnesses and lower bounds

- Stores a concrete coordinate in each unique-root certificate and recursively collects unique-leaf and certified midpoint witnesses.
- Proves every collected witness is an interior root and proves the collector is duplicate-free using strict separation of child intervals.
- Consequently, the collector length is a sound lower bound on the number of distinct interior roots.
- Lean CI: run 43795945691, 14 targets.

### P27.46 — completeness of fully resolved root partitions

- Adds the converse direction: if the partition tree is fully resolved, every interior root of the parent interval must occur in the witness collector.
- Combines completeness with P27.45 soundness to prove membership equivalence between the witness list and all interior roots.
- Defines an exact root-count certificate as the witness-list length plus that membership equivalence. The exact count is conditional on explicit strict-to-nonstrict order conversion and trichotomy.
- Does not yet prove that a practical floating-point/Python producer can construct the required evidence. Endpoint roots remain excluded from the *interior* count and require separate reporting if a closed-interval count is desired.
- Tangential/multiple roots still require a method beyond strict-derivative monotonicity, e.g. exact Sturm certificates.

### P27.46 — exact interior root count from fully resolved trees

- Formal module: `CCFSM/P2746.lean`.
- Adds the converse to P27.45: every interior root in a fully resolved tree must be represented by a collected witness.
- The exact-count proposition includes all three necessary parts: witness-list length, pairwise distinctness, and equivalence between list membership and the interior-root predicate.
- Requires explicit strict-order trichotomy and strict-to-nonstrict conversion. The count is for the open interval; endpoint roots are intentionally separate.
- - Lean CI passed: run 43798130936; all 15 targets built, including CCFSM.P2746.

### P27.47 — Sturm certificates for tangential and multiple roots

- Design only: `CCFSM/P2747_STURM_CERTIFICATE_DESIGN.md`.
- Specifies rational signed-remainder certificates, exact endpoint one-sided signs, and open-interval variation counts.
- Intended to complement strict-monotonicity certificates when derivative zeros or tangential roots prevent P27.37 unique-leaf proofs.
- No Sturm implementation or theorem is claimed yet.
