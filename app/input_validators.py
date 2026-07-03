from decimal import Decimal, InvalidOperation
from app.exceptions import ValidationError

class InputValidator:
    @staticmethod
    def validate_number(value, config):
        try:
            number = Decimal(str(value).strip())
            if abs(number) > config.max_input_value:
                raise ValidationError(f"Value exceeds maximum allowed: {config.max_input_value}")
            return number.normalize()
        except InvalidOperation:
            raise ValidationError(f"Invalid number format: {value}")
