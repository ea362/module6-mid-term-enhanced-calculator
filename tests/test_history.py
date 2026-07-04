import logging
from unittest.mock import Mock
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.history import LoggingObserver, AutoSaveObserver
from app.calculation import Calculation
from app.calculator import Calculator
from app.operations import OperationFactory


def test_logging_observer(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    config = CalculatorConfig()
    logging.basicConfig(
        filename=str(config.log_file),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    calc = Calculator(config)
    observer = LoggingObserver(config)
    calc.add_observer(observer)

    op = OperationFactory.create_operation("add")
    calc.set_operation(op)
    calc.perform_operation(Decimal("2"), Decimal("3"))

    # Log file should be created
    assert config.log_file.exists()
    content = config.log_file.read_text()
    assert "add" in content


def test_autosave_observer_triggers_save(monkeypatch):
    calc = Mock(spec=Calculator)
    calc.config = Mock(auto_save=True)
    observer = AutoSaveObserver(calc)
    observer.update(Mock(spec=Calculation))
    calc.save_history.assert_called_once()