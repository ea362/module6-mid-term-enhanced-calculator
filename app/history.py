from abc import ABC, abstractmethod
import logging
from app.calculation import Calculation

class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation): pass

class LoggingObserver(HistoryObserver):
    def update(self, calculation):
        logging.info(
            f"Operation: {calculation.operation}, "
            f"Operand1: {calculation.operand1}, "
            f"Operand2: {calculation.operand2}, "
            f"Result: {calculation.result}"
        )

class AutoSaveObserver(HistoryObserver):
    def __init__(self, calculator):
        self.calculator = calculator
    def update(self, calculation):
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")
