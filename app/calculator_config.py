from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import os
from dotenv import load_dotenv
from app.exceptions import ConfigurationError

load_dotenv()

@dataclass
class CalculatorConfig:
    base_dir: Path = Path(os.getenv('CALCULATOR_BASE_DIR', Path.cwd()))
    max_history_size: int = int(os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000'))
    auto_save: bool = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower() in ('true', '1')
    precision: int = int(os.getenv('CALCULATOR_PRECISION', '10'))
    max_input_value: Decimal = Decimal(os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999'))
    default_encoding: str = os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')

    @property
    def history_dir(self) -> Path:
        return self.base_dir / "history"

    @property
    def history_file(self) -> Path:
        return self.history_dir / "calculator_history.csv"

    @property
    def log_dir(self) -> Path:
        return self.base_dir / "logs"

    @property
    def log_file(self) -> Path:
        return self.log_dir / "calculator.log"

    def validate(self):
        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")
        if self.precision <= 0:
            raise ConfigurationError("precision must be positive")
        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")
