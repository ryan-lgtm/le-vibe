"""STEP 9: ``lvibe pip-audit``."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from le_vibe import launcher


def test_pip_audit_missing_requirements_exits_1(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(
        "le_vibe.supply_chain_check.requirements_txt_path",
        lambda: tmp_path / "missing-requirements.txt",
    )
    monkeypatch.setattr(sys, "argv", ["launcher", "pip-audit"])
    assert launcher.main() == 1
    err = capsys.readouterr().err
    assert "sbom-signing-audit.md" in err


def test_pip_audit_no_tool_exits_127(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    req = tmp_path / "requirements.txt"
    req.write_text("pytest==1.0.0\n", encoding="utf-8")
    monkeypatch.setattr(
        "le_vibe.supply_chain_check.requirements_txt_path",
        lambda: req,
    )
    monkeypatch.setattr(
        "le_vibe.supply_chain_check.shutil.which",
        lambda name: None if name == "pip-audit" else "/usr/bin/true",
    )
    monkeypatch.setattr(sys, "argv", ["launcher", "pip-audit"])
    assert launcher.main() == 127
    assert "pip-audit not on PATH" in capsys.readouterr().err
