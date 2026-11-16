import CCFSM.P2738

/-!
# CCFSM P27.39: exact interval multiplication — nonnegative quadrant

This module proves the endpoint-product enclosure in the nonnegative
quadrant. It isolates the ordered-multiplication law as an explicit
algebraic assumption. No floating-point operations occur here.

The full four-sign-case theorem (including intervals crossing zero) is
deliberately left as a separate obligation; it must not be inferred from
this nonnegative-quadrant result alone.
-/

namespace CCFSM.P2739

open CCFSM.P2735

/--
Order laws needed for the nonnegative-quadrant multiplication theorem.
For a concrete ordered semiring these are standard consequences of
order-compatible multiplication, but the Lean kernel requires them to be
provided explicitly in this dependency-light project.
-/
structure NonnegativeProductOrder (α : Type)
    [LE α] [Mul α] [OfNat α 0] where
  le_trans : ∀ {a b c : α}, a ≤ b → b ≤ c → a ≤ c
  mul_mono_nonneg :
    ∀ {a b c d : α},
      0 ≤ a → a ≤ b → 0 ≤ c → c ≤ d → a * c ≤ b * d

/-- Exact endpoint product interval for two nonnegative intervals. -/
def nonnegativeProduct {α : Type}
    [LE α] [Mul α] [OfNat α 0]
    (I J : Interval α) : Interval α :=
  ⟨I.lower * J.lower, I.upper * J.upper⟩

/--
Four-factor monotonicity yields the exact lower endpoint bound in the
nonnegative quadrant: lower endpoints are nonnegative and each interior
point lies above its lower endpoint.
-/
theorem nonnegativeProduct_lower {α : Type}
    [LE α] [Mul α] [OfNat α 0]
    (ord : NonnegativeProductOrder α)
    (I J : Interval α) (x y : α)
    (hI0 : 0 ≤ I.lower) (hJ0 : 0 ≤ J.lower)
    (hx : I.Contains x) (hy : J.Contains y) :
    (I.lower * J.lower) ≤ x * y := by
  exact ord.mul_mono_nonneg hI0 hx.1 hJ0 hy.1

/--
The upper endpoint bound follows because membership and nonnegative lower
endpoints imply that the interior points are themselves nonnegative.
-/
theorem nonnegativeProduct_upper {α : Type}
    [LE α] [Mul α] [OfNat α 0]
    (ord : NonnegativeProductOrder α)
    (I J : Interval α) (x y : α)
    (hI0 : 0 ≤ I.lower) (hJ0 : 0 ≤ J.lower)
    (hx : I.Contains x) (hy : J.Contains y) :
    (x * y) ≤ (I.upper * J.upper) := by
  have hx0 : 0 ≤ x := ord.le_trans hI0 hx.1
  have hy0 : 0 ≤ y := ord.le_trans hJ0 hy.1
  exact ord.mul_mono_nonneg hx0 hx.2 hy0 hy.2

/-- Soundness of the exact endpoint-product interval in the nonnegative quadrant. -/
theorem nonnegativeProduct_sound {α : Type}
    [LE α] [Mul α] [OfNat α 0]
    (ord : NonnegativeProductOrder α)
    (I J : Interval α) (x y : α)
    (hI0 : 0 ≤ I.lower) (hJ0 : 0 ≤ J.lower)
    (hx : I.Contains x) (hy : J.Contains y) :
    (nonnegativeProduct I J).Contains (x * y) := by
  constructor
  · exact nonnegativeProduct_lower ord I J x y hI0 hJ0 hx hy
  · exact nonnegativeProduct_upper ord I J x y hI0 hJ0 hx hy

/--
The result is ordered when both input intervals are ordered and have
nonnegative lower endpoints.
-/
theorem nonnegativeProduct_ordered {α : Type}
    [LE α] [Mul α] [OfNat α 0]
    (ord : NonnegativeProductOrder α)
    (I J : Interval α)
    (hI : I.lower ≤ I.upper) (hJ : J.lower ≤ J.upper)
    (hI0 : 0 ≤ I.lower) (hJ0 : 0 ≤ J.lower) :
    (nonnegativeProduct I J).lower ≤ (nonnegativeProduct I J).upper := by
  exact ord.mul_mono_nonneg hI0 hI hJ0 hJ

end CCFSM.P2739
