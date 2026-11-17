# CCFSM Lean proof kernel

This is an isolated Lean 4 project pinned to Lean **v4.35.0**. The formal
modules do not change the Python implementation or the CCFSM version line.

## Formal modules

### P27.34 — outward-rounded interval addition contract

- Proves endpoint ordering and enclosure from scalar lower/upper rounding
  contracts and monotonicity of exact addition.
- Provides an adapter for combining the proved addition operation with
  separately certified multiplication.
- The actual IEEE-754 `nextafter` functions are not verified by this
  abstract contract.

### P27.35 — Horner interval enclosure

- Coefficients are stored in descending degree order, matching the Python
  implementation.
- Proves enclosure of exact polynomial evaluation conditional on sound
  interval addition and multiplication.

### P27.36 — monotone-root theorem contract

- Proves uniqueness of an interior root from strict monotonicity.
- Existence requires a justified intermediate-value argument; deriving
  strict monotonicity from derivative-sign bounds is a separate obligation.

### P27.37 — proof-carrying root-isolation certificates

- No-root leaves carry a closed-interval exclusion proof.
- Unique-root leaves carry existence and uniqueness on the open interval.
- Unresolved leaves make no root-count claim.
- Subdivision lemmas cover the parent interval and handle split-point roots
  explicitly.

### P27.38 — certified interval-multiplication interface

- Introduces `SoundIntervalMultiplication`: multiplication is admissible only
  with a theorem enclosing every product of points from its input intervals.
- Composes this contract with P27.34 outward addition into the
  `IntervalArithmetic` interface consumed by P27.35.
- It does not itself prove a concrete endpoint algorithm.

### P27.39 — exact interval product in the nonnegative quadrant

- Proves the endpoint-product enclosure for intervals whose lower endpoints
  are nonnegative, under explicit order-compatible multiplication laws.
- This is exact algebra, not a floating-point rounding proof.
- Negative and zero-crossing intervals are outside this module's scope.

### P27.40 — signed scalar monotonicity

- Proves the sign split for multiplication by a fixed scalar over an ordered
  interval: nonnegative factors are monotone and nonpositive factors are
  antitone.
- Supplies separate left- and right-factor lemmas.
- Concrete ordered-ring laws remain explicit assumptions.

### P27.41 — four-corner product envelope

- Proves that any common lower/upper bounds of the four endpoint products
  bound every interior product.
- Applies signed scalar monotonicity successively in each coordinate.
- Does not assume a particular min/max implementation.

### P27.42 — concrete four-corner extrema

- Defines a comparison-tree `min4`/`max4` and proves their bounds for all
  four endpoint products.
- Combines these results with P27.41 for exact-arithmetic interval products
  across arbitrary sign combinations, including zero-crossing intervals.
- Adapts the result to P27.38's certified multiplication interface.
- This is not a proof of IEEE-754 directed rounding.

### P27.43 — exact-rational interval certificate prototype

- Design obligations for finite binary64 values, `nextafter`, signed zero,
  subnormals, and overflow are recorded in
  `CCFSM/P2743_IEEE754_DESIGN.md`.
- A Python-side independent checker recomputes add, multiply, and divide
  interval ranges from binary64 endpoints as exact dyadic rationals.
- It is not yet a Lean proof of Python/IEEE-754 refinement and does not
  verify expression provenance, external input soundness, or signed-zero
  bit semantics.

### P27.44 — proof-carrying root-partition tree

- `CCFSM/P2744.lean` defines a dependent tree indexed by exact closed
  interval endpoints, with proof-carrying leaf certificates and separate
  midpoint evidence (no-root, root, unresolved).
- Proves closed-domain coverage and recursive soundness of attached evidence.
- `FullyResolved` is a structural flag excluding unresolved nodes; by
  itself it is not an aggregate root-count theorem.
- Design: `CCFSM/P2744_CERTIFICATE_PIPELINE_DESIGN.md`.

### P27.45 — explicit root witnesses and lower bounds

- `CCFSM/P2745.lean` collects unique-leaf witnesses and certified midpoint
  roots.
- Proves every collected coordinate is an interior root and proves the
  collector duplicate-free using strict child-interval separation.
- Consequently, the witness-list length is a sound lower bound on the
  number of distinct interior roots.
- Lean CI: run 43795945691, 14 targets.

### P27.46 — exact interior root count

- `CCFSM/P2746.lean` proves the converse: in a fully resolved tree, every
  interior root occurs in the witness collector.
- Combines soundness, completeness, and duplicate-freedom into an exact
  interior-count proposition.
- Requires explicit strict-order transitivity, irreflexivity,
  strict-to-nonstrict conversion, and trichotomy.
