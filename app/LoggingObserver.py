import logging

class LoggingObserver:
    def __init__(self, config):
        self.config = config

    def update(self, calculation):
        logging.info(
            f"Operation: {calculation.operation}, "
            f"Operands: {calculation.operands}, "
            f"Result: {calculation.result}"
        )
