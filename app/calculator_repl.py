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
                    print(f"{Colors.OKBLUE}\nAvailable Commands:{Colors.ENDC}")
                    for cmd, desc in help_dict.items():
                        print(f"{Colors.OKGREEN}{cmd:15}{Colors.ENDC} - {desc}")
                    continue

                if command == 'exit':
                    try:
                        calc.save_history()
                        print(f"{Colors.OKGREEN}History saved successfully.{Colors.ENDC}")
                    except Exception as e:
                        print(f"{Colors.WARNING}Warning: Could not save history: {e}{Colors.ENDC}")
                    print(f"{Colors.OKBLUE}Goodbye!{Colors.ENDC}")
                    break

                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print(f"{Colors.WARNING}History is empty.{Colors.ENDC}")
                    else:
                        print(f"{Colors.HEADER}\nCalculation History:{Colors.ENDC}")
                        for item in calc.history:
                            print(f"{Colors.OKBLUE}{item.operation}({item.operand1}, {item.operand2}) = {item.result}{Colors.ENDC}")
                    continue

                if command == 'clear':
                    calc.clear_history()
                    print(f"{Colors.OKGREEN}History cleared.{Colors.ENDC}")
                    continue

                if command == 'undo':
                    try:
                        calc.undo()
                        print(f"{Colors.OKGREEN}Undid last calculation.{Colors.ENDC}")
                    except Exception as e:
                        print(f"{Colors.FAIL}Error undoing last calculation: {e}{Colors.ENDC}")
                    continue


                if command == 'redo':
                    try:
                        calc.redo()
                        print(f"{Colors.OKGREEN}Redid last undone calculation.{Colors.ENDC}")
                    except Exception as e:
                        print(f"{Colors.FAIL}Error redoing last undone calculation: {e}{Colors.ENDC}")
                    continue

                if command == 'save':
                    try:
                        calc.save_history()
                        print(f"{Colors.OKGREEN}History saved successfully.{Colors.ENDC}")
                    except Exception as e:
                        print(f"{Colors.FAIL}Error saving history: {e}{Colors.ENDC}")
                    continue

                if command == 'load':
                    try:
                        calc.load_history()
                        print(f"{Colors.OKGREEN}History loaded successfully.{Colors.ENDC}")
                    except Exception as e:
                        print(f"{Colors.FAIL}Error loading history: {e}{Colors.ENDC}")
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
                        print(f"{Colors.FAIL}Invalid number format: {e}{Colors.ENDC}")
                        continue

                    filtered_df = calc.filter_history(operation, min_value, max_value)

                    if filtered_df.empty:
                        print(f"{Colors.WARNING}No matching history entries found.{Colors.ENDC}")
                    else:
                        print(f"{Colors.OKGREEN}\nFiltered History:{Colors.ENDC}")
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
                        print(f"{Colors.FAIL}Invalid number format: {e}{Colors.ENDC}")
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
                        print(f"{Colors.FAIL}Invalid number format: {e}{Colors.ENDC}")
                        continue

                    calc.export_filtered_history_to_excel(operation or None, min_value, max_value)

                if command == "analytics":
                    operation = input("Enter operation to analyze (or leave blank for all): ").strip()
                    operation = operation or None

                    stats = calc.analyze_history(operation)

                    if not stats:
                        print(f"{Colors.WARNING}No matching history to analyze.{Colors.ENDC}")
                    else:
                        print(f"{Colors.OKGREEN}Analytics Summary:{Colors.ENDC}")
                        for key, value in stats.items():
                            print(f"  {key}: {value}")
                
                if command in ['add','subtract','multiply','divide','power','root','modulus','int_divide','percent', 'abs_diff']:
                    try:
                        print(f"{Colors.OKGREEN}\nEnter numbers (or 'cancel' to abort):{Colors.ENDC}")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print(f"{Colors.WARNING}Operation cancelled.{Colors.ENDC}")
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print(f"{Colors.WARNING}Operation cancelled.{Colors.ENDC}")
                            continue

                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)
                        result = calc.perform_operation(operation,a, b)

                        if isinstance(result, Decimal):
                            result = result.normalize()

                        print(f"\nResult: {result}")
                    except ValidationError as e:
                        logging.error(f"Validation error: {e}")
                        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")

                    except OperationError as e:
                        logging.error(f"Operation error: {e}")
                        print(f"{Colors.FAIL}Operation failed: {e}{Colors.ENDC}")

                    except Exception as e:
                        logging.error(f"Unexpected error: {e}")
                        print(f"{Colors.FAIL}Invalid input. Use: command number1 number2{Colors.ENDC}")
                    continue

                print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print(f"{Colors.WARNING}Operation cancelled.{Colors.ENDC}")
                continue
            except EOFError:
                print(f"{Colors.WARNING}Input terminated. Exiting...{Colors.ENDC}")
                break
            except Exception as e:
                print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
                continue

    except Exception as e:
        print(f"{Colors.FAIL}Fatal error: {e}{Colors.ENDC}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise
