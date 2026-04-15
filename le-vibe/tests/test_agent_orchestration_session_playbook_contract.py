"""Contract: docs/AGENT_ORCHESTRATION_SESSION_PLAYBOOK.md — 70-task orchestration hardening backlog (le-vibe/README index)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_agent_orchestration_session_playbook_opener_principles_roster_and_backlog():
    text = (_repo_root() / "docs" / "AGENT_ORCHESTRATION_SESSION_PLAYBOOK.md").read_text(encoding="utf-8")
    assert "# Agent Orchestration Session Playbook" in text
    assert "Purpose: provide a repeatable, one-chat-per-task progression to harden orchestration" in text
    assert "Use this as a sequential backlog for 70 engineering chat sessions." in text
    assert "Each task is scoped so a Cursor engineering agent can complete it in one focused session." in text
    assert "## Working principles" in text
    assert "One session, one shippable increment" in text
    assert "Every session must end with updated tests or explicit test evidence." in text
    assert "Subagents must provide evidence, not opinions, when debating." in text
    assert "Disagreements resolve through documented decision records and scorecards." in text
    assert "Operator agent owns goals, constraints, and acceptance criteria." in text
    assert "## Canonical subagent roster" in text
    assert "## Canonical subagent roster (SaaS personas)" in text
    assert "@sme" in text
    assert "@props" in text
    assert "@prod" in text
    assert "@be-eng" in text
    assert "@fe-eng" in text
    assert "@do-eng" in text
    assert "@marketing" in text
    assert "@cs" in text
    assert "@rev" in text
    assert "## Session backlog (70 tasks)" in text
    assert "1. Define operator-to-subagent message envelope schema" in text
    assert "2. Define subagent-to-operator response schema (result, evidence, confidence, blockers, next action)." in text
    assert "### Phase 1 - Foundations and contracts (1-10)" in text
    assert "### Phase 2 - Subagent role specialization (11-20)" in text
    assert "### Phase 3 - Debate and argumentation loop (21-30)" in text
    assert "### Phase 4 - Cross-subagent communication (31-40)" in text
    assert "### Phase 5 - Prioritization and execution governance (41-50)" in text
    assert "### Phase 6 - Delivery controls and safety (51-60)" in text
    assert "### Phase 7 - Product-goal closure and milestone completion (61-70)" in text
    assert "Sessions 1-20: protocol and role contracts." in text
    assert "Sessions 21-40: debate + communication reliability." in text
    assert "Sessions 41-60: prioritization and safety controls." in text
    assert "Sessions 61-70: milestone closure logic and release readiness." in text
    assert "69. Add release-readiness summary generated from all session records." in text
    assert "70. Add tests proving stop condition stays false until product goals and final milestone are complete." in text
