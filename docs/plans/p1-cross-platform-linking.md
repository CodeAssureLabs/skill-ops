# Implementation Plan - P1: Cross-Platform Linking (ADR-001)

This plan implements the cross-platform linking strategy defined in [ADR-001](/docs/adr/001-cross-platform-linking-strategy.md), ensuring Skill-Ops works reliably on Windows without requiring Administrator privileges.

## User Review Required

> [!IMPORTANT]
>
> - On Windows, we will use **Directory Junctions** instead of Symbolic Links.
> - Junctions do not require elevation or Developer Mode, making the CLI much more portable.
> - We will add an optional `--link-strategy` flag to the `hydrate` command for users who need manual control (e.g., forcing a `copy`).

## Proposed Changes

### [Component] Skill-Ops CLI Core

#### [MODIFY] [core.py](https://github.com/CodeAssureLabs/skill-ops/cli/skill_ops/core.py)

- Introduce a `create_link(source: Path, target: Path, strategy: Optional[str] = None)` helper.
- Implement platform-aware logic:
  - **POSIX (macOS/Linux)**: Default to `os.symlink`.
  - **Windows**: Default to `mklink /J` (via `subprocess`).
- Update `hydrate_skills` to use this abstraction.

### [Component] Skill-Ops CLI Interface

#### [MODIFY] [cli.py](https://github.com/CodeAssureLabs/skill-ops/cli/skill_ops/cli.py)

- Update `hydrate` command to accept `--link-strategy` (enum: `symlink`, `junction`, `copy`).
- Pass the strategy down to the core logic.

## Verification Plan

### Automated Tests

- Mock `os.name` and verify the correct linking command is selected.
- Mock `subprocess.run` to ensure `mklink /J` is called correctly on simulated Windows.

### Manual Verification

1. Run `skill-ops hydrate` on macOS and verify symlinks are still created.
2. Provide a verification script for the user to run on a Windows machine (if available) to confirm junction creation without elevation.
