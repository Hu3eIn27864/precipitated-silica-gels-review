"""P26.13: exact Markov-Lukacs/SOCP certificates for quadratic positivity.

For q(x)=m+a*x+b*(x**2-1/12) on [-1/2,1/2], nonnegativity is
equivalent to q(x)=[1,x] Q [1,x]^T + lam*(1/4-x^2), with Q positive
semidefinite and lam >= 0. The 2x2 PSD condition is checked exactly with
Fractions. This is a finite-dimensional conic representation, not a solver.
"""
from fractions import Fraction

from ccfsm_p26_8_verified_dual_certificate import _F
from ccfsm_p26_9_primal_dual_feasibility import _poly_min_exact
from ccfsm_p26_12_exact_affine_parameterization import (
    evaluate_exact_affine_parameterization, verify_affine_candidate,
)


def certify_cell_nonnegative(mean, linear, quadratic):
    """Return an exact Markov-Lukacs certificate, or None if q is negative."""
    m, a, b = map(_F, (mean, linear, quadratic))
    A0 = m - b / 12
    lower = max(Fraction(0), -b)
    upper = 4 * A0
    if lower > upper:
        return None
    # The determinant condition is maximized by this rational vertex,
    # clamped to the interval on which both diagonal entries are nonnegative.
    vertex = 2 * A0 - b / 2
    lam = min(upper, max(lower, vertex))
    q00 = A0 - lam / 4
    q01 = a / 2
    q11 = b + lam
    determinant = q00 * q11 - q01 * q01
    if q00 < 0 or q11 < 0 or determinant < 0 or lam < 0:
        return None
    # Verify coefficient identity and PSD conditions exactly.
    reconstructed = (q00 + lam / 4, 2 * q01, q11 - lam)
    expected = (m - b / 12, a, b)
    if reconstructed != expected:
        raise ArithmeticError("internal Markov-Lukacs identity failure")
    minimum = _poly_min_exact(m, a, b)
    if minimum < 0:
        raise ArithmeticError("PSD certificate contradicts exact polynomial minimum")
    return {
        "lambda": lam,
        "Q": ((q00, q01), (q01, q11)),
        "determinant": determinant,
        "minimum_exact": minimum,
        "identity_exact": True,
        "psd_exact": True,
    }


def verify_global_candidate(chart, linear, quadratic):
    """Verify all three global moments and one exact SOS certificate per cell."""
    moment_check = verify_affine_candidate(chart, linear, quadratic)
    certificates = tuple(
        certify_cell_nonnegative(m, a, b)
        for m, a, b in zip(chart["averages"], linear, quadratic)
    )
    positive = all(c is not None for c in certificates)
    return {
        "verified": moment_check["global_moments_exact"] and positive,
        "global_moments_exact": moment_check["global_moments_exact"],
        "cellwise_nonnegative_exact": positive,
        "moment_residuals_exact": moment_check["moment_residuals_exact"],
        "cell_certificates": certificates,
    }


def verify_free_coordinates(chart, free_values):
    """Apply the exact conic certificate after P26.12 affine reconstruction."""
    linear, quadratic = evaluate_exact_affine_parameterization(chart, free_values)
    result = verify_global_candidate(chart, linear, quadratic)
    result["linear"] = linear
    result["quadratic"] = quadratic
    return result


def run_study():
    cases = [
        ("strictly_positive", Fraction(2), Fraction(1, 5), Fraction(1, 7)),
        ("nonnegative_endpoint_touch", Fraction(1, 3), Fraction(1), Fraction(1)),
        ("zero_polynomial", Fraction(0), Fraction(0), Fraction(0)),
        ("negative_constant", Fraction(-1), Fraction(0), Fraction(0)),
        ("negative_interior", Fraction(1, 10), Fraction(0), Fraction(-2)),
    ]
    rows = []
    for name, m, a, b in cases:
        cert = certify_cell_nonnegative(m, a, b)
        rows.append({
            "case": name,
            "certified_nonnegative": cert is not None,
            "minimum_exact": str(_poly_min_exact(m, a, b)),
            "lambda": None if cert is None else str(cert["lambda"]),
            "determinant": None if cert is None else str(cert["determinant"]),
        })
    return {
        "scope": "exact Markov-Lukacs certificates for 1-D quadratic polynomials on [-1/2,1/2]",
        "cases": rows,
        "formulation": "q(x)=[1,x]Q[1,x]^T + lambda*(1/4-x^2), Q positive semidefinite, lambda>=0",
        "status": "certificate construction and verification only; no conic optimizer is included",
        "limitations": [
            "fixed cell means and piecewise quadratic fields in one dimension",
            "does not itself find globally coupled free coordinates satisfying all cell cones",
            "no 2-D/3-D extension and no physical validation",
        ],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_study(), indent=2))
