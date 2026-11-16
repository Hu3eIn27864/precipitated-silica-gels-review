import CCFSM.P2746

/-!
# CCFSM P27.48: endpoint ownership and closed-interval root counts

P27.46 gives an exact count on the open interval. This module adds explicit
outer-endpoint evidence and combines endpoint and interior witnesses without
double-counting shared boundaries.

The order laws needed for the closed-domain completeness argument are explicit.
-/

namespace CCFSM.P2748

open CCFSM.P2737
open CCFSM.P2744
open CCFSM.P2745
open CCFSM.P2746

/-- Exact evidence for a root predicate at one fixed outer endpoint. -/
inductive EndpointCertificate {α : Type} (p : α → Prop) (endpoint : α) : Type
  | root : p endpoint → EndpointCertificate p endpoint
  | noRoot : ¬ p endpoint → EndpointCertificate p endpoint
  | unresolved : EndpointCertificate p endpoint

/-- A resolved endpoint certificate makes either a positive or negative claim. -/
def EndpointResolved {α : Type} {p : α → Prop} {endpoint : α} :
    EndpointCertificate p endpoint → Prop
  | .root _ => True
  | .noRoot _ => True
  | .unresolved => False

/-- Only a certified endpoint root contributes a coordinate witness. -/
def endpointRootWitnesses {α : Type} {p : α → Prop} {endpoint : α} :
    EndpointCertificate p endpoint → List α
  | .root _ => [endpoint]
  | .noRoot _ => []
  | .unresolved => []

/-- Every endpoint witness is the certified endpoint and satisfies p. -/
theorem endpointRootWitnesses_sound {α : Type}
    {p : α → Prop} {endpoint x : α}
    (evidence : EndpointCertificate p endpoint)
    (hx : x ∈ endpointRootWitnesses evidence) :
    x = endpoint ∧ p x := by
  cases evidence with
  | root h =>
      simp [endpointRootWitnesses] at hx
      subst x
      exact ⟨rfl, h⟩
  | noRoot h =>
      simp [endpointRootWitnesses] at hx
  | unresolved =>
      simp [endpointRootWitnesses] at hx

/-- The endpoint collector is duplicate-free. -/
theorem endpointRootWitnesses_allDistinct {α : Type}
    {p : α → Prop} {endpoint : α}
    (evidence : EndpointCertificate p endpoint) :
    AllDistinct (endpointRootWitnesses evidence) := by
  cases evidence <;> simp [endpointRootWitnesses, AllDistinct]

