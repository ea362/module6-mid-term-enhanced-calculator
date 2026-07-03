import pytest
from app.exceptions import CalculatorError, ValidationError, OperationError

def test_validation_error_is_calculator_error():
    with pytest.raises(CalculatorError):
        raise ValidationError("Invalid")
