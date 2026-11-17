# P27.49 — exact Euclidean polynomial division design

## Scope

This design specifies the next formal layer after the initial canonical
rational polynomial core in `P2749.lean`. The coefficient convention remains
ascending degree order. Coefficients are exact elements of Lean core `Rat`.

The divisor must be nonzero. Division by the zero polynomial is a malformed
request and must not return a quotient/remainder pair.

## Degree and leading coefficient

For a nonzero canonical polynomial `p`:

- `leadingCoefficient? p = some c` with `c ≠ 0`;
- `degree? p = some d`, where `d = p.coefficients.length - 1`.

For zero, the degree remains `none`. Any recursive termination measure must
handle zero explicitly; it must not silently treat the zero polynomial as
having the same degree as a nonzero constant.

## One cancellation step

Let `R` be the current remainder and `B ≠ 0` the divisor. If
`degree(B) ≤ degree(R)`, define:

```text
k = degree(R) - degree(B)
c = leadingCoefficient(R) / leadingCoefficient(B)
T = c * X^k
R' = R - T * B
```

All operations are over `Rat`. The leading coefficient of `T * B` is
exactly the leading coefficient of `R`, so the degree-`degree(R)` term
cancels. The proof must use the nonzero leading coefficient of `B` and
the exact field law for rational division. It must establish either
`R' = 0` or `degree(R') < degree(R)`.

The strict decrease is the termination argument. A recursion on the original
dividend degree is therefore well-founded. Do not use an arbitrary fuel limit
as the mathematical termination proof.

## Recursive quotient/remainder algorithm

For nonzero `B`:

- If `R = 0`, return quotient zero and remainder zero.
- If `degree(R) < degree(B)`, return quotient zero and remainder `R`.
- Otherwise perform one cancellation step `T,R'`, recursively divide
  `R'` by `B`, and add `T` to the recursive quotient.

The resulting pair `(Q, S)` must satisfy:

```text
A = Q * B + S
S = 0 or degree(S) < degree(B)
```

## Certificate checker

The checker should not need to trust the long-division producer. A compact
certificate contains the exact canonical coefficient vectors for `A`,
`B`, `Q`, and `S`. The checker verifies:

1. `B ≠ 0`;
2. canonical coefficient encoding for all four polynomials;
3. exact polynomial multiplication and addition;
4. coefficientwise equality `A = Q * B + S`;
5. `S = 0` or `degree(S) < degree(B)`.

Uniqueness of quotient and remainder is a separate Lean theorem. It is useful
for proving that the checker accepts at most one valid pair for a fixed
`A,B`, but is not needed to re-run the producer's algorithm.

## Proof obligations

- Prove leading-coefficient and degree behavior for scalar multiplication,
  monomial shifts, addition, and multiplication.
- Prove cancellation of the top coefficient in the one-step remainder.
- Prove strict degree decrease for every nonterminal step.
- Prove the recursive algorithm's quotient/remainder identity.
- Prove the remainder degree bound.
- Prove uniqueness using exact polynomial arithmetic and the fact that a
  product of nonzero rational polynomials is nonzero.
- Add adversarial tests: zero divisor, constant divisor, divisor degree
  larger than dividend, exact divisibility, negative leading coefficients,
  and a remainder whose leading coefficient cancels exactly.

## Sturm integration

Only after the division theorem and checker pass should the signed remainder
sequence be constructed:

```text
S₀ = p
S₁ = p'
Sᵢ₊₁ = -rem(Sᵢ₋₁, Sᵢ)
```

The sequence terminates when the next remainder is zero; the last nonzero
member is retained as the gcd representative. The zero polynomial is never
inserted as a sign-bearing sequence member.

## Current status

Design only. The P27.49 module currently implements canonical polynomial
representation, evaluation, derivative coefficients, addition and
multiplication, with exact evaluation laws. It does not yet implement
polynomial division or prove degree behavior of the arithmetic operations.


## Formal progress update (2026-11-16)

The Lean coefficient-list foundation now verifies aligned subtraction and
exact cancellation of equal final coefficients. If the coefficient vectors
are `xs ++ [a]` and `ys ++ [a]` with equal prefix lengths, their
coefficientwise difference is exactly
`subtractCoefficients xs ys ++ [0]`. Normalization removes this final zero,
and a proved length bound shows the normalized result has at most the common
prefix length.

