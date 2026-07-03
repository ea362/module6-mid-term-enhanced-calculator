import os
from pathlib import Path
from dotenv import load_dotenv
from decimal import Decimal

class CalculatorConfig:
    def __init__(self):
        load_dotenv()

        # Base directory
        self.base_dir = Path(os.getenv("CALCULATOR_BASE_DIR", "."))

        # Derived directories
        self.log_dir = self.base_dir / "logs"
        self.history_dir = self.base_dir / "history"

        # Files
        self.log_file = self.log_dir / "calculator.log"
        self.history_file = self.history_dir / "history.csv"

        # Settings
        self.max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "1000"))
        self.auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
        self.precision = int(os.getenv("CALCULATOR_PRECISION", "10"))
        self.max_input_value = Decimal(os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1e999"))
        self.default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")

        # Setup directories
        self.setup_directories()

        # Validate configuration
        self.validate()

    def setup_directories(self):
        """Create required directories if they do not exist."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def validate(self):
        """Validate configuration values."""
        if self.max_history_size <= 0:
            raise ValueError("CALCULATOR_MAX_HISTORY_SIZE must be positive")

        if self.precision <= 0:
            raise ValueError("CALCULATOR_PRECISION must be positive")

        if self.max_input_value <= 0:
            raise ValueError("CALCULATOR_MAX_INPUT_VALUE must be positive")
