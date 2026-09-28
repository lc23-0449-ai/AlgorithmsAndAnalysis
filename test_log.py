import random
import math
from log import log


def test_works_for_exact_power():
    assert log(3, 81) == 4


def test_works_for_inexact_power():
    assert log(2, 7) == 2


def test_works_if_a_is_greater_than_b():
    assert log(2, 1) == 0


def test_works_if_division_would_skip_over_1():
    assert log(3, 8) == 1


def test_matches_math_library():
    for i in range(100):
        a = random.randint(2, 10)
        b = random.randint(1, 1000000000)
        assert log(a, b) == math.floor(math.log(b, a))
