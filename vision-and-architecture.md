# Skill-Ops Vision & Architecture

Skill-Ops is an "Agentic DevOps" framework designed to manage, synchronize, and orchestrate AI Agent capabilities across multiple repositories and operational scales.

## The Core Problem

Most AI agent systems (Claude, Cursor, Aider) manage "skills" either globally or per-project. This creates fragmentation, configuration drift, and namespace collisions for developers who work across multiple teams or organizations.

## The Skill-Ops Solution

Skill-Ops treats AI capabilities as **Infrastructure as Code**, using a hierarchical namespacing strategy and identity-based resolution.

### 1. Hierarchical Namespacing

Skills are organized into four distinct scopes to ensure clear governance and portability:

| Layer | Governance | Purpose |
| :--- | :--- | :--- |
| **Personal** | Developer | Private shortcuts, personal preferences, and cross-project utilities. |
| **Team** | Team Lead | Shared workflows, code review standards, and project-agnostic team tools. |
| **Org** | Enterprise | Corporate guidelines, security protocols, and shared infrastructure scripts. |
| **Repo** | Codebase | Repository-specific logic (e.g., this project's versioning protocol). |

### 2. Manifest vs. Resolution (Identity-Based)

To prevent "Namespace Collisions" (e.g., Repo A and Repo B both having a different idea of what "team" skills are), Skill-Ops separates the **Intent** from the **Reality**.

#### The Manifest (`.agent/skill-ops.json`)

Committed to the repository. It defines *what* is needed using a **Unique Remote Source**.

```json
{
  "namespaces": {
    "team": {
      "path": ".agent/skills/team",
      "remote": "git@github.com:codeassure-labs/core-skills.git"
    },
    "repo": {
      "path": ".agent/skills/repo",
      "type": "local"
    }
  }
}
```

#### The Local Registry (`~/.skill-ops/registry.json`)

Stored on the developer's machine. It maps those **Remotes** to **Local Paths**.

```json
{
  "clones": {
    "git@github.com:codeassure-labs/core-skills.git": "/Users/kimsia/Projects/ca-skills"
  }
}
```

### 3. The Hydration Pattern

The system uses **Symbolic Links** to project external skills into the repository's `.agent/skills/` directory.

- **Process**: A synchronization tool reads the Manifest and Registry to physically create symlinks.
- **Result**: The AI Agent always sees a consistent folder structure (`.agent/skills/{personal,team,org,repo}`) regardless of where the source files are actually stored on the machine.

#### The `.agent/.gitignore` (Self-Contained Exclusion)

To prevent machine-specific symlinks from being committed, a local `.gitignore` is placed alongside the manifest. Note that `skills/repo/` is **omitted** from this list because repository-specific skills are native to the codebase and should be committed:

```text
# .agent/.gitignore
# because we are adopting skill-ops hydration framework
skills/personal
skills/org
skills/team
```

This ensures the repository remains clean of external links while allowing project-specific capabilities to be versioned.

## Design Decisions

### 1. Conflict Resolution Order

**Q:** What happens if `team` and `repo` both define a skill named `version-manager`?

**A:** Use "most specific wins" — the resolution order is:

```text
repo > org > team > personal
```

The rationale: repository-specific skills are closest to the codebase and should override broader defaults. If explicit disambiguation is needed, agents can reference skills by full path (e.g., `team/version-manager` vs `repo/version-manager`).

### 2. Schema Versioning

**Q:** How do we handle manifest format changes over time?

**A:** Add a `schema_version` field to the manifest for future migration paths:

```json
{
  "schema_version": "1.0",
  "namespaces": { ... }
}
```

This enables the hydration tooling to detect and upgrade older manifests.

### 3. Skill Discovery

**Q:** How will developers find what team/org skills exist?

**A:** Two mechanisms:

1. **Local Catalog**: The CLI/extension can list available skills from hydrated namespaces.
2. **Remote Registry**: Org-level skill repos can publish a `skills.json` manifest listing all available skills with descriptions.

### 4. The `skill_registry` Key

**Q:** What is the purpose of the explicit `skill_registry` mapping in the manifest?

**A:** The `skill_registry` is the canonical list of **active/enabled** skills, separate from what's available in the namespace folders. This allows:

- Repos to selectively enable only certain skills from a namespace
- Explicit declaration of which skills are "in scope" for agent discovery
- Version pinning or feature flags per skill in the future

---

## Form Factor Analysis

Skill-Ops requires multiple form factors to achieve full coverage across the AI agent ecosystem:

### Required Form Factors

| Form Factor | Priority | Purpose |
| :--- | :--- | :--- |
| **CLI** | P0 (Core) | Foundation for all other tools. Performs hydration, validation, and can be invoked in CI/CD. |
| **VS Code Extension** | P1 | Primary IDE integration. Auto-hydration on workspace open, UI for skill management. |
| **Claude Desktop Plugin** | P2 | Enables Claude to discover and use skills outside of VS Code (standalone agent use). |

### Form Factor Details

#### CLI (`skill-ops`)

The **bedrock** of the system. All other form factors delegate to or wrap the CLI.

**Core Commands:**

- `skill-ops hydrate` — Read manifest + registry, create/update symlinks
- `skill-ops validate` — Check for broken symlinks, missing skills
- `skill-ops list` — Show available skills by namespace
- `skill-ops init` — Bootstrap a new `.agent/skill-ops.json`

**Why P0:** The CLI can be used in CI/CD pipelines, pre-commit hooks, and by other tools. It's the portable, scriptable foundation.

#### VS Code Extension

The **primary developer experience** for most users.

**Capabilities:**

- **Auto-hydration**: Trigger `skill-ops hydrate` on `onDidOpenWorkspace`
- **Identity Resolution**: Map `personal` namespace based on logged-in GitHub/GitLab identity
- **Skill Browser**: Tree view showing available skills across all namespaces
- **Inline Actions**: "Add skill to repo", "Update from remote"

**Why P1:** VS Code is the dominant editor for AI-assisted coding. The extension makes skill management invisible/automatic.

#### Claude Desktop Plugin (MCP Server)

Enables **standalone Claude usage** without VS Code.

**Capabilities:**

- Expose hydrated skills to Claude Desktop via MCP tools/resources
- Provide a "list skills" tool for Claude to discover capabilities
- Potentially a "run skill script" tool for executable skills

**Why P2:** Covers the use case of developers using Claude Desktop directly, or for non-IDE workflows (e.g., DevOps tasks, documentation generation).

### Optional/Future Form Factors

| Form Factor | Purpose |
| :--- | :--- |
| **JetBrains Plugin** | IDE coverage for IntelliJ, PyCharm, etc. |
| **GitHub Action** | CI-based skill validation and hydration |
| **Web Dashboard** | Org-level skill catalog and governance UI |

---

## Roadmap & Reference Implementation

The **CodeAssure Smartly Demo Dashboard** serves as "Customer Zero" and the reference implementation for the `repo/version-manager` pattern.
