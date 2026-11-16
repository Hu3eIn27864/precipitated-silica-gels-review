import CCFSM.P2735

/-!
# CCFSM P27.34: outward-rounded interval addition contract

This module isolates the scalar rounding obligations needed by interval
addition. It proves that endpoint construction is sound when the supplied
lower/upper rounding functions enclose exact addition and addition is
monotone. It does not implement or verify IEEE-754 nextafter itself.
-/

namespace CCFSM.P2734

open CCFSM.P2735

/--
A scalar outward-addition interface. A concrete IEEE-754 implementation
must separately establish lower_sound and upper_sound for every finite
input pair and must handle overflow according to its fail-closed policy.
-/
structure OutwardAddition (α : Type) [LE α] [Add α] where
  downAdd : α → α → α
  upAdd : α → α → α
  lower_sound : ∀ (a b : α), downAdd a b ≤ a + b
  upper_sound : ∀ (a b : α), a + b ≤ upAdd a b
  add_mono : ∀ {a b c d : α}, a ≤ b → c ≤ d → a + c ≤ b + d
  le_trans : ∀ {a b c : α}, a ≤ b → b ≤ c → a ≤ c

/-- Endpoint-wise outward-rounded interval addition. -/
def intervalAdd {α : Type} [LE α] [Add α]
    (ops : OutwardAddition α) (I J : Interval α) : Interval α :=
  ⟨ops.downAdd I.lower J.lower, ops.upAdd I.upper J.upper⟩

/-- Ordered input intervals produce an ordered output interval. -/
theorem intervalAdd_ordered {α : Type} [LE α] [Add α]
    (ops : OutwardAddition α) (I J : Interval α)
    (hI : I.lower ≤ I.upper) (hJ : J.lower ≤ J.upper) :
    (intervalAdd ops I J).lower ≤ (intervalAdd ops I J).upper := by
  unfold intervalAdd
  exact ops.le_trans (ops.lower_sound I.lower J.lower)
    (ops.le_trans (ops.add_mono hI hJ) (ops.upper_sound I.upper J.upper))

/--
Soundness of outward-rounded interval addition: every sum of points from
the input intervals belongs to the constructed output interval.
-/
theorem intervalAdd_sound {α : Type} [LE α] [Add α]
    (ops : OutwardAddition α) (I J : Interval α) (x y : α)
    (hx : I.Contains x) (hy : J.Contains y) :
    (intervalAdd ops I J).Contains (x + y) := by
  constructor
  · unfold intervalAdd Interval.Contains at *
    exact ops.le_trans (ops.lower_sound I.lower J.lower)
      (ops.add_mono hx.1 hy.1)
  · unfold intervalAdd Interval.Contains at *
    exact ops.le_trans (ops.add_mono hx.2 hy.2)
      (ops.upper_sound I.upper J.upper)

end CCFSM.P2734
