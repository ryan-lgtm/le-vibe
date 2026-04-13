"""STEP 10 / H3: monorepo discovery for ci-smoke / ci-editor-gate."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from le_vibe.qa_scripts import (
    EDITOR_GATE_REL,
    SMOKE_REL,
    find_monorepo_root,
    run_ci_editor_gate_captured,
    run_ci_smoke_captured,
)


def test_find_monorepo_root_in_checkout():
    root = find_monorepo_root()
    assert root is not None
    assert (root / SMOKE_REL).is_file()


def test_le_vibe_repo_root_overrides(monkeypatch, tmp_path: Path):
    fake = tmp_path / "fake"
    fake.mkdir()
    (fake / "packaging" / "scripts").mkdir(parents=True)
    (fake / "packaging" / "scripts" / "ci-smoke.sh").write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_REPO_ROOT", str(fake))
    assert find_monorepo_root() == fake.resolve()


def test_run_ci_smoke_captured_invokes_bash_with_capture(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    fake = tmp_path / "fake"
    fake.mkdir()
    (fake / "packaging" / "scripts").mkdir(parents=True)
    (fake / "packaging" / "scripts" / "ci-smoke.sh").write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_REPO_ROOT", str(fake))
    calls: list[tuple[list[str], dict]] = []

    def fake_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append((cmd, kwargs))
        return subprocess.CompletedProcess(cmd, 0, stdout="x\n", stderr="y\n")

    monkeypatch.setattr("le_vibe.qa_scripts.subprocess.run", fake_run)
    rc, out, err = run_ci_smoke_captured(["--help"])
    assert rc == 0
    assert out == "x\n"
    assert err == "y\n"
    assert len(calls) == 1
    assert calls[0][1].get("capture_output") is True
    root = fake.resolve()
    assert calls[0][0][:3] == ["bash", str(root / SMOKE_REL), "--help"]


def test_run_ci_editor_gate_captured_invokes_bash_with_capture(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    fake = tmp_path / "fake_editor"
    fake.mkdir()
    (fake / "packaging" / "scripts").mkdir(parents=True)
    (fake / "packaging" / "scripts" / "ci-smoke.sh").write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
    (fake / "packaging" / "scripts" / "ci-editor-gate.sh").write_text("#!/bin/sh\necho gate\n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_REPO_ROOT", str(fake))
    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 2, stdout="", stderr="bad")

    monkeypatch.setattr("le_vibe.qa_scripts.subprocess.run", fake_run)
    rc, out, err = run_ci_editor_gate_captured([])
    assert rc == 2
    assert out == ""
    assert err == "bad"
    root = fake.resolve()
    assert calls[0][:3] == ["bash", str(root / EDITOR_GATE_REL)]

