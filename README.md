# Module 6 Mid Term Project: Enhanced Calculator Command-Line Application

## Project Overview

The **Enhanced Calculator** is a Python‑based command‑line application that performs advanced arithmetic operations while demonstrating key software‑engineering principles.
It integrates **Object‑Oriented Programming (OOP)**, **design patterns** (Factory, Observer, Memento), **data management** with pandas, **configuration management** using environment variables, and **logging** for traceability.
The project also includes unit testing and a **CI/CD pipeline** via GitHub Actions to ensure reliability and maintainability.

## Project Structure
```
app/
    __init__.py
    calculator.py
    calculation.py
    operations.py
    calculator_config.py
    calculator_memento.py
    history.py
    input_validators.py
    calculator_repl.py

tests/
    conftest.py
    test_calculator.py
    test_calculation.py
    test_operations.py
    test_history.py
    test_input_validators.py
    test_exceptions.py
    test_calculator_repl.py

```

## Setup Instructions

**1. Clone the repository**
```
git clone https://github.com/<your‑username>/module6‑mid‑term‑enhanced‑calculator.git
cd module6‑mid‑term‑enhanced‑calculator
```

**2. Create and activate a virtual environment**
```
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

**3. Install dependencies**
```
pip install -r requirements.txt
```

**4. Verify installation**
```
python --version
pytest --version
```

## Virtual Environment Instructions
The virtual environment isolates project dependencies from your global Python installation.

**To activate:**
```
source venv/bin/activate
```
**To reinstall dependencies after cloning:**
```
pip install -r requirements.txt
```

## How to Run Tests
All tests are written with **pytest** and **pytest‑cov**.

**Run the full suite:**
```
pytest
```
**Run with coverage enforcement:**
```
pytest --cov=app --cov-fail-under=90
```
**View detailed coverage report:**
```
pytest --cov=app --cov-report=term-missing
```

---

### ** Test Installation**
Run:

```bash
pip install .
```

Then start your REPL
calc-repl
