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
    assert calc.show_history() == []

def test_show_history_with_entries():
    calc = Calculator()
    op = OperationFactory.create_operation("add")
    calc.set_operation(op)
    calc.perform_operation(2, 3)
    history = calc.show_history()
    assert len(history) == 1

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

def test_save_history():
    calc = Calculator()
    calc.save_history()  # no exception expected

def test_load_history():
    calc = Calculator()
    calc.load_history()  # no exception expected

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

def test_save_history_empty():
    """Cover early return when history is empty."""
    calc = Calculator()
    calc.save_history()  # no error, does nothing

def test_load_history_missing_file():
    """Cover early return when history file does not exist."""
    calc = Calculator()
    # Ensure file does not exist
    if calc.config.history_file.exists():
        calc.config.history_file.unlink()
    calc.load_history()  # should do nothing

def test_filter_history_missing_file():
    """Cover early return when history file missing."""
    calc = Calculator()
    df = calc.filter_history()
    assert df.empty

def test_analyze_history_missing_file():
    """Cover early return when history file missing."""
    calc = Calculator()
    stats = calc.analyze_history()
    assert stats == {}

def test_export_filtered_empty_csv(tmp_path, monkeypatch):
    """Cover 'No matching entries' branch in export_csv."""
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    config = CalculatorConfig()
    calc = Calculator(config)
    op_add = OperationFactory.create_operation("add")
    calc.set_operation(op_add)
    calc.perform_operation(Decimal("2"), Decimal("3"))  # result 5
    calc.save_history()
    # Filter with min > max so DataFrame becomes empty
    calc.export_filtered_history_to_csv(
        operation="add", min_value=Decimal("10"), max_value=Decimal("1")
    )
    # No file should be created; we can check it doesn't exist
    csv_path = config.history_dir / "filtered_history.csv"
    assert not csv_path.exists()

def test_export_filtered_empty_excel(tmp_path, monkeypatch):
    """Cover 'No matching entries' branch in export_excel."""
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    config = CalculatorConfig()
    calc = Calculator(config)
    op_add = OperationFactory.create_operation("add")
    calc.set_operation(op_add)
    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.save_history()
    calc.export_filtered_history_to_excel(
        operation="add", min_value=Decimal("10"), max_value=Decimal("1")
    )
    xlsx_path = config.history_dir / "filtered_history.xlsx"
    assert not xlsx_path.exists()

def test_analyze_history_empty_after_filter(tmp_path, monkeypatch):
    """Cover empty DataFrame after filtering."""
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))
    config = CalculatorConfig()
    calc = Calculator(config)
    op_add = OperationFactory.create_operation("add")
    calc.set_operation(op_add)
    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.save_history()
    stats = calc.analyze_history("multiply")  # no such operation
    assert stats == {}