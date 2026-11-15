"""P26.20 reproducible exact positivity-under-refinement study."""
from fractions import Fraction
import json
from pathlib import Path

from ccfsm_p26_13_markov_lukacs_socp import certify_cell_nonnegative
from ccfsm_p26_19_exact_profile_restriction import restrict_quadratic_profile
from ccfsm_p26_20_refinement_positivity import verify_refined_profile_certificates


def _run_case(name, parent_edges, means, linear, quadratic, fine_edges):
    profile = restrict_quadratic_profile(parent_edges, means, linear, quadratic, fine_edges)
    certs = []
    for m, a, b in zip(profile["averages"], profile["linear"], profile["quadratic"]):
        # Restriction exports exact rational strings; normalize before P26.13.
        cert = certify_cell_nonnegative(*(Fraction(str(v)) for v in (m, a, b)))
        if cert is None:
            raise ArithmeticError("%s: a restricted child lost nonnegativity" % name)
        certs.append(cert)
    verification = verify_refined_profile_certificates(profile, certs)
    if not verification["verified"]:
        raise ArithmeticError("%s: independent child-certificate verification failed" % name)
    return {"name": name, "parent_cells": len(means), "child_cells": len(fine_edges) - 1,
            "child_certificates_verified": len(certs), "all_verified": verification["verified"],
            "minimum_child_polynomial_value": [str(cert["minimum_exact"]) for cert in certs]}


def run_study(output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    cases = [
        _run_case("strictly_positive_nonuniform", (0, 1), (2,),
                  (Fraction(1, 5),), (Fraction(1, 10),),
                  (0, Fraction(1, 7), Fraction(1, 2), Fraction(5, 6), 1)),
        _run_case("endpoint_touching", (0, 1), (Fraction(1, 3),), (1,), (1,),
                  (0, Fraction(1, 3), Fraction(2, 3), 1)),
        _run_case("zero_profile", (0, 1), (0,), (0,), (0,),
                  (0, Fraction(1, 4), Fraction(3, 4), 1)),
        _run_case("two_parent_cells", (0, Fraction(1, 2), 1), (2, 3),
                  (0, Fraction(1, 7)), (Fraction(1, 10), Fraction(1, 8)),
                  (0, Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), 1)),
    ]
    summary = {
        "scope": "exact positivity preservation for 1-D piecewise-quadratic profiles on nested meshes",
        "cases": cases,
        "all_child_certificates_verified": all(c["all_verified"] for c in cases),
        "independent_verifier": "Fraction-only identity and 2x2 PSD check; no P26.13 constructor import",
        "limitations": [
            "exact restriction preserves the same polynomial, not arbitrary remapping",
            "certificate construction uses P26.13; verification is independently implemented",
            "only rational 1-D nested meshes and quadratic cell profiles",
            "no 2-D/3-D extension and no physical or experimental validation",
        ],
    }
    if not summary["all_child_certificates_verified"]:
        raise ArithmeticError("P26.20 study did not verify every child certificate")
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True),
                                      encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="ccfsm-p26-20-results")
    run_study(parser.parse_args().output_dir)