/-- The closed-domain witness list has one owner for each outer endpoint. -/
def closedRootWitnesses {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (tree : RootIsolationTree p lo hi)
    (loEvidence : EndpointCertificate p lo)
    (hiEvidence : EndpointCertificate p hi) : List α :=
  endpointRootWitnesses loEvidence ++
    certifiedRootWitnesses tree ++
    endpointRootWitnesses hiEvidence

/-- Predicate for a root in the closed parent interval. -/
def ClosedRoot {α : Type} [LE α] [LT α]
    (p : α → Prop) (lo hi x : α) : Prop :=
  lo ≤ x ∧ x ≤ hi ∧ p x

/-- Every closed witness is a genuine root in the closed parent interval. -/
theorem closedRootWitnesses_sound {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (lt_to_le : ∀ {a b : α}, a < b → a ≤ b)
    (tree : RootIsolationTree p lo hi)
    (loEvidence : EndpointCertificate p lo)
    (hiEvidence : EndpointCertificate p hi)
    (hlohi : lo < hi) :
    ∀ {x}, x ∈ closedRootWitnesses tree loEvidence hiEvidence →
      ClosedRoot p lo hi x := by
  intro x hx
  simp only [closedRootWitnesses] at hx
  rcases List.mem_append.mp hx with hloOrInterior | hhi
  · rcases List.mem_append.mp hloOrInterior with hlo | hinterior
    · obtain ⟨rfl, hp⟩ := endpointRootWitnesses_sound loEvidence hlo
      exact ⟨le_refl _, lt_to_le hlohi, hp⟩
    · obtain ⟨hlo, hhi, hp⟩ :=
        certifiedRootWitnesses_sound (by
          intro a b c hab hbc
          exact lt_trans hab hbc) tree hinterior
      exact ⟨lt_to_le hlo, lt_to_le hhi, hp⟩
  · obtain ⟨rfl, hp⟩ := endpointRootWitnesses_sound hiEvidence hhi
    exact ⟨lt_to_le hlohi, le_refl _, hp⟩

/-- Distinct endpoint and interior regions cannot share a witness. -/
theorem closedRootWitnesses_allDistinct {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (lt_transitive : ∀ {a b c : α}, a < b → b < c → a < c)
    (lt_irrefl : ∀ a : α, ¬ a < a)
    (tree : RootIsolationTree p lo hi)
    (loEvidence : EndpointCertificate p lo)
    (hiEvidence : EndpointCertificate p hi)
    (hlohi : lo < hi) :
    AllDistinct (closedRootWitnesses tree loEvidence hiEvidence) := by
  have hLoMid :
      ∀ x, x ∈ endpointRootWitnesses loEvidence →
        ∀ y, y ∈ certifiedRootWitnesses tree → x ≠ y := by
    intro x hx y hy hxy
    obtain ⟨rfl, _⟩ := endpointRootWitnesses_sound loEvidence hx
    subst y
    have hylt := (certifiedRootWitnesses_sound lt_transitive tree hy).1
    exact (lt_irrefl _ hylt).elim
  have hMidHi :
      ∀ x, x ∈ certifiedRootWitnesses tree →
        ∀ y, y ∈ endpointRootWitnesses hiEvidence → x ≠ y := by
    intro x hx y hy hxy
    obtain ⟨rfl, _⟩ := endpointRootWitnesses_sound hiEvidence hy
    subst x
    have hxlt := (certifiedRootWitnesses_sound lt_transitive tree hx).2.1
    exact (lt_irrefl _ hxlt).elim
  have hLoHi :
      ∀ x, x ∈ endpointRootWitnesses loEvidence →
        ∀ y, y ∈ endpointRootWitnesses hiEvidence → x ≠ y := by
    intro x hx y hy hxy
    obtain ⟨rfl, _⟩ := endpointRootWitnesses_sound loEvidence hx
    obtain ⟨rfl, _⟩ := endpointRootWitnesses_sound hiEvidence hy
    subst y
    exact (lt_irrefl _ hlohi).elim
  have hFirst :=
    allDistinct_append (endpointRootWitnesses_allDistinct loEvidence)
      (certifiedRootWitnesses_allDistinct lt_transitive lt_irrefl tree)
      hLoMid
  have hFirstHi :
      ∀ x, x ∈ (endpointRootWitnesses loEvidence ++
          certifiedRootWitnesses tree) →
        ∀ y, y ∈ endpointRootWitnesses hiEvidence → x ≠ y := by
    intro x hx y hy hxy
    rcases List.mem_append.mp hx with hLo | hMid
    · exact hLoHi x hLo y hy hxy
    · exact hMidHi x hMid y hy hxy
  exact allDistinct_append hFirst
    (endpointRootWitnesses_allDistinct hiEvidence) hFirstHi

/--
The closed witness collector is complete when the interior tree and both
outer endpoint certificates are fully resolved. The supplied order laws make
the endpoint/interior trichotomy explicit.
-/
theorem closedRootWitnesses_complete {α : Type} [LE α] [LT α]
    {p : α → Prop} {lo hi : α}
    (lt_transitive : ∀ {a b c : α}, a < b → b < c → a < c)
    (lt_irrefl : ∀ a : α, ¬ a < a)
    (lt_to_le : ∀ {a b : α}, a < b → a ≤ b)
    (le_lt_trans : ∀ {a b c : α}, a ≤ b → b < c → a < c)
    (le_antisymm : ∀ {a b : α}, a ≤ b → b ≤ a → a = b)
    (trichotomy : ∀ a b : α, a < b ∨ a = b ∨ b < a)
    (tree : RootIsolationTree p lo hi)
    (hresolved : FullyResolved tree)
    (loEvidence : EndpointCertificate p lo)
    (hloResolved : EndpointResolved loEvidence)
    (hiEvidence : EndpointCertificate p hi)
    (hhiResolved : EndpointResolved hiEvidence)
    (hlohi : lo < hi)
    (x : α) :
    x ∈ closedRootWitnesses tree loEvidence hiEvidence ↔
      ClosedRoot p lo hi x := by
  constructor
  · exact closedRootWitnesses_sound lt_to_le tree loEvidence hiEvidence hlohi
  · rintro ⟨hlox, hxhi, hpx⟩
    rcases trichotomy x lo with hxlo | hxEqLo | hlox'
    · exact False.elim (lt_irrefl x (le_lt_trans hlox hxlo))
    · subst x
      cases loEvidence with
      | root hp =>
          simp [closedRootWitnesses, endpointRootWitnesses]
      | noRoot hno =>
          exact False.elim (hno hpx)
      | unresolved =>
          exact False.elim hloResolved
    · rcases trichotomy x hi with hxhi' | hxEqHi | hhix
      · have hInterior : InteriorRoot p lo hi x := ⟨hlox', hxhi', hpx⟩
        have hmem := (collected_iff_interior_root lt_transitive
          lt_to_le trichotomy tree hresolved x).mpr hInterior
        simp only [closedRootWitnesses]
        exact List.mem_append.mpr (Or.inl (List.mem_append.mpr (Or.inr hmem)))
      · subst x
        cases hiEvidence with
        | root hp =>
            simp [closedRootWitnesses, endpointRootWitnesses]
          | noRoot hno =>
            exact False.elim (hno hpx)
          | unresolved =>
            exact False.elim hhiResolved
      · exact False.elim (lt_irrefl x (le_lt_trans hxhi hhix))

end CCFSM.P2748
