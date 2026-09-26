from check import legal_target, solve_target, valid_target


def test_hand_cases():
    unit = {"numbers":[1],"sum":3}
    assert valid_target(unit,{"b":[1],"c":[1]})
    assert not valid_target(unit,{"b":[2],"c":[1]})
    pair = {"numbers":[1,3],"sum":5}
    assert valid_target(pair,{"b":[2,1],"c":[2,1]})
    assert not legal_target({"numbers":[1,1],"sum":4})
    assert not legal_target({"numbers":[1,2],"sum":5})
    impossible = {"numbers":[1,2,6],"sum":7}
    assert legal_target(impossible)
    assert solve_target(impossible) == {"status":"NO-SOLUTION"}


if __name__ == "__main__":
    test_hand_cases()