This establishes the algebraic shape of the cancellation step and now also
proves strict coefficient-vector length decrease for equal-leading-term
cancellation. For nonzero canonical vectors, coefficient length is exactly
degree plus one, so this is the intended well-founded measure for long
division. The full polynomial step remains open: we still need the formal
bridge from shifted/scaled divisor multiplication to coefficient vectors,
the exact rational leading-coefficient quotient, and a theorem connecting
the quotient to the divisor's leading coefficient.

CI run 43868853530 passed all 17 aggregate Lean targets for the cancellation
lemmas. The strict length-decrease lemma was added in commit
`b4cbc26351a35b110b7b9f5b00ef734ee974cf96`; its aggregate CI is pending.

## Refined implementation sequence after the list-level cancellation lemma

The implementation should now avoid treating the list-length lemma as if it
were already a polynomial-degree theorem. The bridge is split into explicit
proof obligations:

1. **Monomial multiplication identity.** Prove that multiplying a canonical
   coefficient vector by the monomial vector `[0, …, 0, c]` is exactly the
   `k)-place shift followed by coefficient scaling. State the identity at
   the raw coefficient-list level first; normalization is a separate step.
2. **Leading coefficient of the shifted divisor.** For nonempty canonical
   `B`, prove that the final coefficient of `X^k * (c * B)` is
   `c * leadingCoefficient(B)`, and that its vector length is
   `k + B.coefficients.length` when `c ≠ 0`.
3. **Exact cancellation scalar.** With `aR` and `aB ≠ 0`, set
   `c = aR / aB`. Prove `c * aB = aR` in `Rat`; do not replace this
   with a floating-point division or a numerical tolerance.
4. **Polynomial one-step theorem.** Combine (1)–(3) with the existing
   aligned-subtraction lemma. Prove the normalized remainder is zero or has
   strictly fewer coefficients than the current nonzero remainder. Convert
   the length statement to degree only after proving the canonical,
   nonzero length/degree correspondence.
5. **Well-founded recursion.** Define the recursive division over the
   current remainder using its natural-number degree (or coefficient length
   with zero handled as a separate terminal case). The recursive call must
   be justified by the strict decrease from (4), not by fuel.
6. **Independent checker.** Keep the producer and checker separate. The
   checker verifies the exact identity `A = Q*B + R` and the remainder
   bound; it must not trust the producer's intermediate cancellation trace.

### Required boundary cases before the division theorem is advertised

- Zero dividend with nonzero divisor returns `Q = 0, R = 0`.
- A nonzero constant divisor is supported and terminates after at most one
  cancellation per nonzero coefficient degree.
- A divisor of greater degree than the dividend returns `Q = 0, R = A`.
- Exact divisibility returns zero remainder.
- Negative leading coefficients are handled by exact rational division.
- The zero divisor is rejected at the API boundary.
- The zero polynomial is never assigned an ordinary natural-number degree.

### Status discipline

The list-level equal-final-coefficient cancellation theorem is proved and
aggregate CI has passed on the relevant code commit. The shifted-monomial
identity, polynomial-level cancellation theorem, recursive division,
quotient/remainder identity, degree bound, uniqueness, and independent
checker are **not yet proved**. No Sturm sequence or root-count theorem
follows from the list-level lemma alone.

## Formal progress update — shifted-vector measure

The Lean module now proves
`shiftedScaleCoefficients_length`: prefixing a coefficient vector with
`k` zero slots and scaling its entries preserves the original vector length
apart from those `k` inserted slots. This is a small but explicit measure
lemma for the monomial-shift representation used by the next cancellation
proof.

It does **not** yet prove the convolution identity between multiplication by
a monomial and shifted scaling, nor does it identify the final coefficient
with the polynomial leading coefficient. Those remain the next bridge
obligations. The new lemma is awaiting aggregate Lean CI.


## Formal progress update — constant-factor convolution

A first coefficient-level multiplication bridge is now proved in
`P2749.lean`: for a nonempty coefficient vector `xs`, convolution with
the singleton coefficient vector `[c]` equals coefficientwise scaling
by `c`. The nonempty premise is intentional: the current recursive
convolution maps an empty second vector to the empty vector, while the
separate shifted/scaled representation can contain inserted zero slots.

This establishes the degree-zero monomial case only. The general
`X^k)-shift identity still requires a lemma controlling the recursive
`addCoefficients` alignment and the inserted zero coefficients. It is not
yet a polynomial-division or leading-coefficient cancellation theorem.

