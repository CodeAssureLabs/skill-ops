import json

from skill_ops.core import create_link, init_manifest, load_manifest, load_registry


def test_load_manifest(mock_manifest, temp_repo):
    manifest = load_manifest(temp_repo / ".agent")
    assert manifest.schema_version == "1.0"
    assert "repo" in manifest.namespaces
    assert "org" in manifest.namespaces


def test_load_registry(mock_registry, temp_home, mocker):
    mocker.patch("skill_ops.core.get_registry_path", return_value=mock_registry)
    registry = load_registry()
    assert "git@github.com:org/skills.git" in registry.clones


def test_init_manifest(temp_repo):
    agent_path = temp_repo / "new_agent"
    manifest_path = init_manifest(agent_path)
    assert manifest_path.exists()
    assert (agent_path / ".gitignore").exists()
    with open(manifest_path, "r") as f:
        data = json.load(f)
        assert data["namespaces"]["repo"]["type"] == "local"


def test_create_link_symlink(temp_repo, mocker):
    source = temp_repo / "source"
    source.mkdir()
    target = temp_repo / "target_link"

    # Mock os.name to be posix
    mocker.patch("os.name", "posix")
    mock_symlink = mocker.patch("os.symlink")

    create_link(source, target, strategy="symlink")
    mock_symlink.assert_called_once_with(source, target)


def test_create_link_junction_windows(temp_repo, mocker):
    source = temp_repo / "source"
    source.mkdir()
    target = temp_repo / "target_junction"

    mocker.patch("os.name", "nt")
    mock_run = mocker.patch("subprocess.run")

    create_link(source, target, strategy="junction")

    # Assert subprocess.run was called with mklink /J
    args = mock_run.call_args[0][0]
    assert "mklink" in args
    assert "/J" in args
    assert str(target.absolute()) in args
    assert str(source.absolute()) in args


def test_create_link_copy(temp_repo):
    source = temp_repo / "source_dir"
    source.mkdir()
    (source / "file.txt").write_text("hello")
    target = temp_repo / "target_copy"

    create_link(source, target, strategy="copy")

    assert target.is_dir()
    assert (target / "file.txt").read_text() == "hello"
