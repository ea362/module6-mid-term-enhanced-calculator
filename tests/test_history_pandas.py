from decimal import Decimal
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig


def test_save_and_load_history(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    config = CalculatorConfig()
    calc = Calculator(config)

    calc.perform_operation("add", Decimal("2"), Decimal("3"))
    calc.save_history()

    assert config.history_file.exists()

    calc2 = Calculator(config)
    calc2.load_history()

    assert len(calc2.history) == 1
    assert calc2.history[0].result == Decimal("5")