The corrected shifted-vector length proof passed aggregate Lean CI on
`a656f5d7d980c511581dd431d226fddf2b58f3a5` (Lean run
`43870379199`; Python run `43870379213`). The new singleton-convolution
lemma is on commit `2d31da40f0a56003c4701db17d88b67e7e0dcb06`;
its Lean CI is queued and has not yet been claimed as passing.


## CI-verified follow-up — singleton convolution (2026-11-16)

The singleton-convolution proof was corrected after the first Lean attempt
left an unsolved tail goal involving addition of an empty coefficient vector.
The module now has the explicit helper theorem
`addCoefficients_nil_right`, and
`multiplyCoefficients_singleton_left` uses it directly.

The corrected head is `331d63aec9aae029b5dc8931ed0bbece57c6792f`.
Aggregate Lean runs `43890786828` and `43890798326` both passed;
the natural-syneresis Python workflow `43890798363` also passed.

This closes the degree-zero singleton case at the raw coefficient-list
level. It does not establish the general monomial-shift convolution identity,
a leading-coefficient theorem, polynomial long division, or a Sturm root
counter. The next proof gate remains the general monomial-shift identity,
with explicit nonempty-input and coefficient-list alignment conditions.


## CI-verified zero-padding alignment (16 November 2026)

`addCoefficients_zero_scaled_left_of_length_le` is now proved in
`CCFSM.P2749`: when the zero-scaled left coefficient vector is no longer
than the right vector, coefficientwise addition returns the right vector
unchanged. The proof explicitly rewrites the mapped zero vector back to the
`scaleCoefficients 0` form expected by the induction hypothesis.

The aggregate Lean proof-kernel workflow passed on commit
`793db5f1ecb6ec4e4bda7974fe856b5673ec1d05` (runs 43895569725 and
43895583835). The Python natural-syneresis workflow for that same commit was
still running at the time of this note.

This alignment lemma is a required ingredient, not the monomial-shift
identity itself. The remaining induction still needs a proved lower bound
on the length of the recursive convolution result, under an explicit
nonempty second-vector premise. Only then can the zero-padded first
convolution layer be shown to leave the shifted recursive tail unchanged.


## CI-verified general monomial-shift convolution (16 November 2026)

The coefficient-list bridge has advanced beyond the singleton case. The Lean
module now proves both:

- `multiplyCoefficients_monomial_length`: convolution of the coefficient
  vector for `X^k * c` with a nonempty right-hand vector has length
  `k + xs.length`;
- `multiplyCoefficients_monomial`: the same convolution is exactly the
  `k`-slot low-degree shift followed by coefficientwise scaling.

The explicit premise `xs ≠ []` is essential for the current recursive
list implementation. For an empty right vector, convolution by a nonempty
monomial vector produces a zero-filled vector rather than the empty list;
the shifted/scaled representation has a different length in that edge case.
The theorem is therefore intentionally stated only for nonempty input and
must not be silently generalized to the zero polynomial representation.

Aggregate Lean proof-kernel CI passed on code head
`f05c6c36dac64e2b358da0534c47c68ba3138eae` (run 43896907930).
This closes the general raw coefficient-list monomial bridge. It does not
yet prove a polynomial-level leading-coefficient theorem, a one-step
Euclidean cancellation theorem, recursive division, or any Sturm result.
The next gate is to connect the shifted/scaled vector's final coefficient
to the leading coefficient of a canonical nonzero divisor, then prove the
exact rational cancellation scalar and lift the existing aligned subtraction
measure to the polynomial division step.


## CI-verified final coefficient of monomial convolution (16 November 2026)

The new theorem `multiplyCoefficients_monomial_final_coefficient`
now lifts the raw monomial-shift identity to the final coefficient: for a
nonempty canonical input coefficient vector and a nonzero scalar `c`,
monomial convolution ends in a nonzero coefficient equal to `c` times
the input's final coefficient. The proof uses the canonical decomposition
`xs = init ++ [originalLast]` and the exact rational zero-product law to
establish nonzeroness.

