"""Contract: docs/PM_STAGE_MAP.md STEP 9 row lists H2 SBOM + E1 (STEP 9)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step9_row_lists_h2_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 9 — H2 SBOM")]
    assert len(rows) == 1
    row = rows[0]
    assert "test_sbom_signing_audit_doc_h2_contract.py" in row
    assert "test_requirements_pins.py" in row
    assert "test_pm_stage_map_step9_contract.py" in row
    assert "le-vibe-python.cdx.json" in row
    assert "requirements.txt" in row
    assert "dependabot.yml" in row
    assert "pip-audit" in row
    assert "ci.yml" in row
    assert "H2" in row or "STEP 9" in row
