import pytest
from decimal import Decimal
from app.calculation import Calculation
from app.exceptions import OperationError

def test_addition():
    calc = Calculation("Addition", Decimal("2"), Decimal("3"))
    assert calc.result == Decimal("5")

def test_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero"):
        Calculation("Division", Decimal("8"), Decimal("0"))

def test_subtraction():
    calc = Calculation("Subtraction", Decimal("5"), Decimal("3"))
    assert calc.result == Decimal("2")

def test_multiplication():
    calc = Calculation("Multiplication", Decimal("4"), Decimal("2"))
    assert calc.result == Decimal("8")

def test_power_positive():
    calc = Calculation("Power", Decimal("2"), Decimal("3"))
    assert calc.result == Decimal("8")

def test_power_negative_exponent():
    with pytest.raises(OperationError, match="Negative exponents"):
        Calculation("Power", Decimal("2"), Decimal("-1"))

def test_root_normal():
    calc = Calculation("Root", Decimal("9"), Decimal("2"))
    assert calc.result == Decimal("3")

def test_root_zero_degree():
    with pytest.raises(OperationError, match="Invalid root"):
        Calculation("Root", Decimal("9"), Decimal("0"))

def test_root_negative_radicand():
    with pytest.raises(OperationError, match="Invalid root"):
        Calculation("Root", Decimal("-9"), Decimal("2"))

def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation"):
        Calculation("Unknown", Decimal("1"), Decimal("2"))

def test_to_dict():
    calc = Calculation("Addition", Decimal("2"), Decimal("3"))
    d = calc.to_dict()
    assert d['operation'] == "Addition"
    assert d['operand1'] == "2"
    assert d['operand2'] == "3"
    assert d['result'] == "5"
    assert 'timestamp' in d

