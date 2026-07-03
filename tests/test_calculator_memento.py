from app.calculator_memento import CalculatorMemento
from app.calculation import Calculation
from decimal import Decimal

def test_memento_stores_history():
    calc = Calculation("Addition", Decimal("2"), Decimal("3"))
    memento = CalculatorMemento([calc])
    assert len(memento.history) == 1
