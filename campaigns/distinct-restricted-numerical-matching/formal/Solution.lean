module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace DistinctRestrictedNumericalMatching

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

structure Formula where
  n : Nat
  clauses : List (List (Nat × Bool))
  deriving Repr

def legalSource (x : Formula) : Bool :=
  x.clauses.all (fun c => c.length ≤ 3 && c.all (fun l => l.1 < x.n))

def sourceWitness (x : Formula) (a : List Bool) : Bool :=
  a.length == x.n && x.clauses.all (fun c => c.any (fun l => a[l.1]? == some l.2))

def encodeSource (x : Formula) : List Bool :=
  encodeNat x.n ++ encodeList (encodeList (fun l => encodeNat l.1 ++ [l.2])) x.clauses

def validSourceOutput := searchOutput legalSource sourceWitness

def legalTarget (x : List Nat × Nat) : Bool :=
  !x.1.isEmpty && decide x.1.Nodup && x.1.all (fun a => a > 0) &&
  (x.1.zipIdx.map (fun (a,i) => a + 2 * (i+1))).sum == x.1.length * x.2
def targetWitness (x : List Nat × Nat) (w : List Nat × List Nat) : Bool :=
  decide (w.1.Perm ((List.range x.1.length).map (· + 1))) &&
  decide (w.2.Perm ((List.range x.1.length).map (· + 1))) &&
  (List.range x.1.length).all (fun i =>
    x.1[i]?.getD 0 + w.1[i]?.getD 0 + w.2[i]?.getD 0 == x.2)
def encodeTarget (x : List Nat × Nat) := encodeList encodeNat x.1 ++ encodeNat x.2
def encodeWitness (w : List Nat × List Nat) := encodeList encodeNat w.1 ++ encodeList encodeNat w.2
def validTargetOutput := searchOutput legalTarget targetWitness

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : Formula → (List Nat × Nat))
    (recover : Formula × Option (List Nat × List Nat) → Option (List Bool)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption encodeWitness) input.2)
    (encodeOption (encodeList (fun b => [b]))) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList (fun b => [b]))) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption encodeWitness) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))

def Goal : Prop :=
  ∃ (forward : Formula → (List Nat × Nat))
    (recover : Formula × Option (List Nat × List Nat) → Option (List Bool)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end DistinctRestrictedNumericalMatching
