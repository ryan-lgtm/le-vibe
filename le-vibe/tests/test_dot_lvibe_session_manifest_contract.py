"""Dogfood: repository ``.lvibe/session-manifest.json`` matches session-manifest.v1 minimal shape."""

from __future__ import annotations

import json
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_dot_lvibe_session_manifest_minimal_shape() -> None:
    sm = _repo_root() / ".lvibe" / "session-manifest.json"
    data = json.loads(sm.read_text(encoding="utf-8"))
    assert data.get("schema_version") == "session-manifest.v1"
    assert isinstance(data.get("meta"), dict)
    assert isinstance(data.get("session_steps"), list)
    assert isinstance(data.get("agents"), dict)
    assert isinstance(data.get("product"), dict)
    meta = data["meta"]
    assert "continue_construction_note" in meta
    assert "ai_pilot_note" in meta


def test_dot_lvibe_session_manifest_has_product_milestones_epics_and_agent_roles() -> None:
    sm = _repo_root() / ".lvibe" / "session-manifest.json"
    data = json.loads(sm.read_text(encoding="utf-8"))
    product = data["product"]
    assert isinstance(product.get("milestones"), list)
    assert len(product["milestones"]) >= 1
    assert isinstance(product.get("epics"), list)
    assert len(product["epics"]) >= 1
    for epic in product["epics"]:
        assert isinstance(epic.get("id"), str) and epic["id"]
        assert isinstance(epic.get("tasks"), list)
    roles = data["agents"].get("roles")
    assert isinstance(roles, list)
    assert len(roles) >= 1
    for r in roles:
        assert isinstance(r, dict)
        assert "skill_path" in r
        assert str(r["skill_path"]).startswith(".lvibe/agents/")


def test_dot_lvibe_session_manifest_has_engineer_completion_protocol() -> None:
    sm = _repo_root() / ".lvibe" / "session-manifest.json"
    data = json.loads(sm.read_text(encoding="utf-8"))
    defaults = data["agents"]["defaults"]
    protocol = defaults.get("engineer_completion_protocol")
    assert isinstance(protocol, list)
    assert len(protocol) >= 3
    text = " ".join(str(item) for item in protocol)
    assert "clean" in text.lower()
    assert "commit" in text.lower()
    assert "push" in text.lower()
