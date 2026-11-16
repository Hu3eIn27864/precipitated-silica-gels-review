import Std

/-!
# CCFSM P27.35: Horner evaluation and interval enclosure

Coefficients are stored in descending order (highest degree first), matching
the Python P27.35 implementation:
[aₙ, ..., a₁, a₀] denotes aₙ*xⁿ + ... + a₁*x + a₀.

The theorem below is parametric in the interval operations. It proves that
Horner evaluation is enclosure-preserving whenever interval addition and
multiplication satisfy their stated soundness contracts. It does not yet
instantiate those contracts with concrete endpoint arithmetic, nor does it
claim IEEE-754 outward-rounding correctness.
-/

namespace CCFSM.P2735

/-- A closed interval represented by its lower and upper endpoints. -/
structure Interval (α : Type) where
  lower : α
  upper : α

/-- Membership in the closed interval. -/
def Interval.Contains {α : Type} [LE α] (I : Interval α) (x : α) : Prop :=
  I.lower ≤ x ∧ x ≤ I.upper

/-- The degenerate interval containing exactly its point (over a partial order). -/
def Interval.point {α : Type} (x : α) : Interval α :=
  ⟨x, x⟩

/--
An interval arithmetic implementation together with the two obligations
needed by the Horner enclosure theorem. Concrete endpoint arithmetic must
prove these obligations before it can be used as a certified implementation.
-/
structure IntervalArithmetic (α : Type) [LE α] [Add α] [Mul α] where
  add : Interval α → Interval α → Interval α
  mul : Interval α → Interval α → Interval α
  point_sound : ∀ x : α, (Interval.point x).Contains x
  add_sound : ∀ (I J : Interval α) (x y : α),
    I.Contains x → J.Contains y → (add I J).Contains (x + y)
  mul_sound : ∀ (I J : Interval α) (x y : α),
    I.Contains x → J.Contains y → (mul I J).Contains (x * y)

/--
Exact scalar Horner evaluation. The coefficient list is in descending
degree order, matching P27.35's Python API.
-/
def horner {α : Type} [Add α] [Mul α] [OfNat α 0] :
    List α → α → α
  | [], _ => 0
  | a :: rest, x => x * horner rest x + a

/-- Interval Horner evaluation using a supplied sound interval arithmetic. -/
def hornerInterval {α : Type} [LE α] [Add α] [Mul α] [OfNat α 0]
    (ops : IntervalArithmetic α) :
    List α → Interval α → Interval α
  | [], _ => Interval.point 0
  | a :: rest, X =>
      ops.add (ops.mul X (hornerInterval ops rest X)) (Interval.point a)

/--
P27.35 core enclosure theorem: if x belongs to X, then the exact polynomial
value at x belongs to the interval returned by interval Horner evaluation.
The proof uses only the soundness contracts of interval addition and
multiplication; it does not hide any floating-point assumptions.
-/
theorem hornerInterval_sound {α : Type}
    [LE α] [Add α] [Mul α] [OfNat α 0]
    (ops : IntervalArithmetic α)
    (coefficients : List α) (X : Interval α) (x : α)
    (hx : X.Contains x) :
    (hornerInterval ops coefficients X).Contains (horner coefficients x) := by
  induction coefficients with
  | nil =>
      change (Interval.point (0 : α)).Contains 0
      exact ops.point_sound 0
  | cons a rest ih =>
      change (ops.add (ops.mul X (hornerInterval ops rest X))
        (Interval.point a)).Contains (x * horner rest x + a)
      exact ops.add_sound (ops.mul X (hornerInterval ops rest X))
        (Interval.point a) (x * horner rest x) a
        (ops.mul_sound X (hornerInterval ops rest X) x (horner rest x)
          hx ih)
        (ops.point_sound a)

end CCFSM.P2735
