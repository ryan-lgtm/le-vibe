"""Contract: docs/README.md STEP14_AUTONOMOUS_ENGINEER_RUNBOOK row lists manifest + icon path."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_docs_readme_step14_autonomous_runbook_row():
    text = (_repo_root() / "docs" / "README.md").read_text(encoding="utf-8")
    assert "| [`STEP14_AUTONOMOUS_ENGINEER_RUNBOOK.md`]" in text
    assert "session-manifest.step14-closeout.v1.example.json" in text
    assert "packaging/icons/.../le-vibe.svg" in text
