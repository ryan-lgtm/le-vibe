"""STEP 9 / H2: ``supply_chain_check`` paths."""

from __future__ import annotations

import subprocess

import pytest

from le_vibe.supply_chain_check import requirements_txt_path, run_pip_audit_captured


def test_requirements_txt_path_in_git_clone():
    p = requirements_txt_path()
    assert p.name == "requirements.txt"
    assert p.is_file(), f"expected {p} in repository checkout"
    assert (p.parent / "le_vibe").is_dir()


def test_run_pip_audit_captured_invokes_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[list[str], dict]] = []

    def fake_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append((cmd, kwargs))
        return subprocess.CompletedProcess(cmd, 0, stdout="ok\n", stderr="")

    monkeypatch.setattr("le_vibe.supply_chain_check.subprocess.run", fake_run)
    rc, out, err = run_pip_audit_captured(["--format", "json"])
    assert rc == 0
    assert out == "ok\n"
    assert err == ""
    assert len(calls) == 1
    assert calls[0][1].get("capture_output") is True
    assert calls[0][1].get("text") is True
    req = requirements_txt_path()
    assert calls[0][0][:3] == ["pip-audit", "-r", str(req)]
    assert calls[0][0][3:] == ["--format", "json"]
