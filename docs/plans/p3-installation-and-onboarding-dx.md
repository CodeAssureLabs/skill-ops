# Plan - P3: Installation & Onboarding DX

The current developer experience requires manual steps before first use — creating `~/.skill-ops/`, hand-editing `registry.json`, and running from a cloned repo. This plan addresses two distinct problems: **configuration bootstrapping** (first-run setup) and **installation** (getting the CLI on the machine).

## Context

Today's onboarding flow:

```text
1. Clone the skill-ops repo
2. cd cli && uv sync
3. mkdir -p ~/.skill-ops
4. Manually create ~/.skill-ops/registry.json
5. Hand-edit JSON to add clone mappings
6. Now you can run skill-ops hydrate
```

Steps 3–5 are error-prone, undiscoverable, and platform-awkward (especially on Windows where `~` behaves differently). Steps 1–2 assume the user has `uv` installed and wants to clone the entire repo just to use the CLI.

## Short Term: CLI Self-Bootstrapping

**Goal:** Eliminate manual directory/file creation. The CLI should handle its own setup.

### [Component] New `setup` Command

#### [NEW] `skill-ops setup`

An interactive first-run command that:

- Creates `~/.skill-ops/` if it doesn't exist (using platform-appropriate home directory resolution).
- Scaffolds an empty `registry.json` with the correct schema.
- Optionally prompts the user to add their first clone mapping interactively.
- Detects the platform and confirms the linking strategy (symlinks vs junctions).
- Prints a summary of what was created and next steps.

#### [MODIFY] `skill-ops hydrate`

- If `~/.skill-ops/registry.json` doesn't exist when `hydrate` is called, auto-create it with an empty `clones` map and emit a warning: `"No registry found. Created empty registry at ~/.skill-ops/registry.json. Run 'skill-ops setup' to configure clone mappings."`
- This makes `hydrate` non-fatal for first-time users who skip `setup`.

### [Component] New `registry` Subcommand

#### [NEW] `skill-ops registry add <remote-url> <local-path>`

- Adds a clone mapping to `~/.skill-ops/registry.json` without hand-editing JSON.
- Validates that `<local-path>` exists and is a directory.
- Creates `~/.skill-ops/` and `registry.json` if they don't exist yet.

#### [NEW] `skill-ops registry list`

- Displays all configured clone mappings from the registry.

#### [NEW] `skill-ops registry remove <remote-url>`

- Removes a clone mapping from the registry.

### Verification

- `skill-ops setup` on a clean machine creates the expected files.
- `skill-ops hydrate` on a machine with no `~/.skill-ops/` does not crash.
- `skill-ops registry add` / `list` / `remove` round-trips correctly.

---

## Medium Term: PyPI Distribution

**Goal:** `pipx install skill-ops` works cross-platform. Users no longer need to clone the repo.

### [Component] Package Configuration

#### [MODIFY] `cli/pyproject.toml`

- Add `[project.scripts]` entry point so `pip install` exposes a `skill-ops` command globally.
- Ensure package metadata (name, version, description, license, Python version constraints) is publication-ready.
- Verify `skill-ops` is available as a package name on PyPI (or choose an alternative like `skill-ops-cli`).

### [Component] Publication Workflow

#### [NEW] GitHub Action for PyPI release

- Triggered on version tags (e.g., `v0.1.0`).
- Builds the package and publishes to PyPI using trusted publishing (OIDC).
- Runs the test suite before publishing.

### Target Onboarding Flow

```text
1. pipx install skill-ops
2. skill-ops setup          # interactive first-run
3. skill-ops init            # in a project repo
4. skill-ops hydrate         # ready to go
```

### Verification

- `pipx install skill-ops` from PyPI installs successfully and `skill-ops --help` works.
- The installed CLI behaves identically to the repo-local `python3 -m skill_ops.cli` invocation.

---

## Long Term: Platform-Specific Package Managers

**Goal:** Native installation via the user's preferred package manager, if adoption warrants maintaining multiple distribution channels.

### Homebrew (macOS / Linux)

#### [NEW] Homebrew Tap

- Create a `homebrew-skill-ops` tap repository (e.g., `github.com/CodeAssureLabs/homebrew-skill-ops`).
- Write a formula that installs from PyPI or from source.
- Enables: `brew install CodeAssureLabs/skill-ops/skill-ops`

### Scoop (Windows)

#### [NEW] Scoop Manifest

- Create a Scoop bucket or submit to the community bucket.
- Manifest points to a release artifact (e.g., a wheel or standalone zip).
- Enables: `scoop install skill-ops`

### Standalone Binaries (Optional)

- Use PyInstaller or Nuitka to produce single-file executables.
- Attach to GitHub Releases for users who don't want Python installed at all.
- Trade-off: larger binary size, more build complexity, but zero runtime dependencies.

### Decision Criteria

These channels should only be pursued when:

- There is measurable user demand (e.g., GitHub issues requesting it).
- The core CLI is stable (post-P2 testing).
- There is capacity to maintain the additional packaging infrastructure.

---

## Priority Summary

| Phase | Effort | Impact | Depends On |
| :--- | :--- | :--- | :--- |
| **Short term** — `setup` + `registry` commands | Low | High — removes biggest DX friction | P0 (CLI exists) |
| **Medium term** — PyPI distribution | Medium | High — one-liner install, cross-platform | Short term (clean onboarding flow to ship) |
| **Long term** — Homebrew / Scoop / binaries | Medium–High per channel | Incremental — convenience for specific audiences | Medium term (stable package on PyPI) |
