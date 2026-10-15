import Challenge
open DistinctRestrictedNumericalMatching
example : legalTarget ([1,3], 5) = true := by native_decide
example : targetWitness ([1,3], 5) ([2,1],[2,1]) = true := by native_decide
example : targetWitness ([1,3], 5) ([1,2],[1,2]) = false := by native_decide
