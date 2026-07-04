from decimal import Decimal
import logging
from logging import config
from app.help_system import BaseHelpProvider, ExtendedHelpDecorator, REPLHelpDecorator
from app.calculator_repl import Colors  # if Colors is defined here

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"

def success(msg): print(f"{Colors.OKGREEN}{msg}{Colors.ENDC}")
def warning(msg): print(f"{Colors.WARNING}{msg}{Colors.ENDC}")
def error(msg): print(f"{Colors.FAIL}{msg}{Colors.ENDC}")
def info(msg): print(f"{Colors.OKBLUE}{msg}{Colors.ENDC}")


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    help_provider = REPLHelpDecorator(
                    ExtendedHelpDecorator(
                        BaseHelpProvider()
                    )
                )

    try:
        calc = Calculator()
        config = CalculatorConfig()

        logging.basicConfig(
            filename=str(config.log_file),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        
        # Register observers for logging and auto-saving
        calc.add_observer(LoggingObserver(config))
        calc.add_observer(AutoSaveObserver(calc))

        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                command = input("\nEnter command: ").strip().lower().split()

                if command == 'help':
                    help_dict = help_provider.get_help()
                    info("Available Commands:")
                    for cmd, desc in help_dict.items():
                        success(f"{cmd:15} - {desc}")
                    continue

                if command == 'exit':
                    try:
                        calc.save_history()
                        success("History saved successfully.")
                    except Exception as e:
                        warning(f"Warning: Could not save history: {e}")
                    info("Goodbye!")
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        warning("History is empty.")
                    else:
                        info("\nCalculation History:")
                        for item in calc.history:
                            success(f"{item.operation}({item.operand1}, {item.operand2}) = {item.result}")
                    continue

                if command == 'clear':
                    calc.clear_history()
                    success("History cleared.")
                    continue

                if command == 'undo':
                    try:
                        calc.undo()
                        success("Undid last calculation.")
                    except Exception as e:
                        error(f"Error undoing last calculation: {e}")
                    continue


                if command == 'redo':
                    try:
                        calc.redo()
                        success("Redid last undone calculation.")
                    except Exception as e:
                        error(f"Error redoing last undone calculation: {e}")
                    continue

                if command == 'save':
                    try:
                        calc.save_history()
                        success("History saved successfully.")
                    except Exception as e:
                        error(f"Error saving history: {e}")
                    continue

                if command == 'load':
                    try:
                        calc.load_history()
                        success("History loaded successfully.")
                    except Exception as e:
                        error(f"Error loading history: {e}")
                    continue

                if command == 'filter':
                    print("Usage: filter operation [min] [max]")
                    operation = input("Enter operation to filter by (or leave blank): ").strip()
                    min_value = input("Enter minimum result value to filter by (or leave blank): ").strip()
                    max_value = input("Enter maximum result value to filter by (or leave blank): ").strip()

                    try:
                        min_value = Decimal(min_value) if min_value else None
                        max_value = Decimal(max_value) if max_value else None
                    except Exception as e:
                        error(f"Invalid number format: {e}")
                        continue

                    filtered_df = calc.filter_history(operation, min_value, max_value)

                    if filtered_df.empty:
                        error("No matching history entries found.")
                    else:
                        success("\nFiltered History:")
                        print(filtered_df)
                    continue

                if command == "export_csv":
                    operation = input("Enter operation to filter by (or leave blank): ").strip()
                    min_value = input("Enter minimum result value (or leave blank): ").strip()
                    max_value = input("Enter maximum result value (or leave blank): ").strip()

                    try:
                        min_value = Decimal(min_value) if min_value else None
                        max_value = Decimal(max_value) if max_value else None
                    except Exception as e:
                        error(f"Invalid number format: {e}")
                        continue

                    calc.export_filtered_history_to_csv(operation or None, min_value, max_value)

                if command == "export_excel":
                    operation = input("Enter operation to filter by (or leave blank): ").strip()
                    min_value = input("Enter minimum result value (or leave blank): ").strip()
                    max_value = input("Enter maximum result value (or leave blank): ").strip()

                    try:
                        min_value = Decimal(min_value) if min_value else None
                        max_value = Decimal(max_value) if max_value else None
                    except Exception as e:
                        error(f"Invalid number format: {e}")
                        continue

                    calc.export_filtered_history_to_excel(operation or None, min_value, max_value)

                if command == "analytics":
                    operation = input("Enter operation to analyze (or leave blank for all): ").strip()
                    operation = operation or None

                    stats = calc.analyze_history(operation)

                    if not stats:
                        warning("No matching history to analyze.")
                    else:
                        success(f"{Colors.OKGREEN}Analytics Summary:{Colors.ENDC}")
                        for key, value in stats.items():
                            success(f"  {key}: {value}")
                
                if command in ['add','subtract','multiply','divide','power','root','modulus','int_divide','percent', 'abs_diff']:
                    try:
                        success("\nEnter numbers (or 'cancel' to abort)")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            warning("Operation cancelled.")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            warning("Operation cancelled.")
                            continue

                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)
                        result = calc.perform_operation(operation,a, b)

                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"\nResult: {result}")
                    except ValidationError as e:
                        logging.error(f"Validation error: {e}")
                        error(f"Validation error: {e}")

                    except OperationError as e:
                        logging.error(f"Operation error: {e}")
                        error(f"Operation failed: {e}")

                    except Exception as e:
                        logging.error(f"Unexpected error: {e}")
                        error(f"Invalid input. Use: command number1 number2")
                    continue

                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                warning("Operation cancelled.")
                continue
            except EOFError:
                warning("Input terminated. Exiting...")
                break
            except Exception as e:
                error(f"Error: {e}")
                continue

    except Exception as e:
        error(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise
