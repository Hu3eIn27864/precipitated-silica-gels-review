# P27.47 — exact Sturm certificates for tangential and multiple roots

## Motivation

P27.36/P27.37 obtain uniqueness from strict monotonicity on an interval. This is intentionally incomplete when the derivative changes sign or vanishes at a tangency. P27.45–P27.46 count roots only when each leaf already carries a sound no-root or unique-root proof. A rational Sturm certificate is a complementary route for polynomial models with rational (or exactly represented dyadic) coefficients.

## Mathematical certificate

For a nonzero polynomial p in Q[x], form the signed remainder sequence:
- S0 = p,
- S1 = p',
- S(i+1) = - rem(S(i-1), S(i)),

terminating when the remainder is zero. The sequence can be shortened by a positive common scaling at each step, but never by a negative scaling because signs encode the variation count.

At a rational endpoint c that is not a root of any sequence member, evaluate the signs exactly and let V(c) be the number of sign changes after zero entries are omitted. For roots at the interval endpoints, use one-sided signs:
- at a+, the sign of the first nonzero Taylor coefficient of each S_i(c+t);
- at b-, the sign of (-1)^k times the first nonzero Taylor coefficient in S_i(b-t).

Then the open-interval count is V(a+) - V(b-). This avoids silently including endpoint roots and supports repeated roots: the signed remainder chain terminates at the polynomial gcd, while the variation theorem counts distinct real roots.

## Proposed serialized certificate

A small independent checker should receive:
1. canonical rational coefficient vectors for p and every S_i;
2. exact quotient/remainder identities S(i-1) = Q_i S_i - S(i+1);
3. a terminal zero-remainder assertion;
4. exact endpoint Taylor sign witnesses (first nonzero derivative order and rational coefficient sign) at a and b;
5. the claimed variation vectors and resulting nonnegative integer count.

The checker recomputes all polynomial arithmetic over Q. It must reject malformed degree drops, zero divisors, inconsistent coefficient encodings, incorrect quotient/remainder identities, and incorrect endpoint sign witnesses. A Python producer may propose the chain, but the checker must not trust producer-supplied signs or counts.

## Proof obligations for a Lean kernel

- Define finite coefficient lists over Q and exact polynomial evaluation/derivative/division.
- Prove uniqueness of quotient/remainder with strict degree decrease.
- Define sign variation on finite lists, ignoring zeros.
- Prove the Sturm variation theorem, including the endpoint one-sided convention.
- Prove repeated-root handling via the gcd/terminal remainder.
- Connect the certificate parser/checker to the mathematical theorem without trusting serialized metadata.

The difficult part is the Sturm variation theorem, not rational arithmetic itself. This should be a separate module rather than extending the monotonicity proof with unproved assumptions.

## Boundary and scope discipline

- The result counts distinct roots in the open interval. Endpoint roots must be reported separately if a closed-interval count is desired.
- A Sturm count is exact only for the exact polynomial supplied. It does not prove that noisy measured coefficients or floating-point input intervals represent the physical silica system.
- For uncertain coefficient intervals, one needs a robust quantified argument (e.g. interval polynomial families), not a point-coefficient Sturm count.
- This is an algorithm/design specification only; no Sturm theorem or Python checker is claimed implemented by this note.


## Degenerate cases and exactness gates

- The input polynomial must be nonzero. The identically-zero polynomial has
  an interval of roots and no finite distinct-root count; it must be rejected
  or routed to a separate degenerate-case result.
- The zero polynomial is never included as a member of the signed remainder
  sequence. In particular, for a nonzero constant polynomial, the derivative
  is zero and the sequence has no nonzero derivative member; the exact root
  count is zero.
- Every nonzero remainder member must have strictly smaller degree than its
  divisor. The checker verifies this degree decrease as well as the exact
  quotient/remainder identity.
- The final nonzero member is a gcd representative up to a nonzero rational
  factor. Any normalization used by the producer must preserve the sign
  sequence; only positive rescaling is harmless for variation counts.
- Endpoint Taylor-sign witnesses are required only for nonzero sequence
  members. A zero polynomial member is omitted, not assigned an invented
  endpoint sign.
- If an endpoint is itself a root of a sequence member, its ordinary
  point-evaluation sign is zero and is not used directly. The first nonzero
  Taylor coefficient gives the one-sided sign on the interior side of that
  endpoint. The endpoint root of the original polynomial is still counted
  separately by the P27.48 endpoint layer.
- A repeated root is counted once as a distinct coordinate by the Sturm
  variation difference. Algebraic multiplicity is a different output and
  would require additional factor/gcd data.

These cases should be explicit in the serialized format and negative tests;
they are not optional implementation conveniences.
