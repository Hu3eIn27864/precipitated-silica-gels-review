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


/-- Exact powers over Rat, with the exponent recursion made explicit. -/
def ratPow (x : Rat) : Nat → Rat
  | 0 => 1
  | Nat.succ n => ratPow x n * x

/-- Canonical coefficient list for a monomial c * X^k. -/
def monomialCoefficients (k : Nat) (c : Rat) : List Rat :=
  List.replicate k 0 ++ [c]

/-- Horner evaluation of a monomial is its exact rational power value. -/
theorem evalCoefficients_monomial (x c : Rat) (k : Nat) :
    evalCoefficients x (monomialCoefficients k c) = ratPow x k * c := by
  induction k with
  | zero =>
      simp [monomialCoefficients, evalCoefficients_constant, ratPow]
  | succ k ih =>
      change evalCoefficients x
        (0 :: monomialCoefficients k c) = ratPow x (k + 1) * c
      rw [evalCoefficients_shift, ih]
      calc
        x * (ratPow x k * c) = (x * ratPow x k) * c := by
          rw [Rat.mul_assoc]
        _ = (ratPow x k * x) * c := by rw [Rat.mul_comm x (ratPow x k)]
        _ = ratPow x (k + 1) * c := by rfl

/-- Exact rational polynomial representing a single monomial. -/
def monomial (k : Nat) (c : Rat) : RatPolynomial :=
  ofCoefficients (monomialCoefficients k c)

/-- Evaluation of a normalized monomial polynomial. -/
theorem eval_monomial (x c : Rat) (k : Nat) :
    eval (monomial k c) x = ratPow x k * c := by
  simp [eval, monomial, ofCoefficients, evalCoefficients_normalize,
    evalCoefficients_monomial]


/-- The option-valued degree is the list length minus one for every nonzero
    canonical polynomial. -/
theorem degree?_some_of_nonempty (p : RatPolynomial)
    (hp : p.coefficients ≠ []) :
    degree? p = some (p.coefficients.length - 1) := by
  obtain ⟨c, hc, hcn⟩ := leadingCoefficient?_nonzero p hp
  simp [degree?, hc]

/-- Every nonzero canonical polynomial has an explicit last coefficient. -/
theorem canonical_coefficients_decompose (p : RatPolynomial)
    (hp : p.coefficients ≠ []) :
    ∃ init last, p.coefficients = init ++ [last] ∧ last ≠ 0 := by
  rcases p.canonical with hnil | ⟨init, last, hcoeff, hlast⟩
  · exact False.elim (hp hnil)
  · exact ⟨init, last, hcoeff, hlast⟩


/-- Prefix a coefficient vector by k zeros after scaling all coefficients. -/
def shiftedScaleCoefficients (k : Nat) (c : Rat) (xs : List Rat) : List Rat :=
  List.replicate k 0 ++ scaleCoefficients c xs

/-- Exact evaluation of a shifted and scaled coefficient vector. -/
theorem evalCoefficients_shiftedScale (x c : Rat) (xs : List Rat) (k : Nat) :
    evalCoefficients x (shiftedScaleCoefficients k c xs) =
      ratPow x k * (c * evalCoefficients x xs) := by
  induction k with
  | zero =>
      simp [shiftedScaleCoefficients, evalCoefficients_scale, ratPow]
  | succ k ih =>
      change evalCoefficients x
        (0 :: shiftedScaleCoefficients k c xs) =
          ratPow x (k + 1) * (c * evalCoefficients x xs)
      rw [evalCoefficients_shift, ih]
      calc
        x * (ratPow x k * (c * evalCoefficients x xs)) =
            (x * ratPow x k) * (c * evalCoefficients x xs) := by
              rw [Rat.mul_assoc]
        _ = (ratPow x k * x) * (c * evalCoefficients x xs) := by
              rw [Rat.mul_comm x (ratPow x k)]
        _ = ratPow x (k + 1) * (c * evalCoefficients x xs) := by rfl

/-- Polynomial scalar multiplication with canonical normalization. -/
def scale (c : Rat) (p : RatPolynomial) : RatPolynomial :=
  ofCoefficients (scaleCoefficients c p.coefficients)

/-- Exact evaluation commutes with rational polynomial scaling. -/
theorem eval_scale (c : Rat) (p : RatPolynomial) (x : Rat) :
    eval (scale c p) x = c * eval p x := by
  simp [eval, scale, ofCoefficients, evalCoefficients_normalize,
    evalCoefficients_scale]


/-- Coefficientwise addition preserves the final pair when prefix lengths match. -/
theorem addCoefficients_append_singleton
    (xs ys : List Rat) (a b : Rat)
    (hlen : xs.length = ys.length) :
    addCoefficients (xs ++ [a]) (ys ++ [b]) =
      addCoefficients xs ys ++ [a + b] := by
  induction xs generalizing ys with
  | nil =>
      cases ys with
      | nil => simp [addCoefficients]
      | cons y ys => simp at hlen
  | cons x xs ih =>
      cases ys with
      | nil => simp at hlen
      | cons y ys =>
          have htail : xs.length = ys.length := Nat.succ.inj hlen
          simp only [List.cons_append, addCoefficients]
          rw [ih ys htail]

