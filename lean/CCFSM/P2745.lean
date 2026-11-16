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


/-- A list is duplicate-free when its head differs from every later entry. -/
def AllDistinct {α : Type} : List α → Prop
  | [] => True
  | a :: rest => (∀ b, b ∈ rest → a ≠ b) ∧ AllDistinct rest

/-- Appending two duplicate-free lists preserves distinctness when they are disjoint. -/
theorem allDistinct_append {α : Type} {xs ys : List α}
    (hxs : AllDistinct xs)
    (hys : AllDistinct ys)
    (hseparate : ∀ x, x ∈ xs → ∀ y, y ∈ ys → x ≠ y) :
    AllDistinct (xs ++ ys) := by
  induction xs generalizing ys hys with
  | nil =>
      simpa [AllDistinct] using hys
  | cons a rest ih =>
      change (∀ b, b ∈ rest → a ≠ b) ∧ AllDistinct rest at hxs
      change (∀ b, b ∈ rest ++ ys → a ≠ b) ∧
        AllDistinct (rest ++ ys)
      constructor
      · intro b hb
        rcases List.mem_append.mp hb with hRest | hYs
        · exact hxs.1 b hRest
        · exact hseparate a (by simp) b hYs
      · apply ih hxs.2 hys
        intro x hx y hy
        exact hseparate x (by simp [hx]) y hy

/-- The list contributed by one split-point certificate is always duplicate-free. -/
theorem splitPointWitnesses_allDistinct {α : Type}
    {p : α → Prop} {mid : α}
    (evidence : SplitPointCertificate p mid) :
    AllDistinct (splitPointWitnesses evidence) := by
  cases evidence <;> simp [splitPointWitnesses, AllDistinct]

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


/--
The recursive witness collector contains no duplicate coordinates.
This uses explicit transitivity and irreflexivity of the strict order, rather
than assuming that a bare LT typeclass supplies an order law.
-/
theorem certifiedRootWitnesses_allDistinct {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (lt_transitive : ∀ {a b c : α}, a < b → b < c → a < c)
    (lt_irrefl : ∀ a : α, ¬ a < a)
    (tree : RootIsolationTree p lo hi) :
    AllDistinct (certifiedRootWitnesses tree) := by
  induction tree with
  | leaf evidence =>
      cases evidence <;> simp [certifiedRootWitnesses, AllDistinct]
  | @split lo m hi left_order right_order midpoint left right ihl ihr =>
      have hLeftBelow : ∀ x, x ∈ certifiedRootWitnesses left → x < mid := by
        intro x hx
        exact (certifiedRootWitnesses_sound lt_transitive left hx).2.1
      have hRightAbove : ∀ x, x ∈ certifiedRootWitnesses right → mid < x := by
        intro x hx
        exact (certifiedRootWitnesses_sound lt_transitive right hx).1
      have hLeftMidSeparate :
          ∀ x, x ∈ certifiedRootWitnesses left →
            ∀ y, y ∈ splitPointWitnesses midpoint → x ≠ y := by
        intro x hx y hy hxy
        obtain ⟨rfl, _⟩ := splitPointWitnesses_sound midpoint hy
        subst x
        exact (lt_irrefl m (hLeftBelow m hx)).elim
      have hLeftRightSeparate :
          ∀ x, x ∈ certifiedRootWitnesses left →
            ∀ y, y ∈ certifiedRootWitnesses right → x ≠ y := by
        intro x hx y hy hxy
        have hxylt := lt_transitive (hLeftBelow x hx) (hRightAbove y hy)
        subst y
        exact (lt_irrefl x hxylt).elim
      have hMidRightSeparate :
          ∀ x, x ∈ splitPointWitnesses midpoint →
            ∀ y, y ∈ certifiedRootWitnesses right → x ≠ y := by
        intro x hx y hy hxy
        obtain ⟨rfl, _⟩ := splitPointWitnesses_sound midpoint hx
        subst y
        exact (lt_irrefl m (hRightAbove m hy)).elim
      have hLeftMid :=
        allDistinct_append ihl (splitPointWitnesses_allDistinct midpoint)
          hLeftMidSeparate
      have hLeftMidRight :
          ∀ x, x ∈ (certifiedRootWitnesses left ++ splitPointWitnesses midpoint) →
            ∀ y, y ∈ certifiedRootWitnesses right → x ≠ y := by
        intro x hx y hy hxy
        rcases List.mem_append.mp hx with hxLeft | hxMid
        · exact hLeftRightSeparate x hxLeft y hy hxy
        · exact hMidRightSeparate x hxMid y hy hxy
      exact allDistinct_append hLeftMid ihr hLeftMidRight

end CCFSM.P2745
