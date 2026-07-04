import os
from pathlib import Path
from dotenv import load_dotenv
from decimal import Decimal

class CalculatorConfig:
    def __init__(
        self,
        base_dir: str | Path | None = None,
        max_history_size: int | None = None,
        auto_save: bool | None = None,
        precision: int | None = None,
        max_input_value: Decimal | None = None,
        default_encoding: str | None = None,
    ):
        load_dotenv()

        # Base directory
        if base_dir is None:
            base_dir = os.getenv("CALCULATOR_BASE_DIR", ".")
        self.base_dir = Path(base_dir)

        # Derived directories
        self.log_dir = self.base_dir / "logs"
        self.history_dir = self.base_dir / "history"

        # Files (use "calculator_history.csv" to match tests)
        self.log_file = self.log_dir / "calculator.log"
        self.history_file = self.history_dir / "calculator_history.csv"

        # Settings – use provided values or fall back to env / defaults
        self.max_history_size = (
            max_history_size
            if max_history_size is not None
            else int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "1000"))
        )

        self.auto_save = (
            auto_save
            if auto_save is not None
            else os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
        )

        self.precision = (
            precision
            if precision is not None
            else int(os.getenv("CALCULATOR_PRECISION", "10"))
        )

        self.max_input_value = (
            max_input_value
            if max_input_value is not None
            else Decimal(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e999"))
        )

        self.default_encoding = (
            default_encoding
            if default_encoding is not None
            else os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
        )

        # Create directories
        self.setup_directories()

        # Do NOT call validate() automatically – let tests call it explicitly

    def setup_directories(self):
        """Create required directories if they do not exist."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def validate(self):
        """Validate configuration values. Raise ValueError if invalid."""
        if self.max_history_size <= 0:
            raise ValueError("CALCULATOR_MAX_HISTORY_SIZE must be positive")
        if self.precision <= 0:
            raise ValueError("CALCULATOR_PRECISION must be positive")
        if self.max_input_value <= 0:
            raise ValueError("CALCULATOR_MAX_INPUT_VALUE must be positive")