"""P26.20: exact positivity preservation and independent SOS certificate checks."""
from fractions import Fraction


def _F(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a rational certificate value")
    if isinstance(value, Fraction):
        return value
    return Fraction(str(value))


def verify_cell_certificate(mean, linear, quadratic, certificate):
    """Independently verify q=[1,x]Q[1,x]^T+lambda(1/4-x^2), Q PSD."""
    try:
        m, a, b = map(_F, (mean, linear, quadratic))
        lam = _F(certificate["lambda"])
        Q = certificate["Q"]
        q00, q01, q10, q11 = _F(Q[0][0]), _F(Q[0][1]), _F(Q[1][0]), _F(Q[1][1])
        if q01 != q10:
            return {"verified": False, "reason": "gram_matrix_not_symmetric"}
        determinant = q00 * q11 - q01 * q01
        if lam < 0 or q00 < 0 or q11 < 0 or determinant < 0:
            return {"verified": False, "reason": "non_psd_gram_or_negative_multiplier"}
        if q00 + lam / 4 != m - b / 12 or 2 * q01 != a or q11 - lam != b:
            return {"verified": False, "reason": "polynomial_identity_mismatch"}
        if "determinant" in certificate and _F(certificate["determinant"]) != determinant:
            return {"verified": False, "reason": "determinant_field_mismatch"}
        return {"verified": True, "reason": "exact_identity_and_psd"}
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError):
        return {"verified": False, "reason": "malformed_certificate"}


def verify_refined_profile_certificates(refined_profile, certificates):
    """Check every child certificate against the exact restricted coefficients."""
    means = refined_profile["averages"]
    linear = refined_profile["linear"]
    quadratic = refined_profile["quadratic"]
    if not (len(means) == len(linear) == len(quadratic) == len(certificates)):
        return {"verified": False, "cell_results": (), "reason": "cell_count_mismatch"}
    results = tuple(verify_cell_certificate(m, a, b, cert)
                    for m, a, b, cert in zip(means, linear, quadratic, certificates))
    ok = all(item["verified"] for item in results)
    return {"verified": ok, "cell_results": results,
            "reason": "all_child_certificates_verified" if ok
                      else "one_or_more_child_certificates_invalid"}
