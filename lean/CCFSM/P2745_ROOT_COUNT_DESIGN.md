# P27.45 design note — certified root witnesses and count bounds

## Purpose

P27.44 now provides a proof-carrying partition tree, closed-domain coverage,
midpoint evidence, and recursive soundness of every leaf claim. The next
missing layer is quantitative: extracting the certified root witnesses and
proving that the resulting lower bound does not count a root more than once.

This note specifies the next formal extension. It does not claim that an
aggregate root-count theorem is already implemented.

## 1. Make unique-root witnesses data

P27.37 currently defines UniqueWitness as a propositionally existential
statement: there exists one interior root and every other interior root is
equal to it. This is sufficient for logical existence/uniqueness, but it does
not provide a computational witness that can be exported into a certificate
file.

P27.45 should use a data structure containing:

- the witness coordinate;
- proof that the witness lies strictly inside its leaf interval;
- proof that the polynomial vanishes at the witness;
- proof that every other interior zero equals the witness.

This avoids extracting data from an existential proposition by classical
choice and lets the producer serialize the claimed witness explicitly. The
checker still validates the proof obligations; it does not trust a serialized
root coordinate.

## 2. Collect root witnesses structurally

Define a recursive witness collector over the P27.44 tree:

- a no-root leaf contributes an empty list;
- a unique-interior-root leaf contributes its explicit witness;
- an unresolved leaf contributes no certified witness;
- a split point with root evidence contributes that midpoint once;
- a split point with no-root or unresolved evidence contributes no root.

The split node is the unique structural owner of its midpoint. The left and
right child interiors are open and cannot include that midpoint.

## 3. Prove range membership and pairwise distinctness

For every tree over [lo, hi], prove that each collected witness lies in the
parent interval and is a root of the declared polynomial.

For a split at m:

- witnesses in the left subtree lie strictly below m;
- witnesses in the right subtree lie strictly above m;
- a certified split-point root is exactly m and appears only once;
- witnesses within each subtree are pairwise distinct by induction.

These facts yield pairwise distinctness of the concatenated witness list.
This is the theorem needed before its list length can be interpreted as a
certified lower bound on the number of distinct roots.

The proof must use exact order relations on the represented domain, not
floating-point proximity or epsilon-based deduplication.

## 4. Root-count lower and upper bounds

The lower bound is the number of pairwise-distinct explicit witnesses in the
collector. Unresolved leaves do not reduce that lower bound; they simply do
not contribute a claimed root.

A finite upper bound needs stronger evidence:

- every closed leaf interval must be certified root-free or to contain
  exactly one interior root;
- each leaf endpoint must be shown not to contain an additional root, or
  be owned by an explicit boundary-root node;
- all split points and the two outer domain endpoints must have root/no-root
  evidence;
- every unique-root leaf must exclude endpoint roots;
- unresolved nodes are forbidden.

Only after these conditions are proved may the root-witness count equal the
total root count on the requested closed domain. P27.44's FullyResolved
predicate alone is not enough, because the current unique-leaf contract
speaks only about the open interior.

## 5. Tangencies and even-multiplicity roots

P27.36's strict-derivative-sign route appropriately returns unresolved when
the derivative enclosure includes zero. This includes tangencies and
even-multiplicity roots. P27.45 must not relabel such intervals as root-free.

For a general polynomial, an exact rational Sturm-sequence certificate is a
candidate complementary route. The next comparison should assess:

- coefficient-domain requirements (rational/dyadic coefficients versus
  arbitrary floating inputs);
- exact sign evaluation at rational endpoints;
- endpoint-root handling and square-free factorization;
- proof size and certificate-checking complexity;
- whether the current interval-Horner route remains useful as a fast exclusion
  filter before invoking exact root counting.

## Acceptance criteria

P27.45 is complete only after:
1. unique-root witnesses are explicit certificate data;
2. tree witness collection is implemented;
3. every collected witness is proved to be a root in the parent domain;
4. pairwise distinctness is proved from tree geometry and midpoint ownership;
5. the lower-bound theorem is proved;
6. the finite upper-bound theorem requires explicit outer-endpoint and
   split-point evidence and rejects unresolved leaves;
7. regression/mutation tests cover duplicate midpoint claims, missing endpoint
   evidence, forged witnesses and tangential roots.

The end result is a certificate for a mathematical polynomial on a stated
domain. It is not, by itself, a root certificate for a noisy physical
measurement or a validation of the CCFSM constitutive model.
