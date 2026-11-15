import unittest
from fractions import Fraction
from ccfsm_p26_17_independent_certificate import build_certificate_report
from ccfsm_p26_18_mesh_equivalence import compare_certificate_reports, rational_input_fingerprint

def primal_report(edges, means, rational=False):
    n=len(means)
    inputs={"edges":edges,"averages":means,"linear":(0,)*n,"quadratic":(0,)*n}
    assessment={"status":"feasible_exact_primal_witness","proof_level":"exact reference witness",
      "primal_witness":{"linear":(0,)*n,"quadratic":(0,)*n,
      "exact_certificate":{"cell_certificates":[
        {"lambda":0,"Q":((m,0),(0,0)),"determinant":0} for m in means]}}}
    return build_certificate_report(inputs,assessment)

class TestP2618MeshEquivalence(unittest.TestCase):
    def test_one_cell_and_two_cell_partition_same_global_targets(self):
        a=primal_report((0,1),(2,))
        b=primal_report((0,Fraction(1,2),1),(2,2))
        result=compare_certificate_reports(a,b)
        self.assertTrue(result["verified"])
        self.assertEqual(result["mesh_cell_counts"],[1,2])

    def test_decimal_and_fraction_aliases_canonicalize(self):
        a={"edges":("0","0.5","1"),"averages":("2","2"),
           "linear":("0","0"),"quadratic":("0","0")}
        b={"edges":(0,Fraction(1,2),1),"averages":(2,2),
           "linear":(0,0),"quadratic":(0,0)}
        self.assertEqual(rational_input_fingerprint(a),rational_input_fingerprint(b))

    def test_different_targets_not_equivalent(self):
        a=primal_report((0,1),(2,))
        b=primal_report((0,1),(3,))
        self.assertEqual(compare_certificate_reports(a,b)["status"],"different_global_targets")

    def test_unresolved_never_promoted(self):
        inputs={"edges":(0,1),"averages":(2,),"linear":(0,),"quadratic":(0,)}
        a=build_certificate_report(inputs,{"status":"unresolved"})
        b=build_certificate_report(inputs,{"status":"unresolved"})
        result=compare_certificate_reports(a,b)
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"],"same_target_but_unresolved")

    def test_changed_hash_is_rejected_before_comparison(self):
        a=primal_report((0,1),(2,))
        b=primal_report((0,1),(2,))
        b["inputs"]["averages"][0]="9"
        self.assertFalse(compare_certificate_reports(a,b)["verified"])

if __name__=="__main__": unittest.main()
