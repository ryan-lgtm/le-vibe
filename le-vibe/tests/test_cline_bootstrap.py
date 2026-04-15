"""C3: Cline startup bootstrap policy is seeded by default."""

from __future__ import annotations

from pathlib import Path

from le_vibe.cline_bootstrap import CLINE_BOOTSTRAP_RULE_NAME, ensure_cline_bootstrap_rule


def test_ensure_cline_bootstrap_rule_creates_default_template(tmp_path: Path) -> None:
    dest = ensure_cline_bootstrap_rule(tmp_path)
    assert dest == tmp_path / ".clinerules" / CLINE_BOOTSTRAP_RULE_NAME
    assert dest.is_file()
    text = dest.read_text(encoding="utf-8")
    assert ".lvibe/session-manifest.json" in text
    assert ".lvibe/**/*.md" in text
    assert "Before making edits, read project context in this order:" in text


def test_ensure_cline_bootstrap_rule_is_idempotent(tmp_path: Path) -> None:
    first = ensure_cline_bootstrap_rule(tmp_path)
    first.write_text("custom\n", encoding="utf-8")
    second = ensure_cline_bootstrap_rule(tmp_path)
    assert second.read_text(encoding="utf-8") == "custom\n"
