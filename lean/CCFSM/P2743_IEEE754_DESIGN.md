# P27.43 design note — IEEE-754 refinement boundary

## Purpose

P27.42 proves the exact-real/algebraic four-corner enclosure under explicit
order and multiplication-monotonicity assumptions. The Python implementation
in `MODELLING/ccfsm/ccfsm_p27_34_interval_flux_filter.py` uses binary
floating-point operations followed by `math.nextafter`. These are different
proof layers. This note records the obligations before claiming that the
Python implementation refines the Lean interval operation.

## Representation boundary

The intended concrete representation is a finite IEEE-754 binary64 value.
Each finite value denotes its exact dyadic rational value. A formal bridge
must define this interpretation and establish that comparisons of finite
binary64 values agree with the order of their dyadic rational interpretations.
NaN and infinities are outside the interval endpoint domain.

## Arithmetic obligations

For every operation used to form an endpoint:

1. The hardware/runtime operation must return the correctly rounded
   round-to-nearest-even binary64 result for the exact operation, or the
   proof must model the actual permitted rounding mode.
2. `nextafter(r, -inf)` and `nextafter(r, +inf)` must be shown to return
   adjacent representable values in the requested direction, including
   signed zero and subnormal transitions.
3. If the rounded operation overflows to infinity, or outward stepping from
   the largest finite value reaches infinity, the interval constructor must
   reject the result (fail closed).
4. Underflow to signed or unsigned zero is not itself an error: outward
   stepping must still enclose the exact dyadic result. This includes products
   smaller than the least positive subnormal.
5. The four products and the min/max comparisons in multiplication must be
   finite before the outward endpoint is accepted. The exact four-corner
   theorem from P27.42 supplies the real-arithmetic enclosure once each
   computed corner is outward-enclosed.
6. Division must reject every denominator interval containing zero. Reciprocal
   endpoint rounding needs its own correctly-rounded division obligation.

## Existing Python behavior and tests

The implementation uses one `nextafter` step after a computed endpoint.
Its soundness is conditional on the runtime operation producing a correctly
rounded binary64 result under the expected rounding mode. The implementation
rejects non-finite interval endpoints and explicitly rejects non-finite raw
multiplication corner products. These checks are fail-closed behavior, not a
formal proof of the runtime's IEEE-754 conformance.

New regression tests compare multiplication endpoints with exact
`Fraction.from_float` corner products across sign combinations, subnormal
underflow, and overflow rejection. Such tests are useful falsification guards;
they do not replace universal proofs.

## Proof strategy options

- **Preferred near-term:** formalize finite binary64 values as exact dyadic
  rationals and prove the `nextafter` adjacency/order lemmas, then prove each
  arithmetic wrapper's outward enclosure.
- **Alternative:** keep the Python kernel as an untrusted producer and use a
  small exact-rational certificate checker. The checker validates endpoint
  inequalities; the producer's speed and completeness are then separate
  concerns.
- Do not treat randomized tests, sampled values, or a successful Lean build as
  proof of IEEE-754 refinement.

## Exit criteria

P27.43 is complete only when the representation map, comparison correctness,
directed-step behavior (including signed zero and subnormals), overflow policy,
and operation-specific enclosure theorems are all explicit and machine-checked.


## Implemented exact-rational checker prototype

The alternative certificate-checking path now has a small Python prototype:

- MODELLING/ccfsm/ccfsm_p27_43_rational_interval_certificate.py
- MODELLING/ccfsm/test_ccfsm_p27_43_rational_interval_certificate.py

The versioned certificate schema is ccfsm.interval-certificate.v1. It contains
an operation (add, mul, or div), two finite endpoint intervals, and
a claimed finite result interval. The checker requires each endpoint to be a JSON floating-point number and normalizes it to a
binary64 value, converts that value with Fraction.from_float, and recomputes
the exact real operation range. For multiplication and division it evaluates
the four exact rational corners; division is rejected when the denominator
interval contains zero. It returns exact rational range bounds and lower/upper
enclosure margins. A malformed certificate is rejected; a well-formed but
too-narrow result is reported as invalid.

This implementation is deliberately an independent verifier, not a producer.
It does not establish that the producer evaluated the intended expression,
that the supplied input intervals enclose an external physical quantity, or
that a particular runtime's nextafter conforms to IEEE-754. Signed zero is
identified with real zero by the rational interpretation, so bit-level signed
zero obligations remain open.

The ten focused tests cover addition, all four sign patterns and intervals
crossing zero for multiplication, rejected lower and upper endpoints,
subnormal underflow, positive and negative denominator intervals, division
through zero, overflow-range rejection, and malformed/non-finite input. An end-to-end test also checks outputs from the existing P27.34 interval producer. Integer JSON tokens are rejected to avoid silently rounding an exact integer into a different binary64 endpoint.
