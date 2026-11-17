# P27.48 — explicit endpoint-root evidence and closed-interval counts

## Objective

P27.45–P27.46 establish a sound and complete witness list for the **open**
interval `(lo, hi)`, provided the partition tree is fully resolved and the
stated strict-order laws are supplied. This is deliberately not yet a count
of roots in `[lo, hi]`: the outer endpoints are not interior witnesses.

P27.48 specifies the missing endpoint layer without changing the meaning of
the existing interior-count theorem.

## Mathematical decomposition

Assume `lo < hi` and let `R(x)` denote the root predicate. The closed-domain
root set is the disjoint union

```text
{ x | lo ≤ x ∧ x ≤ hi ∧ R(x) }
 =
{lo | R(lo)} ∪ {x | lo < x ∧ x < hi ∧ R(x)} ∪ {hi | R(hi)}.
```

Because `lo < hi`, the two endpoint coordinates differ, and neither endpoint
belongs to the open interval. Therefore the distinct-root count decomposes as

```text
N_closed = N_interior + 1[R(lo)] + 1[R(hi)].
```

Here `1[Q]` is 1 when proposition `Q` holds and 0 otherwise. The formula is
about **distinct coordinates**, not algebraic multiplicity. A root of
multiplicity 2 at an endpoint contributes one to this count.

## Endpoint evidence record

Each outer endpoint receives exactly one of three states:

- `Root`: a proof of `R(lo)` or `R(hi)`;
- `NoRoot`: a proof of its negation;
- `Unresolved`: no count contribution is permitted.

The endpoint evidence must be tied to the exact same endpoint value used by
the indexed `RootIsolationTree`; it must not be copied from a rounded,
reconstructed, or differently normalized coordinate.

A fully resolved closed-interval certificate therefore requires all of:

1. a `FullyResolved` interior partition tree;
2. sound endpoint evidence at `lo`;
3. sound endpoint evidence at `hi`;
4. a proof `lo < hi`;
5. the P27.46 order assumptions needed for interior completeness and
   duplicate-free witnesses.

If either endpoint is unresolved, the certificate may still report the
interior count, but it must not report an exact closed-interval count.

## Witness-list construction and ownership

The canonical closed witness list is ordered as:

```text
[lo if Root(lo)] ++ certifiedRootWitnesses(tree)
             ++ [hi if Root(hi)]
```

The endpoint is included once, independent of whether a neighboring leaf's
closed-domain exclusion or split convention mentions it. The tree's current
unique-root witnesses are strictly interior by construction (P27.45), so
neither endpoint can duplicate an interior witness. The strict inequality
`lo < hi` proves the two endpoint witnesses are distinct.

The checker should verify endpoint states directly and then verify the
interior witness list using P27.45/P27.46. It must not infer endpoint absence
from a list being complete only for the open interval.

## Relationship to Sturm certificates

For a polynomial represented exactly over `ℚ`, the P27.47 Sturm design uses
one-sided signs at `lo+` and `hi-` to count roots strictly inside the
interval. Endpoint evaluation `p(lo)=0` and `p(hi)=0` is a separate exact
test. This cleanly avoids accidental inclusion of endpoint roots in the
variation difference.

For uncertain coefficient intervals or measured coefficients, a point
polynomial endpoint test is not enough: the quantified uncertainty model
must be included in the certificate semantics.

## Lean implementation obligations

- Define an endpoint certificate indexed by the exact endpoint and root
  predicate, with constructors for root, no-root, and unresolved.
- Prove its soundness by cases.
- Define a closed witness collector that prepends/appends only certified
  endpoint roots.
- Prove its soundness for the closed interval.
- Prove pairwise distinctness using `lo < hi`, interior witness strictness,
  and P27.45's existing duplicate-freedom theorem.
- Prove the exact closed-count theorem from P27.46 plus the two endpoint
  truth values. Keep the open-interval theorem unchanged.
- Add tests for neither, either, and both endpoints being roots, including
  roots also appearing in adjacent closed leaf bounds.

## Acceptance criteria

P27.48 is complete only when the Lean module builds in CI and proves that
the closed witness list is sound, duplicate-free, and complete for
`lo ≤ x ∧ x ≤ hi ∧ R(x)`. A prose decomposition or tests alone do not meet
this gate.

## Scope

This is a formal counting and certificate-ownership task. It does not prove
that a numerical root-isolation algorithm finds every root, that floating
point endpoint values are exact physical boundaries, or that CCFSM's
constitutive equations are physically validated.


## Minimal acceptance examples

For a root predicate with a fully certified interior partition:

| Endpoint status | Interior count | Closed count |
|---|---:|---:|
| neither endpoint is a root | n | n |
| only lo is a root | n | n + 1 |
| only hi is a root | n | n + 1 |
| both endpoints are roots | n | n + 2 |

The four cases must be represented by endpoint proof terms, not inferred from
the witness-list length. A repeated endpoint root still contributes exactly
one coordinate. The case `lo = hi` is excluded from this theorem: it is a
singleton-domain problem and needs its own specification rather than applying
the two-endpoint formula.
