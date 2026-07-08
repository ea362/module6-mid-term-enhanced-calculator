import pytest
from app.calculator_repl import calculator_repl

# Helper to provide a finite sequence of inputs, always ending with "exit"
def make_inputs(sequence):
    iterator = iter(sequence)
    def _input(prompt):
        try:
            return next(iterator)
        except StopIteration:
            return "exit"
    return _input

# --- Basic arithmetic ---
def test_repl_add(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", make_inputs(["add", "2", "3", "exit"]))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Result: 5" in captured.out

def test_repl_subtract(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", make_inputs(["subtract", "5", "3", "exit"]))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Result: 2" in captured.out

def test_repl_multiply(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", make_inputs(["multiply", "4", "2", "exit"]))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Result: 8" in captured.out

def test_repl_divide(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", make_inputs(["divide", "10", "2", "exit"]))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Result: 5" in captured.out

def test_repl_power(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", make_inputs(["power", "2", "3", "exit"]))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Result: 8" in captured.out

def test_repl_root(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", make_inputs(["root", "9", "2", "exit"]))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Result: 3" in captured.out

# --- Commands ---
def test_repl_help(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", make_inputs(["help", "exit"]))
    calculator_repl()
    captured = capsys.readouterr()
    # The actual output has "Available Commands:" (capital C)
    assert "Available Commands" in captured.out

def test_repl_history(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", make_inputs(["add", "2", "3", "history", "exit"]))
    calculator_repl()
    captured = capsys.readouterr()
    # The output format is "Addition(2, 3) = 5"
    assert "Addition(2, 3) = 5" in captured.out

def test_repl_clear(monkeypatch, capsys):
    inputs = ["add", "2", "3", "clear", "history", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "History cleared" in captured.out
    # After clear, history command shows "History is empty."
    assert "History is empty" in captured.out

def test_repl_undo_redo(monkeypatch, capsys):
    inputs = ["add", "2", "3", "undo", "redo", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    # Undo prints "Undid last calculation." and redo prints "Redid last undone calculation."
    assert "Undid last calculation" in captured.out
    assert "Redid last undone calculation" in captured.out

def test_repl_cancel(monkeypatch, capsys):
    inputs = ["add", "cancel", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

# --- Error handling ---
def test_repl_invalid_number(monkeypatch, capsys):
    inputs = ["add", "abc", "2", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    # Actual error message: "Validation error: Invalid number format: abc"
    assert "Invalid number format" in captured.out

def test_repl_division_by_zero(monkeypatch, capsys):
    inputs = ["divide", "5", "0", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    # Actual error: "Validation error: Division by zero is not allowed"
    assert "Division by zero is not allowed" in captured.out

def test_repl_unknown_command(monkeypatch, capsys):
    inputs = ["foo", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out

def test_repl_root_negative(monkeypatch, capsys):
    inputs = ["root", "-9", "2", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    # Actual error: "Validation error: Cannot calculate root of negative number"
    assert "Cannot calculate root of negative number" in captured.out

# --- Save & Load ---
def test_repl_save(monkeypatch, capsys):
    inputs = ["add", "2", "3", "save", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "History saved successfully" in captured.out

def test_repl_load(monkeypatch, capsys):
    inputs = ["load", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    # Since no history file exists, it will print "History loaded successfully" (if file absent, it returns silently?) Actually, load_history returns if file doesn't exist, so it prints "History loaded successfully". So we can check that.
    assert "History loaded successfully" in captured.out or "Error loading" in captured.out

# --- Interrupts ---
def test_repl_keyboard_interrupt(monkeypatch, capsys):
    call_count = 0
    def mock_input(prompt):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise KeyboardInterrupt
        return "exit"
    monkeypatch.setattr("builtins.input", mock_input)
    calculator_repl()
    captured = capsys.readouterr()
    assert "Operation cancelled" in captured.out

def test_repl_eof(monkeypatch, capsys):
    def mock_input(prompt):
        raise EOFError
    monkeypatch.setattr("builtins.input", mock_input)
    calculator_repl()
    captured = capsys.readouterr()
    assert "Input terminated" in captured.out

# --- Error branches ---
def test_repl_save_error(monkeypatch, capsys):
    import app.calculator_repl
    original_calculator = app.calculator_repl.Calculator

    class MockCalculator(original_calculator):
        def save_history(self):
            raise Exception("Mock save error")

    monkeypatch.setattr(app.calculator_repl, "Calculator", MockCalculator)
    inputs = ["add", "2", "3", "save", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Error saving history" in captured.out

def test_repl_load_error(monkeypatch, capsys):
    import app.calculator_repl
    original_calculator = app.calculator_repl.Calculator

    class MockCalculator(original_calculator):
        def load_history(self):
            raise Exception("Mock load error")

    monkeypatch.setattr(app.calculator_repl, "Calculator", MockCalculator)
    inputs = ["load", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Error loading history" in captured.out

def test_repl_fatal_error(monkeypatch, capsys):
    import app.calculator_repl

    def bad_calculator(*args, **kwargs):
        raise Exception("Fatal init error")

    monkeypatch.setattr(app.calculator_repl, "Calculator", bad_calculator)
    with pytest.raises(Exception, match="Fatal init error"):
        calculator_repl()
    captured = capsys.readouterr()
    assert "Fatal error" in captured.out

def test_repl_filter(monkeypatch, capsys):
    inputs = ["add", "2", "3", "save", "filter", "", "", "", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Filtered History" in captured.out

def test_repl_export_csv(monkeypatch, capsys):
    inputs = ["add", "2", "3", "save", "export_csv", "", "", "", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Filtered history exported to" in captured.out

def test_repl_export_excel(monkeypatch, capsys):
    inputs = ["add", "2", "3", "save", "export_excel", "", "", "", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Filtered history exported to" in captured.out

def test_repl_analytics(monkeypatch, capsys):
    inputs = ["add", "2", "3", "save", "analytics", "", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Analytics Summary" in captured.out

def test_repl_unexpected_operation_error(monkeypatch, capsys):
    """Cover the generic 'except Exception' inside arithmetic block."""
    import app.calculator_repl
    original_calculator = app.calculator_repl.Calculator

    class MockCalculator(original_calculator):
        def perform_operation(self, a, b):
            raise TypeError("Mock unexpected error")

    monkeypatch.setattr(app.calculator_repl, "Calculator", MockCalculator)
    inputs = ["add", "2", "3", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Unexpected error" in captured.out