Aggregate Lean proof-kernel CI passed on code head
`9532794979961d955878d22bc9f9294bba48b3aa` (run 43897466565).
This establishes the shifted-divisor leading coefficient at the raw
coefficient-list level, conditional on canonical nonzero input and nonzero
scalar. It is not yet a polynomial-division theorem. The next step is to
instantiate the scalar as `aR / aB` and use exact rational cancellation
`(aR / aB) * aB = aR`, then combine it with the existing aligned
subtraction measure.


## CI-verified exact final-term cancellation (16 November 2026)

The raw coefficient-list division step is now closed for a single monomial
term. `multiplyCoefficients_monomial_cancels_final` proves that if the
divisor coefficient vector ends in a nonzero `aB`, convolution by the
monomial coefficient vector with scalar `aR / aB` ends in exactly
`aR`. The proof combines the nonempty-input monomial-shift identity
with Lean core's exact rational identity `Rat.div_mul_cancel`.

Aggregate Lean proof-kernel CI passed on head
`df9b9d846d5aa3e8b379fa1347d5bf6ead91fd55` (run 43897845062).
This is the key raw-list cancellation mechanism for polynomial long division.
Remaining obligations are to package the result for canonical polynomial
objects, prove the full subtraction vector is canonically normalized with
strict degree decrease, define quotient/remainder recursion, and verify the
independent remainder identity and degree bound. The Sturm sequence and
root-count theorem remain downstream and open.


## CI-verified strict decrease for one monomial subtraction (16 November 2026)

The theorem `normalize_subtract_monomial_step_length_strict` now
connects the raw monomial cancellation result to the existing aligned
subtraction measure. Under three explicit hypotheses — (i) the dividend
coefficient vector ends in `aR`, (ii) the divisor coefficient vector
ends in a nonzero `aB`, and (iii) the shifted divisor and dividend
coefficient vectors have equal lengths (`r.length = k + d.length`) —
subtracting the monomial multiple and normalizing strictly decreases the
dividend coefficient-vector length.

Aggregate Lean proof-kernel CI passed on head
`58395a0ff57652d34813195c1d55ef703bb185bf` (run 43898301079).
This is a genuine one-step termination measure for the raw coefficient-list
long-division operation. It is not yet a recursive quotient/remainder
implementation: the next proof must package the hypotheses and result for
canonical `RatPolynomial` values, establish the degree/length relation
for nonzero canonical polynomials, and implement well-founded recursion with
a separately checked quotient/remainder identity and degree bound.


## CI-verified degree/length correspondence (16 November 2026)

Added `degree?_add_one_eq_length`: every nonzero canonical
`RatPolynomial` has an option-valued degree `d` satisfying
`d + 1 = coefficients.length`. Aggregate Lean proof-kernel CI passed
on head `d48061afe287a0be9f371a77e11fe1d0e18b0678` (run
43898652903).

This closes the basic measure conversion needed to turn the raw normalized
coefficient-vector decrease into a polynomial-degree decrease once the
subtraction step is packaged as a `RatPolynomial`. The current theorem
is a degree/length identity only; it does not yet assert the degree of a
particular division remainder.


## CI-verified polynomial-level one-step degree decrease (16 November 2026)

Two further results connect the list-level termination argument to the
`RatPolynomial` API:

- `degree?_lt_of_normalized_length_lt` converts a strict decrease in
  normalized coefficient-vector length into a strict degree decrease,
  provided both the dividend and normalized result are nonzero.
- `degree?_monomial_subtract_step_lt` packages the raw monomial
  subtraction result as a canonical `RatPolynomial` and proves that
  its degree is strictly below the dividend degree under the explicit
  final-coefficient, nonzero-divisor and equal-shifted-length hypotheses.

Aggregate Lean proof-kernel CI passed on head
`69d0b1fb18f1894ab13a53e2bb0ec1130dfb7f99` (run 43898966855).
This is now a polynomial-object one-step decrease theorem, not merely a
list-length statement. It still does not define a quotient/remainder
recursion or establish the remainder identity and quotient-degree bound.
The next gate is to make the step computable from nonzero canonical
polynomials (derive the shift from their degrees and the scalar from their
leading coefficients), then define well-founded recursion and prove its
specification independently.


