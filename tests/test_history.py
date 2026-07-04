from unittest.mock import Mock
from app.calculator_config import CalculatorConfig
from app.history import LoggingObserver, AutoSaveObserver
from app.calculation import Calculation
from app.calculator import Calculator
from decimal import Decimal

def test_logging_observer(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    config = CalculatorConfig()
    calc = Calculator(config)

    observer = LoggingObserver(config)
    calc.register_observer(observer)

    calc.perform_operation("add", Decimal("2"), Decimal("3"))

    log_file = config.log_file
    assert log_file.exists()
    assert "add" in log_file.read_text()



def test_autosave_observer_triggers_save(monkeypatch):
    calc = Mock(spec=Calculator)
    calc.config = Mock(auto_save=True)
    observer = AutoSaveObserver(calc)
    observer.update(Mock(spec=Calculation))
    calc.save_history.assert_called_once()
