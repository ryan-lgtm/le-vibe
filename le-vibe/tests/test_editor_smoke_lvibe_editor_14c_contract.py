"""Contract: editor/smoke-lvibe-editor.sh + ci-editor-gate keep STEP 14.c (lvibe ↔ binary smoke)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_smoke_lvibe_editor_script_contract():
    text = (_repo_root() / "editor" / "smoke-lvibe-editor.sh").read_text(encoding="utf-8")
    assert "14.c" in text or "STEP 14" in text
    assert "le_vibe.launcher" in text
    assert "--skip-first-run" in text
    assert "--editor" in text
    assert "--version" in text
    assert "LE_VIBE_EDITOR" in text
    assert "ollama" in text


def test_ci_editor_gate_bash_n_smoke_lvibe_editor():
    text = (_repo_root() / "packaging" / "scripts" / "ci-editor-gate.sh").read_text(encoding="utf-8")
    assert "smoke-lvibe-editor.sh" in text
    assert "bash -n" in text