## CI-verified canonical monomial-subtraction operation (16 November 2026)

Added `subtractMonomial` as a canonical `RatPolynomial` operation:
it subtracts a monomial multiple of a divisor polynomial from a dividend and
normalizes the result. The theorem `degree?_subtractMonomial_lt`
proves strict degree decrease when the dividend and divisor have the
specified final coefficients, the divisor final coefficient is nonzero,
the shifted divisor has the same coefficient-vector length as the dividend,
and the normalized result is nonzero.

Aggregate Lean proof-kernel CI passed on head
`a080b7debf84ab3ca96a2402f90f3a625b5134db` (run 43899165470).
This provides a named canonical-polynomial step suitable for a future
well-founded recursion. The remaining work is to derive its shift and scalar
automatically from the two polynomials, handle the zero remainder branch,
define the quotient accumulator, and prove the quotient/remainder identity
and remainder-degree bound.


## CI-verified automatic leading-term subtraction (16 November 2026)

Added `leadingCoefficient?_eq_last` to expose the final ascending
coefficient of every nonzero canonical polynomial through the existing
leading-coefficient accessor. On that basis, `subtractMonomialLeading`
now selects the degree shift `p.length - q.length` and scalar
`aR / aB` automatically from the two leading coefficients (with a
zero fallback only to keep the definition total outside its intended
nonzero-input domain).

The theorem `degree?_subtractMonomialLeading_lt` proves that for
nonzero canonical dividend and divisor, with divisor coefficient length no
greater than the dividend's, the automatically selected subtraction has
strictly smaller degree whenever its normalized result is nonzero.
Aggregate Lean proof-kernel CI passed on head
`962b98271e9f58b2e3093b38dac9b5109e1951a4` (run 43899461813).

This removes the caller-supplied shift and leading-coefficient witnesses
from the one-step theorem. The remaining recursion design must handle the
zero remainder as a terminal case, accumulate quotient monomials, and prove
the quotient/remainder identity and the remainder-degree bound.


## Division-step terminal branch — 17 November 2026

The Lean module now packages the automatic leading-term subtraction result
as a zero-or-strict-degree-decrease statement:
`subtractMonomialLeading_zero_or_degree_lt`. For nonzero canonical
dividend and divisor with divisor coefficient length no greater than the
dividend's, the subtraction result is either the zero polynomial (whose
option-valued degree is `none`) or has strictly smaller degree than the
dividend.

This removes the need for callers to supply a separate nonzero-result
hypothesis when setting up the recursion's measure. The new theorem is on
commit `1193ae22d83095e091fac92e83da9d0e7c778e51`; aggregate Lean and
Python CI are pending. It is not yet a quotient/remainder recursion and does
not establish the quotient/remainder identity or remainder-degree bound.


## Exact evaluation law for a division step — 17 November 2026

Added `eval_subtractMonomial` in `CCFSM.P2749`. It proves that a
single canonical subtraction step evaluates exactly as
`eval p x - (ratPow x k * c) * eval q x`. This is the algebraic invariant
needed to telescope the repeated subtraction steps into a quotient/remainder
identity. The statement is about exact rational polynomial evaluation; the
well-founded recursion and its accumulated quotient are still to be defined.
The theorem is on code commit `a74332648eb9418c54a194946af0e2aa20389f97`;
its aggregate Lean CI is pending.


## Exact evaluation law — corrected proof and CI (17 November 2026)

The proof of eval_subtractMonomial was corrected to unfold the canonical
coefficient representation and use the exact coefficient-list evaluation
laws directly. The Lean proof-kernel workflow now passes on commit
8fbbe1d9298b4a9aea07fd18d0542ee6f55dab72 (runs 44010877202 and
44010883527). The natural-syneresis Python workflow for this commit is still
running and is not yet claimed as passed.

The theorem establishes the pointwise evaluation law for one subtraction
step. Together with the zero-or-strict-degree-decrease theorem, it supplies
the two main ingredients for well-founded long division: a terminating
remainder update and an exact algebraic update law. The next implementation
should define the quotient increment as the selected monomial, update the
quotient accumulator and remainder together, and prove preservation of the
invariant eval p x = eval q_acc x * eval divisor x + eval remainder x.

