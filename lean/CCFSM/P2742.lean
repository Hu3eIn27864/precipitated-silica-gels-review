import CCFSM.P2741

/-!
# CCFSM P27.42: concrete four-corner extrema

A comparison tree computes the minimum and maximum of four endpoint products.
The accompanying lemmas prove that the returned values bound every corner.
Together with P27.41 this yields a concrete exact-arithmetic interval product.

The order is assumed total and transitive, and comparisons must be decidable.
No floating-point rounding theorem is claimed here.
-/

namespace CCFSM.P2742

/-- Binary minimum selected by a decidable order comparison. -/
def min2 {α : Type} [LE α] [DecidableLE α] (a b : α) : α :=
  if a ≤ b then a else b

/-- Binary maximum selected by a decidable order comparison. -/
def max2 {α : Type} [LE α] [DecidableLE α] (a b : α) : α :=
  if a ≤ b then b else a

/-- Minimum of four values, using a fixed comparison tree. -/
def min4 {α : Type} [LE α] [DecidableLE α]
    (a b c d : α) : α :=
  min2 (min2 a b) (min2 c d)

/-- Maximum of four values, using a fixed comparison tree. -/
def max4 {α : Type} [LE α] [DecidableLE α]
    (a b c d : α) : α :=
  max2 (max2 a b) (max2 c d)

/-- A binary minimum is no greater than its left argument. -/
theorem min2_le_left {α : Type} [LE α] [Mul α] [OfNat α 0] [DecidableLE α]
    (ord : CCFSM.P2741.FourCornerOrder α) (a b : α) :
    min2 a b ≤ a := by
  by_cases h : a ≤ b
  · simp only [min2, if_pos h]
    exact ord.le_refl a
  · have hba : b ≤ a := (ord.scalar.le_total a b).resolve_left h
    simp only [min2, if_neg h]
    exact hba

/-- A binary minimum is no greater than its right argument. -/
theorem min2_le_right {α : Type} [LE α] [Mul α] [OfNat α 0] [DecidableLE α]
    (ord : CCFSM.P2741.FourCornerOrder α) (a b : α) :
    min2 a b ≤ b := by
  by_cases h : a ≤ b
  · simp only [min2, if_pos h]
    exact h
  · simp only [min2, if_neg h]
    exact ord.le_refl b

/-- A binary maximum is no smaller than its left argument. -/
theorem left_le_max2 {α : Type} [LE α] [Mul α] [OfNat α 0] [DecidableLE α]
    (ord : CCFSM.P2741.FourCornerOrder α) (a b : α) :
    a ≤ max2 a b := by
  by_cases h : a ≤ b
  · simp only [max2, if_pos h]
    exact h
  · simp only [max2, if_neg h]
    exact ord.le_refl a

/-- A binary maximum is no smaller than its right argument. -/
theorem right_le_max2 {α : Type} [LE α] [Mul α] [OfNat α 0] [DecidableLE α]
    (ord : CCFSM.P2741.FourCornerOrder α) (a b : α) :
    b ≤ max2 a b := by
  by_cases h : a ≤ b
  · simp only [max2, if_pos h]
    exact ord.le_refl b
  · have hba : b ≤ a := (ord.scalar.le_total a b).resolve_left h
    simp only [max2, if_neg h]
    exact hba

/-- The four-value minimum is below each of its four inputs. -/
theorem min4_le_each {α : Type} [LE α] [Mul α] [OfNat α 0] [DecidableLE α]
    (ord : CCFSM.P2741.FourCornerOrder α) (a b c d : α) :
    min4 a b c d ≤ a ∧ min4 a b c d ≤ b ∧
    min4 a b c d ≤ c ∧ min4 a b c d ≤ d := by
  unfold min4
  have hab := min2_le_left ord a b
  have hcd := min2_le_left ord c d
  have hleft := min2_le_left ord (min2 a b) (min2 c d)
  have hright := min2_le_right ord (min2 a b) (min2 c d)
  have ha := min2_le_left ord a b
  have hb := min2_le_right ord a b
  have hc := min2_le_left ord c d
  have hd := min2_le_right ord c d
  exact ⟨ord.le_trans hleft ha, ord.le_trans hleft hb,
    ord.le_trans hright hc, ord.le_trans hright hd⟩

