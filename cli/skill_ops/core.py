import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel


class Namespace(BaseModel):
    path: str
    remote: Optional[str] = None
    type: str = "remote"


class Manifest(BaseModel):
    schema_version: str = "1.0"
    namespaces: Dict[str, Namespace]


class Registry(BaseModel):
    clones: Dict[str, str]


def get_registry_path() -> Path:
    return Path.home() / ".skill-ops" / "registry.json"


def load_manifest(path: Path) -> Manifest:
    manifest_file = path / "skill-ops.json"
    if not manifest_file.exists():
        raise FileNotFoundError(f"Manifest not found at {manifest_file}")
    with open(manifest_file, "r") as f:
        return Manifest.model_validate(json.load(f))


def load_registry() -> Registry:
    reg_path = get_registry_path()
    if not reg_path.exists():
        return Registry(clones={})
    with open(reg_path, "r") as f:
        return Registry.model_validate(json.load(f))


def init_manifest(agent_path: Path) -> Path:
    agent_path.mkdir(parents=True, exist_ok=True)
    manifest_file = agent_path / "skill-ops.json"
    if manifest_file.exists():
        raise FileExistsError(f"Manifest already exists at {manifest_file}")

    default_manifest = {
        "schema_version": "1.0",
        "namespaces": {"repo": {"path": ".agent/skills/repo", "type": "local"}},
    }

    with open(manifest_file, "w") as f:
        json.dump(default_manifest, f, indent=2)

    # Initialize .gitignore if it doesn't exist
    gitignore = agent_path / ".gitignore"
    if not gitignore.exists():
        with open(gitignore, "w") as f:
            f.write("# Skill-Ops hydration exclusions\n")
            f.write("skills/personal\n")
            f.write("skills/org\n")
            f.write("skills/team\n")

    return manifest_file


def create_link(source: Path, target: Path, strategy: Optional[str] = None):
    """
    Create a link from source to target using the specified strategy or platform default.
    Strategies: 'symlink', 'junction', 'copy'
    """
    if not strategy:
        strategy = "junction" if os.name == "nt" else "symlink"

    if strategy == "junction":
        if os.name != "nt":
            # Fallback to symlink on non-Windows if junction requested
            os.symlink(source, target)
        else:
            # Force absolute paths for Junctions as per ADR-001
            subprocess.run(
                [
                    "cmd",
                    "/c",
                    "mklink",
                    "/J",
                    str(target.absolute()),
                    str(source.absolute()),
                ],
                check=True,
                capture_output=True,
            )
    elif strategy == "copy":
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
    else:  # default to symlink
        os.symlink(source, target)


def hydrate_skills(
    force: bool = False, strategy: Optional[str] = None
) -> Dict[str, int]:
    cwd = Path.cwd()
    agent_path = cwd / ".agent"
    manifest = load_manifest(agent_path)
    registry = load_registry()

    stats = {}

    for ns_name, ns in manifest.namespaces.items():
        if ns.type == "local":
            stats[ns_name] = 1  # Just mark it as present
            continue

        if not ns.remote:
            continue

        target_path = cwd / ns.path
        source_path_str = registry.clones.get(ns.remote)

        if not source_path_str:
            print(f"Warning: No local clone found for remote {ns.remote}")
            continue

        source_path = Path(source_path_str)
        if not source_path.exists():
            print(f"Warning: Source path {source_path} does not exist")
            continue

        # Create parent directory if needed
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if target_path.exists():
            if (
                force
                or target_path.is_symlink()
                or (os.name == "nt" and strategy == "junction")
            ):
                if target_path.is_symlink():
                    target_path.unlink()
                elif target_path.is_dir():
                    shutil.rmtree(target_path)
            else:
                print(
                    f"Skipping {ns_name}: path {target_path} already exists and is not a symlink"
                )
                continue

        create_link(source_path, target_path, strategy=strategy)
        stats[ns_name] = sum(
            1
            for p in source_path.iterdir()
            if p.is_dir() and not p.name.startswith(".")
        )

    return stats


def list_skills() -> Dict[str, List[str]]:
    cwd = Path.cwd()
    agent_skills_path = cwd / ".agent" / "skills"

    if not agent_skills_path.exists():
        return {}

    result = {}
    for ns_dir in agent_skills_path.iterdir():
        if ns_dir.is_dir():
            skills = []
            # Check if it's a symlink or real dir
            for skill_dir in ns_dir.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith("."):
                    skills.append(skill_dir.name)
            if skills:
                result[ns_dir.name] = sorted(skills)

    return result


def validate_hydration() -> List[str]:
    cwd = Path.cwd()
    agent_skills_path = cwd / ".agent" / "skills"

    if not agent_skills_path.exists():
        return ["No .agent/skills directory found"]

    issues = []
    for ns_dir in agent_skills_path.iterdir():
        if ns_dir.is_dir():
            if ns_dir.is_symlink():
                # Check if the symlink is broken
                if not ns_dir.exists():
                    source = os.readlink(ns_dir)
                    issues.append(
                        f"Namespace {ns_dir.name}: Broken symlink pointing to {source}"
                    )
            else:
                # Local repo namespace, check contents
                pass

    return issues