**Silica-gel scope:** this is reusable exact algebra infrastructure, not a
silica-gel constitutive law, fitted parameter, or physical validation. Its
potential CCFSM role is downstream: exact manipulation/checking of rational
characteristic polynomials or linearized stability relations, once such a
polynomial is derived from an explicitly stated CCFSM subsystem. No such
CCFSM-specific polynomial has yet been connected to this module.


## Concrete CCFSM integration target — P27.37 / P27.49

The intended connection is now made explicit. CCFSM v4.2.57 P27.37 performs
adaptive polynomial root isolation for the polynomial enclosures used in the
CCFSM event/flux certification chain. P27.49 supplies an exact-rational
Python-to-Lean payload boundary for those polynomial/domain inputs. The
present P2749 rational-polynomial module is intended to become an independent
exact-arithmetic backend for that certificate chain.

A future Sturm sequence based on exact Euclidean remainders could strengthen
the root-counting side of P27.37/P27.49, particularly where interval
monotonicity tests leave a subinterval unresolved. It is not yet integrated:
P27.37 currently uses interval exclusion and derivative/endpoint criteria;
P27.49 currently serializes and validates exact rational payloads, and its
Lean checker must still be audited separately. The division theorem and
Sturm sequence remain prerequisites, not existing capabilities. Any
resulting certificate would verify a polynomial statement generated by the
CCFSM numerical pipeline; it would not by itself validate the silica-gel
constitutive model or the physical interpretation of a detected event.


## Quotient-accumulator invariant — 17 November 2026

Added `rational_division_update_identity` and `eval_division_update` in
`CCFSM.P2749`. The latter formalizes the exact telescoping step: if the
quotient accumulator is increased by `c * X^k` and the remainder is
decreased by the same monomial multiple of the divisor, then the evaluated
quantity

`eval quotient * eval divisor + eval remainder`

is unchanged at every rational evaluation point. This is the key invariant
needed for the eventual global identity `P = Q * D + R`.

The new code is commit `fbf5e2b146727e4a6e3935006c99659425652228`.
Its aggregate Lean proof-kernel CI is queued as run `44086735929` at the
time of this note; no pass is claimed until that run completes. This theorem
is still only a one-step invariant: the quotient accumulator is not yet
implemented as a recursive object, and termination, remainder degree,
uniqueness and Sturm counting remain open.


## Verified quotient/remainder update invariant — 17 November 2026

The scalar cancellation proof was completed using Lean core's exact rational
additive-inverse law. The module now proves:

- `rational_division_update_identity`: the scalar identity behind one update;
- `eval_division_update`: adding one quotient monomial and subtracting
  the same monomial multiple of the divisor preserves
  `eval Q x * eval D x + eval R x` at every rational x;
- `DivisionState`, `divisionStep` and `runDivisionSteps`: a finite,
  explicitly supplied sequence of quotient/remainder updates;
- `eval_runDivisionSteps`: the evaluation invariant is preserved by
  every such finite trace.

Aggregate Lean proof-kernel CI passed on exact code head
`1fff86cbf00b7b5b92ba2c72e41fc00b6d0fefe0` (run `44087441806`).
The natural-syneresis workflow for this head is still running at the time of
this note.

**Important boundary:** `runDivisionSteps` is a trace interpreter, not yet
the Euclidean-division algorithm. The trace terms are supplied explicitly;
the code does not yet prove that a leading-term policy generates a finite
trace, that the final remainder is zero or has degree below the divisor, or
that the resulting quotient/remainder are unique. Those remain the next
formal gates before a Sturm sequence can be implemented.


## Dividend-initialized trace identity — Lean CI correction (17 November 2026)

Added `eval_zero`, `initialDivisionState` and
`eval_runDivisionSteps_from_dividend`. Starting from the zero
quotient and the full dividend as remainder, every explicitly supplied finite
trace now has the direct evaluated identity
`eval Q(x) * eval D(x) + eval R(x) = eval P(x)`.

The first proof attempt exposed only a simplification mismatch in the final
`0 + eval P(x)` term; it was replaced with an explicit two-line
`calc` proof. The corrected aggregate Lean proof-kernel build passed on
code head `ddfbb1c0bac70df8d793132d5167ff6e8ce6004a` (run
`44087914969`). The natural-syneresis workflow for this exact code head
is still running.

