import json

import pytest


@pytest.fixture
def temp_home(tmp_path):
    """Mock home directory for registry storage."""
    home = tmp_path / "home"
    home.mkdir()
    return home


@pytest.fixture
def mock_registry(temp_home):
    """Create a mock registry.json in the temp home."""
    registry_dir = temp_home / ".skill-ops"
    registry_dir.mkdir()
    registry_file = registry_dir / "registry.json"
    data = {"clones": {"git@github.com:org/skills.git": str(temp_home / "org-skills")}}
    with open(registry_file, "w") as f:
        json.dump(data, f)
    return registry_file


@pytest.fixture
def temp_repo(tmp_path):
    """Mock repository directory."""
    repo = tmp_path / "repo"
    repo.mkdir()
    return repo


@pytest.fixture
def mock_manifest(temp_repo):
    """Create a mock skill-ops.json in the temp repo."""
    agent_dir = temp_repo / ".agent"
    agent_dir.mkdir()
    manifest_file = agent_dir / "skill-ops.json"
    data = {
        "schema_version": "1.0",
        "namespaces": {
            "repo": {"path": ".agent/skills/repo", "type": "local"},
            "org": {
                "path": ".agent/skills/org",
                "remote": "git@github.com:org/skills.git",
            },
        },
    }
    with open(manifest_file, "w") as f:
        json.dump(data, f)
    return manifest_file
