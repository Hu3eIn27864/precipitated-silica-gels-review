import Init

namespace CCFSM.P2749

/-- Remove leading zeros from a coefficient list stored in reverse order. -/
def trimReversed : List Rat → List Rat
  | [] => []
  | a :: rest => if a = 0 then trimReversed rest else a :: rest

/-- The trimmed reversed list is empty or begins with a nonzero coefficient. -/
theorem trimReversed_shape (xs : List Rat) :
    trimReversed xs = [] ∨
      ∃ a rest, trimReversed xs = a :: rest ∧ a ≠ 0 := by
  induction xs with
  | nil =>
      simp [trimReversed]
  | cons a rest ih =>
      simp only [trimReversed]
      split
      · exact ih
      · rename_i h
        exact Or.inr ⟨a, rest, rfl, h⟩

/-- Remove trailing zero coefficients from an ascending coefficient list. -/
def normalizeCoefficients (xs : List Rat) : List Rat :=
  (trimReversed xs.reverse).reverse

/-- A canonical coefficient list is empty or has a nonzero final coefficient. -/
def CanonicalCoefficients (xs : List Rat) : Prop :=
  xs = [] ∨ ∃ init last, xs = init ++ [last] ∧ last ≠ 0

theorem normalizeCoefficients_canonical (xs : List Rat) :
    CanonicalCoefficients (normalizeCoefficients xs) := by
  unfold CanonicalCoefficients normalizeCoefficients
  rcases trimReversed_shape xs.reverse with h | ⟨a, rest, hshape, ha⟩
  · left
    simp [h]
  · right
    refine ⟨rest.reverse, a, ?_, ha⟩
    simp [hshape]

/-- Exact rational polynomial, coefficients stored in ascending degree order.
    The invariant rules out trailing zero coefficients. -/
structure RatPolynomial where
  coefficients : List Rat
  canonical : CanonicalCoefficients coefficients

/-- Construct a canonical polynomial by trimming high-degree zero terms. -/
def ofCoefficients (xs : List Rat) : RatPolynomial :=
  ⟨normalizeCoefficients xs, normalizeCoefficients_canonical xs⟩

/-- The zero polynomial has the unique empty coefficient representation. -/
def zero : RatPolynomial := ofCoefficients []

/-- Horner evaluation of an ascending coefficient list. -/
def evalCoefficients (x : Rat) (xs : List Rat) : Rat :=
  xs.foldr (fun a acc => a + x * acc) 0

/-- Exact polynomial evaluation over the core rational field. -/
def eval (p : RatPolynomial) (x : Rat) : Rat :=
  evalCoefficients x p.coefficients

/-- Coefficients of the formal derivative, before canonical trimming. -/
def derivativeCoefficients : List Rat → List Rat
  | [] => []
  | _ :: rest => derivativeTail 1 rest
where
  derivativeTail (n : Nat) : List Rat → List Rat
    | [] => []
    | a :: rest =>
        (Rat.ofInt (Int.ofNat n) * a) :: derivativeTail (n + 1) rest

/-- Formal derivative, normalized to canonical coefficient form. -/
def derivative (p : RatPolynomial) : RatPolynomial :=
  ofCoefficients (derivativeCoefficients p.coefficients)

/-- Coefficientwise addition, extending the shorter polynomial with zeros. -/
def addCoefficients : List Rat → List Rat → List Rat
  | [], ys => ys
  | xs, [] => xs
  | a :: as, b :: bs => (a + b) :: addCoefficients as bs

/-- Exact polynomial addition followed by canonical trimming. -/
def add (p q : RatPolynomial) : RatPolynomial :=
  ofCoefficients (addCoefficients p.coefficients q.coefficients)

/-- Multiply every coefficient by one exact rational scalar. -/
def scaleCoefficients (a : Rat) (xs : List Rat) : List Rat :=
  xs.map (fun b => a * b)

/-- Exact polynomial multiplication by recursive convolution. -/
def multiplyCoefficients : List Rat → List Rat → List Rat
  | [], _ => []
  | a :: as, bs =>
      addCoefficients (scaleCoefficients a bs)
        (0 :: multiplyCoefficients as bs)

/-- Exact polynomial multiplication followed by canonical trimming. -/
def multiply (p q : RatPolynomial) : RatPolynomial :=
  ofCoefficients (multiplyCoefficients p.coefficients q.coefficients)

theorem zero_coefficients_empty : zero.coefficients = [] := by
  simp [zero, ofCoefficients, normalizeCoefficients, trimReversed]

end CCFSM.P2749


/-- A reversed coefficient list beginning with a nonzero value is unchanged. -/
theorem trimReversed_nonzero_head (a : Rat) (rest : List Rat)
    (ha : a ≠ 0) :
    trimReversed (a :: rest) = a :: rest := by
  simp [trimReversed, ha]

/-- Canonical coefficient lists are fixed points of normalization. -/
theorem normalizeCoefficients_of_canonical (xs : List Rat)
    (hxs : CanonicalCoefficients xs) :
    normalizeCoefficients xs = xs := by
  rcases hxs with hnil | ⟨init, last, hxs, hlast⟩
  · simp [normalizeCoefficients, hnil, trimReversed]
  · subst xs
    simp [normalizeCoefficients, List.reverse_append, trimReversed, hlast]

/-- Normalization is idempotent. -/
theorem normalizeCoefficients_idempotent (xs : List Rat) :
    normalizeCoefficients (normalizeCoefficients xs) =
      normalizeCoefficients xs :=
  normalizeCoefficients_of_canonical _ (normalizeCoefficients_canonical xs)

/-- The leading coefficient, when present, is the last ascending coefficient. -/
def leadingCoefficient? (p : RatPolynomial) : Option Rat :=
  p.coefficients.reverse.head?

/-- A nonzero canonical polynomial has a nonzero leading coefficient. -/
theorem leadingCoefficient?_nonzero (p : RatPolynomial)
    (hp : p.coefficients ≠ []) :
    ∃ c, leadingCoefficient? p = some c ∧ c ≠ 0 := by
  rcases p.canonical with hnil | ⟨init, last, hcoeff, hlast⟩
  · exact False.elim (hp hnil)
  · refine ⟨last, ?_, hlast⟩
    simp [leadingCoefficient?, hcoeff, List.reverse_append]

/-- The degree of zero is undefined; nonzero degree is list length minus one. -/
def degree? (p : RatPolynomial) : Option Nat :=
  match leadingCoefficient? p with
  | none => none
  | some _ => some (p.coefficients.length - 1)

theorem degree?_zero : degree? zero = none := by
  simp [degree?, leadingCoefficient?, zero_coefficients_empty]
