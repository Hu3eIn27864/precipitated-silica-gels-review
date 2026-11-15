import copy
import unittest
from fractions import Fraction
from ccfsm_p26_17_independent_certificate import build_certificate_report, verify_certificate_report

class TestP2617IndependentCertificate(unittest.TestCase):
    def setUp(self):
        self.inputs={"edges":(0,Fraction(1,2),1),"averages":(2,2),
                     "linear":(0,0),"quadratic":(0,0)}

    def test_primal_report_verified(self):
        assessment={"status":"feasible_exact_primal_witness","proof_level":"exact",
            "primal_witness":{"linear":(0,0),"quadratic":(0,0),
            "exact_certificate":{"cell_certificates":[
              {"lambda":0,"Q":((2,0),(0,0)),"determinant":0},
              {"lambda":0,"Q":((2,0),(0,0)),"determinant":0}]}}}
        report=build_certificate_report(self.inputs,assessment)
        result=verify_certificate_report(report)
        self.assertTrue(result["verified"])
        self.assertEqual(result["status"],"feasible_exact_primal_witness")

    def test_invalid_primal_gram_rejected(self):
        assessment={"status":"feasible_exact_primal_witness","primal_witness":{
            "linear":(0,0),"quadratic":(0,0),
            "exact_certificate":{"cell_certificates":[
              {"lambda":0,"Q":((2,0),(0,-1)),"determinant":-2},
              {"lambda":0,"Q":((2,0),(0,0)),"determinant":0}]}}}
        report=build_certificate_report(self.inputs,assessment)
        self.assertFalse(verify_certificate_report(report)["verified"])

    def test_dual_report_recomputed(self):
        inputs={"edges":(0,Fraction(2,5),1),"averages":(0,0),
                "linear":(1,0),"quadratic":(0,0)}
        assessment={"status":"certified_infeasible","dual_certificate":{
            "max_direction":8,"directions_checked":12,
            "certificate":{"direction":(1,0),"sqrt_digits":20}}}
        report=build_certificate_report(inputs,assessment)
        result=verify_certificate_report(report)
        self.assertTrue(result["verified"])
        self.assertEqual(result["status"],"certified_infeasible")

    def test_unresolved_is_not_promoted(self):
        report=build_certificate_report(self.inputs,{"status":"unresolved"})
        result=verify_certificate_report(report)
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"],"unresolved")

    def test_fingerprint_detects_mutation(self):
        report=build_certificate_report(self.inputs,{"status":"unresolved"})
        changed=copy.deepcopy(report); changed["inputs"]["averages"][0]="99"
        self.assertEqual(verify_certificate_report(changed)["status"],"invalid_report")

if __name__=="__main__": unittest.main()
