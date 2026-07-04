from decimal import Decimal
from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.operations import OperationFactory


def test_export_filtered_history(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    config = CalculatorConfig()
    calc = Calculator(config)

    op_add = OperationFactory.create_operation("add")
    calc.set_operation(op_add)
    calc.perform_operation(Decimal("2"), Decimal("3"))
    calc.perform_operation(Decimal("10"), Decimal("20"))

    # Ensure history is saved
    calc.save_history()
    assert config.history_file.exists()

    # Export with filters
    calc.export_filtered_history_to_csv(operation="add", min_value=Decimal("5"))
    calc.export_filtered_history_to_excel(operation="add", min_value=Decimal("5"))

    csv_path = config.history_dir / "filtered_history.csv"
    xlsx_path = config.history_dir / "filtered_history.xlsx"

    assert csv_path.exists()
    assert xlsx_path.exists()