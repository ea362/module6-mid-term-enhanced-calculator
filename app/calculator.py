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

    def perform_operation(self, a, b):
        if not hasattr(self, 'operation_strategy'):
            raise OperationError("No operation set")

        validated_a = InputValidator.validate_number(a, self.config)
        validated_b = InputValidator.validate_number(b, self.config)
        result = self.operation_strategy.execute(validated_a, validated_b)

        calc = Calculation(self.operation_strategy.__class__.__name__, validated_a, validated_b)
        self.undo_stack.append(CalculatorMemento(self.history.copy()))
        self.redo_stack.clear()
        self.history.append(calc)

        self.notify_observers(calc)

        return result
    
    def save_history(self):
        """Save calculation history to a CSV file using pandas."""
        return [f"{calc.operation} {calc.operand1} {calc.operand2} = {calc.result}" for calc in self.history]

    def load_history(self):
        """Load calculation history from a CSV file using pandas."""
        pass

    def show_history(self):
        """Return formatted history of calculations."""
        return [f"{calc.operation} {calc.operand1} {calc.operand2} = {calc.result}" for calc in self.history]

    def clear_history(self):
        """Clear calculation history and undo/redo stacks."""
        self.history.clear()
        self.undo_stack.clear()
        self.redo_stack.clear()

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
