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
  xs.reverse.foldl (fun acc a => acc * x + a) 0

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


/-- Removing leading zero coefficients in reverse order preserves Horner evaluation. -/
theorem evalFoldl_trimReversed (x : Rat) (xs : List Rat) :
    (trimReversed xs).foldl (fun acc a => acc * x + a) 0 =
      xs.foldl (fun acc a => acc * x + a) 0 := by
  induction xs with
  | nil =>
      rfl
  | cons a rest ih =>
      simp only [trimReversed]
      split
      · rename_i h
        subst a
        simpa [Rat.zero_add] using ih
      · rfl

/-- Canonical trimming preserves exact polynomial evaluation. -/
theorem evalCoefficients_normalize (x : Rat) (xs : List Rat) :
    evalCoefficients x (normalizeCoefficients xs) =
      evalCoefficients x xs := by
  simp [evalCoefficients, normalizeCoefficients, List.reverse_reverse,
    evalFoldl_trimReversed]

/-- Evaluation of a polynomial with a new constant coefficient. -/
theorem evalCoefficients_cons (x a : Rat) (xs : List Rat) :
    evalCoefficients x (a :: xs) =
      evalCoefficients x xs * x + a := by
  simp [evalCoefficients, List.reverse_cons, List.foldl_append]

/-- Horner evaluation respects coefficientwise polynomial addition. -/
theorem evalCoefficients_add (x : Rat) (xs ys : List Rat) :
    evalCoefficients x (addCoefficients xs ys) =
      evalCoefficients x xs + evalCoefficients x ys := by
  induction xs generalizing ys with
  | nil =>
      simp [addCoefficients, evalCoefficients, Rat.zero_add]
  | cons a rest ih =>
      cases ys with
      | nil =>
          simp [addCoefficients, evalCoefficients, Rat.add_zero]
      | cons b tail =>
          rw [addCoefficients, evalCoefficients_cons,
            evalCoefficients_cons, evalCoefficients_cons]
          rw [ih]
          calc
            (evalCoefficients x rest + evalCoefficients x tail) * x + (a + b) =
                (evalCoefficients x rest * x + evalCoefficients x tail * x) +
                  (a + b) := by rw [Rat.add_mul]
            _ = (evalCoefficients x rest * x + a) +
                  (evalCoefficients x tail * x + b) := by
                    simp [Rat.add_assoc, Rat.add_comm, Rat.add_left_comm]

/-- Scaling every coefficient scales the exact polynomial value. -/
theorem evalCoefficients_scale (x a : Rat) (xs : List Rat) :
    evalCoefficients x (scaleCoefficients a xs) =
      a * evalCoefficients x xs := by
  induction xs with
  | nil =>
      simp [scaleCoefficients, evalCoefficients]
  | cons b rest ih =>
      change evalCoefficients x (a * b :: scaleCoefficients a rest) =
        a * evalCoefficients x (b :: rest)
      rw [evalCoefficients_cons, ih, evalCoefficients_cons]
      calc
        (a * evalCoefficients x rest) * x + a * b =
            a * (evalCoefficients x rest * x) + a * b := by
              rw [Rat.mul_assoc]
        _ = a * (evalCoefficients x rest * x + b) := by
              rw [Rat.mul_add]

/-- Prefixing a zero constant coefficient multiplies the value by x. -/
theorem evalCoefficients_shift (x : Rat) (xs : List Rat) :
    evalCoefficients x (0 :: xs) =
      x * evalCoefficients x xs := by
  rw [evalCoefficients_cons]
  simp [Rat.add_zero, Rat.mul_comm]

/-- Horner evaluation respects recursive coefficient convolution. -/
theorem evalCoefficients_multiply (x : Rat) (xs ys : List Rat) :
    evalCoefficients x (multiplyCoefficients xs ys) =
      evalCoefficients x xs * evalCoefficients x ys := by
  induction xs generalizing ys with
  | nil =>
      simp [multiplyCoefficients, evalCoefficients]
  | cons a rest ih =>
      rw [multiplyCoefficients, evalCoefficients_add,
        evalCoefficients_scale, evalCoefficients_shift, ih]
      calc
        a * evalCoefficients x ys +
            x * (evalCoefficients x rest * evalCoefficients x ys) =
            (evalCoefficients x rest * x + a) *
              evalCoefficients x ys := by
                calc
                  a * evalCoefficients x ys +
                      x * (evalCoefficients x rest * evalCoefficients x ys) =
                      a * evalCoefficients x ys +
                        (evalCoefficients x rest * x) * evalCoefficients x ys := by
                          rw [← Rat.mul_assoc, Rat.mul_comm x (evalCoefficients x rest),
                            Rat.mul_assoc]
                  _ = (a + evalCoefficients x rest * x) *
                        evalCoefficients x ys := by rw [← Rat.add_mul]
                  _ = (evalCoefficients x rest * x + a) *
                        evalCoefficients x ys := by rw [Rat.add_comm]
        _ = evalCoefficients x (a :: rest) *
              evalCoefficients x ys := by
                exact congrArg (fun z : Rat => z * evalCoefficients x ys)
                  (evalCoefficients_cons x a rest).symm

