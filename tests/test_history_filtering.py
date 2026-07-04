from decimal import Decimal
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.operations import OperationFactory


def test_filter_history(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    config = CalculatorConfig()
    calc = Calculator(config)

    op_add = OperationFactory.create_operation("add")
    calc.set_operation(op_add)
    calc.perform_operation(Decimal("2"), Decimal("3"))   # result = 5
    calc.perform_operation(Decimal("10"), Decimal("20")) # result = 30

    op_mul = OperationFactory.create_operation("multiply")
    calc.set_operation(op_mul)
    calc.perform_operation(Decimal("2"), Decimal("5"))   # result = 10

    calc.save_history()
    assert config.history_file.exists()

    df = calc.filter_history(operation="add")
    assert len(df) == 2

    df2 = calc.filter_history(operation="add", min_value=Decimal("10"))
    assert len(df2) == 1
    assert float(df2.iloc[0]["result"]) == 30