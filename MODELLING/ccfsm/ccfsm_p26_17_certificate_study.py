"""P26.17 reproducible certificate-report export for reference cases."""
from __future__ import annotations
import json
from pathlib import Path
from ccfsm_p26_15_global_primal_dual import assess_global_primal_dual_feasibility
from ccfsm_p26_17_independent_certificate import write_certificate_report, verify_certificate_report

def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[
      ("primal_constant_profile",(0,0.5,1),(2,2),(0,0),(0,0)),
      ("dual_zero_inventory_nonzero_modes",(0,0.4,1),(0,0),(1,0),(0,0)),
    ]
    rows=[]
    for name,edges,means,linear,quadratic in cases:
        inputs={"edges":edges,"averages":means,"linear":linear,"quadratic":quadratic}
        assessment=assess_global_primal_dual_feasibility(
            edges,means,linear,quadratic,max_direction=12,
            denominators=(1,),offset_radius=0,max_iterations=100)
        path=out/(name+".json")
        write_certificate_report(path,inputs,assessment)
        verified=verify_certificate_report(json.loads(path.read_text(encoding="utf-8")))
        rows.append({"case":name,"assessment_status":assessment["status"],
                     "independent_status":verified["status"],
                     "independently_verified":verified["verified"],"report":path.name})
        if assessment["status"] in ("feasible_exact_primal_witness","certified_infeasible") and not verified["verified"]:
            raise ArithmeticError("independent verifier rejected generated exact certificate: "+name)
    summary={"scope":"1-D exact rational P26 primal-dual certificate reporting","cases":rows,
             "rule":"unresolved reports are retained as unresolved and never promoted",
             "limitations":["finite dual and primal witness searches remain incomplete",
                            "independent verification is mathematical software verification only",
                            "no physical or experimental validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-17-results")
    run_study(p.parse_args().output_dir)
