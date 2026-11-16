import CCFSM.P2740

/-!
# CCFSM P27.41: four-corner product envelope

This module proves a global enclosure statement without choosing a concrete
min/max operator: every common lower bound of the four corner products is a
lower bound for every interior product, and every common upper bound is an
upper bound for every interior product.

The result is exact algebra over explicit order-compatible multiplication
laws. It does not establish IEEE-754 directed rounding.
-/

namespace CCFSM.P2741

/--
Transitivity is kept explicit because this Lean project intentionally avoids
a dependency on Mathlib's ordered-ring hierarchy.
-/
structure FourCornerOrder (α : Type)
    [LE α] [Mul α] [OfNat α 0] where
  scalar : CCFSM.P2740.SignedProductOrder α
  le_trans : ∀ {p q r : α}, p ≤ q → q ≤ r → p ≤ r

/--
The product of two points in ordered intervals lies between every common
lower and upper bound of the four endpoint products.

This is the four-corner extremum property in order-theoretic form. A concrete
min4/max4 implementation can be connected later by proving that its outputs
are respectively common lower and upper bounds of the four corners.
-/
theorem product_between_four_corners {α : Type}
    [LE α] [Mul α] [OfNat α 0]
    (ord : FourCornerOrder α)
    (a b c d x y lower upper : α)
    (hab : a ≤ b) (hcd : c ≤ d)
    (hax : a ≤ x) (hxb : x ≤ b)
    (hcy : c ≤ y) (hyd : y ≤ d)
    (hl_ac : lower ≤ a * c) (hl_ad : lower ≤ a * d)
    (hl_bc : lower ≤ b * c) (hl_bd : lower ≤ b * d)
    (hu_ac : a * c ≤ upper) (hu_ad : a * d ≤ upper)
    (hu_bc : b * c ≤ upper) (hu_bd : b * d ≤ upper) :
    lower ≤ x * y ∧ x * y ≤ upper := by
  have hxc := CCFSM.P2740.right_scalar_between_endpoints
    ord.scalar c a x b hab hax hxb
  have hxd := CCFSM.P2740.right_scalar_between_endpoints
    ord.scalar d a x b hab hax hxb
  have hl_xc : lower ≤ x * c := by
    cases hxc with
    | inl h =>
        exact ord.le_trans hl_ac h.1
    | inr h =>
        exact ord.le_trans hl_bc h.1
  have hu_xc : x * c ≤ upper := by
    cases hxc with
    | inl h =>
        exact ord.le_trans h.2 hu_bc
    | inr h =>
        exact ord.le_trans h.2 hu_ac
  have hl_xd : lower ≤ x * d := by
    cases hxd with
    | inl h =>
        exact ord.le_trans hl_ad h.1
    | inr h =>
        exact ord.le_trans hl_bd h.1
  have hu_xd : x * d ≤ upper := by
    cases hxd with
    | inl h =>
        exact ord.le_trans h.2 hu_bd
    | inr h =>
        exact ord.le_trans h.2 hu_ad
  have hxy := CCFSM.P2740.left_scalar_between_endpoints
    ord.scalar x c y d hcd hcy hyd
  constructor
  · cases hxy with
    | inl h =>
        exact ord.le_trans hl_xc h.1
    | inr h =>
        exact ord.le_trans hl_xd h.1
  · cases hxy with
    | inl h =>
        exact ord.le_trans h.2 hu_xd
    | inr h =>
        exact ord.le_trans h.2 hu_xc

end CCFSM.P2741
