from fraction import Fraction
import pytest


def test_represents_simple_fraction():
    assert str(Fraction(2, 3)) == '2/3'
    assert repr(Fraction(2, 3)) == '2/3'


def test_reduces_to_lowest_terms():
    assert str(Fraction(4, 20)) == '1/5'


def test_handles_negative_numerator():
    assert str(Fraction(-3, 8)) == '-3/8'


def test_handles_negative_denominator():
    assert str(Fraction(3, -4)) == '-3/4'


def test_handles_negative_numerator_and_denominator():
    assert str(Fraction(-2, -9)) == '2/9'


def test_represents_improper_fraction():
    assert str(Fraction(3, 2)) == '3/2'


def test_adds():
    a = Fraction(1, 2)
    b = Fraction(1, 3)
    assert str(a + b) == '5/6'


def test_subtracts():
    a = Fraction(2, 3)
    b = Fraction(1, 2)
    assert str(a - b) == '1/6'


def test_multiplies():
    a = Fraction(2, 3)
    b = Fraction(1, 2)
    assert str(a * b) == '1/3'


def test_divides():
    a = Fraction(3, 4)
    b = Fraction(5, 8)
    assert str(a / b) == '6/5'


def test_approximates():
    assert float(Fraction(1, 3)) == pytest.approx(1/3)