/-- Subtraction preserves the final pair when prefix lengths match. -/
theorem subtractCoefficients_append_singleton
    (xs ys : List Rat) (a b : Rat)
    (hlen : xs.length = ys.length) :
    subtractCoefficients (xs ++ [a]) (ys ++ [b]) =
      subtractCoefficients xs ys ++ [a - b] := by
  unfold subtractCoefficients negateCoefficients
  rw [List.map_append]
  have hmap : xs.length = (ys.map (fun z => -z)).length := by
    simpa using hlen
  change addCoefficients (xs ++ [a])
      (ys.map (fun z => -z) ++ [-b]) =
    addCoefficients xs (ys.map (fun z => -z)) ++ [a - b]
  rw [addCoefficients_append_singleton xs (ys.map (fun z => -z)) a (-b) hmap]
  simp [Rat.sub_eq_add_neg]

/-- Removing one trailing zero does not change canonical normalization. -/
theorem normalizeCoefficients_append_zero (xs : List Rat) :
    normalizeCoefficients (xs ++ [0]) = normalizeCoefficients xs := by
  simp [normalizeCoefficients, List.reverse_append, trimReversed]

/-- Trimming reversed coefficients never increases the list length. -/
theorem trimReversed_length_le (xs : List Rat) :
    (trimReversed xs).length ≤ xs.length := by
  induction xs with
  | nil =>
      simp [trimReversed]
  | cons a rest ih =>
      simp only [trimReversed]
      split
      · exact Nat.le_trans ih (Nat.le_succ _)
      · exact Nat.le_refl _

/-- Canonical normalization never increases the number of coefficients. -/
theorem normalizeCoefficients_length_le (xs : List Rat) :
    (normalizeCoefficients xs).length ≤ xs.length := by
  simpa [normalizeCoefficients] using trimReversed_length_le xs.reverse


/-- Aligned coefficient subtraction cancels equal final coefficients. -/
theorem subtractCoefficients_append_equal_last
    (xs ys : List Rat) (a : Rat)
    (hlen : xs.length = ys.length) :
    subtractCoefficients (xs ++ [a]) (ys ++ [a]) =
      subtractCoefficients xs ys ++ [0] := by
  rw [subtractCoefficients_append_singleton xs ys a a hlen]
  exact congrArg (fun z : Rat => subtractCoefficients xs ys ++ [z])
    (Rat.sub_self)

/-- Aligned coefficient addition cannot increase the common vector length. -/
theorem addCoefficients_length_le_of_equal
    (xs ys : List Rat) (hlen : xs.length = ys.length) :
    (addCoefficients xs ys).length ≤ xs.length := by
  induction xs generalizing ys with
  | nil =>
      cases ys with
      | nil => simp [addCoefficients]
      | cons y ys => simp at hlen
  | cons x xs ih =>
      cases ys with
      | nil => simp at hlen
      | cons y ys =>
          have htail : xs.length = ys.length := Nat.succ.inj hlen
          simp only [addCoefficients, List.length_cons]
          exact Nat.succ_le_succ (ih ys htail)

/-- The coefficient vector produced by aligned subtraction has no more
    entries than either input prefix once the equal leading term is cancelled. -/
theorem normalize_aligned_cancellation_length
    (xs ys : List Rat) (a : Rat)
    (hlen : xs.length = ys.length) :
    (normalizeCoefficients
      (subtractCoefficients (xs ++ [a]) (ys ++ [a]))).length ≤ xs.length := by
  rw [subtractCoefficients_append_equal_last xs ys a hlen]
  rw [normalizeCoefficients_append_zero]
  exact Nat.le_trans
    (normalizeCoefficients_length_le (subtractCoefficients xs ys))
    (addCoefficients_length_le_of_equal xs (negateCoefficients ys)
      (by simpa [negateCoefficients] using hlen))


/-- Equal-leading-term cancellation strictly decreases the canonical
    coefficient-vector length. This is the well-founded measure used by the
    forthcoming long-division recursion (length = degree + 1 for nonzero
    canonical polynomials). -/
theorem normalize_aligned_cancellation_length_strict
    (xs ys : List Rat) (a : Rat)
    (hlen : xs.length = ys.length) :
    (normalizeCoefficients
      (subtractCoefficients (xs ++ [a]) (ys ++ [a]))).length <
        (xs ++ [a]).length := by
  have hbound :=
    normalize_aligned_cancellation_length xs ys a hlen
  simpa using Nat.lt_succ_of_le hbound


/-- Shifting a coefficient vector by k degrees and scaling it does not
    change its length except for the k inserted low-degree zero slots. -/
theorem shiftedScaleCoefficients_length (k : Nat) (c : Rat)
    (xs : List Rat) :
    (shiftedScaleCoefficients k c xs).length = k + xs.length := by
  simp [shiftedScaleCoefficients, scaleCoefficients]


/-- Adding an empty coefficient vector on the right leaves the left
    coefficient vector unchanged. -/
theorem addCoefficients_nil_right (xs : List Rat) :
    addCoefficients xs [] = xs := by
  cases xs <;> rfl

/-- Multiplication by a constant polynomial scales a nonempty coefficient
    vector exactly. The nonempty premise excludes the implementation's
    empty-list edge case, where the recursive convolution returns []. -/
theorem multiplyCoefficients_singleton_left (c : Rat) (xs : List Rat)
    (hxs : xs ≠ []) :
    multiplyCoefficients [c] xs = scaleCoefficients c xs := by
  cases xs with
  | nil => exact False.elim (hxs rfl)
  | cons b bs =>
      simp only [multiplyCoefficients, scaleCoefficients, List.map_cons,
        addCoefficients]
      simp [addCoefficients_nil_right, Rat.add_zero]


