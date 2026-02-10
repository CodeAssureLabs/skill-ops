# Implementation Plan - P2: Testing Strategy (pytest)

This plan outlines the testing strategy for the Skill-Ops CLI to ensure reliability across all core commands and the platform-specific linking logic.

## Proposed Changes

### [Component] Skill-Ops CLI Testing

#### [MODIFY] [pyproject.toml](https://github.com/CodeAssureLabs/skill-ops/cli/pyproject.toml)

- Add `pytest` and `pytest-mock` to development dependencies.

#### [NEW] [cli/tests/conftest.py](https://github.com/CodeAssureLabs/skill-ops/cli/tests/conftest.py)

- Define shared fixtures for temporary directories and mock manifest/registry files.

#### [NEW] [cli/tests/test_core.py](https://github.com/CodeAssureLabs/skill-ops/cli/tests/test_core.py)

- Unit tests for logic in `core.py`:
  - `load_manifest` and `load_registry` with valid/invalid data.
  - `init_manifest` directory/file creation and `.gitignore` content.
  - `create_link` logic mocking `os.name` and `subprocess`.
  - `hydrate_skills` logic mocking the filesystem.

#### [NEW] [cli/tests/test_cli.py](https://github.com/CodeAssureLabs/skill-ops/cli/tests/test_cli.py)

- Integration/CLI tests using `typer.testing.CliRunner`:
  - `init` command output and side effects.
  - `list` command output based on mock hydration state.
  - `hydrate` command with various flags (`--force`, `--link-strategy`).
  - `validate` command for healthy and broken links.

## Verification Plan

### Automated Tests

- Run the newly created test suite:

```bash
cd cli
uv run pytest
```

### Manual Verification

- None required beyond running the automated suite.
