"""Tests for `.lvibe/` workspace hub and gitignore append."""

from __future__ import annotations

from pathlib import Path

from le_vibe.workspace_hub import (
    ensure_gitignore_has_lvibe,
    ensure_lvibe_workspace,
    prepare_workspaces_for_editor_args,
    workspace_roots_from_editor_args,
)


def test_workspace_roots_dot_resolves(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    roots = workspace_roots_from_editor_args(["."])
    assert len(roots) == 1
    assert roots[0] == tmp_path.resolve()


def test_workspace_roots_skips_flags(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    roots = workspace_roots_from_editor_args(["-n", "."])
    assert roots == [tmp_path.resolve()]


def test_ensure_lvibe_creates_layout(tmp_path: Path):
    root = tmp_path / "proj"
    root.mkdir()
    lv = ensure_lvibe_workspace(root)
    assert lv.is_dir()
    assert (lv / "manifest.yaml").is_file()
    assert (lv / "AGENTS.md").is_file()
    assert (lv / "memory" / "incremental.md").is_file()
    assert (lv / "session-manifest.json").is_file()
    assert len(list((lv / "agents").glob("*/skill.md"))) == 8
    assert (root / ".continue" / "rules" / "00-le-vibe-lvibe-memory.md").is_file()
    assert (root / ".continue" / "rules" / "01-le-vibe-product-welcome.md").is_file()
    assert (lv / "WELCOME.md").is_file()
    assert (lv / "workflows" / "setup-workspace.md").is_file()
    assert "/setup-workspace" in (lv / "workflows" / "setup-workspace.md").read_text(encoding="utf-8")
    agents_md = (lv / "AGENTS.md").read_text(encoding="utf-8")
    assert "USER RESPONSE REQUIRED" in agents_md
    assert "§7.2" in agents_md
    assert "numbered questions" in agents_md


def test_gitignore_append_idempotent(tmp_path: Path):
    root = tmp_path / "p"
    root.mkdir()
    gi = root / ".gitignore"
    gi.write_text("*.log\n", encoding="utf-8")
    assert ensure_gitignore_has_lvibe(root) is True
    text = gi.read_text(encoding="utf-8")
    assert ".lvibe/" in text
    assert ensure_gitignore_has_lvibe(root) is False


def test_gitignore_missing_noop(tmp_path: Path):
    root = tmp_path / "q"
    root.mkdir()
    assert ensure_gitignore_has_lvibe(root) is False


def test_prepare_workspaces(tmp_path: Path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    prepare_workspaces_for_editor_args(["."])
    assert (tmp_path / ".lvibe" / "manifest.yaml").is_file()
    # no .gitignore — do not create
    assert not (tmp_path / ".gitignore").exists()


def test_gitignore_already_has_lvibe(tmp_path: Path):
    root = tmp_path / "r"
    root.mkdir()
    (root / ".gitignore").write_text(".lvibe/\n", encoding="utf-8")
    assert ensure_gitignore_has_lvibe(root) is False
