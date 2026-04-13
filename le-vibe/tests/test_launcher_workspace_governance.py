"""STEP 15: ``lvibe workspace-governance``."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from le_vibe import launcher


def test_workspace_governance_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(tmp_path), "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["workspace_root"] == str(tmp_path.resolve())
    assert data["consent"] is None
    assert data["cap_mb_effective"] >= 10
    assert data["usage_bytes"] == 0
    assert data["within_cap"] is True
    assert "policy_file" in data


def test_workspace_governance_human(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "workspace-governance", "-C", str(tmp_path)])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "STEP 15" in out
    assert "Consent:" in out
    assert str(tmp_path.resolve()) in out
