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
