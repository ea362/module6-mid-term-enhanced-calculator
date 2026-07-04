from decimal import Decimal

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig


def test_export_filtered_history(tmp_path, monkeypatch):
    monkeypatch.setenv("CALCULATOR_BASE_DIR", str(tmp_path))

    config = CalculatorConfig()
    calc = Calculator(config)

    calc.perform_operation("add", Decimal("2"), Decimal("3"))
    calc.perform_operation("add", Decimal("10"), Decimal("20"))
    calc.save_history()

    calc.export_filtered_history_to_csv(operation="add", min_value=Decimal("5"))
    calc.export_filtered_history_to_excel(operation="add", min_value=Decimal("5"))

    csv_path = config.history_dir / "filtered_history.csv"
    xlsx_path = config.history_dir / "filtered_history.xlsx"

    assert csv_path.exists()
    assert xlsx_path.exists()
