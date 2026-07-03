import pytest
from decimal import Decimal
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.operations import OperationFactory
from app.exceptions import ConfigurationError, OperationError, ValidationError

def test_perform_operation_addition():
    calc = Calculator()
    operation = OperationFactory.create_operation("add")
    calc.set_operation(operation)
    result = calc.perform_operation(2, 3)
    assert result == Decimal("5")

def test_undo_and_redo():
    calc = Calculator()
    operation = OperationFactory.create_operation("add")
    calc.set_operation(operation)
    calc.perform_operation(2, 3)
    calc.undo()
    assert calc.history == []
    calc.redo()
    assert len(calc.history) == 1

def test_undo_empty():
    calc = Calculator()
    assert calc.undo() is False

def test_redo_empty():
    calc = Calculator()
    assert calc.redo() is False

def test_perform_operation_no_operation():
    calc = Calculator()
    with pytest.raises(OperationError, match="No operation set"):
        calc.perform_operation(1, 2)

def test_show_history_empty():
    calc = Calculator()
    assert calc.show_history() == []  # assuming returns list

def test_show_history_with_entries():
    calc = Calculator()
    op = OperationFactory.create_operation("add")
    calc.set_operation(op)
    calc.perform_operation(2, 3)
    history = calc.show_history()
    assert len(history) == 1
    # We can check string content if we implement show_history, but for now just exists

def test_clear_history():
    calc = Calculator()
    op = OperationFactory.create_operation("add")
    calc.set_operation(op)
    calc.perform_operation(2, 3)
    calc.clear_history()
    assert calc.history == []
    assert calc.undo_stack == []
    assert calc.redo_stack == []

def test_add_observer_and_notify():
    from unittest.mock import Mock
    calc = Calculator()
    mock_observer = Mock()
    calc.add_observer(mock_observer)
    op = OperationFactory.create_operation("add")
    calc.set_operation(op)
    calc.perform_operation(2, 3)
    mock_observer.update.assert_called_once()
    # Also check that notify_observers is called inside perform_operation

def test_save_history():
    calc = Calculator()
    # Just call to cover, no exception expected
    calc.save_history()

def test_load_history():
    calc = Calculator()
    calc.load_history()

def test_properties():
    config = CalculatorConfig()
    assert config.history_dir == config.base_dir / "history"
    assert config.history_file == config.history_dir / "calculator_history.csv"
    assert config.log_dir == config.base_dir / "logs"
    assert config.log_file == config.log_dir / "calculator.log"

def test_validate_precision_zero():
    config = CalculatorConfig(precision=0)
    with pytest.raises(ConfigurationError, match="precision must be positive"):
        config.validate()

def test_validate_max_input_value_zero():
    config = CalculatorConfig(max_input_value=Decimal("0"))
    with pytest.raises(ConfigurationError, match="max_input_value must be positive"):
        config.validate()

def test_perform_operation_invalid_input():
    calc = Calculator()
    op = OperationFactory.create_operation("add")
    calc.set_operation(op)
    with pytest.raises(ValidationError, match="Invalid number format"):
        calc.perform_operation("abc", 2)

def test_perform_operation_division_by_zero():
    calc = Calculator()
    op = OperationFactory.create_operation("divide")
    calc.set_operation(op)
    with pytest.raises(ValidationError, match="Division by zero"):
        calc.perform_operation(5, 0)