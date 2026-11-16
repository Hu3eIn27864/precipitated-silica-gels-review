import Std

/-!
# CCFSM P27.36: monotone polynomial root theorem contract

This module formalizes the order-theoretic core of the P27.36 argument.
A strict monotonicity certificate gives at most one interior zero. An
intermediate-value certificate plus strict opposite endpoint signs gives
existence. Their combination yields exactly one interior zero.

The module does NOT yet prove that an interval enclosure of the derivative
with strict sign implies strict monotonicity, nor does it prove the
intermediate-value property for the concrete real polynomial implementation.
Those are separate analytic obligations.
-/

namespace CCFSM.P2736

/-- A strict monotonicity condition restricted to the open interval. -/
def StrictMonoOn {α β : Type} [LT α] [LT β]
    (p : α → β) (lo hi : α) : Prop :=
  ∀ ⦃x y : α⦄, lo < x → x < hi → lo < y → y < hi →
    x < y → p x < p y

/-- A strict decreasing condition restricted to the open interval. -/
def StrictAntiOn {α β : Type} [LT α] [LT β]
    (p : α → β) (lo hi : α) : Prop :=
  ∀ ⦃x y : α⦄, lo < x → x < hi → lo < y → y < hi →
    x < y → p y < p x

/-- A function is strictly monotone if it is strictly increasing or decreasing. -/
def StrictlyMonotoneOn {α β : Type} [LT α] [LT β]
    (p : α → β) (lo hi : α) : Prop :=
  StrictMonoOn p lo hi ∨ StrictAntiOn p lo hi

/-- An interior zero of p on the open interval (lo, hi). -/
def InteriorZero {α β : Type} [LT α] [Zero β]
    (p : α → β) (lo hi x : α) : Prop :=
  lo < x ∧ x < hi ∧ p x = 0

/-- Strict monotonicity excludes two distinct interior zeros. -/
theorem monotone_roots_unique {α β : Type}
    [LT α] [LT β] [Zero β]
    (p : α → β) (lo hi : α)
    (hmono : StrictlyMonotoneOn p lo hi)
    (htrichotomy : ∀ x y : α, x < y ∨ x = y ∨ y < x)
    (hzero_irrefl : ¬ (0 : β) < 0)
    {x y : α}
    (hx : InteriorZero p lo hi x)
    (hy : InteriorZero p lo hi y) :
    x = y := by
  rcases htrichotomy x y with hxy | heq | hyx
  · rcases hmono with hinc | hdec
    · have hlt := hinc hx.1 hx.2.1 hy.1 hy.2.1 hxy
      rw [hx.2.2, hy.2.2] at hlt
      exact (hzero_irrefl hlt).elim
    · have hlt := hdec hx.1 hx.2.1 hy.1 hy.2.1 hxy
      rw [hx.2.2, hy.2.2] at hlt
      exact (hzero_irrefl hlt).elim
  · exact heq
  · rcases hmono with hinc | hdec
    · have hlt := hinc hy.1 hy.2.1 hx.1 hx.2.1 hyx
      rw [hy.2.2, hx.2.2] at hlt
      exact (hzero_irrefl hlt).elim
    · have hlt := hdec hy.1 hy.2.1 hx.1 hx.2.1 hyx
      rw [hy.2.2, hx.2.2] at hlt
      exact (lt_irrefl 0 hlt).elim

/-- Strictly opposite endpoint signs, in either orientation. -/
def CrossesZero {α β : Type} [LT β] [Zero β]
    (p : α → β) (lo hi : α) : Prop :=
  (p lo < 0 ∧ 0 < p hi) ∨ (p hi < 0 ∧ 0 < p lo)

/--
An explicit intermediate-value obligation for this particular interval.
For continuous real polynomials this is supplied by the intermediate value
theorem; the present core-Lean module treats it as a named assumption.
-/
structure IntermediateValueOn {α β : Type}
    [LT α] [LT β] [Zero β]
    (p : α → β) (lo hi : α) : Prop where
  exists_between :
    CrossesZero p lo hi →
      ∃ x, InteriorZero p lo hi x

/-- Monotonicity plus the intermediate-value property gives one interior zero. -/
theorem unique_root_of_monotone_crossing {α β : Type}
    [LT α] [LT β] [Zero β]
    (p : α → β) (lo hi : α)
    (hmono : StrictlyMonotoneOn p lo hi)
    (htrichotomy : ∀ x y : α, x < y ∨ x = y ∨ y < x)
    (hzero_irrefl : ¬ (0 : β) < 0)
    (hiv : IntermediateValueOn p lo hi)
    (hcross : CrossesZero p lo hi) :
    ∃ x, InteriorZero p lo hi x ∧
      ∀ y, InteriorZero p lo hi y → y = x := by
  obtain ⟨x, hx⟩ := hiv.exists_between hcross
  refine ⟨x, hx, ?_⟩
  intro y hy
  exact (monotone_roots_unique p lo hi hmono htrichotomy hzero_irrefl hy hx).symm

end CCFSM.P2736
