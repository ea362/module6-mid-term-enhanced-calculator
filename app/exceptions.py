class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass

class ValidationError(CalculatorError):
    """Raised when input validation fails."""
    pass

class OperationError(CalculatorError):
    """Raised when an operation fails."""
    pass

class ConfigurationError(CalculatorError):
    """Raised when configuration settings are invalid."""
    pass
