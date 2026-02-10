# Walkthrough - Phase 2: Unit Testing (pytest)

This phase ensures the core logic and CLI interface of Skill-Ops are robust and maintainable through an automated test suite.

## Test Suite Overview

I have implemented **11 tests** using `pytest` and `pytest-mock`, covering:

### 1. Core Logic (`tests/test_core.py`)

- **Manifest/Registry Loading**: Verifies that `skill-ops.json` and `registry.json` are parsed correctly into Pydantic models.
- **Initialization**: Ensures `skill-ops init` correctly bootstraps the `.agent/` directory and `.gitignore`.
- **Linking Abstraction**: Verified that `create_link` calls the correct OS-level commands (Simulated Windows `mklink` vs POSIX `os.symlink`).
- **Copy Strategy**: Confirmed that the `copy` strategy physically duplicates files/folders.

### 2. CLI Interface (`tests/test_cli.py`)

- **Command Output**: Uses `typer.testing.CliRunner` to verify terminal output for `init`, `list`, and `validate`.
- **Edge Cases**: Verifies that `hydrate` fails gracefully if missing a manifest.
- **Discovery**: Confirmed that `list` correctly aggregates hydrated skills across namespaces.

## How to Run Tests

To run the full test suite locally, use the following command:

```bash
cd cli && export PYTHONPATH=$PYTHONPATH:$(pwd) && python3 -m pytest tests/
```

## Results

```text
tests/test_cli.py .....             [ 45%]
tests/test_core.py ......           [100%]
=========== 11 passed in 0.13s ============
```
