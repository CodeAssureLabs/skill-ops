# Skill-Ops

Skill-Ops is an **"Agentic DevOps"** framework designed to manage, synchronize, and orchestrate AI Agent capabilities across multiple repositories and operational scales.

## The Core Problem

Most AI agent systems (Claude, Cursor, Aider) manage "skills" either globally or per-project.

This is not friendly for individuals and teams who want to become "ai-native".

We want ambitious people and teams to easily use and interchange between their personal agentic skills, and the agentic skills provided by their company.

Skill-Ops solves this by using a hierarchical namespacing strategy and identity-based resolution.

Skill-Ops adopts **Infrastructure as Code** as a philosophy to manage agentic skills.

### Before: The Cluttered Repo

Without a framework, skills are scattered. Some are hardcoded, some are manual copies, and some are untracked. This creates a "works on my machine" nightmare for AI Agents.

```text
.agent/
└── skills/              # Flat and cluttered
    ├── git-helper/       # Personal skill (manual copy)
    ├── deploy/           # Team skill (cloned manually)
    └── build-rules/      # Repo-native skill
```

### After: The Skill-Ops Way

With Skill-Ops, you have a clean, hierarchical structure. The AI Agent knows exactly where to look, and every link is resolveable via the manifest.

```text
.agent/
├── skill-ops.json       # Canonical Manifest (VCS tracked)
├── .gitignore           # Local exclusion of external links
└── skills/
    ├── personal/        # Namespaced: Individual developer
    ├── team/            # Namespaced: Shared team skills
    ├── org/             # Namespaced: Corporate standards
    └── repo/            # Project-specific
```

## Key Features

- **Hierarchical Namespacing**: Organize skills into `personal`, `team`, `org`, and `repo` scopes.
- **Hydration Pattern**: Project external skills into your repository via a local manifest and registry.
- **Cross-Platform**: Intelligent linking strategy—uses **Directory Junctions** on Windows (no elevation required) and **Symbolic Links** on macOS/Linux.
- **Agent Discovery**: Integrated `list` and `validate` commands to help agents discover and verify available capabilities.

## Hydration Mechanics

Skill-Ops assumes a clear distinction between **external dependencies** (personal, team, org) and **native repository content** (repo).

```text
Local Project Repo (CLI: skill-ops hydrate)
└── .agent/skills/
    ├── personal/ ------> [External] local-clones/my-private-skills
    ├── team/ ----------> [External] local-clones/team-core-skills
    ├── org/ -----------> [External] local-clones/corporate-standard-skills
    └── repo/ (Native) -> [Internal] .agent/skills/repo (Committed to Git)
```

- **External Namespaces**: These are symlinked (or junctions on Windows) to external directories defined in your global `~/.skill-ops/registry.json`. They allow you to bring in your own battle-tested tools without cluttering the project repository.
- **Native Namespace (`repo`)**: Content in this directory is part of the repository's codebase and is committed to version control. This is for skills that are specific to the unique logic of the project.

## Global Setup

Before you can hydrate skills in individual repositories, you must define where your remote skill repositories are cloned on your local machine. This is managed through a global registry.

**1. Create the registry directory:**

```bash
mkdir -p ~/.skill-ops
```

**2. Initialize the registry file:**

Create `~/.skill-ops/registry.json` (on Windows, this is `%USERPROFILE%\.skill-ops\registry.json`) and map your remote Git URLs to their local clone paths:

```json
{
  "clones": {
    "git@github.com:your-org/team-skills.git": "/Users/yourname/Projects/team-skills",
    "git@github.com:your-name/personal-skills.git": "/Users/yourname/Projects/personal-skills"
  }
}
```

Once configured, the CLI will use these paths to "hydrate" any repository that references these remotes.

## Getting Started

### 1. Installation

The Skill-Ops CLI is located in the `cli/` directory.

```bash
cd cli
uv sync
```

### 2. Basic Usage

**Initialize a repository:**

```bash
python3 -m skill_ops.cli init
```

**Effect**: Creates the `.agent/` directory, a default `skill-ops.json` manifest, and a `.agent/.gitignore` file to ensure links aren't committed to VCS.

**Hydrate skills (create links):**

```bash
python3 -m skill_ops.cli hydrate
```

**Effect**: Resolves namespaces from the manifest against your local `~/.skill-ops/registry.json`. Creates symbolic links (POSIX) or Directory Junctions (Windows) in `.agent/skills/`. Use `--force` to overwrite existing links.

**List available skills:**

```bash
python3 -m skill_ops.cli list
```

**Effect**: Scans the hydrated `.agent/skills/` directory and displays an organized tree of all available skills by namespace. No filesystem changes.

**Validate link integrity:**

```bash
python3 -m skill_ops.cli validate
```

**Effect**: Checks every link in the `.agent/skills/` directory to ensure the destination path exists and is a valid directory. Reports broken links or missing sources. No filesystem changes.

## Architecture & Vision

For a deep dive into the design philosophy, scoped namespacing, and hydration patterns, see [Vision & Architecture](docs/vision-and-architecture.md).

## Project Roadmap

The project is being developed in phases. Detailed walkthroughs and implementation plans are available for each milestone:

- **Phase 0: CLI Implementation**: Core commands (`init`, `hydrate`, `list`, `validate`). [Walkthrough](docs/plans/p0-walkthrough.md)
- **Phase 1: Cross-Platform Linking**: Windows Junctions vs. POSIX Symlinks. [Walkthrough](docs/plans/p1-walkthrough.md)
- **Phase 2: Automated Testing**: 11-test suite using `pytest`. [Walkthrough](docs/plans/p2-walkthrough.md)

## Development

To run the test suite:

```bash
cd cli
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 -m pytest tests/
```

---

*Skill-Ops: Infrastructure for the Agentic Era.*
