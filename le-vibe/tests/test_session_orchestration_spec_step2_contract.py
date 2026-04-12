"""Contract: docs/SESSION_ORCHESTRATION_SPEC.md keeps STEP 2 + session_orchestrator pointer."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_session_orchestration_spec_documents_step2_and_e1():
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "STEP 2" in text
    assert "session_orchestrator" in text
    assert "test_session_orchestrator.py" in text
    assert "test_session_orchestration_spec_step2_contract.py" in text
    assert "ensure_pm_session_artifacts" in text
    assert "apply_opening_skip" in text
    assert "session_manifest_example_source_path" in text
    assert "schemas/session-manifest.v1.example.json" in text
    assert "spec-phase2.md" in text and "§14" in text


def test_session_orchestration_spec_phase2_paragraph_lists_linux_compile_tarball():
    """STEP 14.e / 14.j: Phase 2 vs this tree paragraph stays honest vs build-le-vibe-ide.yml."""
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "linux_compile" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-editor-nvmrc-sync.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "node --version" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text


def test_session_orchestration_spec_phase2_paragraph_lists_14d_branding_honesty():
    """STEP 14.d: SESSION_ORCHESTRATION_SPEC separates PM session work from IDE branding staging."""
    text = (_repo_root() / "docs" / "SESSION_ORCHESTRATION_SPEC.md").read_text(encoding="utf-8")
    assert "14.d" in text
    assert "branding-staging.checklist.md" in text
    assert "read before overrides" in text
    assert "14.c vs 14.d" in text
