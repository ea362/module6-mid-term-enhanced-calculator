from dataclasses import dataclass, field
import datetime
from app.calculation import Calculation

@dataclass
class CalculatorMemento:
    history: list[Calculation]
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
