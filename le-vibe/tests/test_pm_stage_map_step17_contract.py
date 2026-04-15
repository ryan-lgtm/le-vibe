"""Contract: docs/PM_STAGE_MAP.md STEP 17 row + AI_PILOT doc opener (STEP 17)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_pm_stage_map_step17_row_lists_continue_readme_and_e1():
    text = (_repo_root() / "docs" / "PM_STAGE_MAP.md").read_text(encoding="utf-8")
    rows = [ln for ln in text.splitlines() if "| **17** — AI Pilot" in ln]
    assert len(rows) == 1
    row = rows[0]
    assert "AI_PILOT_AND_CONTINUE.md" in row
    assert "PRODUCT_SPEC.md" in row
    assert "continue_workspace.py" in row
    assert "test_root_readme_ai_pilot_contract.py" in row
    assert "test_privacy_and_ai_pilot_prioritization_cargo_contract.py" in row
    assert "test_pm_stage_map_step17_contract.py" in row
    assert "STEP 17" in row


def test_ai_pilot_continue_doc_opener_step17_and_e1():
    text = (_repo_root() / "docs" / "AI_PILOT_AND_CONTINUE.md").read_text(encoding="utf-8")
    head = "\n".join(text.splitlines()[:12])
    assert "STEP 17" in head
    assert "PM_STAGE_MAP" in head
    assert "continue_workspace.py" in head
    assert "test_root_readme_ai_pilot_contract.py" in head
    assert "test_pm_stage_map_step17_contract.py" in head


def test_ai_pilot_continue_doc_guards_and_evidence_table_step17():
    """§3.1 user gate + §4 roster — PRODUCT_SPEC §7.2, E1 evidence, SECURITY / privacy."""
    text = (_repo_root() / "docs" / "AI_PILOT_AND_CONTINUE.md").read_text(encoding="utf-8")
    assert "USER RESPONSE REQUIRED" in text
    assert "§7.2" in text
    assert "## 4. Relationship to other docs" in text
    assert "SESSION_ORCHESTRATION_SPEC.md" in text
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE.md" in text
    assert "privacy-and-telemetry.md" in text
    assert "SECURITY.md" in text


def test_ai_pilot_continue_doc_canonical_roster_cites_product_spec_section9_and_authority_siblings():
    """**Canonical roster** — PRODUCT_SPEC §9 table + PROMPT_BUILD / SESSION_ORCHESTRATION / PM map / SECTION8 evidence."""
    text = (_repo_root() / "docs" / "AI_PILOT_AND_CONTINUE.md").read_text(encoding="utf-8")
    roster = text.split("**Canonical roster:**", 1)[1].split("**`.deb`", 1)[0]
    assert "§9" in roster
    assert "PROMPT_BUILD_LE_VIBE" in roster
    assert "SESSION_ORCHESTRATION_SPEC" in roster
    assert "PM_STAGE_MAP" in roster
    assert "PRODUCT_SPEC_SECTION8_EVIDENCE" in roster


def test_ai_pilot_continue_ai_pilot_section_locks_visible_multi_agent_observability():
    """Prioritization mirror: AI Pilot keeps visible coordination (live-watching style intent)."""
    text = (_repo_root() / "docs" / "AI_PILOT_AND_CONTINUE.md").read_text(encoding="utf-8")
    section = text.split("## 2. **AI Pilot**", 1)[1].split("## 3. Intelligent", 1)[0]
    assert "near–real time" in section
    assert "user can **witness** multi-agent style negotiation" in section
    assert "not a black box" in section