/-- Adding a zero-scaled coefficient vector on the left leaves the right
    vector unchanged whenever the latter is at least as long. This captures
    the zero-padding alignment needed by the monomial-shift convolution proof. -/
theorem addCoefficients_zero_scaled_left_of_length_le
    (xs ys : List Rat) (hlen : xs.length ≤ ys.length) :
    addCoefficients (scaleCoefficients 0 xs) ys = ys := by
  induction xs generalizing ys with
  | nil =>
      simp [scaleCoefficients, addCoefficients]
  | cons a rest ih =>
      cases ys with
      | nil =>
          simp at hlen
      | cons b tail =>
          have htail : rest.length ≤ tail.length :=
            Nat.le_of_succ_le_succ hlen
          simp only [scaleCoefficients, List.map_cons, Rat.zero_mul,
            addCoefficients]
          have hscale : List.map (fun _ : Rat => (0 : Rat)) rest =
              scaleCoefficients 0 rest := by
            simp [scaleCoefficients, Rat.zero_mul]
          rw [hscale, ih tail htail]
          simp [Rat.zero_add]


/-- Convolution by a monomial has the expected coefficient-vector length
    whenever the right-hand coefficient vector is nonempty. -/
theorem multiplyCoefficients_monomial_length (k : Nat) (c : Rat)
    (xs : List Rat) (hxs : xs ≠ []) :
    (multiplyCoefficients (monomialCoefficients k c) xs).length =
      k + xs.length := by
  induction k with
  | zero =>
      rw [show monomialCoefficients 0 c = [c] by rfl]
      rw [multiplyCoefficients_singleton_left c xs hxs]
      simp [scaleCoefficients]
  | succ k ih =>
      change (addCoefficients (scaleCoefficients 0 xs)
        (0 :: multiplyCoefficients (monomialCoefficients k c) xs)).length =
          Nat.succ k + xs.length
      have htail := ih
      have hle : xs.length ≤ k + xs.length + 1 := by
        simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
          (Nat.le_add_right xs.length (k + 1))
      have halign := addCoefficients_zero_scaled_left_of_length_le
        xs (0 :: multiplyCoefficients (monomialCoefficients k c) xs)
        (by simpa [htail] using hle)
      rw [halign]
      simp [htail, Nat.succ_eq_add_one, Nat.add_assoc, Nat.add_comm,
        Nat.add_left_comm]


/-- Convolution by a monomial is exactly the corresponding low-degree
    shift followed by coefficientwise scaling, for nonempty right input. -/
theorem multiplyCoefficients_monomial (k : Nat) (c : Rat)
    (xs : List Rat) (hxs : xs ≠ []) :
    multiplyCoefficients (monomialCoefficients k c) xs =
      shiftedScaleCoefficients k c xs := by
  induction k with
  | zero =>
      rw [show monomialCoefficients 0 c = [c] by rfl]
      exact multiplyCoefficients_singleton_left c xs hxs
  | succ k ih =>
      change addCoefficients (scaleCoefficients 0 xs)
        (0 :: multiplyCoefficients (monomialCoefficients k c) xs) =
          0 :: shiftedScaleCoefficients k c xs
      have htail := ih
      have hlen := multiplyCoefficients_monomial_length k c xs hxs
      have hle : xs.length ≤ k + xs.length + 1 := by
        simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
          (Nat.le_add_right xs.length (k + 1))
      have halign := addCoefficients_zero_scaled_left_of_length_le
        xs (0 :: multiplyCoefficients (monomialCoefficients k c) xs)
        (by simpa [hlen] using hle)
      rw [halign, htail]


/-- For a nonzero canonical input and nonzero scalar, monomial convolution
    ends in the expected scaled leading coefficient. -/
theorem multiplyCoefficients_monomial_final_coefficient
    (k : Nat) (c : Rat) (xs : List Rat)
    (hxs : xs ≠ []) (hcanon : CanonicalCoefficients xs)
    (hc : c ≠ 0) :
    ∃ init last,
      multiplyCoefficients (monomialCoefficients k c) xs = init ++ [last] ∧
        last ≠ 0 ∧
        ∃ init originalLast,
          xs = init ++ [originalLast] ∧ last = c * originalLast := by
  rcases hcanon with hnil | ⟨init, originalLast, hcoeff, hlast⟩
  · exact False.elim (hxs hnil)
  · subst xs
    rw [multiplyCoefficients_monomial k c (init ++ [originalLast])
      (by simp)]
    have hproduct : c * originalLast ≠ 0 := by
      intro hzero
      rcases Rat.mul_eq_zero.mp hzero with hzero | hzero
      · exact hc hzero
      · exact hlast hzero
    refine ⟨List.replicate k 0 ++ scaleCoefficients c init,
      c * originalLast, ?_, hproduct,
      ⟨init, originalLast, rfl, rfl⟩⟩
    simp [shiftedScaleCoefficients, scaleCoefficients, List.map_append,
      List.append_assoc]


/-- Choosing the quotient of a target final coefficient by a nonzero
    divisor final coefficient makes the monomial-convolution final term
    cancel that divisor coefficient exactly. -/
