import CCFSM.P2744

/-!
# CCFSM P27.45: explicit root witnesses from proof-carrying trees

The P27.37 unique-leaf certificate now stores a witness coordinate as data.
This module collects those interior witnesses and separately certified
midpoint roots into a list, then proves every collected point is an actual
root strictly inside the parent domain.

Pairwise distinctness and exact aggregate root-count bounds remain separate
theorems; list length must not be called a root count until those are proved.
-/

namespace CCFSM.P2745

open CCFSM.P2737
open CCFSM.P2744

/-- A split point contributes a witness only when its certificate proves a root. -/
def splitPointWitnesses {α : Type} {p : α → Prop} {mid : α}
    (evidence : SplitPointCertificate p mid) : List α :=
  match evidence with
  | .noRoot _ => []
  | .root _ => [mid]
  | .unresolved => []

/-- Any witness emitted by a split-point certificate is exactly its midpoint root. -/
theorem splitPointWitnesses_sound {α : Type}
    {p : α → Prop} {mid x : α}
    (evidence : SplitPointCertificate p mid)
    (hx : x ∈ splitPointWitnesses evidence) :
    x = mid ∧ p x := by
  cases evidence with
  | noRoot h =>
      simp [splitPointWitnesses] at hx
  | root h =>
      simp [splitPointWitnesses] at hx
      subst x
      exact ⟨rfl, h⟩
  | unresolved =>
      simp [splitPointWitnesses] at hx

/--
Collect all explicit root witnesses from a P27.44 partition tree.
Unresolved leaves and split points contribute no asserted roots.
-/
def certifiedRootWitnesses {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α} :
    RootIsolationTree p lo hi → List α
  | .leaf (.noRoot _) => []
  | .leaf (.unique evidence) => [evidence.witness]
  | .leaf (.unresolved) => []
  | .split _ _ midpoint left right =>
      certifiedRootWitnesses left ++
        splitPointWitnesses midpoint ++
        certifiedRootWitnesses right

/--
Every collected witness is a genuine root in the open interior of the
parent interval. This theorem establishes validity, not pairwise distinctness.
-/
theorem certifiedRootWitnesses_sound {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (lt_transitive : ∀ {a b c : α}, a < b → b < c → a < c)
    (tree : RootIsolationTree p lo hi) :
    ∀ {x}, x ∈ certifiedRootWitnesses tree →
      InteriorRoot p lo hi x := by
  induction tree with
  | leaf evidence =>
      cases evidence with
      | noRoot h =>
          intro x hx
          simp [certifiedRootWitnesses] at hx
      | unique witness =>
          intro x hx
          simp [certifiedRootWitnesses] at hx
          subst x
          exact witness.isRoot
      | unresolved =>
          intro x hx
          simp [certifiedRootWitnesses] at hx
  | @split lo mid hi left_order right_order midpoint left right ihl ihr =>
      intro x hx
      simp only [certifiedRootWitnesses] at hx
      rcases List.mem_append.mp hx with hxLeftMiddle | hxRight
      · rcases List.mem_append.mp hxLeftMiddle with hxLeft | hxMiddle
        · rcases ihl hxLeft with ⟨hlo, hmid, hroot⟩
          exact ⟨hlo, lt_transitive hmid right_order, hroot⟩
        · obtain ⟨rfl, hroot⟩ := splitPointWitnesses_sound midpoint hxMiddle
          exact ⟨left_order, right_order, hroot⟩
      · rcases ihr hxRight with ⟨hmid, hhi, hroot⟩
        exact ⟨lt_transitive left_order hmid, hhi, hroot⟩

end CCFSM.P2745
