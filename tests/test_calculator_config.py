import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError

def test_default_configuration():
    config = CalculatorConfig()
    assert config.precision > 0

def test_invalid_max_history_size():
    # Now we can pass keyword arg directly
    config = CalculatorConfig(max_history_size=-1)
    with pytest.raises(ValueError, match="CALCULATOR_MAX_HISTORY_SIZE must be positive"):
        config.validate()

def test_properties():
    config = CalculatorConfig()
    assert config.history_dir == config.base_dir / "history"
    assert config.history_file == config.history_dir / "calculator_history.csv"
    assert config.log_dir == config.base_dir / "logs"
    assert config.log_file == config.log_dir / "calculator.log"

def test_validate_precision_zero():
    config = CalculatorConfig(precision=0)
    with pytest.raises(ValueError, match="CALCULATOR_PRECISION must be positive"):
        config.validate()

def test_validate_max_input_value_zero():
    config = CalculatorConfig(max_input_value=Decimal("0"))
    with pytest.raises(ValueError, match="CALCULATOR_MAX_INPUT_VALUE must be positive"):
        config.validate()

def test_validate_valid():
    config = CalculatorConfig()
    config.validate()  # should not raise