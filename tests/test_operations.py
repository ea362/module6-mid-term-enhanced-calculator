import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.operations import OperationFactory
from app.exceptions import ValidationError

def test_addition_operation():
    op = OperationFactory.create_operation("add")
    assert op.execute(Decimal("2"), Decimal("3")) == Decimal("5")

def test_division_by_zero():
    op = OperationFactory.create_operation("divide")
    with pytest.raises(ValidationError):
        op.execute(Decimal("5"), Decimal("0"))

def test_subtraction_operation():
    op = OperationFactory.create_operation("subtract")
    assert op.execute(Decimal("5"), Decimal("3")) == Decimal("2")

def test_multiplication_operation():
    op = OperationFactory.create_operation("multiply")
    assert op.execute(Decimal("4"), Decimal("2")) == Decimal("8")

def test_division_operation():
    op = OperationFactory.create_operation("divide")
    assert op.execute(Decimal("10"), Decimal("2")) == Decimal("5")

def test_power_operation():
    op = OperationFactory.create_operation("power")
    assert op.execute(Decimal("2"), Decimal("3")) == Decimal("8")

def test_power_negative_exponent():
    op = OperationFactory.create_operation("power")
    with pytest.raises(ValidationError, match="Negative exponents"):
        op.execute(Decimal("2"), Decimal("-1"))

def test_root_operation():
    op = OperationFactory.create_operation("root")
    assert op.execute(Decimal("9"), Decimal("2")) == Decimal("3")

def test_root_zero_degree():
    op = OperationFactory.create_operation("root")
    with pytest.raises(ValidationError, match="Zero root"):
        op.execute(Decimal("9"), Decimal("0"))

def test_root_negative_radicand():
    op = OperationFactory.create_operation("root")
    with pytest.raises(ValidationError, match="Cannot calculate root of negative"):
        op.execute(Decimal("-9"), Decimal("2"))

def test_factory_unknown():
    with pytest.raises(ValueError, match="Unknown operation"):
        OperationFactory.create_operation("unknown")

def test_validate_valid():
    config = CalculatorConfig()
    config.validate()  # should not raise

def test_root_exact():
    op = OperationFactory.create_operation("root")
    assert op.execute(Decimal("16"), Decimal("2")) == Decimal("4")
    assert op.execute(Decimal("100"), Decimal("2")) == Decimal("10")

def test_factory_unknown_operation():
    with pytest.raises(ValueError, match="Unknown operation"):
        OperationFactory.create_operation("nonexistent")

def test_modulus():
    op = OperationFactory.create_operation("modulus")
    assert op.execute(Decimal("10"), Decimal("3")) == Decimal("1")

def test_modulus_zero():
    op = OperationFactory.create_operation("modulus")
    with pytest.raises(ValidationError):
        op.execute(Decimal("10"), Decimal("0"))

def test_int_divide():
    op = OperationFactory.create_operation("int_divide")
    assert op.execute(Decimal("10"), Decimal("3")) == Decimal("3")

def test_percent():
    op = OperationFactory.create_operation("percent")
    assert op.execute(Decimal("50"), Decimal("200")) == Decimal("25")

def test_abs_diff():
    op = OperationFactory.create_operation("abs_diff")
    assert op.execute(Decimal("10"), Decimal("3")) == Decimal("7")
