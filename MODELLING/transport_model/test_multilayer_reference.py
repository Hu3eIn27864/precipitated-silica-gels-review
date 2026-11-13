#!/usr/bin/env python3
"""Independent three-layer transfer-matrix eigenvalue verification."""
import math
import unittest
from multilayer_reference import multilayer_eigenvalues, multilayer_characteristic


class MultilayerReferenceTests(unittest.TestCase):
    def test_identical_three_layers_recover_homogeneous_spectrum(self):
        length = 1.0
        rates = multilayer_eigenvalues([2.0]*3, [0.5]*3,
                                       [0.2, 0.3, 0.5], n_modes=5)
        expected = [0.5/2.0*(n*math.pi/length)**2 for n in range(1, 6)]
        for actual, reference in zip(rates, expected):
            self.assertAlmostEqual(actual, reference, places=8)

    def test_heterogeneous_three_layer_modes_are_ordered_and_roots(self):
        storage = [1.0, 2.0, 0.7]
        mobility = [1.0, 0.15, 0.6]
        widths = [0.25, 0.4, 0.35]
        rates = multilayer_eigenvalues(storage, mobility, widths, n_modes=6)
        self.assertTrue(all(b > a for a, b in zip(rates, rates[1:])))
        for rate in rates:
            residual = multilayer_characteristic(
                math.sqrt(rate), storage, mobility, widths)
            self.assertLess(abs(residual), 2e-9)


    def test_contact_resistance_zero_limit_and_slower_modes(self):
        s=[1.0,2.0,0.7]; lam=[1.0,0.15,0.6]; w=[0.25,0.4,0.35]
        base=multilayer_eigenvalues(s,lam,w,n_modes=4)
        zero=multilayer_eigenvalues(s,lam,w,n_modes=4,contact_resistances=[0.0,0.0])
        finite=multilayer_eigenvalues(s,lam,w,n_modes=4,contact_resistances=[0.03,0.08])
        for a,b in zip(base,zero):
            self.assertAlmostEqual(a,b,places=11)
        self.assertTrue(all(x<y for x,y in zip(finite,base)))
        for rate in finite:
            self.assertLess(abs(multilayer_characteristic(
                math.sqrt(rate),s,lam,w,[0.03,0.08])),2e-9)

    def test_contact_resistance_validation(self):
        with self.assertRaises(ValueError):
            multilayer_eigenvalues([1.0,2.0],[1.0,1.0],[0.5,0.5],
                                   contact_resistances=[-0.1])
        with self.assertRaises(ValueError):
            multilayer_eigenvalues([1.0,2.0],[1.0,1.0],[0.5,0.5],
                                   contact_resistances=[0.1,0.2])

    def test_rejects_invalid_layer_definitions(self):
        with self.assertRaises(ValueError):
            multilayer_eigenvalues([1.0, 2.0], [1.0], [0.5, 0.5])
        with self.assertRaises(ValueError):
            multilayer_eigenvalues([1.0], [0.0], [1.0])


if __name__ == "__main__":
    unittest.main()