- Counts roots in the open interval only; outer endpoint roots are separate.
- Lean CI: runs 43798130936 and 43798184721, 15 targets built.

### P27.47 — Sturm certificates for tangential and multiple roots

- Design only: `CCFSM/P2747_STURM_CERTIFICATE_DESIGN.md`.
- Specifies exact rational signed-remainder sequences, one-sided endpoint
  signs, and open-interval variation counts.
- Intended to complement strict-monotonicity certificates for tangential
  and multiple roots.
- No Sturm implementation, checker, or theorem is claimed.

### P27.48 — endpoint-root evidence and closed-interval counts

- Formal module: `CCFSM/P2748.lean`; design and acceptance criteria:
  `CCFSM/P2748_ENDPOINT_ROOT_DESIGN.md`.
- Defines root/no-root/unresolved endpoint evidence and adds only certified
  endpoint roots to the closed witness list.
- Proves closed-witness soundness, duplicate-freedom, and completeness from
  a fully resolved P27.46 interior tree plus resolved endpoint evidence.
- The completeness theorem states the order assumptions explicitly and
  requires `lo < hi`; singleton intervals are outside its scope.
- Lean CI passed on the formal implementation: run 43828394409; all 16 targets built, including `CCFSM.P2748`.

### P27.49 — exact rational polynomial foundation and Sturm roadmap

- Initial Lean module: `CCFSM/P2749.lean`; implementation plan:
  `CCFSM/P2749_STURM_LEAN_IMPLEMENTATION_PLAN.md`.
- Uses Lean core `Rat` (confirmed under the pinned Lean v4.35.0 toolchain,
  without Mathlib) and ascending-degree coefficient lists.
- Implements canonical trailing-zero normalization, Horner evaluation,
  formal derivative coefficients, coefficientwise addition, negation and
  subtraction, scalar multiplication, recursive convolution multiplication,
  monomial vectors, and shifted/scaled coefficient vectors.
- Proves normalized lists are canonical and normalization is idempotent;
  proves degree extraction and nonzero leading-coefficient decomposition
  for every nonzero canonical polynomial.
- Proves normalization preserves evaluation and that polynomial addition,
  subtraction, negation, scalar multiplication, multiplication, monomial
  evaluation, and shifted scaling obey their exact evaluation laws.
- Formal derivative coefficients are implemented, with exact evaluation
  examples for constant, linear and quadratic inputs, including zero leading
  coefficients. General derivative evaluation semantics remain open.
- The first list-level long-division lemma is now proved: aligned
  subtraction cancels equal final coefficients exactly, and normalization
  reduces the coefficient-vector length below its original length.
  Lean CI run 43868853530 passed all 17 aggregate targets.
- Exact Euclidean polynomial division remains design-only
  (`CCFSM/P2749_EUCLIDEAN_DIVISION_DESIGN.md`). The next gate is to connect
  monomial-shift/scalar multiplication to the divisor coefficients, then
  derive the exact rational leading-coefficient quotient and lift the length
  reduction to a strict polynomial-degree bound. No Sturm sequence,
  root-count theorem, or Sturm checker is claimed.
- Python/Lean bridge: design `CCFSM/P2749_PYTHON_LEAN_BRIDGE_DESIGN.md`,
  serializer `../MODELLING/ccfsm/ccfsm_p27_49_rational_certificate.py`, and
  tests `../MODELLING/ccfsm/test_ccfsm_p27_49_rational_certificate.py`.
  Python CI run 43841573685 passed the full CCFSM test job. The existing
  P27.37 search routine is not yet connected to the serializer, and Lean does
  not yet parse/verify the payload.

## Open obligations

- Connect exact interval operations to concrete numeric representations and
  prove directed rounding for the actual floating-point endpoint operations.
- Connect polynomial/derivative bounds to root certificates and prove the
  algorithm-to-certificate extraction and search-completeness obligations.
- Implement and prove a Sturm checker for exact rational polynomials,
  including repeated roots and endpoint conventions.
- Complete the P27.49 polynomial-division proof chain and signed-remainder/Sturm checker.
- Establish a producer-to-checker provenance link for serialized
  certificates.

P27.48 endpoint ownership and the closed-interval witness count are now
formalized in `CCFSM/P2748.lean`; the theorem is conditional on a fully
resolved interior partition, resolved endpoint evidence, and a nondegenerate
interval.

The Lean results are mathematical/software-verification results only. They
do not validate the physical constitutive equations or material parameters
of CCFSM.

## Build

From this directory run `lake update` once if no `lake-manifest.json` is
present, then `lake build`. The dedicated GitHub Actions workflow performs
both commands.
