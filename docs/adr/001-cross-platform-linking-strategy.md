# ADR-001: Cross-Platform Linking Strategy

**Status:** Accepted
**Date:** 2026-02-10

## Context

Skill-Ops uses the "Hydration Pattern" to project external skills into a repository's `.agent/skills/` directory via filesystem links. This works seamlessly on macOS and Linux using symbolic links, but Windows presents challenges:

- NTFS symlinks require **Administrator privileges** or **Developer Mode** (Windows 10 Build 14972+).
- Enterprise environments often restrict Developer Mode via Group Policy.
- Git for Windows defaults `core.symlinks=false`, replacing symlinks with plain text stub files on clone.

Since skill-ops targets developers across all major platforms, the CLI must handle linking reliably on Windows without requiring elevated privileges or special configuration.

## Decision

Use **symbolic links** on macOS/Linux and **directory junctions** on Windows.

### Why Directory Junctions on Windows

- Created via `mklink /J` — **no elevation or Developer Mode required**.
- Transparent to applications — they see a real directory.
- The hydration pattern links at the **namespace directory level** (e.g., `.agent/skills/team` -> source directory), which maps directly to what junctions support.

### What We Considered

| Option | Pros | Cons |
| :--- | :--- | :--- |
| **Symlinks everywhere** | Single code path | Requires Developer Mode or Admin on Windows; broken in many enterprise setups |
| **Directory junctions on Windows** | No elevation needed; transparent to apps | Local paths only; directories only (not individual files) |
| **Copy fallback** | Works everywhere | No live-sync; edits to source not reflected until re-hydration; confusing mental model |
| **Hardlinks** | No elevation for files | Directories not supported; only works on same volume |

## Implementation

1. **Platform detection** at hydration time determines the linking strategy.
2. **macOS/Linux:** Use `fs.symlink` to create symbolic links.
3. **Windows:** Use directory junctions (via `child_process` calling `mklink /J`, or a Node.js library that wraps junction creation).
4. **`--link-strategy` flag:** Allow explicit override (`symlink`, `junction`, `copy`) for edge cases.
5. **`skill-ops validate`** checks link health and reports the strategy in use (e.g., `team namespace: junction (Windows)`).
6. **State tracking:** Record the strategy used per namespace in a local state file so that validate and subsequent hydrations are aware of the current linking method.

## Consequences

- The CLI has a platform-specific code path for link creation, but the rest of the system (validate, list, resolution) is link-strategy agnostic since both symlinks and junctions are transparent at the filesystem level.
- Individual file linking is **not supported** under the junction strategy. The hydration pattern must continue to operate at the directory level. This is consistent with the current architecture.
- The `copy` fallback exists as an escape hatch but is not the default on any platform. Users who opt into it accept that changes require re-hydration.
