"""Tests for recipe-to-speciation equilibrium in CCFSM v0.4a."""
import unittest
from ccfsm_recipe_speciation_v04a import (
    SodiumSilicateRecipe, solve_sodium_silicate_sulfuric_acid)


def recipe(**overrides):
    values=dict(total_silica_mol_l=0.10,silicate_modulus=3.3,
                sulfuric_acid_mol_l=0.0,activity_model="davies")
    values.update(overrides)
    return SodiumSilicateRecipe(**values)


class TestRecipeSpeciation(unittest.TestCase):
    def test_sodium_silicate_alone_is_alkaline(self):
        r=solve_sodium_silicate_sulfuric_acid(recipe())
        self.assertGreater(r.pH,9.0)
        self.assertLess(r.pH,14.0)

    def test_more_sulfuric_acid_lowers_pH(self):
        a=solve_sodium_silicate_sulfuric_acid(recipe())
        b=solve_sodium_silicate_sulfuric_acid(recipe(sulfuric_acid_mol_l=0.035))
        self.assertLess(b.pH,a.pH)

    def test_electroneutrality_and_analytical_balances_close(self):
        r=solve_sodium_silicate_sulfuric_acid(recipe(sulfuric_acid_mol_l=0.025))
        self.assertLess(abs(r.charge_residual_mol_l),1e-9)
        self.assertLess(abs(r.dissolved_silicon_residual_mol_l),1e-10)
        self.assertLess(abs(r.sulfate_balance_residual_mol_l),1e-10)
        self.assertLess(abs(r.sodium_balance_residual_mol_l),1e-10)

    def test_sulfate_pairing_is_nonnegative_and_balanced(self):
        r=solve_sodium_silicate_sulfuric_acid(recipe(sulfuric_acid_mol_l=0.03))
        self.assertGreaterEqual(r.sodium_sulfate_pair_mol_l,0.0)
        self.assertGreaterEqual(r.bisulfate_mol_l,0.0)
        self.assertGreaterEqual(r.sulfate_mol_l,0.0)
        self.assertLessEqual(r.sodium_sulfate_pair_mol_l,0.03)

    def test_dissolved_fraction_applies_to_silica_speciation(self):
        r=solve_sodium_silicate_sulfuric_acid(recipe(dissolved_silica_fraction=0.5))
        self.assertAlmostEqual(r.dissolved_silicon_total_mol_l,0.05,places=10)

    def test_stock_solution_mixing_calculates_final_totals(self):
        r=SodiumSilicateRecipe.from_stock_solutions(
            silicate_stock_silica_mol_l=1.0,silicate_modulus=3.3,
            silicate_stock_volume_l=0.1,sulfuric_acid_stock_mol_l=1.0,
            sulfuric_acid_stock_volume_l=0.01,water_volume_l=0.89)
        self.assertAlmostEqual(r.total_silica_mol_l,0.1)
        self.assertAlmostEqual(r.sulfuric_acid_mol_l,0.01)
        self.assertAlmostEqual(r.total_sodium_mol_l,2*0.1/3.3)

    def test_davies_refuses_extrapolation_above_limit(self):
        with self.assertRaises(ValueError):
            solve_sodium_silicate_sulfuric_acid(recipe(
                total_silica_mol_l=1.0,sulfuric_acid_mol_l=0.5,
                max_davies_ionic_strength_mol_l=0.5))

    def test_ideal_activity_is_an_explicit_option(self):
        r=solve_sodium_silicate_sulfuric_acid(recipe(activity_model="ideal"))
        self.assertEqual(r.activity_model,"ideal")
        self.assertGreater(r.ionic_strength_mol_l,0.0)

    def test_invalid_recipe_is_rejected(self):
        with self.assertRaises(ValueError):
            recipe(silicate_modulus=0.0)
        with self.assertRaises(ValueError):
            recipe(dissolved_silica_fraction=1.1)
        with self.assertRaises(ValueError):
            SodiumSilicateRecipe.from_stock_solutions(
                silicate_stock_silica_mol_l=1.0,silicate_modulus=3.3,
                silicate_stock_volume_l=0.0,sulfuric_acid_stock_mol_l=1.0,
                sulfuric_acid_stock_volume_l=0.0,water_volume_l=0.0)


if __name__=="__main__":
    unittest.main()
