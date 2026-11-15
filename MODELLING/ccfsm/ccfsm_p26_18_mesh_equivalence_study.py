"""P26.18 reproducible cross-partition and rational-alias comparison."""
from __future__ import annotations
import json
from pathlib import Path
from fractions import Fraction
from ccfsm_p26_17_independent_certificate import build_certificate_report, verify_certificate_report
from ccfsm_p26_18_mesh_equivalence import compare_certificate_reports, rational_input_fingerprint

def _reference_primal(edges, means):
    n=len(means)
    inputs={"edges":edges,"averages":means,"linear":(0,)*n,"quadratic":(0,)*n}
    assessment={"status":"feasible_exact_primal_witness","proof_level":"constructed exact constant-profile reference witness",
      "primal_witness":{"linear":(0,)*n,"quadratic":(0,)*n,
      "exact_certificate":{"cell_certificates":[
        {"lambda":0,"Q":((m,0),(0,0)),"determinant":0} for m in means]}}}
    return build_certificate_report(inputs,assessment)

def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    one=_reference_primal((0,1),(2,))
    two=_reference_primal((0,Fraction(1,2),1),(2,2))
    alias_inputs_a={"edges":("0","0.5","1"),"averages":("2","2"),
                    "linear":("0","0"),"quadratic":("0","0")}
    alias_inputs_b={"edges":(0,Fraction(1,2),1),"averages":(2,2),
                    "linear":(0,0),"quadratic":(0,0)}
    comparison=compare_certificate_reports(one,two)
    rows={"one_cell.json":one,"two_cells.json":two}
    for filename,report in rows.items():
        (out/filename).write_text(json.dumps(report,indent=2,sort_keys=True),encoding="utf-8")
    summary={"cross_partition_comparison":comparison,
      "rational_aliases_equal":rational_input_fingerprint(alias_inputs_a)==rational_input_fingerprint(alias_inputs_b),
      "independent_checks":{"one_cell":verify_certificate_report(one),
                            "two_cells":verify_certificate_report(two)},
      "scope":"same exact global moment targets and verified certificate status; not equality of local function spaces",
      "limitations":["different partitions may define different piecewise-polynomial feasible sets",
                     "moment equivalence does not prove equality of reconstructed local profiles",
                     "constructed reference witnesses test the verifier/comparator, not a new global solver",
                     "software verification is not physical or experimental validation"]}
    if not comparison["verified"] or not summary["rational_aliases_equal"]:
        raise ArithmeticError("P26.18 equivalence regression failed")
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument("--output-dir",default="ccfsm-p26-18-results")
    run_study(parser.parse_args().output_dir)
