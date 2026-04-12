"""Default CI must fetch editor/vscodium so ci-editor-gate.sh runs H6 checks on GitHub Actions."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_yml_checkout_uses_recursive_submodules_for_editor_vendoring():
    text = (_repo_root() / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "actions/checkout@v4" in text
    assert "submodules: recursive" in text