theorem multiplyCoefficients_monomial_cancels_final
    (k : Nat) (aR aB : Rat) (xs : List Rat)
    (hdecomp : ∃ pre, xs = pre ++ [aB]) (haB : aB ≠ 0) :
    ∃ pre,
      multiplyCoefficients (monomialCoefficients k (aR / aB)) xs =
        pre ++ [aR] := by
  rcases hdecomp with ⟨pre, rfl⟩
  rw [multiplyCoefficients_monomial k (aR / aB) (pre ++ [aB]) (by simp)]
  have hcancel : aR / aB * aB = aR := Rat.div_mul_cancel haB
  refine ⟨List.replicate k 0 ++ scaleCoefficients (aR / aB) pre, ?_⟩
  simp only [shiftedScaleCoefficients, scaleCoefficients, List.map_append,
    List.map_cons, List.map_nil]
  rw [List.append_assoc, hcancel]


/-- One monomial long-division subtraction strictly shortens the
    normalized coefficient vector, provided the dividend and shifted divisor
    have matching lengths and the divisor's final coefficient is nonzero. -/
theorem normalize_subtract_monomial_step_length_strict
    (k : Nat) (aR aB : Rat) (r d : List Rat)
    (hr : ∃ rpre, r = rpre ++ [aR])
    (hd : ∃ dpre, d = dpre ++ [aB])
    (haB : aB ≠ 0)
    (hsize : r.length = k + d.length) :
    (normalizeCoefficients
      (subtractCoefficients r
        (multiplyCoefficients (monomialCoefficients k (aR / aB)) d))).length <
      r.length := by
  rcases hr with ⟨rpre, rfl⟩
  rcases hd with ⟨dpre, rfl⟩
  obtain ⟨qpre, hq⟩ :=
    multiplyCoefficients_monomial_cancels_final k aR aB
      (dpre ++ [aB]) ⟨dpre, rfl⟩ haB
  have hprodlen :=
    multiplyCoefficients_monomial_length k (aR / aB)
      (dpre ++ [aB]) (by simp)
  have htot : (rpre ++ [aR]).length = (qpre ++ [aR]).length := by
    calc
      (rpre ++ [aR]).length = k + (dpre ++ [aB]).length := hsize
      _ = (multiplyCoefficients
            (monomialCoefficients k (aR / aB)) (dpre ++ [aB])).length :=
              hprodlen.symm
      _ = (qpre ++ [aR]).length := by rw [hq]
  have hprefix : rpre.length = qpre.length := by
    apply Nat.succ.inj
    simpa using htot
  rw [hq]
  exact normalize_aligned_cancellation_length_strict rpre qpre aR hprefix


/-- For every nonzero canonical polynomial, its option-valued degree plus
    one is exactly the coefficient-vector length. -/
theorem degree?_add_one_eq_length (p : RatPolynomial)
    (hp : p.coefficients ≠ []) :
    ∃ d, degree? p = some d ∧ d + 1 = p.coefficients.length := by
  have hdegree := degree?_some_of_nonempty p hp
  refine ⟨p.coefficients.length - 1, hdegree, ?_⟩
  cases hcoeff : p.coefficients with
  | nil => exact False.elim (hp hcoeff)
  | cons a rest => simp


/-- A strict decrease in normalized coefficient-vector length gives a
    strict decrease in option-valued polynomial degree whenever both
    canonical polynomials are nonzero. -/
theorem degree?_lt_of_normalized_length_lt
    (p : RatPolynomial) (xs : List Rat)
    (hp : p.coefficients ≠ [])
    (hxs : normalizeCoefficients xs ≠ [])
    (hlen : (normalizeCoefficients xs).length < p.coefficients.length) :
    ∃ dResult dDividend,
      degree? (ofCoefficients xs) = some dResult ∧
        degree? p = some dDividend ∧ dResult < dDividend := by
  have hresult_nonempty : (ofCoefficients xs).coefficients ≠ [] := by
    simpa [ofCoefficients] using hxs
  obtain ⟨dResult, hresult_degree, hresult_length⟩ :=
    degree?_add_one_eq_length (ofCoefficients xs) hresult_nonempty
  obtain ⟨dDividend, hdividend_degree, hdividend_length⟩ :=
    degree?_add_one_eq_length p hp
  refine ⟨dResult, dDividend, hresult_degree, hdividend_degree, ?_⟩
  have hsucc : dResult + 1 < dDividend + 1 := by
    simpa [ofCoefficients, hresult_length, hdividend_length] using hlen
  exact Nat.lt_of_succ_lt_succ hsucc


/-- Polynomial-level degree decrease for one exact monomial subtraction.
    The dividend and divisor coefficient lists must have the stated final
    coefficients and matching shifted lengths; the normalized result must
    remain nonzero for its degree to be defined. -/
theorem degree?_monomial_subtract_step_lt
    (p : RatPolynomial) (d : List Rat) (k : Nat) (aR aB : Rat)
    (hr : ∃ rpre, p.coefficients = rpre ++ [aR])
    (hd : ∃ dpre, d = dpre ++ [aB])
    (haB : aB ≠ 0)
    (hsize : p.coefficients.length = k + d.length)
    (hresult : normalizeCoefficients (subtractCoefficients p.coefficients
        (multiplyCoefficients (monomialCoefficients k (aR / aB)) d)) ≠ []) :
    ∃ dResult dDividend,
      degree? (ofCoefficients (subtractCoefficients p.coefficients
        (multiplyCoefficients (monomialCoefficients k (aR / aB)) d))) = some dResult ∧
        degree? p = some dDividend ∧ dResult < dDividend := by
  have hp : p.coefficients ≠ [] := by
    rcases hr with ⟨rpre, hcoeff⟩
    rw [hcoeff]
    simp
  have hstep := normalize_subtract_monomial_step_length_strict
    k aR aB p.coefficients d hr hd haB hsize
  exact degree?_lt_of_normalized_length_lt p (subtractCoefficients p.coefficients
        (multiplyCoefficients (monomialCoefficients k (aR / aB)) d)) hp hresult hstep


