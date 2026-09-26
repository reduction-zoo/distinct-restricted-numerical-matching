# 3-SAT → Distinct Restricted Numerical 3-Dimensional Matching

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

The target gives n distinct positive binary integers a_i and a sum σ, with sum_i(a_i+2i)=nσ. Find permutations b and c of [n] such that a_i+b_i+c_i=σ for every i, or report NO-SOLUTION.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This asks whether arithmetic matching remains hard when two lists are fixed consecutive integers and the remaining list is distinct.

## Difficulty

Known numerical matching reductions need not preserve distinctness and consecutive lists simultaneously.

## Literature context

The restriction fixes two numerical lists to consecutive integers and makes the remaining list distinct. Hardness for general numerical matching does not establish this restriction.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Finite Pinwheel Scheduling: the k-Visits Problem](https://arxiv.org/html/2507.11681v2): Finite Pinwheel Scheduling: the k-Visits Problem, Definition 12, gives the RN3DM domain above with a multiset A. The ICALP 2026 follow-up, Sections 3.1 and 8, asks whether hardness remains for a simple set. It instead proves hardness with only one interval set fixed, which does not settle this case.
- [ICALP 2026 follow-up](https://drops.dagstuhl.de/storage/00lipics/lipics-vol374-icalp2026/html/LIPIcs.ICALP.2026.122/LIPIcs.ICALP.2026.122.html): Finite Pinwheel Scheduling: the k-Visits Problem, Definition 12, gives the RN3DM domain above with a multiset A. The ICALP 2026 follow-up, Sections 3.1 and 8, asks whether hardness remains for a simple set. It instead proves hardness with only one interval set fixed, which does not settle this case.
- [On the X-rays of permutations](https://math.mit.edu/~apost/papers/xray.pdf): Bebeacua, Mansour, Postnikov and Severini, On the X-rays of permutations, Section 4, Conjecture 4.2, proposes necessary inequalities as sufficient for binary X-rays. Nordh, A note on X-rays of permutations and a problem of Brualdi and Fritscher, Proposition 4, Corollary 6 and Problem 14, connects this to extremal Skolem sets and explicitly asks for a polynomial recognition algorithm.
- [A note on X-rays of permutations and a problem of Brualdi and Fritscher](https://arxiv.org/html/1707.03928v1): Bebeacua, Mansour, Postnikov and Severini, On the X-rays of permutations, Section 4, Conjecture 4.2, proposes necessary inequalities as sufficient for binary X-rays. Nordh, A note on X-rays of permutations and a problem of Brualdi and Fritscher, Proposition 4, Corollary 6 and Problem 14, connects this to extremal Skolem sets and explicitly asks for a polynomial recognition algorithm.
- [Binary X-rays of doubly stochastic matrices](https://arxiv.org/html/2608.01442v1): Li, Liu and Yao, Binary X-rays of doubly stochastic matrices, 2 August 2026, Conjecture 1.5 and Theorem 1.7, retains the permutation conjecture and proves its doubly stochastic relaxation. Section 5, Conjecture 5.1, identifies the remaining binary integrality assertion. Their counterexample to a broader triangular-table saturation statement does not refute this assertion. The theorem is therefore not a polynomial algorithm for the target matching.

Fixed from board record `website/questions/distinct-restricted-numerical-matching.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