/-- Exact evaluation of normalized polynomial multiplication is multiplicative. -/
theorem eval_multiply (p q : RatPolynomial) (x : Rat) :
    eval (multiply p q) x = eval p x * eval q x := by
  simp [eval, multiply, ofCoefficients, evalCoefficients_normalize,
    evalCoefficients_multiply]

/-- Exact evaluation of normalized polynomial addition is additive. -/
theorem eval_add (p q : RatPolynomial) (x : Rat) :
    eval (add p q) x = eval p x + eval q x := by
  simp [eval, add, ofCoefficients, evalCoefficients_normalize,
    evalCoefficients_add]


/-- The derivative of a constant polynomial has no coefficients. -/
theorem derivativeCoefficients_constant (a : Rat) :
    derivativeCoefficients [a] = [] := by
  simp [derivativeCoefficients, derivativeCoefficients.derivativeTail]

/-- The derivative coefficients of a linear polynomial are its slope. -/
theorem derivativeCoefficients_linear (a b : Rat) :
    derivativeCoefficients [a, b] = [Rat.ofInt 1 * b] := by
  rfl

/-- The derivative coefficients of a quadratic polynomial are exact. -/
theorem derivativeCoefficients_quadratic (a b c : Rat) :
    derivativeCoefficients [a, b, c] = [Rat.ofInt 1 * b, Rat.ofInt 2 * c] := by
  rfl


/-- Exact Horner values for constant and linear coefficient lists. -/
theorem evalCoefficients_constant (x a : Rat) :
    evalCoefficients x [a] = a := by
  simp [evalCoefficients, Rat.zero_add]

theorem evalCoefficients_linear (x a b : Rat) :
    evalCoefficients x [a, b] = a + b * x := by
  simp [evalCoefficients, Rat.add_comm, Rat.mul_comm, Rat.add_zero]


/-- The derivative of a constant polynomial evaluates to zero. -/
theorem eval_derivative_constant (x a : Rat) :
    eval (derivative (ofCoefficients [a])) x = 0 := by
  change evalCoefficients x
    (normalizeCoefficients (derivativeCoefficients (normalizeCoefficients [a]))) = 0
  by_cases ha : a = 0
  · subst a
    simp [normalizeCoefficients, trimReversed, derivativeCoefficients,
      evalCoefficients]
  · have hcan : CanonicalCoefficients [a] :=
      Or.inr ⟨[], a, by simp, ha⟩
    have hnorm := normalizeCoefficients_of_canonical [a] hcan
    rw [hnorm, derivativeCoefficients_constant, evalCoefficients_normalize]
    simp [evalCoefficients]

/-- The derivative of a linear polynomial evaluates to its exact slope
    coefficient (including the core rational embedding of one). -/
theorem eval_derivative_linear (x a b : Rat) :
    eval (derivative (ofCoefficients [a, b])) x =
      Rat.ofInt 1 * b := by
  change evalCoefficients x
    (normalizeCoefficients (derivativeCoefficients (normalizeCoefficients [a, b]))) =
      Rat.ofInt 1 * b
  by_cases hb : b = 0
  · subst b
    have hnorm : normalizeCoefficients [a, 0] =
        normalizeCoefficients [a] := by
      simp [normalizeCoefficients, trimReversed]
    rw [hnorm]
    change eval (derivative (ofCoefficients [a])) x = Rat.ofInt 1 * 0
    rw [eval_derivative_constant]
    simp [Rat.mul_zero]
  · have hcan : CanonicalCoefficients [a, b] :=
      Or.inr ⟨[a], b, by simp, hb⟩
    have hnorm := normalizeCoefficients_of_canonical [a, b] hcan
    rw [hnorm, evalCoefficients_normalize, derivativeCoefficients_linear]
    exact evalCoefficients_constant x _

/-- The derivative of a quadratic polynomial evaluates to its exact
    first-degree derivative polynomial. -/
