import CCFSM.P2737

/-!
# CCFSM P27.44: proof-carrying interval partition trees

This module formalizes the recursive partition structure and the separate
evidence attached to every split point. In particular, a root at a shared
midpoint is represented by one point certificate, not inferred by counting
both adjacent closed child intervals.

The module proves domain coverage and soundness of all attached leaf and
midpoint evidence. It does not yet prove aggregate root-count bounds, provide
a serialized producer format, or connect Python output to Lean proof terms.
-/

namespace CCFSM.P2744

/-- Exact evidence for the value of the polynomial at a subdivision point. -/
inductive SplitPointCertificate {α : Type} (p : α → Prop) (mid : α) : Type
  | noRoot : ¬ p mid → SplitPointCertificate p mid
  | root : p mid → SplitPointCertificate p mid
  | unresolved : SplitPointCertificate p mid

/-- Every split-point constructor carries only the claim it actually proves. -/
def SplitPointCertificateSound {α : Type} {p : α → Prop} {mid : α} :
    SplitPointCertificate p mid → Prop
  | .noRoot _h => ¬ p mid
  | .root _h => p mid
  | .unresolved => True

/-- Recursive certificate tree whose indices are its exact closed domain. -/
inductive RootIsolationTree {α : Type} [LE α] [LT α]
    (p : α → Prop) : α → α → Type
  | leaf {lo hi : α}
      (evidence : CCFSM.P2737.LeafCertificate p lo hi) :
      RootIsolationTree p lo hi
  | split {lo mid hi : α}
      (left_order : lo < mid)
      (right_order : mid < hi)
      (midpoint_evidence : SplitPointCertificate p mid)
      (left : RootIsolationTree p lo mid)
      (right : RootIsolationTree p mid hi) :
      RootIsolationTree p lo hi

/--
A point is covered by a leaf trivially, or by one of the children plus the
corresponding closed-half interval condition at a split point.
-/
def CoversPoint {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α} :
    RootIsolationTree p lo hi → α → Prop
  | .leaf _, _ => True
  | .split (mid := mid) _ _ _ left right, x =>
      (x ≤ mid ∧ CoversPoint left x) ∨
      (mid ≤ x ∧ CoversPoint right x)

/--
Every point of the parent closed interval is covered by a descendant leaf.
The child intervals are closed and overlap at the midpoint; explicit midpoint
evidence is stored separately in the split constructor.
-/
theorem closed_domain_covered {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (tree : RootIsolationTree p lo hi)
    (x : α)
    (hlo : lo ≤ x)
    (hhi : x ≤ hi)
    (le_total : ∀ a b : α, a ≤ b ∨ b ≤ a) :
    CoversPoint tree x := by
  induction tree with
  | leaf evidence =>
      trivial
  | @split lo mid hi hleft hright midpoint left right ihl ihr =>
      by_cases hxm : x ≤ mid
      · exact Or.inl ⟨hxm, ihl hlo hxm⟩
      · have hmx : mid ≤ x := (le_total x mid).resolve_left hxm
        exact Or.inr ⟨hmx, ihr hmx hhi⟩

/--
All leaf and split-point claims carried by the tree are sound. Unresolved
constructors contribute True and therefore never imply a root count.
-/
def TreeEvidenceSound {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α} :
    RootIsolationTree p lo hi → Prop
  | .leaf evidence =>
      CCFSM.P2737.CertificateSound p lo hi evidence
  | .split _ _ midpoint left right =>
      SplitPointCertificateSound midpoint ∧
        TreeEvidenceSound left ∧ TreeEvidenceSound right

/-- The recursive tree preserves the soundness contract of every certificate. -/
theorem tree_evidence_sound {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (tree : RootIsolationTree p lo hi) :
    TreeEvidenceSound tree := by
  induction tree with
  | @leaf lo' hi' evidence =>
      exact CCFSM.P2737.certificate_sound p lo' hi' evidence
  | @split lo' mid' hi' left_order right_order midpoint left right ihl ihr =>
      exact ⟨by cases midpoint <;> trivial, ihl, ihr⟩

/--
A fully resolved tree has no unresolved leaf or midpoint evidence. This is a
structural predicate only; aggregate root-count exactness still requires the
separate ownership/count theorem and endpoint treatment described in the
P27.44 design note.
-/
def FullyResolved {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α} :
    RootIsolationTree p lo hi → Prop
  | .leaf (.noRoot _) => True
  | .leaf (.unique _) => True
  | .leaf (.unresolved) => False
  | .split _ _ (.noRoot _) left right =>
      FullyResolved left ∧ FullyResolved right
  | .split _ _ (.root _) left right =>
      FullyResolved left ∧ FullyResolved right
  | .split _ _ (.unresolved) _ _ => False

end CCFSM.P2744
