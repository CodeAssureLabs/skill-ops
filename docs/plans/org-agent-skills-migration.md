# Migration Plan: Git Helper & Git Stacking to Org Agent Skills

This plan details the process of moving the `git-helper` and `git-stacking` skills from the experimental `skill-ops` repository to their new permanent home in the `org-agent-skills` repository.

## User Review Required

> [!IMPORTANT]
> Since the files in `skill-ops` are uncommitted, I will use `cp -r` to copy them to the new repository first, and then only remove them from the source once you've verified the move.

> [!NOTE]
> I am proposing to place the skills directly at the root of `org-agent-skills`, e.g., `/Users/your-username/Projects/org-agent-skills/git-helper/`. Please confirm if you'd prefer them in a `skills/` subdirectory.

## The Skill-Ops Setup (Canonical Example)

To make the org-level skills available to `codeassure-github-bot` (and other repos), we will implement the **Hydration Pattern**:

1. **Remote Source**: `git@github.com:CodeAssureLabs/org-agent-skills.git` (The new repo).
2. **Local Registry** (`~/.skill-ops/registry.json`): Maps the remote to `/Users/your-username/Projects/org-agent-skills`.
3. **Repo Manifest** (`codeassure-github-bot/.agent/skill-ops.json`):

    ```json
    {
      "namespaces": {
        "org": {
          "path": ".agent/skills/org",
          "remote": "git@github.com:CodeAssureLabs/org-agent-skills.git"
        }
      }
    }
    ```

4. **Hydration (POC)**: We will manually simulate the hydration process by creating symlinks:
    `codeassure-github-bot/.agent/skills/org` -> `org-agent-skills`

> [!IMPORTANT]
> **Do not commit symlinks**. Symlinks are machine-specific (they use absolute paths). Ensure `.agent/skills/` is added to your `.gitignore`. Only the manifest `.agent/skill-ops.json` should be committed.

## Proposed Changes

### [org-agent-skills](https://github.com/CodeAssureLabs/org-agent-skills)

Summary: Structure and populate the new org-level skills repository.

#### [NEW] [README.md](https://github.com/CodeAssureLabs/org-agent-skills/README.md)

Creation of a README explaining the purpose of this repository as the central hub for CodeAssure organization-level skills.

#### [NEW] [git-helper](https://github.com/CodeAssureLabs/org-agent-skills/git-helper)

Migration of all files from `skill-ops/.agent/skills/org/git-helper`.

#### [NEW] [git-stacking](https://github.com/CodeAssureLabs/org-agent-skills/git-stacking)

Migration of all files from `skill-ops/.agent/skills/org/git-stacking`.

---

### [skill-ops](https://github.com/CodeAssureLabs/skill-ops)

Summary: Cleanup of migrated skills (Stage 2 - after verification).

#### [DELETE] [git-helper](https://github.com/CodeAssureLabs/skill-ops/.agent/skills/org/git-helper)

Removal of the skill folder after successful migration and verification.

#### [DELETE] [git-stacking](https://github.com/CodeAssureLabs/skill-ops/.agent/skills/org/git-stacking)

Removal of the skill folder after successful migration and verification.

---

### [codeassure-github-bot](https://github.com/CodeAssureLabs/codeassure-github-bot)

Summary: Migrate from monolithic skills symlink to namespaced Skill-Ops structure.

#### [NEW] [.agent/skill-ops.json](https://github.com/CodeAssureLabs/codeassure-github-bot/.agent/skill-ops.json)

Manifest defining the `org` namespace and pointing to the `org-agent-skills` remote.

#### [NEW] [.agent/.gitignore](https://github.com/CodeAssureLabs/codeassure-github-bot/.agent/.gitignore)

Local exclusion of namespaced skill folders to keep the root `.gitignore` clean.

---

### Home Directory

#### [NEW] ~/.skill-ops/registry.json

Creation of the global registry mapping remote SSH URLs to local project paths.

## Verification Plan

### Automated Verification

- I will run `diff -r` between the source and destination to ensure absolute parity of the uncommitted files.
- I will verify symlink integrity in `codeassure-github-bot`.
- I will check that `git-helper` and `git-stacking` are discoverable under the `org/` namespace.

### Manual Verification

1. Review the new structure in `org-agent-skills`.
2. Verify that `codeassure-github-bot` can successfully access both `personal` and `org` skills.
3. Confirm that the move from `skill-ops` can proceed (deletion).
