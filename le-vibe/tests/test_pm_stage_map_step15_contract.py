"""Contract: docs/PM_STAGE_MAP.md STEP 15 row lists `.lvibe/` governance + E1 (STEP 15)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step15_row_lists_governance_modules_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| 15 — `.lvibe/`")]
    assert len(rows) == 1
    row = rows[0]
    assert "§5.1" in row or "5.1" in row
    assert "workspace_hub.py" in row
    assert "workspace_consent.py" in row
    assert "workspace_policy.py" in row
    assert "workspace_storage.py" in row
    assert "test_workspace_consent.py" in row
    assert "test_workspace_storage.py" in row
    assert "test_workspace_hub.py" in row
    assert "test_pm_stage_map_step15_contract.py" in row
    assert "STEP 15" in row


def test_workspace_hub_module_docstring_lists_product_spec_step15():
    import le_vibe.workspace_hub as wh

    doc = wh.__doc__ or ""
    assert "PRODUCT_SPEC" in doc
    assert "STEP 15" in doc
    assert "PM_STAGE_MAP" in doc
    assert "workspace_consent" in doc
    assert "workspace_policy" in doc


def test_workspace_consent_and_policy_docstrings_mention_step15():
    import le_vibe.workspace_consent as wc
    import le_vibe.workspace_policy as wp

    assert "STEP 15" in (wc.__doc__ or "")
    assert "PM_STAGE_MAP" in (wc.__doc__ or "")
    assert "STEP 15" in (wp.__doc__ or "")
    assert "PM_STAGE_MAP" in (wp.__doc__ or "")
