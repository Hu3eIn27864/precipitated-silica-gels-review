# P27.44 design note — proof-carrying root-isolation pipeline

## Purpose and scope

P27.35 proves Horner enclosure conditional on sound interval addition and
multiplication. P27.36 proves uniqueness of an interior root from strict
monotonicity and states the intermediate-value obligation explicitly. P27.37
defines proof-carrying leaf contracts and a midpoint coverage lemma. P27.44
must connect these pieces into a serializable, independently checkable
certificate pipeline.

This document is a design specification for the remaining P27.44 work. The first formal tree/coverage layer is now implemented in P2744.lean and compiles in Lean CI (run 43794492273). The aggregate root-count and serialization layers below remain open. Nothing here is physical validation of CCFSM.

## Certificate layers

### 1. Problem identity

A certificate must identify, without ambiguity:

- schema version;
- coefficient order (descending degree first, as in P27.35);
- coefficient representation and exact interpretation;
- domain endpoints and their representation;
- the interval-arithmetic backend / certificate schema version;
- the arithmetic environment or exact-rational interpretation used by the
  checker.

The certificate must not silently coerce integers, decimal strings, NaN or
infinity into a different real problem.

### 2. Operation-enclosure evidence

The producer may submit intermediate interval-operation certificates for
Horner evaluation of the polynomial and its derivative. The independent
P27.43 checker can validate exact real addition, multiplication and division
ranges over finite binary64 endpoint intervals.

The current checker does not yet validate the provenance of the polynomial
expression tree, derivative coefficient construction, or the connection
between a submitted operation sequence and the declared coefficient list.
P27.44 must add expression/provenance binding (for example, a canonical
Horner instruction sequence with a coefficient-list digest) before accepting
an enclosure as evidence for the declared polynomial.

### 3. Leaf evidence

The logical leaf statuses should remain distinct:

- **no-root:** a proof that the polynomial has no root on the complete closed
  leaf interval;
- **unique interior root:** a witness of existence and a uniqueness proof on
  the open leaf interval, together with strict endpoint signs so that neither
  endpoint is itself another root;
- **boundary root:** an explicit point certificate for a root exactly at a
  subdivision boundary, with one deterministic ownership rule so the point
  is counted exactly once;
- **unresolved:** no root-count claim.

The existing P27.37 noRoot and unique constructors already carry their
logical evidence. The current unresolved constructor intentionally carries
no claim. P27.44 should extend this model carefully rather than infer
existence merely because an interval enclosure contains zero.

## Split-point ownership

P27.37 deliberately leaves a root at a shared midpoint unresolved in the two
adjacent closed child intervals. This is safe and avoids double counting, but
cannot yield a complete finite root count.

For a complete certificate, use an explicit boundary-root node or a
half-open ownership convention. The proof must establish:

1. the parent closed interval is covered by the two child intervals plus the
   shared midpoint;
2. a midpoint root is represented by one point certificate only;
3. the left and right open interiors do not include the midpoint;
4. a no-root child cannot be accepted if its closed interval contains the
   midpoint root;
5. a unique-interior-root child must separately exclude endpoint roots;
6. unresolved leaves keep the global upper root-count bound unbounded.

Do not solve this merely by deduplicating floating-point approximations of
root coordinates. The ownership rule belongs in the logical certificate.

## Tree structure and aggregate bounds

A proposed tree has:

- leaf(interval, evidence);
- split(parent, midpoint, left, right, midpoint_evidence).

Every node is indexed by exact parent endpoints. The split proof stores strict
ordering of endpoints and midpoint. Child intervals are closed for coverage;
root interiors are open, and midpoint evidence is separate.

For a fully sound aggregation:

- each accepted unique-interior-root leaf contributes one certified root;
- each accepted boundary-root node contributes one certified root;
- no-root leaves contribute zero;
- unresolved leaves contribute an unknown nonnegative count;
- the global lower bound is the number of pairwise-distinct certified root
  witnesses;
- a finite upper bound is emitted only when all domain points, including
  outer endpoints and every split point, have complete no-root/root evidence.

Pairwise distinctness follows from disjoint open leaf interiors plus unique
ownership of all boundary points. This must be proved, not inferred from
numerical proximity.

## Trust boundary

The producer/search algorithm is untrusted. It may fail to find roots or may
return unresolved leaves; that affects completeness, not soundness, provided
the checker rejects invalid claims.

The checker must independently verify:
- tree interval nesting and exact parent coverage;
- split-point ownership and no duplicate boundary-root nodes;
- each no-root interval exclusion;
- each unique-root existence and uniqueness argument;
- derivative strict sign and endpoint sign conditions when those are the
  chosen proof route;
- every interval-operation certificate and its link to the exact expression
  being evaluated;
- aggregate lower/upper root-count bounds.

Search completeness, termination under subdivision limits, and producer
performance remain separate from certificate soundness.

## Acceptance gates

P27.44 is complete only after:
1. a versioned data schema is fixed;
2. exact problem identity and expression provenance are bound;
3. split-point root ownership is formalized;
4. tree coverage and aggregate count bounds are proved in Lean;
5. the checker rejects malformed, incomplete and inconsistent certificates;
6. mutation tests demonstrate rejection of duplicate, missing and forged
   boundary-root evidence;
7. Python producer output is checked independently, without trusting the
   producer's root count or status labels.

No CCFSM constitutive law or material parameter is part of this certificate
pipeline. Software proof does not establish physical validity.


## Implemented first formal layer

P2744.lean now provides:

- a dependent RootIsolationTree indexed by its closed interval endpoints;
- proof-carrying leaves that reuse the P27.37 LeafCertificate;
- a separate SplitPointCertificate with only no-root, root, or unresolved
  claims at each midpoint;
- CoversPoint and a Lean theorem that every point of the parent closed domain
  is covered by a descendant leaf path;
- TreeEvidenceSound and a recursive theorem that all attached leaf and
  midpoint claims satisfy their logical contracts;
- FullyResolved as a structural predicate that excludes unresolved nodes.

The Lean CI build passed for this module (run 43794492273).

The module does not yet count certified roots, prove pairwise-distinct root
witnesses, certify outer endpoint roots, or compute a finite upper root-count
bound. FullyResolved alone must not be interpreted as a mathematically exact
root count. Those are explicit next proof obligations, together with
serialization and expression provenance.
