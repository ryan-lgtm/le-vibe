"""Tests for `.lvibe/` workspace hub and gitignore append."""

from __future__ import annotations

from pathlib import Path

import pytest

from le_vibe.workspace_hub import (
    ensure_gitignore_has_lvibe,
    ensure_lvibe_workspace,
    prepare_workspaces_for_editor_args,
    workspace_roots_from_editor_args,
)


def _expected_agent_skill_count() -> int:
    templates_dir = Path(__file__).resolve().parents[1] / "templates" / "agents"
    return len([p for p in templates_dir.glob("*.md") if p.name.lower() != "readme.md"])


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
    assert len(list((lv / "agents").glob("*/skill.md"))) == _expected_agent_skill_count()
    assert (root / ".continue" / "rules" / "00-le-vibe-lvibe-memory.md").is_file()
    assert (root / ".continue" / "rules" / "01-le-vibe-product-welcome.md").is_file()
    assert (root / ".clinerules" / "00-le-vibe-bootstrap.md").is_file()
    assert (lv / "WELCOME.md").is_file()
    assert (lv / "workflows" / "setup-workspace.md").is_file()
    assert "/setup-workspace" in (lv / "workflows" / "setup-workspace.md").read_text(encoding="utf-8")
    agents_md = (lv / "AGENTS.md").read_text(encoding="utf-8")
    assert "USER RESPONSE REQUIRED" in agents_md
    assert "§7.2" in agents_md
    assert "numbered questions" in agents_md
    assert "Deterministic recall order" in agents_md
    assert "session-manifest.json" in agents_md
    assert "rag/refs/" in agents_md
    assert "Avoid broad `.lvibe/**` rescans" in agents_md
    assert (
        "- **Deterministic recall order:** `session-manifest.json` → `memory/incremental.md` (tail) / "
        "`memory/workspace-scan.md` → `rag/refs/` relevant refs → only required "
        "`agents/<agent_id>/skill.md` files."
    ) in agents_md
    deterministic_line = next(
        line for line in agents_md.splitlines() if line.strip().startswith("- **Deterministic recall order:**")
    )
    assert "memory/incremental.md" in deterministic_line
    assert "memory/workspace-scan.md" in deterministic_line
    i_manifest = agents_md.index("session-manifest.json")
    i_memory = agents_md.index("memory/incremental.md")
    i_rag = agents_md.index("rag/refs/")
    i_skills = agents_md.index("agents/<agent_id>/skill.md")
    assert i_manifest < i_memory < i_rag < i_skills


def test_gitignore_append_idempotent(tmp_path: Path):
    root = tmp_path / "p"
    root.mkdir()
    gi = root / ".gitignore"
    gi.write_text("*.log\n", encoding="utf-8")
    assert ensure_gitignore_has_lvibe(root) is True
    text = gi.read_text(encoding="utf-8")
    assert ".lvibe/" in text
    assert ensure_gitignore_has_lvibe(root) is False


def test_gitignore_append_adds_newline_before_block_when_file_has_no_trailing_newline(
    tmp_path: Path,
) -> None:
    root = tmp_path / "p-no-nl"
    root.mkdir()
    gi = root / ".gitignore"
    gi.write_text("*.log", encoding="utf-8")
    assert ensure_gitignore_has_lvibe(root) is True
    text = gi.read_text(encoding="utf-8")
    assert ".lvibe/" in text
    assert "*.log" in text
    assert text.index("*.log") < text.index(".lvibe/")
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


@pytest.mark.parametrize("line", [".lvibe", ".lvibe/**"])
def test_gitignore_skip_append_when_lvibe_listed_without_slash_or_glob(tmp_path: Path, line: str) -> None:
    """workspace_hub._gitignore_already_mentions_lvibe — no duplicate Lé Vibe block."""
    root = tmp_path / "gitig-variants"
    root.mkdir()
    gi = root / ".gitignore"
    gi.write_text(f"{line}\n", encoding="utf-8")
    assert ensure_gitignore_has_lvibe(root) is False
    assert gi.read_text(encoding="utf-8").strip() == line


def test_deterministic_recall_order_aligned_between_continue_rule_and_agents_md(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    continue_rule = (
        tmp_path / ".continue" / "rules" / "00-le-vibe-lvibe-memory.md"
    ).read_text(encoding="utf-8")
    agents_md = (tmp_path / ".lvibe" / "AGENTS.md").read_text(encoding="utf-8")

    continue_section = continue_rule.split("**Deterministic recall order (token-efficient):**", 1)[1].split(
        "Avoid broad `.lvibe/**` rescans",
        1,
    )[0]
    agents_section = agents_md.split("**Deterministic recall order:**", 1)[1].split(
        "Avoid broad `.lvibe/**` rescans",
        1,
    )[0]
    ordered_stages = [
        "session-manifest.json",
        "memory/incremental.md",
        "rag/refs/",
        "agents/<agent_id>/skill.md",
    ]
    continue_positions = [continue_section.index(token) for token in ordered_stages]
    agents_positions = [agents_section.index(token) for token in ordered_stages]
    assert continue_positions == sorted(continue_positions)
    assert agents_positions == sorted(agents_positions)
    assert "memory/workspace-scan.md" in continue_section
    assert "memory/workspace-scan.md" in agents_section
