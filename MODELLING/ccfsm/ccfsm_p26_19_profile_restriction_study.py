"""P26.19 exact profile restriction/coarsening reference study."""
from fractions import Fraction
import json
from pathlib import Path
from ccfsm_p26_19_exact_profile_restriction import round_trip_profile

def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[
      {"name":"one_cell_nonuniform_refinement","parent_edges":(0,1),"means":(2,),
       "linear":(Fraction(1,5),),"quadratic":(Fraction(1,10),),
       "fine_edges":(0,Fraction(1,4),Fraction(3,4),1)},
      {"name":"two_parent_cells","parent_edges":(0,Fraction(1,2),1),"means":(2,3),
       "linear":(0,Fraction(1,7)),"quadratic":(Fraction(1,10),Fraction(1,8)),
       "fine_edges":(0,Fraction(1,4),Fraction(1,2),Fraction(3,4),1)}
    ]
    results=[]
    for case in cases:
        result=round_trip_profile(case["parent_edges"],case["means"],case["linear"],
                                  case["quadratic"],case["fine_edges"])
        results.append({"name":case["name"],"round_trip_exact":result["round_trip_exact"],
                        "restricted":result["restriction"],"coarsened":result["coarsening"]})
    summary={"cases":results,"all_round_trips_exact":all(x["round_trip_exact"] for x in results),
      "mathematical_scope":"exact restriction and recovery of piecewise-quadratic cell polynomials on nested 1-D meshes",
      "limitations":["requires exact nested partitions with identical domain endpoints",
        "coarsening recovers a parent quadratic only when child data are exact restrictions of it",
        "equal global moments alone do not imply local profile equivalence",
        "no arbitrary nonmatching-mesh projection or 2-D/3-D extension",
        "software verification is not physical or experimental validation"]}
    if not summary["all_round_trips_exact"]: raise ArithmeticError("P26.19 exact local round-trip regression failed")
    (out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument("--output-dir",default="ccfsm-p26-19-results")
    run_study(parser.parse_args().output_dir)
