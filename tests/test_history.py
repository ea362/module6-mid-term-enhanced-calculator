from unittest.mock import Mock
from app.history import LoggingObserver, AutoSaveObserver
from app.calculation import Calculation
from app.calculator import Calculator
from decimal import Decimal

def test_logging_observer_logs(monkeypatch):
    monkeypatch.setattr("logging.info", lambda msg: msg)
    observer = LoggingObserver()
    calc = Calculation("Addition", Decimal("2"), Decimal("3"))
    observer.update(calc)

def test_autosave_observer_triggers_save(monkeypatch):
    calc = Mock(spec=Calculator)
    calc.config = Mock(auto_save=True)
    observer = AutoSaveObserver(calc)
    observer.update(Mock(spec=Calculation))
    calc.save_history.assert_called_once()
