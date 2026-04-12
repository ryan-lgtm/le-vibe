"""Contract: root README Operator troubleshooting lists STEP 6 / E5 structured log story."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_operator_troubleshooting_lists_components_and_tail():
    text = (_repo_root() / "README.md").read_text(encoding="utf-8")
    assert "Operator troubleshooting & observability" in text
    assert "le-vibe.log.jsonl" in text
    assert "managed_ollama" in text
    assert "workspace" in text
    assert "lvibe_storage" in text
    assert "tail -f" in text
    assert "privacy-and-telemetry.md" in text
    assert "LE_VIBE_STRUCTURED_LOG" in text
