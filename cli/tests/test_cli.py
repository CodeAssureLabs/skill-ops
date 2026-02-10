from pathlib import Path

from skill_ops.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_init(temp_repo):
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--path", ".agent"])
        assert result.exit_code == 0
        assert "Successfully initialized Skill-Ops manifest" in result.output
        assert Path(".agent/skill-ops.json").exists()


def test_cli_list_empty(temp_repo):
    with runner.isolated_filesystem():
        # Create empty .agent structure
        Path(".agent/skills").mkdir(parents=True)
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "No skills found." in result.output


def test_cli_list_with_skills(temp_repo):
    with runner.isolated_filesystem():
        # Create mock skills
        skills_dir = Path(".agent/skills/org")
        skills_dir.mkdir(parents=True)
        (skills_dir / "git-helper").mkdir()
        (skills_dir / "git-stacking").mkdir()

        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "org" in result.output
        assert "git-helper" in result.output
        assert "git-stacking" in result.output


def test_cli_validate_success(temp_repo):
    with runner.isolated_filesystem():
        Path(".agent/skills").mkdir(parents=True)
        result = runner.invoke(app, ["validate"])
        assert result.exit_code == 0
        assert "All symlinks are valid!" in result.output


def test_cli_hydrate_error_no_manifest(temp_repo):
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["hydrate"])
        assert result.exit_code == 1
        assert "Error hydrating skills" in result.output