/-- Subtract a scalar monomial multiple of a divisor polynomial and
    normalize the resulting coefficient vector. -/
def subtractMonomial (p q : RatPolynomial) (k : Nat) (c : Rat) :
    RatPolynomial :=
  ofCoefficients
    (subtractCoefficients p.coefficients
      (multiplyCoefficients (monomialCoefficients k c) q.coefficients))

/-- The canonical polynomial produced by an exact monomial cancellation
    has strictly smaller degree, provided it is nonzero and the shifted
    divisor has the same coefficient-vector length as the dividend. -/
theorem degree?_subtractMonomial_lt
    (p q : RatPolynomial) (k : Nat) (aR aB : Rat)
    (hr : ∃ rpre, p.coefficients = rpre ++ [aR])
    (hd : ∃ dpre, q.coefficients = dpre ++ [aB])
    (haB : aB ≠ 0)
    (hsize : p.coefficients.length = k + q.coefficients.length)
    (hresult : (subtractMonomial p q k (aR / aB)).coefficients ≠ []) :
    ∃ dResult dDividend,
      degree? (subtractMonomial p q k (aR / aB)) = some dResult ∧
        degree? p = some dDividend ∧ dResult < dDividend := by
  have hp : p.coefficients ≠ [] := by
    rcases hr with ⟨rpre, hcoeff⟩
    rw [hcoeff]
    simp
  have hstep := normalize_subtract_monomial_step_length_strict
    k aR aB p.coefficients q.coefficients hr hd haB hsize
  have hresult' :
      normalizeCoefficients
        (subtractCoefficients p.coefficients
          (multiplyCoefficients (monomialCoefficients k (aR / aB))
            q.coefficients)) ≠ [] := by
    simpa [subtractMonomial, ofCoefficients] using hresult
  exact degree?_lt_of_normalized_length_lt p
    (subtractCoefficients p.coefficients
      (multiplyCoefficients (monomialCoefficients k (aR / aB))
        q.coefficients)) hp hresult' hstep


/-- The leading-coefficient accessor returns the final ascending
    coefficient of every nonempty canonical polynomial. -/
theorem leadingCoefficient?_eq_last (p : RatPolynomial)
    (hp : p.coefficients ≠ []) :
    ∃ pre last,
      p.coefficients = pre ++ [last] ∧ last ≠ 0 ∧
        leadingCoefficient? p = some last := by
  obtain ⟨pre, last, hcoeff, hlast⟩ :=
    canonical_coefficients_decompose p hp
  refine ⟨pre, last, hcoeff, hlast, ?_⟩
  simp [leadingCoefficient?, hcoeff, List.reverse_append]


/-- Select the leading-term monomial subtraction from two nonzero
    canonical polynomials. The zero fallback keeps the definition total;
    the degree-decrease theorem below requires both inputs to be nonzero. -/
def subtractMonomialLeading (p q : RatPolynomial) : RatPolynomial :=
  match leadingCoefficient? p, leadingCoefficient? q with
  | some aR, some aB =>
      subtractMonomial p q (p.coefficients.length - q.coefficients.length)
        (aR / aB)
  | _, _ => zero

/-- For nonzero canonical dividend and divisor with divisor length no
    greater than dividend length, the automatically selected leading-term
    subtraction strictly decreases degree whenever its result is nonzero. -/
theorem degree?_subtractMonomialLeading_lt
    (p q : RatPolynomial)
    (hp : p.coefficients ≠ []) (hq : q.coefficients ≠ [])
    (hlen : q.coefficients.length ≤ p.coefficients.length)
    (hresult : (subtractMonomialLeading p q).coefficients ≠ []) :
    ∃ dResult dDividend,
      degree? (subtractMonomialLeading p q) = some dResult ∧
        degree? p = some dDividend ∧ dResult < dDividend := by
  obtain ⟨rpre, aR, hr, haR, hleadR⟩ := leadingCoefficient?_eq_last p hp
  obtain ⟨dpre, aB, hd, haB, hleadB⟩ := leadingCoefficient?_eq_last q hq
  have hsize : p.coefficients.length =
      (p.coefficients.length - q.coefficients.length) + q.coefficients.length :=
    (Nat.sub_add_cancel hlen).symm
  have hresult' :
      (subtractMonomial p q (p.coefficients.length - q.coefficients.length)
        (aR / aB)).coefficients ≠ [] := by
    simpa [subtractMonomialLeading, hleadR, hleadB] using hresult
  have hstep := degree?_subtractMonomial_lt p q
    (p.coefficients.length - q.coefficients.length) aR aB
    ⟨rpre, hr⟩ ⟨dpre, hd⟩ haB hsize hresult'
  simpa [subtractMonomialLeading, hleadR, hleadB] using hstep


/-- The automatically selected leading-term subtraction either produces
    the zero polynomial or a nonzero polynomial of strictly smaller degree.
    This packages the terminal branch needed by a well-founded division
    recursion without assigning a natural degree to zero. -/
