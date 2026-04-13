"""STEP 9: ``lvibe pip-audit``."""

from __future__ import annotations

import json
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


def test_pip_audit_missing_requirements_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    missing = tmp_path / "missing-requirements.txt"
    monkeypatch.setattr(
        "le_vibe.supply_chain_check.requirements_txt_path",
        lambda: missing,
    )
    monkeypatch.setattr(sys, "argv", ["launcher", "pip-audit", "--json"])
    assert launcher.main() == 1
    data = json.loads(capsys.readouterr().out)
    assert data["error"] == "requirements_txt_missing"
    assert str(missing) in data["requirements_path"]


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


def test_pip_audit_no_tool_json(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
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
    monkeypatch.setattr(sys, "argv", ["launcher", "pip-audit", "--json"])
    assert launcher.main() == 127
    data = json.loads(capsys.readouterr().out)
    assert data["error"] == "pip_audit_not_on_path"


def test_pip_audit_json_ok(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    req = tmp_path / "requirements.txt"
    req.write_text("pytest==1.0.0\n", encoding="utf-8")
    monkeypatch.setattr("le_vibe.supply_chain_check.requirements_txt_path", lambda: req)
    monkeypatch.setattr(
        "le_vibe.supply_chain_check.shutil.which",
        lambda name: "/usr/bin/pip-audit" if name == "pip-audit" else "/usr/bin/true",
    )
    monkeypatch.setattr(
        "le_vibe.supply_chain_check.run_pip_audit_captured",
        lambda extra: (0, "no issues\n", ""),
    )
    monkeypatch.setattr(sys, "argv", ["launcher", "pip-audit", "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is True
    assert data["exit_code"] == 0
    assert str(req) == data["requirements_path"]


def test_pip_audit_json_forwards_extra_args(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    req = tmp_path / "requirements.txt"
    req.write_text("pytest==1.0.0\n", encoding="utf-8")
    monkeypatch.setattr("le_vibe.supply_chain_check.requirements_txt_path", lambda: req)
    monkeypatch.setattr(
        "le_vibe.supply_chain_check.shutil.which",
        lambda name: "/usr/bin/pip-audit" if name == "pip-audit" else "/usr/bin/true",
    )
    captured: list[list[str]] = []

    def fake(extra: list[str]) -> tuple[int, str, str]:
        captured.append(extra)
        return 3, "", "vuln"

    monkeypatch.setattr("le_vibe.supply_chain_check.run_pip_audit_captured", fake)
    monkeypatch.setattr(sys, "argv", ["launcher", "pip-audit", "--json", "--format", "json"])
    assert launcher.main() == 3
    data = json.loads(capsys.readouterr().out)
    assert data["pip_audit_extra_args"] == ["--format", "json"]
    assert data["ok"] is False
    assert captured == [["--format", "json"]]
