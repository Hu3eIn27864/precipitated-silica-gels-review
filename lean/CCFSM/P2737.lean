import Std

/-!
# CCFSM P27.37: proof-carrying root-isolation certificates

This module formalizes the logical contract of P27.37 leaf classifications.
It does not verify floating-point interval arithmetic, the Python implementation,
or the physical CCFSM model. Those remain explicit external obligations.
-/

/-- A point is an interior root of p on the open interval (lo, hi). -/
def CCFSM.P2737.InteriorRoot {α : Type} [LT α]
    (p : α → Prop) (lo hi x : α) : Prop :=
  lo < x ∧ x < hi ∧ p x

namespace CCFSM.P2737

/-- Explicit core-Lean encoding of existence and uniqueness. -/
def UniqueWitness {α : Type} (q : α → Prop) : Prop :=
  ∃ x, q x ∧ ∀ y, q y → y = x

/--
A data-carrying unique-root witness. Unlike the propositionally existential
UniqueWitness below, this structure stores the witness coordinate explicitly
so a certificate producer can serialize it and an independent checker can
validate its root/uniqueness claims.
-/
structure UniqueRootEvidence {α : Type} [LT α]
    (p : α → Prop) (lo hi : α) : Type where
  witness : α
  isRoot : InteriorRoot p lo hi witness
  unique : ∀ y, InteriorRoot p lo hi y → y = witness

/--
A leaf result carries its own proof:
* noRoot excludes roots on the entire closed interval;
* unique certifies exactly one root in the open interval;
* unresolved makes no mathematical claim.
Endpoint roots are deliberately not silently assigned to a unique-root leaf.
-/
inductive LeafCertificate {α : Type} [LE α] [LT α]
    (p : α → Prop) (lo hi : α) : Type
  | noRoot :
      (∀ x, lo ≤ x → x ≤ hi → ¬ p x) →
      LeafCertificate p lo hi
  | unique :
      UniqueRootEvidence p lo hi →
      LeafCertificate p lo hi
  | unresolved :
      LeafCertificate p lo hi

/-- The proposition guaranteed by a leaf certificate. -/
def CertificateSound {α : Type} [LE α] [LT α]
    (p : α → Prop) (lo hi : α) :
    LeafCertificate p lo hi → Prop
  | .noRoot _ => ∀ x, lo ≤ x → x ≤ hi → ¬ p x
  | .unique evidence =>
      ∃ x, InteriorRoot p lo hi x ∧
        ∀ y, InteriorRoot p lo hi y → y = x
  | .unresolved => True

/-- Every leaf certificate satisfies its declared contract. -/
theorem certificate_sound {α : Type} [LE α] [LT α]
    (p : α → Prop) (lo hi : α)
    (c : LeafCertificate p lo hi) :
    CertificateSound p lo hi c := by
  cases c with
  | noRoot h => exact h
  | unique h => exact ⟨h.witness, h.isRoot, h.unique⟩
  | unresolved => trivial

/-- A unique-root certificate supplies an interior root. -/
theorem unique_certificate_has_root {α : Type} [LT α]
    (p : α → Prop) (lo hi : α)
    (h : UniqueWitness (InteriorRoot p lo hi)) :
    ∃ x, InteriorRoot p lo hi x := by
  rcases h with ⟨x, hx, _⟩
  exact ⟨x, hx⟩

/-- The uniqueness clause rules out a second, distinct interior root. -/
theorem unique_certificate_is_unique {α : Type} [LT α]
    (p : α → Prop) (lo hi : α)
    (h : UniqueWitness (InteriorRoot p lo hi))
    {x y : α} (hx : InteriorRoot p lo hi x)
    (hy : InteriorRoot p lo hi y) : x = y := by
  rcases h with ⟨w, hw, huniq⟩
  exact (huniq x hx).trans (huniq y hy).symm

/--
Closed child intervals cover their parent interval when they share a midpoint.
The overlap at the midpoint is intentional; root certificates use open interiors.
-/
theorem midpoint_cover {α : Type} [LE α]
    {lo mid hi x : α}
    (hxlo : lo ≤ x) (hxhi : x ≤ hi)
    (hle_total : ∀ a b : α, a ≤ b ∨ b ≤ a) :
    (lo ≤ x ∧ x ≤ mid) ∨ (mid ≤ x ∧ x ≤ hi) := by
  rcases hle_total x mid with hxm | hmx
  · exact Or.inl ⟨hxlo, hxm⟩
  · exact Or.inr ⟨hmx, hxhi⟩

/--
An interior root of a parent interval is either interior to the left child,
exactly at the split point, or interior to the right child.
A split-point root is therefore an explicit boundary case.
-/
theorem midpoint_root_split {α : Type} [LT α]
    {lo mid hi x : α}
    (hx : lo < x ∧ x < hi)
    (htrichotomy : ∀ a b : α, a < b ∨ a = b ∨ b < a) :
    (lo < x ∧ x < mid) ∨
      (x = mid) ∨
      (mid < x ∧ x < hi) := by
  rcases htrichotomy x mid with hleft | heq | hright
  · exact Or.inl ⟨hx.1, hleft⟩
  · exact Or.inr (Or.inl heq)
  · exact Or.inr (Or.inr ⟨hright, hx.2⟩)

end CCFSM.P2737
