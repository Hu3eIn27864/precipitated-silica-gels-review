import unittest

from ccfsm_p27_37_adaptive_polynomial_root_isolation import isolate_polynomial_roots


class P2737AdaptivePolynomialRootIsolationTests(unittest.TestCase):
    def test_simple_linear_root_is_certified(self):
        result = isolate_polynomial_roots([1.0, -0.3], 0.0, 1.0)
        self.assertTrue(result["complete"])
        self.assertEqual(result["certified_unique_root_count"], 1)
        self.assertEqual(result["root_count_bounds"], (1, 1))
        roots = [x for x in result["leaves"] if x["status"] == "certified_unique_root"]
        self.assertEqual(len(roots), 1)
        self.assertLess(roots[0]["interval"][0], 0.3)
        self.assertGreater(roots[0]["interval"][1], 0.3)

    def test_two_simple_roots_are_isolated_separately(self):
        result = isolate_polynomial_roots([1.0, -0.9, 0.14], 0.0, 1.0)
        self.assertTrue(result["complete"])
        self.assertEqual(result["certified_unique_root_count"], 2)
        self.assertEqual(result["root_count_bounds"], (2, 2))

    def test_positive_polynomial_certified_root_free(self):
        result = isolate_polynomial_roots([1.0, 0.0, 1.0], 1.0, 2.0)
        self.assertTrue(result["complete"])
        self.assertEqual(result["certified_unique_root_count"], 0)
        self.assertEqual(result["root_count_bounds"], (0, 0))

    def test_tangential_root_remains_unresolved(self):
        result = isolate_polynomial_roots([1.0, -1.0, 0.25], 0.0, 1.0, max_depth=5)
        self.assertFalse(result["complete"])
        self.assertGreater(result["unresolved_leaf_count"], 0)
        self.assertIsNone(result["root_count_bounds"][1])

    def test_root_at_subdivision_boundary_is_not_double_counted(self):
        # The parent is not monotone; subdivision lands exactly on the simple
        # root x=0.5. Both closed child intervals retain an unresolved endpoint
        # leaf, so neither child claims the shared boundary root as interior.
        result = isolate_polynomial_roots(
            [1.0, -3.5, 3.76, -1.13], 0.0, 1.0, max_depth=5
        )
        self.assertFalse(result["complete"])
        self.assertEqual(result["certified_unique_root_count"], 0)
        self.assertIsNone(result["root_count_bounds"][1])
        boundary_leaves = [
            leaf for leaf in result["leaves"]
            if leaf["interval"][0] == 0.5 or leaf["interval"][1] == 0.5
        ]
        self.assertEqual(len(boundary_leaves), 2)
        self.assertTrue(all(leaf["root_count"] is None for leaf in boundary_leaves))

    def test_depth_limit_is_reported(self):
        # This polynomial is not monotone on the parent interval, so the
        # zero-depth budget must leave a genuinely unresolved root problem.
        result = isolate_polynomial_roots(
            [1.0, -3.5, 3.76, -1.13], 0.0, 1.0, max_depth=0
        )
        self.assertFalse(result["complete"])
        self.assertEqual(result["unresolved_leaf_count"], 1)
        self.assertEqual(result["leaves"][0]["status"], "unresolved_subdivision_limit")

    def test_partition_covers_domain_without_gaps(self):
        result = isolate_polynomial_roots([1.0, -0.3], 0.0, 1.0)
        leaves = result["leaves"]
        self.assertEqual(leaves[0]["interval"][0], 0.0)
        self.assertEqual(leaves[-1]["interval"][1], 1.0)
        for first, second in zip(leaves, leaves[1:]):
            self.assertEqual(first["interval"][1], second["interval"][0])

    def test_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            isolate_polynomial_roots([], 0.0, 1.0)
        with self.assertRaises(ValueError):
            isolate_polynomial_roots([float("nan"), 1.0], 0.0, 1.0)
        with self.assertRaises(ValueError):
            isolate_polynomial_roots([1.0, 0.0], 1.0, 0.0)
        with self.assertRaises(ValueError):
            isolate_polynomial_roots([1.0, 0.0], 0.0, 1.0, max_depth=-1)
        with self.assertRaises(ValueError):
            isolate_polynomial_roots([1.0, 0.0], 0.0, 1.0, min_width=0.0)


if __name__ == "__main__":
    unittest.main()