This remains a finite-trace theorem, not a completed division algorithm.
The algorithmic leading-term policy, well-founded recursion, final
remainder-degree bound, polynomial-level identity and uniqueness are still
open.


## Warning cleanup and latest code verification — 17 November 2026

Removed an unused simplifier argument in the existing degree/length lemma;
the proof itself is unchanged. Aggregate Lean proof-kernel CI passes on
the resulting code head `03f538b1467f08e676bd839e4da5e0f3d6355bff`
(runs `44088140579` and `44088148474`). The natural-syneresis
workflow for this exact head is still running (`44088148169`).

The strongest currently Lean-verified division result is therefore the
dividend-initialized finite-trace identity above. No recursive long-division
algorithm or Sturm root-count theorem is claimed.


## Automatic leading-term update — first Lean-verified step (17 November 2026)

Added `leadingDivisionStep` and `eval_leadingDivisionStep`. The new
state transition now selects the quotient monomial directly from the current
remainder and divisor leading coefficients, using the degree offset
`remainder.coefficients.length - divisor.coefficients.length` and exact
rational coefficient ratio. When both leading coefficients are present, the
evaluated quotient/remainder invariant is proved for that automatically
selected update.

Aggregate Lean proof-kernel CI passed on code head
`b7a7922126c47390945263fede12d4a171b1ebd4` (run
`44088742824`).

**Boundary:** this is one automatically selected transition, not yet a
recursive algorithm. The next gate is to prove the transition is taken only
when the divisor degree fits, prove the nonzero remainder strictly decreases
in the chosen measure, and compose transitions with a well-founded
termination argument. No Sturm root count is claimed.


## Degree-fit guard and strict decrease for the automatic step — 17 November 2026

The automatic transition is now guarded: it performs a leading-term
subtraction only when the divisor coefficient-vector length is no greater
than the current remainder length. If the divisor does not fit, the state
is left unchanged. This prevents the invalid degree-offset-zero subtraction
that would otherwise occur when the divisor degree exceeds the remainder.

Added `degree?_leadingDivisionStep_zero_or_lt`. Under nonzero leading
coefficients and the degree-fit premise, the guarded transition either
produces the zero polynomial or a nonzero remainder of strictly smaller
degree. Aggregate Lean proof-kernel CI passed on exact code head
`5730a10e1ac863f3386feafa57eef172d32b9967` (run
`44089056837`).

This establishes the local decrease fact needed by a well-founded
recursion, but the recursive driver and its global termination theorem are
not yet implemented. In particular, no final quotient/remainder degree
bound or Sturm root count is claimed.


## Bounded automatic leading-division evaluator — 17 November 2026

A total, fuel-bounded evaluator has now been added:

- `runLeadingDivisionFuel divisor state fuel` applies the automatic
  `leadingDivisionStep` at most `fuel` times.
- Structural recursion on the natural fuel makes the evaluator total without
  a termination argument about polynomial degrees.
- The intended invariant is proved for every fuel value: the evaluated
  quotient-times-divisor plus remainder equals the corresponding initial
  value at every rational evaluation point.
- If a leading coefficient is unavailable or the divisor's coefficient
  length exceeds the remainder's, the guarded transition leaves the state
  unchanged; otherwise it applies the exact monomial update.

This is an executable bounded evaluator and a useful bridge to an unbounded
algorithm, but the fuel is an external bound. It does **not** prove that a
specific degree-derived fuel is sufficient, that the final remainder has
degree below the divisor, or that the quotient/remainder are unique. The
new theorem is awaiting aggregate Lean CI on commit
`31429876de78308617710a000099206483956df9`; do not treat it as verified
until that run completes successfully.


### CI status correction — bounded evaluator

The bounded evaluator theorem passed aggregate Lean proof-kernel CI on
commit `31429876de78308617710a000099206483956df9` (runs `44090098824`
and `44090090852`). The natural-syneresis workflow for that exact code
head (`44090098730`) was still running at this documentation update.
The documentation-head Lean workflow is queued. This supersedes the
pending-CI sentence in the preceding subsection.


