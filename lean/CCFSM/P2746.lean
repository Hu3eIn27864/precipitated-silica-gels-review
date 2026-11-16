import CCFSM.P2745

/-!
# CCFSM P27.46: completeness of fully resolved root partitions

P27.45 proves that collected witnesses are distinct genuine roots. This
module develops the converse direction: under a fully resolved partition,
every interior root must occur in the witness list.

The theorem deliberately requires explicit order laws. It does not infer
trichotomy or strict-to-nonstrict conversion from bare typeclasses.
-/

namespace CCFSM.P2746

open CCFSM.P2737
open CCFSM.P2744
open CCFSM.P2745

/--
Every interior root of a fully resolved partition occurs in its witness list.
The proof partitions the root into the left child, split point, or right child.
-/
theorem every_interior_root_is_collected {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (lt_to_le : ∀ {a b : α}, a < b → a ≤ b)
    (trichotomy : ∀ a b : α, a < b ∨ a = b ∨ b < a)
    (tree : RootIsolationTree p lo hi)
    (hresolved : FullyResolved tree)
    {x : α} (hx : InteriorRoot p lo hi x) :
    x ∈ certifiedRootWitnesses tree := by
  induction tree generalizing x with
  | leaf evidence =>
      cases evidence with
      | noRoot h =>
          exact False.elim (h x (lt_to_le hx.1) (lt_to_le hx.2) hx.2.2)
      | unique witness =>
          have hEq := witness.unique x hx
          subst x
          simp [certifiedRootWitnesses]
      | unresolved =>
          cases hresolved
  | @split lo mid hi leftOrder rightOrder midpoint left right ihl ihr =>
      rcases hresolved with ⟨hleft, hright⟩
      rcases trichotomy x mid with hleftOfMid | hAtMid | hrightOfMid
      · have hxLeft : InteriorRoot p lo mid x := ⟨hx.1, hleftOfMid, hx.2.2⟩
        have hmem := ihl hleft hxLeft
        exact List.mem_append.mpr
          (Or.inl (List.mem_append.mpr (Or.inl hmem)))
      · subst x
        cases midpoint with
        | noRoot hNo =>
            exact False.elim (hNo hx.2.2)
        | root hRoot =>
            have hmem : mid ∈ splitPointWitnesses (.root hRoot) := by
              simp [splitPointWitnesses]
            exact List.mem_append.mpr
              (Or.inl (List.mem_append.mpr (Or.inr hmem)))
        | unresolved =>
            contradiction
      · have hxRight : InteriorRoot p mid hi x := ⟨hrightOfMid, hx.2.1, hx.2.2⟩
        have hmem := ihr hright hxRight
        exact List.mem_append.mpr (Or.inr hmem)

/--
For a fully resolved tree, the collected witness list and the set of
interior roots have exactly the same members. Together with P27.45's
duplicate-freedom theorem, its length is therefore the exact interior-root
count (provided the supplied strict-order laws hold).
-/
theorem collected_iff_interior_root {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (lt_transitive : ∀ {a b c : α}, a < b → b < c → a < c)
    (lt_irrefl : ∀ a : α, ¬ a < a)
    (lt_to_le : ∀ {a b : α}, a < b → a ≤ b)
    (trichotomy : ∀ a b : α, a < b ∨ a = b ∨ b < a)
    (tree : RootIsolationTree p lo hi)
    (hresolved : FullyResolved tree)
    (x : α) :
    x ∈ certifiedRootWitnesses tree ↔ InteriorRoot p lo hi x := by
  constructor
  · exact certifiedRootWitnesses_sound lt_transitive tree
  · intro hx
    exact every_interior_root_is_collected lt_to_le trichotomy
      tree hresolved hx

/-- Exact root count is a witness-list length plus membership equivalence. -/
def ExactInteriorRootCount {α : Type} [LE α] [LT α]
    (p : α → Prop) (lo hi : α)
    (tree : RootIsolationTree p lo hi) (n : Nat) : Prop :=
  (certifiedRootWitnesses tree).length = n ∧
    ∀ x, x ∈ certifiedRootWitnesses tree ↔ InteriorRoot p lo hi x

/--
A fully resolved partition supplies an exact count, not merely a lower bound.
The count is the length of the duplicate-free, complete witness list.
-/
theorem fullyResolved_exact_root_count {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (lt_transitive : ∀ {a b c : α}, a < b → b < c → a < c)
    (lt_irrefl : ∀ a : α, ¬ a < a)
    (lt_to_le : ∀ {a b : α}, a < b → a ≤ b)
    (trichotomy : ∀ a b : α, a < b ∨ a = b ∨ b < a)
    (tree : RootIsolationTree p lo hi)
    (hresolved : FullyResolved tree) :
    ExactInteriorRootCount p lo hi tree
      (certifiedRootWitnesses tree).length := by
  constructor
  · rfl
  · intro x
    exact collected_iff_interior_root lt_transitive lt_irrefl
      lt_to_le trichotomy tree hresolved x

end CCFSM.P2746
