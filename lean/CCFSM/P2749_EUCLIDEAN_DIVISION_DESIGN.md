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
