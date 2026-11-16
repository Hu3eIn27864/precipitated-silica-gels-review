# P27.49 — Lean implementation plan for exact rational Sturm certificates

## Goal

P27.47 defines the mathematical certificate contract. P27.49 should begin the
formal implementation in small verified layers, rather than attempting the
Sturm variation theorem and serialized checker in one step.

The target is an exact count of **distinct real roots of one nonzero polynomial
with rational coefficients** on an open rational interval. It is not a
certificate for a family of uncertain coefficients and it is not a proof of
physical CCFSM behavior.

## Layer 1 — canonical rational polynomials

Use a finite coefficient sequence in ascending degree order:
`[a₀, a₁, …, aₙ]` represents `a₀ + a₁x + … + aₙxⁿ`.

Required invariants and operations:

- Canonical zero is the empty coefficient list.
- A nonzero canonical polynomial has a nonzero final coefficient.
- Trimming removes only trailing zero coefficients.
- Addition, negation, multiplication, scalar multiplication, evaluation,
  and formal derivative are exact.
- Prove that each operation preserves canonical form.
- Prove evaluation agrees with the recursive/Horner definition.

Before committing to this representation, add a minimal CI probe confirming
that the pinned Lean v4.35.0 core rational type and required numerator /
denominator operations are available without importing Mathlib. If not,
define a small normalized rational wrapper and prove its arithmetic laws
before proceeding.

## Layer 2 — Euclidean division

Define polynomial quotient and remainder for a divisor with nonzero leading
coefficient. The long-division recursion must be structurally or
well-foundedly justified by a strict decrease in the degree of the current
remainder.

Prove:

1. `A = Q * B + R`;
2. `R = 0` or `degree(R) < degree(B)`;
3. quotient/remainder uniqueness under the same divisor condition.

Do not expose a division operation on the zero polynomial divisor. The checker
must reject it as malformed input.

## Layer 3 — signed remainder sequence

For nonzero `p`:

- Start with `S₀ = p`.
- If `p'` is nonzero, set `S₁ = p'`.
- Repeatedly set `Sᵢ₊₁ = -rem(Sᵢ₋₁, Sᵢ)` until the next remainder is zero.
- Store the final nonzero member (a gcd representative) and the terminal
  zero-remainder fact separately.

The zero polynomial is not a sequence member. A nonzero constant polynomial
has no nonzero derivative member and has zero roots. The identically-zero
input polynomial is rejected because it has no finite isolated-root count.

Any normalization of a sequence member must be by a strictly positive
rational factor if sign-variation data are to remain unchanged. The quotient /
remainder identity must be adjusted and rechecked after normalization.

## Layer 4 — exact signs and one-sided endpoint signs

For a nonzero polynomial `S` and rational endpoint `c`, ordinary evaluation
determines the sign when `S(c) ≠ 0`.

If `S(c) = 0`, find the least `k` whose Taylor coefficient at `c` is
nonzero. Its sign is the sign immediately to the right. Immediately to the
left, multiply that coefficient's sign by `(-1)^k`.

Prove existence of such a `k` for every nonzero polynomial, including
constant polynomials. The zero polynomial is omitted from the sequence and
has no endpoint sign.

Define sign variation on finite sign lists by deleting zero entries and
counting adjacent sign changes. The endpoint routine should return a
nonzero sign for every nonzero sequence member.

## Layer 5 — Sturm theorem

Only after Layers 1–4 are stable should the project prove the variation
theorem. The proof must establish:

- adjacent signed-remainder members cannot vanish simultaneously at a point
  unless the terminal gcd also vanishes;
- at a root of an intermediate sequence member, its neighbors have opposite
  signs, so the variation count does not change across that point;
- at a root of the original polynomial, the variation count drops by one
  when moving left-to-right, counting a repeated root once;
- the difference `V(a+) - V(b-)` equals the number of distinct roots in
  `(a,b)`.

The exact endpoint convention is essential. A closed-interval count is
obtained separately by P27.48 endpoint evidence, never by silently changing
the Sturm endpoint signs.

## Layer 6 — certificate checker and adversarial fixtures

The serialized certificate should contain canonical coefficient vectors,
quotient/remainder identities, endpoint Taylor-order/sign witnesses,
variation vectors, and the claimed count. The checker recomputes all exact
arithmetic; it does not trust supplied signs, degrees, or counts.

Minimum fixtures:

- `p(x)=x-1` on intervals with one interior root and with one endpoint root;
- `p(x)=(x-1)^2` to test tangency / multiplicity two but distinct count one;
- `p(x)=(x-1)^2(x+2)` to test a repeated and a simple root;
- a nonzero constant polynomial;
- the identically-zero polynomial (must be rejected);
- malformed quotient/remainder identities;
- incorrect endpoint Taylor order or sign;
- incorrect variation vectors and negative claimed counts.

## Acceptance gates

P27.49 should be split into independently buildable milestones:

1. canonical rational polynomial arithmetic;
2. exact Euclidean division with degree-decrease proof;
3. signed remainder sequence construction and soundness;
4. exact endpoint sign/variation functions;
5. Sturm variation theorem;
6. serialized certificate checker.

A successful build of an early layer must not be described as a completed
Sturm root counter. The full P27.49 claim is earned only after the theorem and
checker are both proved and exercised by adversarial fixtures.


## Progress checkpoint (2026-11-16)

### Layer 1 — initial foundation implemented

- Lean core `Rat` is available under the pinned v4.35.0 toolchain without
  Mathlib; this was checked by a successful CI probe.
- `CCFSM/P2749.lean` now defines ascending-degree rational coefficient
  lists with a canonical trailing-zero invariant.
- Trailing-zero normalization is proved canonical and idempotent.
- Horner evaluation, formal derivative coefficient generation,
  coefficientwise addition, scalar multiplication, and recursive convolution
  multiplication are implemented.
- Exact evaluation is proved invariant under normalization and compatible
  with polynomial addition and multiplication.
- Still open within Layer 1: a semantic theorem for the formal derivative,
  explicit coefficient arithmetic test vectors, and any polynomial
  Euclidean-division operation.

### Python bridge foundation

- `MODELLING/ccfsm/ccfsm_p27_49_rational_certificate.py` implements
  canonical rational serialization and validation.
- Binary64 values are converted through their exact `as_integer_ratio()`
  representation; Python descending-power coefficients are reversed into
  Lean ascending-degree order.
- Tests cover subnormals, negative zero canonicalization, malformed rational
  encodings, duplicate JSON keys, schema/order errors, nonfinite values, and
  noncanonical zero/trailing-zero polynomials.
- This is not yet a producer for P27.37's partition tree, and Lean does not
  yet parse the payload.
- The complete Lean polynomial build passed in CI run 43842515932
  (17 jobs). Python serializer regression tests passed in run 43841573685;
  the expanded trailing-zero test run remains to be checked.

### Next proof gate

Before starting Euclidean division, prove the derivative-evaluation
identity over `Rat` and add explicit examples for constant, linear,
quadratic, zero, and repeated-factor polynomials. Keep the zero polynomial
outside the finite Sturm-count API.
