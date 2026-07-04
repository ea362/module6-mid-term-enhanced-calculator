from decimal import Decimal
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig


def test_filter_history(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    config = CalculatorConfig()
    calc = Calculator(config)

    calc.perform_operation("add", Decimal("2"), Decimal("3"))   # result = 5
    calc.perform_operation("add", Decimal("10"), Decimal("20")) # result = 30
    calc.perform_operation("multiply", Decimal("2"), Decimal("5")) # result = 10

    calc.save_history()

    df = calc.filter_history(operation="add")
    assert len(df) == 2

    df2 = calc.filter_history(operation="add", min_value=Decimal("10"))
    assert len(df2) == 1
    assert float(df2.iloc[0]["result"]) == 30
