import pytest
from decimal import Decimal

from app.calculator import Calculator
from app.operations import OperationFactory
from app.calculator_config import CalculatorConfig


@pytest.fixture
def config():
    """Provide a default CalculatorConfig for tests."""
    return CalculatorConfig()


@pytest.fixture
def calculator(config):
    """Provide a fresh Calculator instance for each test."""
    return Calculator(config=config)


@pytest.fixture
def add_operation():
    """Provide an Addition operation instance."""
    return OperationFactory.create_operation("add")


@pytest.fixture
def subtract_operation():
    """Provide a Subtraction operation instance."""
    return OperationFactory.create_operation("subtract")


@pytest.fixture
def multiply_operation():
    """Provide a Multiplication operation instance."""
    return OperationFactory.create_operation("multiply")


@pytest.fixture
def divide_operation():
    """Provide a Division operation instance."""
    return OperationFactory.create_operation("divide")


@pytest.fixture
def sample_decimal_pair():
    """Provide a reusable pair of Decimal operands."""
    return Decimal("10"), Decimal("5")
