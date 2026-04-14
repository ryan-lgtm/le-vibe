"""Continue workspace rules (`.continue/rules`) point agents at `.lvibe/`."""

from __future__ import annotations

import subprocess
from pathlib import Path

from le_vibe.continue_workspace import (
    LVIBE_CONTINUE_RULE_NAME,
    PRODUCT_WELCOME_RULE_NAME,
    ensure_continue_lvibe_rules,
)
from le_vibe.workspace_hub import ensure_lvibe_workspace


def test_ensure_continue_rules_idempotent(tmp_path: Path):
    created = ensure_continue_lvibe_rules(tmp_path)
    assert len(created) == 2
    assert {p.name for p in created} == {LVIBE_CONTINUE_RULE_NAME, PRODUCT_WELCOME_RULE_NAME}
    mem = (tmp_path / ".continue" / "rules" / LVIBE_CONTINUE_RULE_NAME).read_text(encoding="utf-8")
    assert ".lvibe/session-manifest.json" in mem
    assert "session-manifest.json" in mem
    assert "session_manifest_example_source_path" in mem
    assert "schemas/session-manifest.v1.example.json" in mem
    assert "iter_tasks_in_epic_order" in mem
    assert "le-vibe/templates/agents" in mem
    assert "lvibe sync-agent-skills" in mem
    assert "sync-lvibe-agent-skills.sh" in mem
    assert "Doc-first staging" in mem
    assert "PM_STAGE_MAP.md" in mem
    assert "Please continue" in mem
    assert "AI Pilot" in mem
    assert "USER RESPONSE REQUIRED" in mem
    assert "numbered questions" in mem
    assert "Use this canonical output shape" in mem
    assert "1: ..." in mem
    assert "2: ..." in mem
    assert "reply by number" in mem
    assert "Deterministic recall order" in mem
    assert "**Deterministic recall order (token-efficient):**" in mem
    assert ".lvibe/session-manifest.json" in mem
    assert ".lvibe/rag/refs/" in mem
    assert "Avoid broad `.lvibe/**` rescans" in mem
    i1 = mem.index("1. `.lvibe/session-manifest.json`")
    i2 = mem.index("2. `.lvibe/memory/incremental.md` tail and `.lvibe/memory/workspace-scan.md` when present")
    i3 = mem.index("3. `.lvibe/rag/refs/` small refs for path-specific evidence")
    i4 = mem.index("4. `.lvibe/agents/<agent_id>/skill.md` only for the roles needed this turn")
    assert i1 < i2 < i3 < i4
    recall_section = mem.split("**Deterministic recall order (token-efficient):**", 1)[1].split(
        "Avoid broad `.lvibe/**` rescans",
        1,
    )[0]
    recall_lines = [
        line.strip()
        for line in recall_section.splitlines()
        if line.strip().startswith(("1. ", "2. ", "3. ", "4. "))
    ]
    assert recall_lines == [
        "1. `.lvibe/session-manifest.json` (current step + active epic/task)",
        "2. `.lvibe/memory/incremental.md` tail and `.lvibe/memory/workspace-scan.md` when present",
        "3. `.lvibe/rag/refs/` small refs for path-specific evidence",
        "4. `.lvibe/agents/<agent_id>/skill.md` only for the roles needed this turn",
    ]
    assert "/setup-workspace" in mem
    assert ".workspace-context-seeded" in mem
    assert "workflows/setup-workspace.md" in mem
    assert "/agent" in mem
    welcome = (tmp_path / ".continue" / "rules" / PRODUCT_WELCOME_RULE_NAME).read_text(encoding="utf-8")
    assert "Welcome to Lé Vibe" in welcome
    assert "Chat/Agent" in welcome
    assert "Quick Open" in welcome
    assert "Ctrl+P" in welcome or "Cmd+P" in welcome
    assert ".lvibe/WELCOME.md" in welcome
    assert ensure_continue_lvibe_rules(tmp_path) == []


def test_sync_lvibe_agent_skills_script_syntax():
    root = Path(__file__).resolve().parents[2]
    script = root / "packaging" / "scripts" / "sync-lvibe-agent-skills.sh"
    assert script.is_file()
    subprocess.run(["bash", "-n", str(script)], check=True)


def test_sync_lvibe_agent_skills_requires_python3_documented():
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "sync-lvibe-agent-skills.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "python3 not on PATH" in text
    assert "SESSION_ORCHESTRATION_SPEC" in text
    assert "test_continue_workspace.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def test_workspace_prepare_writes_continue_rules_and_welcome(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    assert (tmp_path / ".continue" / "rules" / LVIBE_CONTINUE_RULE_NAME).is_file()
    assert (tmp_path / ".continue" / "rules" / PRODUCT_WELCOME_RULE_NAME).is_file()
    assert (tmp_path / ".lvibe" / "WELCOME.md").is_file()
    assert "Welcome to Lé Vibe" in (tmp_path / ".lvibe" / "WELCOME.md").read_text(encoding="utf-8")
