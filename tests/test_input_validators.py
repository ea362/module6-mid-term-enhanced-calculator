import pytest
from decimal import Decimal
from app.input_validators import InputValidator
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError

config = CalculatorConfig(max_input_value=Decimal("1000"))

def test_validate_number_positive():
    assert InputValidator.validate_number("123", config) == Decimal("123")

def test_validate_number_invalid():
    with pytest.raises(ValidationError):
        InputValidator.validate_number("abc", config)

def test_validate_number_exceeds_max():
    config = CalculatorConfig(max_input_value=Decimal("100"))
    with pytest.raises(ValidationError, match="exceeds maximum"):
        InputValidator.validate_number("200", config)