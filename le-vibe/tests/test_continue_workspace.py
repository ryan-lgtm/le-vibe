"""Continue workspace rules (`.continue/rules`) point agents at `.lvibe/`."""

from __future__ import annotations

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
    assert "session-manifest.json" in mem
    assert "Doc-first staging" in mem
    assert "PM_STAGE_MAP.md" in mem
    assert "Please continue" in mem
    assert "AI Pilot" in mem
    assert "USER RESPONSE REQUIRED" in mem
    assert "numbered questions" in mem
    welcome = (tmp_path / ".continue" / "rules" / PRODUCT_WELCOME_RULE_NAME).read_text(encoding="utf-8")
    assert "Welcome to Lé Vibe" in welcome
    assert "Cursor" in welcome
    assert ensure_continue_lvibe_rules(tmp_path) == []


def test_workspace_prepare_writes_continue_rules_and_welcome(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    assert (tmp_path / ".continue" / "rules" / LVIBE_CONTINUE_RULE_NAME).is_file()
    assert (tmp_path / ".continue" / "rules" / PRODUCT_WELCOME_RULE_NAME).is_file()
    assert (tmp_path / ".lvibe" / "WELCOME.md").is_file()
    assert "Welcome to Lé Vibe" in (tmp_path / ".lvibe" / "WELCOME.md").read_text(encoding="utf-8")
