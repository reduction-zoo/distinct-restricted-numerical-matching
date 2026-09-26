# Prepared contract

Source: `{"num_vars": n, "clauses": [[signed_literal, ...], ...]}` with `n >= 0` and clauses of at most three literals. Output a satisfying Boolean `{"assignment": [...]}` or `{"status":"NO-SOLUTION"}`.

Target: `{"numbers": [a_1,...,a_n], "sum": sigma}` with `n >= 1`, distinct positive integers, and `sum(a_i+2i)=n*sigma` for one-based `i`. Output permutations `{"b":[...],"c":[...]}` of `1..n` satisfying `a_i+b_i+c_i=sigma`, or `{"status":"NO-SOLUTION"}`.

`algorithm.py` reads source JSON from stdin and emits legal target JSON. `algorithm.py --extract` reads `{"source":source,"target_solution":output}` and emits a valid source output. Both commands are deterministic, polynomial time, independent subprocesses. Errors exit nonzero; diagnostics go to stderr. Recovery must handle every valid target output.
