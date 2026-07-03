from abc import ABC, abstractmethod
import logging
from app.calculation import Calculation

class HistoryObserver(ABC):
    @abstractmethod
    def update(self, calculation: Calculation): pass

class LoggingObserver(HistoryObserver):
    def update(self, calculation):
        logging.info(f"{calculation.operation}({calculation.operand1}, {calculation.operand2}) = {calculation.result}")

class AutoSaveObserver(HistoryObserver):
    def __init__(self, calculator):
        self.calculator = calculator
    def update(self, calculation):
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")
