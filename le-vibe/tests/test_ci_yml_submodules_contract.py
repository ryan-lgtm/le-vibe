"""Default CI must fetch editor/vscodium so ci-editor-gate.sh runs H6 checks on GitHub Actions."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ci_yml_checkout_uses_recursive_submodules_for_editor_vendoring():
    text = (_repo_root() / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "actions/checkout@v4" in text
    assert "submodules: recursive" in text


def test_ci_yml_header_documents_le_vibe_deb_artifact_stack_only_step14():
    """STEP 14 / §7.3: default CI artifact does not include le-vibe-ide .deb — header says so."""
    text = (_repo_root() / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "upload name le-vibe-deb" in text
    assert "not le-vibe-ide" in text
    assert "apt-repo-releases.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
