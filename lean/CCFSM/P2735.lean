import Std

/-!
# CCFSM P27.35: Horner evaluation and interval enclosure

Coefficients are stored in ascending order (constant term first):
[a₀, a₁, ..., aₙ] denotes a₀ + a₁*x + ... + aₙ*xⁿ.

The theorem below is parametric in the interval operations.  It proves that
Horner evaluation is enclosure-preserving whenever interval addition and
multiplication satisfy their stated soundness contracts.  It does not yet
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

theorem Interval.point_contains {α : Type} [LE α] (x : α) :
    (Interval.point x).Contains x := by
  exact ⟨le_rfl, le_rfl⟩

/--
An interval arithmetic implementation together with the two obligations
needed by the Horner enclosure theorem.  Concrete endpoint arithmetic must
prove these obligations before it can be used as a certified implementation.
-/
structure IntervalArithmetic (α : Type) [LE α] [Add α] [Mul α] where
  add : Interval α → Interval α → Interval α
  mul : Interval α → Interval α → Interval α
  add_sound : ∀ (I J : Interval α) (x y : α),
    I.Contains x → J.Contains y → (add I J).Contains (x + y)
  mul_sound : ∀ (I J : Interval α) (x y : α),
    I.Contains x → J.Contains y → (mul I J).Contains (x * y)

/--
Exact scalar Horner evaluation.  The coefficient list is in ascending
degree order, so [a₀, a₁, ..., aₙ] evaluates to
a₀ + x*(a₁ + x*(... + x*aₙ)).
-/
def horner {α : Type} [Add α] [Mul α] [OfNat α 0] :
    List α → α → α
  | [], _ => 0
  | a :: rest, x => a + x * horner rest x

/-- Interval Horner evaluation using a supplied sound interval arithmetic. -/
def hornerInterval {α : Type} [LE α] [Add α] [Mul α] [OfNat α 0]
    (ops : IntervalArithmetic α) :
    List α → Interval α → Interval α
  | [], _ => Interval.point 0
  | a :: rest, X =>
      ops.add (Interval.point a) (ops.mul X (hornerInterval ops rest X))

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
      simp [hornerInterval, horner, Interval.Contains, Interval.point]
  | cons a rest ih =>
      change (ops.add (Interval.point a)
        (ops.mul X (hornerInterval ops rest X))).Contains
        (a + x * horner rest x)
      exact ops.add_sound (Interval.point a) (ops.mul X (hornerInterval ops rest X))
        a (x * horner rest x)
        (Interval.point_contains a)
        (ops.mul_sound X (hornerInterval ops rest X) x (horner rest x)
          hx (ih hx))

end CCFSM.P2735
