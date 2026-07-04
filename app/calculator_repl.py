from decimal import Decimal
import logging
from logging import config

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
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
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    print("\nAvailable commands:")
                    print("  add, subtract, multiply, divide")
                    print("  power, root, modulus, int_divide")
                    print("  percent, abs_diff")
                    print("\nOther commands:")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  filter - Filter history by operation")
                    print("  export_csv - Export history to CSV")
                    print("  export_excel - Export history to Excel")
                    print("  exit - Exit the calculator")
                    continue

                if command == 'exit':
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Warning: Could not save history: {e}")
                    print("Goodbye!")
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print("History is empty.")
                    else:
                        print("\nCalculation History:")
                        for item in calc.history:
                            print(f"{item.operation}({item.operand1}, {item.operand2}) = {item.result}")
                    continue

                if command == 'clear':
                    calc.clear_history()
                    print("History cleared")
                    continue

                if command == 'undo':
                    try:
                        calc.undo()
                        print("Undid last calculation.")
                    except Exception as e:
                        print(f"Error undoing last calculation: {e}")
                    continue

                if command == 'redo':
                    try:
                        calc.redo()
                        print("Redid last undone calculation.")
                    except Exception as e:
                        print(f"Error redoing last undone calculation: {e}")
                    continue

                if command == 'save':
                    try:
                        calc.save_history()
                        print("History saved successfully")
                    except Exception as e:
                        print(f"Error saving history: {e}")
                    continue

                if command == 'load':
                    try:
                        calc.load_history()
                        print("History loaded successfully")
                    except Exception as e:
                        print(f"Error loading history: {e}")
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
                        print(f"Invalid number format: {e}")
                        continue

                    filtered_df = calc.filter_history(operation, min_value, max_value)

                    if filtered_df.empty:
                        print("No matching history entries found.")
                    else:
                        print("\nFiltered History:")
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
                        print(f"Invalid number format: {e}")
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
                        print(f"Invalid number format: {e}")
                        continue

                    calc.export_filtered_history_to_excel(operation or None, min_value, max_value)

                if command in ['add','subtract','multiply','divide','power','root','modulus','int_divide','percent', 'abs_diff']:
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation cancelled")
                            continue

                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)
                        result = calc.perform_operation(operation,a, b)

                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"\nResult: {result}")
                    except ValidationError as e:
                        logging.error(f"Validation error: {e}")
                        print(f"Error: {e}")

                    except OperationError as e:
                        logging.error(f"Operation error: {e}")
                        print(f"Operation failed: {e}")

                    except Exception as e:
                        logging.error(f"Unexpected error: {e}")
                        print(f"Invalid input. Use: command number1 number2")
                    continue

                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nOperation cancelled")
                continue
            except EOFError:
                print("\nInput terminated. Exiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise
