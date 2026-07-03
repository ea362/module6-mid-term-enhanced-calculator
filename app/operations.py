from abc import ABC, abstractmethod
from decimal import Decimal
from app.exceptions import ValidationError

class Operation(ABC):
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        pass

class Addition(Operation):
    def execute(self, a, b): return a + b

class Subtraction(Operation):
    def execute(self, a, b): return a - b

class Multiplication(Operation):
    def execute(self, a, b): return a * b

class Division(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValidationError("Division by zero is not allowed")
        return a / b

class Power(Operation):
    def execute(self, a, b):
        if b < 0:
            raise ValidationError("Negative exponents not supported")
        return Decimal(pow(float(a), float(b)))

class Root(Operation):
    def execute(self, a, b):
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")
        return Decimal(pow(float(a), 1 / float(b)))

class OperationFactory:
    _operations = {
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root
    }

    @classmethod
    def create_operation(cls, name: str) -> Operation:
        op_class = cls._operations.get(name.lower())
        if not op_class:
            raise ValueError(f"Unknown operation: {name}")
        return op_class()