theorem subtractMonomialLeading_zero_or_degree_lt
    (p q : RatPolynomial)
    (hp : p.coefficients ≠ []) (hq : q.coefficients ≠ [])
    (hlen : q.coefficients.length ≤ p.coefficients.length) :
    degree? (subtractMonomialLeading p q) = none ∨
      ∃ dResult dDividend,
        degree? (subtractMonomialLeading p q) = some dResult ∧
          degree? p = some dDividend ∧ dResult < dDividend := by
  by_cases hresult : (subtractMonomialLeading p q).coefficients = []
  · left
    simp [degree?, leadingCoefficient?, hresult]
  · right
    exact degree?_subtractMonomialLeading_lt p q hp hq hlen hresult


/-- Evaluation of one canonical monomial-subtraction step is exactly
    dividend minus the selected monomial multiple of the divisor. -/
theorem eval_subtractMonomial (p q : RatPolynomial) (k : Nat)
    (c x : Rat) :
    eval (subtractMonomial p q k c) x =
      eval p x - ratPow x k * (c * eval q x) := by
  simp [subtractMonomial, eval, ofCoefficients,
    evalCoefficients_normalize, evalCoefficients_subtract,
    evalCoefficients_multiply, evalCoefficients_monomial,
    Rat.mul_assoc]


/-- Scalar conservation identity behind one quotient/remainder update. -/
theorem rational_division_update_identity
    (qValue termValue divisorValue remainderValue : Rat) :
    (qValue + termValue) * divisorValue +
        (remainderValue - termValue * divisorValue) =
      qValue * divisorValue + remainderValue := by
  calc
    (qValue + termValue) * divisorValue +
        (remainderValue - termValue * divisorValue) =
      qValue * divisorValue +
        (termValue * divisorValue +
          (remainderValue - termValue * divisorValue)) := by
            rw [Rat.add_mul, Rat.add_assoc]
    _ = qValue * divisorValue + remainderValue := by
          congr 1
          calc
            termValue * divisorValue +
                (remainderValue - termValue * divisorValue) =
              termValue * divisorValue +
                (remainderValue + -(termValue * divisorValue)) := by
                  rw [Rat.sub_eq_add_neg]
            _ = (termValue * divisorValue + remainderValue) +
                -(termValue * divisorValue) := by
                  rw [Rat.add_assoc]
            _ = (remainderValue + termValue * divisorValue) +
                -(termValue * divisorValue) := by
                  rw [Rat.add_comm (termValue * divisorValue) remainderValue]
            _ = remainderValue +
                (termValue * divisorValue +
                  -(termValue * divisorValue)) := by
                  rw [← Rat.add_assoc]
            _ = remainderValue := by
                  rw [Rat.add_neg_cancel, Rat.add_zero]

/-- Adding one monomial to the quotient while subtracting the same
    monomial multiple of the divisor from the remainder preserves the
    evaluated quotient-times-divisor-plus-remainder invariant. -/
theorem eval_division_update
    (quotient remainder divisor : RatPolynomial)
    (k : Nat) (c x : Rat) :
    eval (add quotient (monomial k c)) x * eval divisor x +
        eval (subtractMonomial remainder divisor k c) x =
      eval quotient x * eval divisor x + eval remainder x := by
  rw [eval_add, eval_monomial, eval_subtractMonomial]
  simpa [Rat.mul_assoc] using
    rational_division_update_identity
      (eval quotient x) (ratPow x k * c) (eval divisor x)
      (eval remainder x)


/-- State of a finite exact long-division trace. -/
structure DivisionState where
  quotient : RatPolynomial
  remainder : RatPolynomial

/-- One trace step adds a quotient monomial and subtracts the same
    monomial multiple of the divisor from the current remainder. -/
def divisionStep (divisor : RatPolynomial) (state : DivisionState)
    (k : Nat) (c : Rat) : DivisionState :=
  { quotient := add state.quotient (monomial k c)
    remainder := subtractMonomial state.remainder divisor k c }

/-- Automatically select the next quotient monomial from the leading
    coefficients of the current remainder and divisor. If either polynomial
    is zero, leave the state unchanged. -/
def leadingDivisionStep (divisor : RatPolynomial)
    (state : DivisionState) : DivisionState :=
  match leadingCoefficient? state.remainder, leadingCoefficient? divisor with
  | some aR, some aB =>
      if divisor.coefficients.length ≤ state.remainder.coefficients.length then
        divisionStep divisor state
          (state.remainder.coefficients.length - divisor.coefficients.length)
          (aR / aB)
      else
        state
  | _, _ => state

/-- A zero remainder, or a divisor coefficient vector longer than
    the remainder vector, is a fixed point of the guarded transition. -/
theorem leadingDivisionStep_eq_self_of_terminal
    (divisor : RatPolynomial) (state : DivisionState)
    (hterminal :
      state.remainder.coefficients = [] ∨
        divisor.coefficients.length > state.remainder.coefficients.length) :
    leadingDivisionStep divisor state = state := by
  rcases hterminal with hzero | hlength
  · simp [leadingDivisionStep, leadingCoefficient?, hzero]
  · cases hR : leadingCoefficient? state.remainder <;>
      cases hB : leadingCoefficient? divisor <;>
      simp [leadingDivisionStep, hR, hB, Nat.not_le_of_gt hlength]

/-- One automatically selected leading-term update preserves the exact
    evaluated quotient/remainder invariant whenever its two leading
    coefficients are available and the divisor degree fits. -/
