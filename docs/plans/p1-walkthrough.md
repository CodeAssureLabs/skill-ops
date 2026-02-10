# Walkthrough - Phase 1: Cross-Platform Linking (ADR-001)

This phase implements the technical solution for safe and reliable filesystem linking across macOS, Linux, and Windows, as defined in [ADR-001](/docs/adr/001-cross-platform-linking-strategy.md).

## Problem Solved

Traditional Symbolic Links on Windows requires **Administrator privileges** or **Developer Mode**, creating friction for developers and potentially breaking in restricted enterprise environments.

## Implementation Details

### 1. Linking Abstraction

I introduced a `create_link` helper in `cli/skill_ops/core.py` that abstracts the platform-specific linking logic:

- **Windows**: Uses **Directory Junctions** via `mklink /J`.
  - Junctions do not require elevation or special developer settings.
  - They are transparent to the OS and AI agents.
- **macOS/Linux**: Uses standard **Symbolic Links** via `os.symlink`.

### 2. Manual Overrides

The `hydrate` command now supports a `--link-strategy` (or `-s`) flag:

- `symlink`: Force standard symbolic links.
- `junction`: Force directory junctions (Windows only).
- `copy`: Fallback that physically copies files (no live-sync).

## Verification Result

On macOS, I verified that:

1. `skill-ops hydrate --link-strategy symlink` creates a proper symbolic link.
2. `skill-ops hydrate --link-strategy copy --force` creates a real directory copy.
3. The default behavior on POSIX correctly selects `symlink`.
