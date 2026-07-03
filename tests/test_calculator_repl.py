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
    assert "Available commands" in captured.out

def test_repl_history(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", make_inputs(["add", "2", "3", "history", "exit"]))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Addition 2 3 = 5" in captured.out

def test_repl_clear(monkeypatch, capsys):
    inputs = ["add", "2", "3", "clear", "history", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "History cleared" in captured.out
    assert "No calculations in history" in captured.out

def test_repl_undo_redo(monkeypatch, capsys):
    inputs = ["add", "2", "3", "undo", "redo", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Operation undone" in captured.out
    assert "Operation redone" in captured.out

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
    assert "Error: Invalid number format" in captured.out

def test_repl_division_by_zero(monkeypatch, capsys):
    inputs = ["divide", "5", "0", "exit"]
    monkeypatch.setattr("builtins.input", make_inputs(inputs))
    calculator_repl()
    captured = capsys.readouterr()
    assert "Error: Division by zero" in captured.out

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
    assert "Error:" in captured.out

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
    assert "History loaded" in captured.out or "Error loading" in captured.out

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

def test_repl_save_error(monkeypatch, capsys):
    """Cover the 'except Exception' branch when save_history fails."""
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
    """Cover the 'except Exception' branch when load_history fails."""
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
    """Cover the outer try/except (fatal error during REPL startup)."""
    import app.calculator_repl

    def bad_calculator(*args, **kwargs):
        raise Exception("Fatal init error")

    monkeypatch.setattr(app.calculator_repl, "Calculator", bad_calculator)
    with pytest.raises(Exception, match="Fatal init error"):
        calculator_repl()
    captured = capsys.readouterr()
    assert "Fatal error" in captured.out

