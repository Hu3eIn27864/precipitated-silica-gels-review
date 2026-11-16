import Std

/-!
# CCFSM P27.37: proof-carrying root-isolation certificates

This module formalizes the logical contract of P27.37 leaf classifications.
It does not verify floating-point interval arithmetic, the Python implementation,
or the physical CCFSM model. Those remain explicit external obligations.
-/

namespace CCFSM.P2737

variable {α : Type} [LinearOrder α]

/-- A point is an interior root of p on the open interval (lo, hi). -/
def InteriorRoot (p : α → Prop) (lo hi x : α) : Prop :=
  lo < x ∧ x < hi ∧ p x

/--
A leaf result carries its own proof:
* noRoot excludes roots on the entire closed interval;
* unique certifies exactly one root in the open interval;
* unresolved makes no mathematical claim.
Endpoint roots are deliberately not silently assigned to a unique-root leaf.
-/
inductive LeafCertificate (p : α → Prop) (lo hi : α) : Type
  | noRoot :
      (∀ x, lo ≤ x → x ≤ hi → ¬ p x) →
      LeafCertificate p lo hi
  | unique :
      (∃! x, InteriorRoot p lo hi x) →
      LeafCertificate p lo hi
  | unresolved :
      LeafCertificate p lo hi

/-- The proposition guaranteed by a leaf certificate. -/
def CertificateSound (p : α → Prop) (lo hi : α) :
    LeafCertificate p lo hi → Prop
  | .noRoot _ => ∀ x, lo ≤ x → x ≤ hi → ¬ p x
  | .unique _ => ∃! x, InteriorRoot p lo hi x
  | .unresolved => True

/-- Every leaf certificate satisfies its declared contract. -/
theorem certificate_sound (p : α → Prop) (lo hi : α)
    (c : LeafCertificate p lo hi) :
    CertificateSound p lo hi c := by
  cases c with
  | noRoot h => exact h
  | unique h => exact h
  | unresolved => trivial

/-- A unique-root certificate supplies an interior root. -/
theorem unique_certificate_has_root (p : α → Prop) (lo hi : α)
    (h : ∃! x, InteriorRoot p lo hi x) :
    ∃ x, InteriorRoot p lo hi x := by
  rcases h with ⟨x, hx, _⟩
  exact ⟨x, hx⟩

/-- The uniqueness clause rules out a second, distinct interior root. -/
theorem unique_certificate_is_unique (p : α → Prop) (lo hi : α)
    (h : ∃! x, InteriorRoot p lo hi x)
    {x y : α} (hx : InteriorRoot p lo hi x)
    (hy : InteriorRoot p lo hi y) : x = y := by
  rcases h with ⟨w, hw, huniq⟩
  exact huniq x hx y hy

/--
Closed child intervals cover their parent interval when they share a midpoint.
The overlap at the midpoint is intentional; root certificates use open interiors.
-/
theorem midpoint_cover {lo mid hi x : α}
    (hxlo : lo ≤ x) (hxhi : x ≤ hi) :
    (lo ≤ x ∧ x ≤ mid) ∨ (mid ≤ x ∧ x ≤ hi) := by
  rcases le_total x mid with hxm | hmx
  · exact Or.inl ⟨hxlo, hxm⟩
  · exact Or.inr ⟨hmx, hxhi⟩

/--
An interior root of a parent interval is either interior to the left child,
exactly at the split point, or interior to the right child.
A split-point root is therefore an explicit boundary case.
-/
theorem midpoint_root_split {lo mid hi x : α}
    (hx : lo < x ∧ x < hi) :
    (lo < x ∧ x < mid) ∨
      (x = mid) ∨
      (mid < x ∧ x < hi) := by
  rcases lt_trichotomy x mid with hleft | heq | hright
  · exact Or.inl ⟨hx.1, hleft⟩
  · exact Or.inr (Or.inl heq)
  · exact Or.inr (Or.inr ⟨hright, hx.2⟩)

end CCFSM.P2737
