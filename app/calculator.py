from decimal import Decimal
import pandas as pd
from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation, OperationFactory
from app.exceptions import OperationError, ValidationError

class Calculator:
    def __init__(self, config=None):
        self.config = config or CalculatorConfig()
        self.history = []
        self.undo_stack = []
        self.redo_stack = []
        self.observers = []

    def add_observer(self, observer: HistoryObserver):
        self.observers.append(observer)

    def notify_observers(self, calculation: Calculation):
        for obs in self.observers:
            obs.update(calculation)

    def set_operation(self, operation: Operation):
        self.operation_strategy = operation
    
    def register_observer(self, observer):
        self.observers.append(observer)

    def perform_operation(self, operation_name, a, b):
        if not hasattr(self, 'operation_strategy'):
            self.operation_strategy = OperationFactory.create_operation(operation_name)

        validated_a = InputValidator.validate_number(a, self.config)
        validated_b = InputValidator.validate_number(b, self.config)

        result = self.operation_strategy.execute(validated_a, validated_b)

        calc = Calculation(operation_name, validated_a, validated_b, result)

        # Save undo snapshot
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.redo_stack.clear()

        # Append to history
        self.history.append(calc)

        # Notify observers
        self.notify_observers(calc)

        return result

    def save_history(self):
        """Save calculation history to CSV using pandas."""
        if not self.history:
            return

        data = {
            "operation": [c.operation for c in self.history],
            "operand1": [str(c.operand1) for c in self.history],
            "operand2": [str(c.operand2) for c in self.history],
            "result": [str(c.result) for c in self.history],
        }

        df = pd.DataFrame(data)
        df.to_csv(self.config.history_file, index=False, encoding=self.config.default_encoding)

    def load_history(self):
        """Load calculation history from CSV using pandas."""
        if not self.config.history_file.exists():
            return

        df = pd.read_csv(self.config.history_file, encoding=self.config.default_encoding)

        self.history.clear()

        for _, row in df.iterrows():
            calc = Calculation(
                row["operation"],
                Decimal(row["operand1"]),
                Decimal(row["operand2"]),
                Decimal(row["result"])
            )
            self.history.append(calc)

        # Clear undo/redo stacks to avoid stale snapshots
        self.undo_stack.clear()
        self.redo_stack.clear()


    def show_history(self):
        """Return formatted history of calculations."""
        return [f"{calc.operation} {calc.operand1} {calc.operand2} = {calc.result}" for calc in self.history]

    def clear_history(self):
        """Clear calculation history and undo/redo stacks."""
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()

    def filter_history(self, operation=None, min_value=None, max_value=None):
        """Return a filtered pandas DataFrame of the calculation history."""
        if not self.config.history_file.exists():
            return pd.DataFrame()

        df = pd.read_csv(self.config.history_file, encoding=self.config.default_encoding)

        # Filter by operation
        if operation:
            df = df[df["operation"] == operation]

        # Filter by minimum result
        if min_value is not None:
            df = df[df["result"].astype(float) >= float(min_value)]

        # Filter by maximum result
        if max_value is not None:
            df = df[df["result"].astype(float) <= float(max_value)]

        return df

    def export_filtered_history_to_csv(self, operation=None, min_value=None, max_value=None):
        """Export filtered history to CSV."""
        df = self.filter_history(operation, min_value, max_value)
        if df.empty:
            print("No matching entries to export.")
            return

        export_path = self.config.history_dir / "filtered_history.csv"
        df.to_csv(export_path, index=False, encoding=self.config.default_encoding)
        print(f"Filtered history exported to {export_path}")


    def export_filtered_history_to_excel(self, operation=None, min_value=None, max_value=None):
        """Export filtered history to Excel."""
        df = self.filter_history(operation, min_value, max_value)
        if df.empty:
            print("No matching entries to export.")
            return

        export_path = self.config.history_dir / "filtered_history.xlsx"
        df.to_excel(export_path, index=False, engine="openpyxl")
        print(f"Filtered history exported to {export_path}")

    def analyze_history(self, operation=None):
        """Return summary statistics for the calculation history."""
        if not self.config.history_file.exists():
            return {}

        df = pd.read_csv(self.config.history_file, encoding=self.config.default_encoding)

        # Filter by operation if provided
        if operation:
            df = df[df["operation"] == operation]

        if df.empty:
            return {}

        # Convert result column to numeric
        df["result"] = df["result"].astype(float)

        analysis = {
            "count": len(df),
            "average_result": df["result"].mean(),
            "min_result": df["result"].min(),
            "max_result": df["result"].max(),
            "sum_result": df["result"].sum(),
        }

        # If no operation filter, include operation frequency
        if not operation:
            analysis["operation_frequency"] = df["operation"].value_counts().to_dict()

        return analysis


    def undo(self):
        if not self.undo_stack:
            return False
        # Save current history for redo
        self.redo_stack.append(CalculatorMemento(self.history.copy()))
        # Restore the previous state
        memento = self.undo_stack.pop()
        self.history = memento.history
        return True

    def redo(self):
        if not self.redo_stack:
            return False
        # Save current history for undo
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        # Restore the next state
        memento = self.redo_stack.pop()
        self.history = memento.history
        return True
