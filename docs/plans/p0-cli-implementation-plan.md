# Skill-Ops CLI Implementation Plan

Skill-Ops is an "Agentic DevOps" framework to manage AI Agent capabilities. This plan covers the creation of the P0 core CLI tool.

## User Review Required

> [!IMPORTANT]
> The CLI will be implemented in Python using `uv` for dependency management and `typer` for the CLI interface. This ensures a modern, type-safe development experience that integrates well with the existing `uv`-based ecosystem in this workspace.

## Proposed Changes

### [Component] Skill-Ops CLI

The CLI will be located in the `skill-ops/cli` subdirectory.

#### [NEW] [cli/pyproject.toml](https://github.com/CodeAssureLabs/skill-ops/cli/pyproject.toml)

Initialize the project with `uv` and define dependencies:

- `typer` for CLI structure
- `pydantic` for config validation
- `rich` for beautiful output

#### [NEW] [cli/skill_ops/cli.py](https://github.com/CodeAssureLabs/skill-ops/cli/skill_ops/cli.py)

Core CLI entry point with command definitions:

- `init`: Create template `.agent/skill-ops.json`.
- `hydrate`: Create symlinks based on manifest and registry.
- `list`: Show available skills.
- `validate`: Check for broken links.

#### [NEW] [cli/skill_ops/core.py](https://github.com/CodeAssureLabs/skill-ops/cli/skill_ops/core.py)

Logic for hydration, symlink management, and `.gitignore` updates.

## Verification Plan

### Automated Tests

I will add a basic test suite using `pytest` to verify:

- Manifest parsing and validation.
- Symlink creation logic (mocked filesystem where appropriate).
- `.gitignore` update logic.

Run tests with:

```bash
uv run pytest
```

### Manual Verification

1. Run `skill-ops init` in a new temp directory.
2. Run `skill-ops hydrate` in the `codeassure-github-bot` repo (after adding it to the local registry) and verify symlinks are created correctly in `.agent/skills/`.
3. Verify that `.agent/.gitignore` is updated with the correct exclusions.
4. Run `skill-ops list` to see the detected skills.