theorem eval_derivative_quadratic (x a b c : Rat) :
    eval (derivative (ofCoefficients [a, b, c])) x =
      Rat.ofInt 1 * b + (Rat.ofInt 2 * c) * x := by
  change evalCoefficients x
    (normalizeCoefficients
      (derivativeCoefficients (normalizeCoefficients [a, b, c]))) =
        Rat.ofInt 1 * b + (Rat.ofInt 2 * c) * x
  by_cases hc : c = 0
  · subst c
    have hnorm : normalizeCoefficients [a, b, 0] =
        normalizeCoefficients [a, b] := by
      simp [normalizeCoefficients, trimReversed]
    rw [hnorm]
    change eval (derivative (ofCoefficients [a, b])) x =
      Rat.ofInt 1 * b + (Rat.ofInt 2 * 0) * x
    rw [eval_derivative_linear]
    simp [Rat.mul_zero, Rat.add_zero]
  · have hcan : CanonicalCoefficients [a, b, c] :=
      Or.inr ⟨[a, b], c, by simp, hc⟩
    have hnorm := normalizeCoefficients_of_canonical [a, b, c] hcan
    rw [hnorm, evalCoefficients_normalize, derivativeCoefficients_quadratic]
    exact evalCoefficients_linear x _ _


/-- Coefficientwise additive inverse. -/
def negateCoefficients (xs : List Rat) : List Rat :=
  xs.map (fun a => -a)

/-- Coefficientwise subtraction, with missing coefficients treated as zero. -/
def subtractCoefficients (xs ys : List Rat) : List Rat :=
  addCoefficients xs (negateCoefficients ys)

/-- Exact Horner evaluation commutes with coefficientwise negation. -/
theorem evalCoefficients_neg (x : Rat) (xs : List Rat) :
    evalCoefficients x (negateCoefficients xs) =
      -evalCoefficients x xs := by
  induction xs with
  | nil =>
      simp [negateCoefficients, evalCoefficients]
  | cons a rest ih =>
      change evalCoefficients x
        (-a :: negateCoefficients rest) =
          -evalCoefficients x (a :: rest)
      rw [evalCoefficients_cons, evalCoefficients_cons, ih]
      simp [Rat.neg_mul, Rat.neg_add]

/-- Exact evaluation of coefficientwise subtraction. -/
theorem evalCoefficients_subtract (x : Rat) (xs ys : List Rat) :
    evalCoefficients x (subtractCoefficients xs ys) =
      evalCoefficients x xs - evalCoefficients x ys := by
  simp [subtractCoefficients, evalCoefficients_add, evalCoefficients_neg,
    Rat.sub_eq_add_neg]

/-- Polynomial negation over exact rational coefficients. -/
def negate (p : RatPolynomial) : RatPolynomial :=
  ofCoefficients (negateCoefficients p.coefficients)

/-- Polynomial subtraction over exact rational coefficients. -/
def subtract (p q : RatPolynomial) : RatPolynomial :=
  ofCoefficients (subtractCoefficients p.coefficients q.coefficients)

/-- Exact polynomial negation agrees with the negative of evaluation. -/
theorem eval_negate (p : RatPolynomial) (x : Rat) :
    eval (negate p) x = -eval p x := by
  simp [eval, negate, ofCoefficients, evalCoefficients_normalize,
    evalCoefficients_neg]

/-- Exact polynomial subtraction agrees with subtraction of evaluations. -/
theorem eval_subtract (p q : RatPolynomial) (x : Rat) :
    eval (subtract p q) x = eval p x - eval q x := by
  simp [eval, subtract, ofCoefficients, evalCoefficients_normalize,
    evalCoefficients_subtract]


/-- Canonical coefficient list for a monomial c * X^k. -/
def monomialCoefficients (k : Nat) (c : Rat) : List Rat :=
  List.replicate k 0 ++ [c]

/-- Horner evaluation of a monomial is its exact rational power value. -/
theorem evalCoefficients_monomial (x c : Rat) (k : Nat) :
    evalCoefficients x (monomialCoefficients k c) = x ^ k * c := by
  induction k with
  | zero =>
      simp [monomialCoefficients, evalCoefficients_constant]
  | succ k ih =>
      change evalCoefficients x
        (0 :: monomialCoefficients k c) = x ^ (k + 1) * c
      rw [evalCoefficients_shift, ih]
      calc
        x * (x ^ k * c) = (x * x ^ k) * c := by
          rw [Rat.mul_assoc]
        _ = (x ^ k * x) * c := by rw [Rat.mul_comm x (x ^ k)]
        _ = x ^ (k + 1) * c := by rw [pow_succ]

/-- Exact rational polynomial representing a single monomial. -/
def monomial (k : Nat) (c : Rat) : RatPolynomial :=
  ofCoefficients (monomialCoefficients k c)

/-- Evaluation of a normalized monomial polynomial. -/
theorem eval_monomial (x c : Rat) (k : Nat) :
    eval (monomial k c) x = x ^ k * c := by
  simp [eval, monomial, ofCoefficients, evalCoefficients_normalize,
    evalCoefficients_monomial]

end CCFSM.P2749
