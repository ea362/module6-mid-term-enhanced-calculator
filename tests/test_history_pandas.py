from decimal import Decimal
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.operations import OperationFactory

def test_save_and_load_history(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    config = CalculatorConfig()
    calc = Calculator(config)

    op_add = OperationFactory.create_operation("add")
    calc.set_operation(op_add)
    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.save_history()

    assert config.history_file.exists()

    calc2 = Calculator(config)
    calc2.load_history()

    assert len(calc2.history) == 1
    assert calc2.history[0].result == Decimal("5")