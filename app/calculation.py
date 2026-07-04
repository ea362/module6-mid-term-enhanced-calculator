from dataclasses import dataclass, field
from decimal import Decimal
import datetime
from app.exceptions import OperationError

@dataclass
class Calculation:
    operation: str
    operand1: Decimal
    operand2: Decimal
    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        self.result = self.calculate()

    def calculate(self):
        ops = {
            "Addition": lambda x, y: x + y,
            "Subtraction": lambda x, y: x - y,
            "Multiplication": lambda x, y: x * y,
            "Division": lambda x, y: x / y if y != 0 else self._raise_div_zero(),
            "Power": lambda x, y: Decimal(pow(float(x), float(y))) if y >= 0 else self._raise_neg_power(),
            "Root": lambda x, y: Decimal(pow(float(x), 1 / float(y))) if x >= 0 and y != 0 else self._raise_invalid_root(x, y)
        }
        op = ops.get(self.operation)
        if not op:
            raise OperationError(f"Unknown operation: {self.operation}")
        return op(self.operand1, self.operand2)

    @staticmethod
    def _raise_div_zero(): raise OperationError("Division by zero is not allowed")
    @staticmethod
    def _raise_neg_power(): raise OperationError("Negative exponents are not supported")
    @staticmethod
    def _raise_invalid_root(x, y): raise OperationError("Invalid root operation")

    def to_dict(self):
        return {
            'operation': self.operation,
            'operand1': str(self.operand1),
            'operand2': str(self.operand2),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Calculation from a dictionary (for CSV loading)."""
        obj = cls(data["operation"], Decimal(data["operand1"]), Decimal(data["operand2"]))
        # Bypass __post_init__ to keep the stored result
        object.__setattr__(obj, "result", Decimal(data["result"]))
        return obj