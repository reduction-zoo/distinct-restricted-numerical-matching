"""Independent 3-SAT and split-graph star-coloring oracles."""

import argparse
import json
import subprocess
import sys
from itertools import permutations, product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def legal_target(target):
    if not isinstance(target,dict) or set(target) != {"numbers","sum"}:
        return False
    values,sigma = target["numbers"],target["sum"]
    return (isinstance(values,list) and len(values) >= 1
            and all(type(a) is int and a > 0 for a in values)
            and len(set(values)) == len(values)
            and type(sigma) is int and sigma > 0
            and sum(values)+len(values)*(len(values)+1) == len(values)*sigma)


def direct_matching(target,b,c):
    n = len(target["numbers"])
    return (isinstance(b,list) and isinstance(c,list)
            and len(b) == n and len(c) == n
            and all(type(value) is int for value in b+c)
            and sorted(b) == list(range(1,n+1)) and sorted(c) == list(range(1,n+1))
            and all(a+x+y == target["sum"] for a,x,y in zip(target["numbers"],b,c)))


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal distinct restricted numerical matching instance")
    n = len(target["numbers"])
    b,c = [z3.Int(f"b_{i}") for i in range(n)],[z3.Int(f"c_{i}") for i in range(n)]
    solver = z3.Solver()
    for row in (b,c):
        solver.add(z3.Distinct(row))
        for value in row:
            solver.add(value >= 1,value <= n)
    for i,a in enumerate(target["numbers"]):
        solver.add(a+b[i]+c[i] == target["sum"])
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive target solver: {result}")
        model = solver.model()
        bs,cs = [model.eval(v).as_long() for v in b],[model.eval(v).as_long() for v in c]
        assert direct_matching(target,bs,cs)
        outputs.append({"b":bs,"c":cs})
        solver.add(z3.Or(*[v != answer for v,answer in zip(b+c,bs+cs)]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"b","c"} and direct_matching(target,output["b"],output["c"])


def exhaustive_target(target):
    n = len(target["numbers"])
    for b in permutations(range(1,n+1)):
        c = [target["sum"]-a-x for a,x in zip(target["numbers"],b)]
        if direct_matching(target,list(b),c):
            return {"b":list(b),"c":c}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for n,clauses,answer in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars":n,"clauses":clauses})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
                             for clause in source["clauses"])
                     for bits in product((False,True),repeat=source["num_vars"]))
        assert ("assignment" in current) == exists == ("assignment" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    checked = 0
    for n in range(1,5):
        for values in permutations(range(1,2*n+1),n):
            total = sum(values)+n*(n+1)
            if total % n:
                continue
            target = {"numbers":list(values),"sum":total//n}
            assert ("b" in solve_target(target)) == ("b" in exhaustive_target(target))
            checked += 1
    print(f"Self-test passed: {len(cases)} source formulas and {checked} exhaustive target instances")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target: {target}")
        for output in target_solutions(target):
            assert valid_target(target,output)
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
