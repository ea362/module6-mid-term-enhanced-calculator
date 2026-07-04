from decimal import Decimal
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.operations import OperationFactory


def test_analyze_history(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    config = CalculatorConfig()
    calc = Calculator(config)

    # Perform calculations
    op_add = OperationFactory.create_operation("add")
    calc.set_operation(op_add)
    calc.perform_operation(Decimal("2"), Decimal("3"))     # 5
    calc.perform_operation(Decimal("10"), Decimal("20"))   # 30

    op_mul = OperationFactory.create_operation("multiply")
    calc.set_operation(op_mul)
    calc.perform_operation(Decimal("2"), Decimal("5"))     # 10

    # Verify history is not empty
    assert len(calc.history) == 3

    # Save – this will create the CSV
    calc.save_history()
    assert config.history_file.exists(), "History file was not created"

    stats = calc.analyze_history("add")
    assert stats["count"] == 2
    assert stats["average_result"] == 17.5
    assert stats["max_result"] == 30

    all_stats = calc.analyze_history()
    assert "operation_frequency" in all_stats
    assert all_stats["operation_frequency"]["add"] == 2