theorem eval_leadingDivisionStep
    (divisor : RatPolynomial) (state : DivisionState)
    (aR aB x : Rat)
    (hR : leadingCoefficient? state.remainder = some aR)
    (hB : leadingCoefficient? divisor = some aB)
    (hlen : divisor.coefficients.length ≤ state.remainder.coefficients.length) :
    eval (leadingDivisionStep divisor state).quotient x *
        eval divisor x +
      eval (leadingDivisionStep divisor state).remainder x =
    eval state.quotient x * eval divisor x +
      eval state.remainder x := by
  simp only [leadingDivisionStep, hR, hB, if_pos hlen, divisionStep]
  exact eval_division_update state.quotient state.remainder divisor
    (state.remainder.coefficients.length - divisor.coefficients.length)
    (aR / aB) x


/-- A guarded automatic leading-term update either terminates at
    the zero remainder or strictly lowers the remainder degree. -/
theorem degree?_leadingDivisionStep_zero_or_lt
    (divisor : RatPolynomial) (state : DivisionState)
    (aR aB : Rat)
    (hR : leadingCoefficient? state.remainder = some aR)
    (hB : leadingCoefficient? divisor = some aB)
    (hlen : divisor.coefficients.length ≤ state.remainder.coefficients.length) :
    degree? (leadingDivisionStep divisor state).remainder = none ∨
      ∃ dResult dDividend,
        degree? (leadingDivisionStep divisor state).remainder = some dResult ∧
          degree? state.remainder = some dDividend ∧
            dResult < dDividend := by
  have hp : state.remainder.coefficients ≠ [] := by
    intro hzero
    simp [leadingCoefficient?, hzero] at hR
  have hq : divisor.coefficients ≠ [] := by
    intro hzero
    simp [leadingCoefficient?, hzero] at hB
  have hdrop := subtractMonomialLeading_zero_or_degree_lt
    state.remainder divisor hp hq hlen
  simpa [leadingDivisionStep, hR, hB, if_pos hlen, divisionStep,
    subtractMonomialLeading] using hdrop


/-- For a nonzero divisor, the guarded leading-term transition is a
    fixed point exactly when the remainder is zero or the divisor no longer
    fits by coefficient-vector length. -/
theorem leadingDivisionStep_eq_self_iff_terminal
    (divisor : RatPolynomial) (state : DivisionState)
    (hdivisor : divisor.coefficients ≠ []) :
    leadingDivisionStep divisor state = state ↔
      state.remainder.coefficients = [] ∨
        divisor.coefficients.length > state.remainder.coefficients.length := by
  constructor
  · intro hstep
    by_cases hrem : state.remainder.coefficients = []
    · exact Or.inl hrem
    · obtain ⟨aR, hR, _⟩ :=
        leadingCoefficient?_nonzero state.remainder hrem
      obtain ⟨aB, hB, _⟩ :=
        leadingCoefficient?_nonzero divisor hdivisor
      by_cases hfit :
          divisor.coefficients.length ≤ state.remainder.coefficients.length
      · have hdrop :=
          degree?_leadingDivisionStep_zero_or_lt
            divisor state aR aB hR hB hfit
        have hdegree := degree?_some_of_nonempty state.remainder hrem
        have hsame := congrArg DivisionState.remainder hstep
        rw [hsame] at hdrop
        rcases hdrop with hzero | ⟨dResult, dDividend, hResult, hDividend, hlt⟩
        · rw [hdegree] at hzero
          cases hzero
        · rw [hdegree] at hResult hDividend
          have heq : dResult = dDividend :=
            Option.some.inj (hResult.symm.trans hDividend)
          exact False.elim (Nat.lt_irrefl dDividend (heq ▸ hlt))
      · exact Or.inr (Nat.lt_of_not_ge hfit)
  · intro hterminal
    exact leadingDivisionStep_eq_self_of_terminal divisor state hterminal

/-- Execute a finite, explicitly supplied sequence of monomial updates.
    This is a trace interpreter, not yet the terminating division algorithm. -/
def runDivisionSteps (divisor : RatPolynomial) :
    DivisionState → List (Nat × Rat) → DivisionState
  | state, [] => state
  | state, (k, c) :: rest =>
      runDivisionSteps divisor (divisionStep divisor state k c) rest

/-- The quotient-times-divisor-plus-remainder evaluation invariant is
    preserved by every finite sequence of exact monomial division steps.
    The trace is supplied explicitly; this theorem does not yet prove that
    the long-division algorithm generates a terminating trace. -/
theorem eval_runDivisionSteps
    (divisor : RatPolynomial) (initial : DivisionState)
    (steps : List (Nat × Rat)) (x : Rat) :
    eval (runDivisionSteps divisor initial steps).quotient x *
        eval divisor x +
      eval (runDivisionSteps divisor initial steps).remainder x =
    eval initial.quotient x * eval divisor x +
      eval initial.remainder x := by
  induction steps generalizing initial with
  | nil =>
      rfl
  | cons step rest ih =>
      cases step with
      | mk k c =>
          calc
            eval (runDivisionSteps divisor
                (divisionStep divisor initial k c) rest).quotient x *
                eval divisor x +
              eval (runDivisionSteps divisor
                (divisionStep divisor initial k c) rest).remainder x =
                eval (divisionStep divisor initial k c).quotient x *
                  eval divisor x +
                eval (divisionStep divisor initial k c).remainder x := by
                  exact ih (divisionStep divisor initial k c)
            _ = eval initial.quotient x * eval divisor x +
                eval initial.remainder x := by
                  exact eval_division_update initial.quotient
                    initial.remainder divisor k c x


