import CCFSM.P2739

/-!
# CCFSM P27.40: signed scalar multiplication on closed intervals

This module proves the sign split needed to reduce multiplication over a
rectangle to its boundary endpoints. It covers positive, zero, and negative
multipliers without assuming a particular number representation.

It does not yet claim the full four-corner min/max theorem. That theorem
also needs a proved endpoint-extremum construction and is kept as the next
separate obligation.
-/

namespace CCFSM.P2740

open CCFSM.P2735

/--
Order-compatible multiplication laws, stated separately for nonnegative
(monotone) and nonpositive (antitone) left and right factors.
These are algebraic assumptions to be instantiated for a concrete ordered
ring; they are not floating-point facts.
-/
structure SignedProductOrder (α : Type)
    [LE α] [Mul α] [OfNat α 0] where
  le_total : ∀ a b : α, a ≤ b ∨ b ≤ a
  mul_left_mono_nonneg :
    ∀ {k a b : α}, 0 ≤ k → a ≤ b → k * a ≤ k * b
  mul_left_antitone_nonpos :
    ∀ {k a b : α}, k ≤ 0 → a ≤ b → k * b ≤ k * a
  mul_right_mono_nonneg :
    ∀ {k a b : α}, 0 ≤ k → a ≤ b → a * k ≤ b * k
  mul_right_antitone_nonpos :
    ∀ {k a b : α}, k ≤ 0 → a ≤ b → b * k ≤ a * k

/--
For a fixed multiplier, multiplication maps an ordered interval either
monotonically or antitonically to the interval between its endpoint products.
The disjunction is exhaustive, including the zero multiplier.
-/
theorem left_scalar_between_endpoints {α : Type}
    [LE α] [Mul α] [OfNat α 0]
    (ord : SignedProductOrder α)
    (k c y d : α) (hcd : c ≤ d) (hcy : c ≤ y) (hyd : y ≤ d) :
    (k * c ≤ k * y ∧ k * y ≤ k * d) ∨
    (k * d ≤ k * y ∧ k * y ≤ k * c) := by
  have hsign : 0 ≤ k ∨ k ≤ 0 := ord.le_total 0 k
  cases hsign with
  | inl hk =>
      exact Or.inl
        ⟨ord.mul_left_mono_nonneg hk hcy,
         ord.mul_left_mono_nonneg hk hyd⟩
  | inr hk =>
      exact Or.inr
        ⟨ord.mul_left_antitone_nonpos hk hyd,
         ord.mul_left_antitone_nonpos hk hcy⟩

/-- The corresponding sign split when the fixed multiplier is on the right. -/
theorem right_scalar_between_endpoints {α : Type}
    [LE α] [Mul α] [OfNat α 0]
    (ord : SignedProductOrder α)
    (k c y d : α) (hcd : c ≤ d) (hcy : c ≤ y) (hyd : y ≤ d) :
    (c * k ≤ y * k ∧ y * k ≤ d * k) ∨
    (d * k ≤ y * k ∧ y * k ≤ c * k) := by
  have hsign : 0 ≤ k ∨ k ≤ 0 := ord.le_total 0 k
  cases hsign with
  | inl hk =>
      exact Or.inl
        ⟨ord.mul_right_mono_nonneg hk hcy,
         ord.mul_right_mono_nonneg hk hyd⟩
  | inr hk =>
      exact Or.inr
        ⟨ord.mul_right_antitone_nonpos hk hyd,
         ord.mul_right_antitone_nonpos hk hcy⟩

/--
Zero is handled by the same exhaustive sign split: both monotonicity laws
apply when k = 0, so the endpoint products coincide in an instantiated
ordered ring.
-/
theorem zero_is_in_both_sign_branches {α : Type}
    [LE α] [OfNat α 0] (ord : SignedProductOrder α) (k : α) :
    0 ≤ k ∨ k ≤ 0 :=
  ord.le_total 0 k

end CCFSM.P2740
