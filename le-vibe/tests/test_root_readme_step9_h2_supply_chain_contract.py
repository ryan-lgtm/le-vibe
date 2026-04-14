"""Contract: root README lists STEP 9 / H2 supply chain + SBOM (Roadmap H2)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_root_readme_step9_h2_supply_chain_section():
    text = (_repo_root() / "docs" / "MONOREPO_DEVELOPER_REFERENCE.md").read_text(encoding="utf-8")
    assert "### Supply chain & SBOM — STEP 9 / H2" in text
    assert "Master orchestrator STEP 9" in text
    assert "pip-audit" in text
    assert "le-vibe-python.cdx.json" in text
    assert "sbom-signing-audit.md" in text
    assert "test_sbom_signing_audit_doc_h2_contract.py" in text
