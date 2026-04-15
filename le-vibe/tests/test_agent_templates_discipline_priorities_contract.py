"""Canonical skill templates include discipline priorities per docs/PRODUCT_SPEC.md *Prioritization*."""

from __future__ import annotations

from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_TEMPLATES = _REPO_ROOT / "le-vibe" / "templates" / "agents"

# Roster: le-vibe/templates/agents/README.md *Canonical SaaS role roster*
_CANONICAL = (
    "subject-matter-industry-expert.md",
    "senior-product-operations.md",
    "senior-product-management.md",
    "senior-backend-engineer.md",
    "senior-frontend-engineer.md",
    "senior-devops-engineer.md",
    "senior-marketing.md",
    "senior-customer-success.md",
    "senior-revenue.md",
)

_SECTION = "## Discipline priorities (top 3–5)"


@pytest.mark.parametrize("name", _CANONICAL)
def test_canonical_agent_has_discipline_priorities_section(name: str) -> None:
    path = _TEMPLATES / name
    text = path.read_text(encoding="utf-8")
    assert _SECTION in text, f"{name}: missing {_SECTION}"
    after = text.split(_SECTION, 1)[1]
    block = after.split("## ", 1)[0]
    bullets = [ln for ln in block.splitlines() if ln.strip().startswith("- ")]
    assert len(bullets) >= 3, f"{name}: expected at least 3 priority bullets, got {len(bullets)}"


def test_canonical_roster_count_matches_parameterized_list() -> None:
    assert len(_CANONICAL) == 9