## Full CI confirmation — current PR head (17 November 2026)

The current PR head `33f52468e9ea22436b2bd39858240e5de5275ad1` has now
passed both project workflows:

- Aggregate Lean proof-kernel workflow: run `44090248305`, conclusion
  `success`.
- Natural-syneresis / Python workflow: run `44090248252`, conclusion
  `success`.

This closes the pending-CI status recorded above. It verifies the formal
code and the existing computational regression workflow; it does not turn
the bounded evaluator into an unbounded Euclidean algorithm. The sufficient
fuel bound, terminal remainder-degree theorem, polynomial-object identity,
uniqueness, and Sturm root-count theorem remain open.


## Absorbing terminal state for bounded division — 17 November 2026

The Lean module now proves two complementary fixed-point facts:

- `leadingDivisionStep_eq_self_of_terminal`: if the current remainder is
  zero, or the divisor coefficient vector is longer than the remainder
  vector, the guarded automatic transition is exactly the identity on the
  complete `DivisionState`.
- `runLeadingDivisionFuel_eq_self_of_terminal`: from either such terminal
  condition, every additional amount of fuel leaves the complete state
  unchanged. This is proved by induction on the evaluator fuel.

The aggregate Lean proof-kernel build step passed on code commit
`263f22c9282c047ce6a76e2863bbbfe0b3931aa6` (run `44099706171`).
The earlier attempt on `4de214b8e14ff4a6cd7531864b7157248641049f`
failed due to proof ordering and incomplete option-case reduction; that
attempt was corrected and is superseded by the passing build above.

**Boundary:** this proves stability *after* a terminal condition holds. It
does not prove that the evaluator reaches that condition within any
particular fuel, nor does it yet provide a degree-derived fuel bound,
quotient/remainder degree theorem, polynomial-object identity, uniqueness,
or Sturm root count.


## Exact terminal-state characterization — 17 November 2026

For a nonzero canonical divisor, the transition's fixed points are now
characterized in both directions by
`leadingDivisionStep_eq_self_iff_terminal`:

`leadingDivisionStep divisor state = state`

holds exactly when the current remainder is zero or the divisor coefficient
vector is longer than the remainder coefficient vector. The nonzero-divisor
premise is essential: a zero divisor has no leading coefficient and would
make every state a fixed point, which is not a valid Euclidean-division
terminal criterion.

The proof combines canonical nonzero leading-coefficient existence with the
previous zero-or-strict-degree-decrease theorem. In the degree-fit case, a
fixed point would force the remainder to have both its original degree and a
strictly smaller degree, a contradiction. Aggregate Lean proof-kernel CI
passed on code head
`8b749603c561c5a14707fb941a7a011fc259486b` (runs `44100191169` and
`44100206759` both report success).

Together with `runLeadingDivisionFuel_eq_self_of_terminal`, this proves
that the guarded evaluator stops changing exactly at the intended terminal
condition and remains there for all additional fuel. It still does not prove
that any fixed degree-derived fuel is sufficient to reach that condition.
The global quotient/remainder degree theorem, polynomial-object identity,
uniqueness and Sturm root count remain open.


## Coefficient-length decrease for the automatic transition — 17 November 2026

Added `leadingDivisionStep_length_zero_or_lt`. Under the existing explicit
leading-coefficient and degree-fit hypotheses, the automatic transition now
has a direct coefficient-vector measure theorem: its remainder is either
the empty zero representation or has strictly fewer coefficients than the
input remainder.

The proof lifts the already verified option-valued degree decrease through
the canonical nonzero degree/length identity. It handles the zero branch
separately, so zero is never assigned a natural-number degree. This gives
the recursive termination argument a directly usable natural-number
measure, without a detour through option-valued degrees at each recursive
call.

Aggregate Lean proof-kernel CI passed on code head
`d9a437ef64ee3a360e937145d4a3d8ef576eeeac` (runs `44100750965` and
`44100763050`). The natural-syneresis/Python workflow for this exact code
head (`44100762940`) remains in progress and is not yet claimed as passed.

**Still open:** the global induction showing that a fuel value bounded by
the initial coefficient length reaches a terminal state; the final
quotient/remainder degree condition; polynomial-object identity and
uniqueness; and the Sturm root-count theorem.
