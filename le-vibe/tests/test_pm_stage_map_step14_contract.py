"""Contract: docs/PM_STAGE_MAP.md STEP 14 row keeps H6 IDE CI + build-linux alias (E1 roster)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _step14_table_row(text: str) -> str:
    rows = [ln for ln in text.splitlines() if ln.lstrip().startswith("| **14 — H6 IDE**")]
    assert len(rows) == 1, f"expected single STEP 14 table row, got {len(rows)}"
    return rows[0]


def test_pm_stage_map_step14_lists_ide_workflows_smoke_and_e1_test_build():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    row = _step14_table_row(text)
    assert "build-le-vibe-ide.yml" in row
    assert "build-linux.yml" in row
    assert "test_build_le_vibe_ide_workflow_contract.py" in row
    assert "linux_compile" in row
    assert "ci-vscodium-bash-syntax.sh" in row
    assert "ci-editor-nvmrc-sync.sh" in row
    assert "ci-vscodium-linux-dev-build.sh" in row
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in row
    assert "fail fast" in row
    assert "vscodium-linux-build.tar.gz" in row
    assert "le_vibe_editor_docs" in row
    assert "LE_VIBE_EDITOR" in row
    assert "ide-ci-metadata" in row
    assert "./editor/smoke.sh" in row
    assert "14.g" in row
    assert "test_launcher_default_editor.py" in row
    assert "test_editor_readme_launcher_order_14g_contract.py" in row
    assert "test_debian_readme_launcher_order_14g_contract.py" in row
    assert "test_editor_build_md_contract.py" in row
    assert "test_spec_phase2_section14_snapshot_contract.py" in row
    assert "test_editor_readme_step14_contract.py" in row
    assert "test_editor_vendoring_md_contract.py" in row


def test_pm_stage_map_notes_step14_fine_grain_closure_and_remaining_gap():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    assert "14.a" in text and "14.j" in text
    assert "CHANGELOG.md" in text
    assert "spec-phase2.md" in text
    assert "linux_compile" in text
    assert ".zip" in text
    assert "test_spec_phase2_section14_snapshot_contract.py" in text
    assert "branding-staging.checklist.md" in text
    assert "ci-editor-gate" in text
