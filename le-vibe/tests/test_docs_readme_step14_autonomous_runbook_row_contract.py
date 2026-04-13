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


def test_step14_autonomous_runbook_documents_closeout_verifier():
    text = (_repo_root() / "docs" / "STEP14_AUTONOMOUS_ENGINEER_RUNBOOK.md").read_text(encoding="utf-8")
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "build machine" in text
    assert "test host" in text
    assert "Definition of done (STEP 14 honest)" in text
    assert "Partial tree" in text
    assert "print-built-codium-path" in text
    assert "print-vsbuild-codium-path" in text
    assert "build-le-vibe-ide-deb.sh --help" in text