/-- The canonical zero polynomial evaluates to zero at every rational point. -/
theorem eval_zero (x : Rat) : eval zero x = 0 := by
  simp [eval, zero, ofCoefficients, normalizeCoefficients, trimReversed,
    evalCoefficients]

/-- Start a division trace with zero quotient and the full dividend as
    remainder. -/
def initialDivisionState (dividend : RatPolynomial) : DivisionState :=
  { quotient := zero, remainder := dividend }

/-- Every finite monomial trace starting from (0, dividend) satisfies the
    evaluated quotient/remainder identity for the original dividend. -/
theorem eval_runDivisionSteps_from_dividend
    (dividend divisor : RatPolynomial)
    (steps : List (Nat × Rat)) (x : Rat) :
    eval (runDivisionSteps divisor (initialDivisionState dividend)
      steps).quotient x * eval divisor x +
      eval (runDivisionSteps divisor (initialDivisionState dividend)
        steps).remainder x = eval dividend x := by
  calc
    eval (runDivisionSteps divisor (initialDivisionState dividend)
        steps).quotient x * eval divisor x +
      eval (runDivisionSteps divisor (initialDivisionState dividend)
        steps).remainder x =
      eval (initialDivisionState dividend).quotient x * eval divisor x +
        eval (initialDivisionState dividend).remainder x :=
          eval_runDivisionSteps divisor (initialDivisionState dividend) steps x
    _ = eval dividend x := by
          simp [initialDivisionState, eval_zero, Rat.zero_mul, Rat.zero_add]


/-- Execute at most fuel automatically selected leading-term division
    updates. This bounded evaluator is total by structural recursion on fuel;
    it is not yet the unbounded Euclidean-division function. -/
def runLeadingDivisionFuel (divisor : RatPolynomial) :
    DivisionState → Nat → DivisionState
  | state, 0 => state
  | state, fuel + 1 =>
      runLeadingDivisionFuel divisor
        (leadingDivisionStep divisor state) fuel

/-- Every bounded leading-division run preserves the exact evaluated
    quotient/remainder invariant. -/
theorem eval_runLeadingDivisionFuel
    (divisor : RatPolynomial) (initial : DivisionState)
    (fuel : Nat) (x : Rat) :
    eval (runLeadingDivisionFuel divisor initial fuel).quotient x *
        eval divisor x +
      eval (runLeadingDivisionFuel divisor initial fuel).remainder x =
    eval initial.quotient x * eval divisor x +
      eval initial.remainder x := by
  induction fuel generalizing initial with
  | zero =>
      rfl
  | succ fuel ih =>
      change
        eval (runLeadingDivisionFuel divisor
          (leadingDivisionStep divisor initial) fuel).quotient x *
            eval divisor x +
          eval (runLeadingDivisionFuel divisor
            (leadingDivisionStep divisor initial) fuel).remainder x =
        eval initial.quotient x * eval divisor x +
          eval initial.remainder x
      calc
        eval (runLeadingDivisionFuel divisor
            (leadingDivisionStep divisor initial) fuel).quotient x *
              eval divisor x +
            eval (runLeadingDivisionFuel divisor
              (leadingDivisionStep divisor initial) fuel).remainder x =
          eval (leadingDivisionStep divisor initial).quotient x *
              eval divisor x +
            eval (leadingDivisionStep divisor initial).remainder x :=
              ih (leadingDivisionStep divisor initial)
        _ = eval initial.quotient x * eval divisor x +
              eval initial.remainder x := by
          by_cases hR : leadingCoefficient? initial.remainder = none
          · have hstep :
                leadingDivisionStep divisor initial = initial := by
              simp [leadingDivisionStep, hR]
            rw [hstep]
          · obtain ⟨aR, hR⟩ := Option.ne_none_iff_exists'.mp hR
            by_cases hB : leadingCoefficient? divisor = none
            · have hstep :
                  leadingDivisionStep divisor initial = initial := by
                simp [leadingDivisionStep, hR, hB]
              rw [hstep]
            · obtain ⟨aB, hB⟩ := Option.ne_none_iff_exists'.mp hB
              by_cases hlen :
                  divisor.coefficients.length ≤
                    initial.remainder.coefficients.length
              · exact eval_leadingDivisionStep divisor initial
                  aR aB x hR hB hlen
              · have hstep :
                    leadingDivisionStep divisor initial = initial := by
                  simp [leadingDivisionStep, hR, hB, hlen]
                rw [hstep]

/-- Once the remainder is zero or the divisor no longer fits, every
    additional bounded evaluator step leaves the complete division state
    unchanged. This is an absorbing-terminal-state theorem, not a proof
    that an arbitrary fuel value reaches such a state. -/
theorem runLeadingDivisionFuel_eq_self_of_terminal
    (divisor : RatPolynomial) (state : DivisionState)
    (fuel : Nat)
    (hterminal :
      state.remainder.coefficients = [] ∨
        divisor.coefficients.length > state.remainder.coefficients.length) :
    runLeadingDivisionFuel divisor state fuel = state := by
  induction fuel with
  | zero => rfl
  | succ fuel ih =>
      simp [runLeadingDivisionFuel,
        leadingDivisionStep_eq_self_of_terminal divisor state hterminal, ih]


end CCFSM.P2749