/-- The four-value maximum is above each of its four inputs. -/
theorem each_le_max4 {α : Type} [LE α] [Mul α] [OfNat α 0] [DecidableLE α]
    (ord : CCFSM.P2741.FourCornerOrder α) (a b c d : α) :
    a ≤ max4 a b c d ∧ b ≤ max4 a b c d ∧
    c ≤ max4 a b c d ∧ d ≤ max4 a b c d := by
  unfold max4
  have hleft := left_le_max2 ord (max2 a b) (max2 c d)
  have hright := right_le_max2 ord (max2 a b) (max2 c d)
  have ha := left_le_max2 ord a b
  have hb := right_le_max2 ord a b
  have hc := left_le_max2 ord c d
  have hd := right_le_max2 ord c d
  exact ⟨ord.le_trans ha hleft, ord.le_trans hb hleft,
    ord.le_trans hc hright, ord.le_trans hd hright⟩

/--
Concrete exact four-corner interval multiplication. Its soundness follows
from the comparison-tree bounds and the P27.41 envelope theorem.
-/
theorem four_corner_product_sound {α : Type}
    [LE α] [DecidableLE α] [Mul α] [OfNat α 0]
    (ord : CCFSM.P2741.FourCornerOrder α)
    (a b c d x y : α)
    (hab : a ≤ b) (hcd : c ≤ d)
    (hax : a ≤ x) (hxb : x ≤ b)
    (hcy : c ≤ y) (hyd : y ≤ d) :
    min4 (a * c) (a * d) (b * c) (b * d) ≤ x * y ∧
    x * y ≤ max4 (a * c) (a * d) (b * c) (b * d) := by
  have hmin := min4_le_each ord (a * c) (a * d) (b * c) (b * d)
  have hmax := each_le_max4 ord (a * c) (a * d) (b * c) (b * d)
  exact CCFSM.P2741.product_between_four_corners ord
    a b c d x y
    (min4 (a * c) (a * d) (b * c) (b * d))
    (max4 (a * c) (a * d) (b * c) (b * d))
    hab hcd hax hxb hcy hyd
    hmin.1 hmin.2.1 hmin.2.2.1 hmin.2.2.2
    hmax.1 hmax.2.1 hmax.2.2.1 hmax.2.2.2


/--
The exact interval operation induced by the four-corner extrema. This is an
abstract exact-arithmetic operation on the endpoint type; it does not add
floating-point rounding.
-/
def exactIntervalMultiply {α : Type}
    [LE α] [DecidableLE α] [Mul α] [OfNat α 0]
    (ord : CCFSM.P2741.FourCornerOrder α)
    (I J : CCFSM.P2735.Interval α) : CCFSM.P2735.Interval α :=
  ⟨min4 (I.lower * J.lower) (I.lower * J.upper)
      (I.upper * J.lower) (I.upper * J.upper),
    max4 (I.lower * J.lower) (I.lower * J.upper)
      (I.upper * J.lower) (I.upper * J.upper)⟩

/--
The concrete four-corner interval operation encloses every product of members
of two ordered input intervals. Membership itself supplies the input-order
proofs, so the adapter can satisfy P27.38's pointwise soundness contract.
-/
theorem exactIntervalMultiply_sound {α : Type}
    [LE α] [DecidableLE α] [Mul α] [OfNat α 0]
    (ord : CCFSM.P2741.FourCornerOrder α)
    (I J : CCFSM.P2735.Interval α) (x y : α)
    (hx : I.Contains x) (hy : J.Contains y) :
    (exactIntervalMultiply ord I J).Contains (x * y) := by
  change min4 (I.lower * J.lower) (I.lower * J.upper)
      (I.upper * J.lower) (I.upper * J.upper) ≤ x * y ∧
    x * y ≤ max4 (I.lower * J.lower) (I.lower * J.upper)
      (I.upper * J.lower) (I.upper * J.upper)
  exact four_corner_product_sound ord
    I.lower I.upper J.lower J.upper x y
    (ord.le_trans hx.1 hx.2) (ord.le_trans hy.1 hy.2)
    hx.1 hx.2 hy.1 hy.2

/--
Adapter from P27.42's concrete exact four-corner operation to the P27.38
multiplication contract. An instance for a concrete numeric type must still
supply the P27.41 signed-order laws; this theorem does not establish IEEE-754
rounding for machine floats.
-/
def asSoundIntervalMultiplication {α : Type}
    [LE α] [DecidableLE α] [Mul α] [OfNat α 0]
    (ord : CCFSM.P2741.FourCornerOrder α) :
    CCFSM.P2738.SoundIntervalMultiplication α :=
  { apply := exactIntervalMultiply ord
    encloses_products := by
      intro I J x y hx hy
      exact exactIntervalMultiply_sound ord I J x y hx hy }

end CCFSM.P2742
