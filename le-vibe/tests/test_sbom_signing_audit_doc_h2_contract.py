"""Contract: docs/sbom-signing-audit.md keeps H2 supply-chain story (STEP 9)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_sbom_signing_audit_doc_lists_pip_audit_and_cyclonedx():
    text = (_repo_root() / "docs" / "sbom-signing-audit.md").read_text(encoding="utf-8")
    assert "pip-audit" in text
    assert "cyclonedx" in text.lower()
    assert "requirements.txt" in text
    assert "ci.yml" in text
    assert "H2" in text or "Roadmap H2" in text
    assert "PM_STAGE_MAP" in text
    assert "STEP 9" in text
    assert "le-vibe-python.cdx.json" in text
    assert "dependabot.yml" in text
