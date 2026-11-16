import CCFSM.P2734

/-!
# CCFSM P27.38: certified interval-multiplication interface

This module makes the multiplication obligation explicit and composes it
with the already proved P27.34 outward-addition contract. It deliberately
does not assert that a particular four-corner floating-point implementation
is sound: that implementation must supply the multiplication enclosure proof.
-/

namespace CCFSM.P2738

open CCFSM.P2735
open CCFSM.P2734

/--
A multiplication implementation is admissible only together with a proof
that every product of members of the input intervals is enclosed.
The endpoints may be computed by any method; their concrete correctness is
the responsibility of the supplied theorem.
-/
structure SoundIntervalMultiplication (α : Type)
    [LE α] [Mul α] where
  apply : Interval α → Interval α → Interval α
  encloses_products : ∀ (I J : Interval α) (x y : α),
    I.Contains x → J.Contains y → (apply I J).Contains (x * y)

/--
Assemble P27.34 outward addition and a separately certified multiplication
into the interval-arithmetic interface consumed by P27.35 Horner evaluation.
-/
def assemble {α : Type}
    [LE α] [Add α] [Mul α] [OfNat α 0]
    (addition : OutwardAddition α)
    (multiplication : SoundIntervalMultiplication α) :
    IntervalArithmetic α :=
  combineWithMultiplication addition multiplication.apply
    multiplication.encloses_products

/-- The assembled multiplication operation retains its enclosure guarantee. -/
theorem assemble_mul_sound {α : Type}
    [LE α] [Add α] [Mul α] [OfNat α 0]
    (addition : OutwardAddition α)
    (multiplication : SoundIntervalMultiplication α)
    (I J : Interval α) (x y : α)
    (hx : I.Contains x) (hy : J.Contains y) :
    ((assemble addition multiplication).mul I J).Contains (x * y) := by
  exact multiplication.encloses_products I J x y hx hy

/-- The assembled addition operation retains the P27.34 enclosure proof. -/
theorem assemble_add_sound {α : Type}
    [LE α] [Add α] [Mul α] [OfNat α 0]
    (addition : OutwardAddition α)
    (multiplication : SoundIntervalMultiplication α)
    (I J : Interval α) (x y : α)
    (hx : I.Contains x) (hy : J.Contains y) :
    ((assemble addition multiplication).add I J).Contains (x + y) := by
  exact intervalAdd_sound addition I J x y hx hy

end CCFSM.P2738
