"""STEP 14: ``lvibe ide-prereqs``."""

from __future__ import annotations

import json
import sys

import pytest

from le_vibe import launcher


def test_ide_prereqs_path_only_branding(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs", "--path-only", "branding"])
    assert launcher.main() == 0
    out = capsys.readouterr().out.strip()
    assert out.endswith("product-branding-merge.json")


def test_ide_prereqs_path_only_vscode_missing(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(
        "le_vibe.ide_packaging_paths.vscode_linux_build_status",
        lambda _root: ("absent", None),
    )
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs", "--path-only", "vscode"])
    rc = launcher.main()
    assert rc == 1
    err = capsys.readouterr().err
    assert "VSCode-linux" in err
    assert "Partial" not in err


def test_ide_prereqs_path_only_vscode_partial(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(
        "le_vibe.ide_packaging_paths.vscode_linux_build_status",
        lambda _root: ("partial", None),
    )
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs", "--path-only", "vscode"])
    assert launcher.main() == 1
    err = capsys.readouterr().err
    assert "Partial VSCode-linux tree present" in err
    assert "Partial tree" in err


def test_ide_prereqs_unknown_key(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs", "--path-only", "nope"])
    assert launcher.main() == 2
    assert "unknown key" in capsys.readouterr().err


def test_ide_prereqs_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs"])
    assert launcher.main() == 1
    assert "PM_STAGE_MAP" in capsys.readouterr().err


def test_ide_prereqs_json_in_checkout(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs", "--json"])
    assert launcher.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["monorepo_root"]
    assert "vscode_linux_ready" in data
    assert data["vscode_linux_partial"] == (
        (not data["vscode_linux_ready"]) and data["vscode_linux_path"] is not None
    )
    assert "static_prereq_files_ok" in data
    assert data["static_prereq_files_ok"] is True
    assert "vscodium_linux_svg_staged" in data
    assert len(data["entries"]) == 9
    assert all("label" in e and "path" in e and "exists" in e for e in data["entries"])


def test_ide_prereqs_json_no_monorepo(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("le_vibe.qa_scripts.find_monorepo_root", lambda: None)
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs", "--json"])
    assert launcher.main() == 1
    data = json.loads(capsys.readouterr().out)
    assert data["error"] == "monorepo_not_found"


def test_ide_prereqs_print_closeout_commands(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs", "--print-closeout-commands"])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "preflight-step14-closeout.sh" in out
    assert "verify-step14-closeout.sh" in out
    assert "PM_DEB_BUILD_ITERATION.md" in out


def test_ide_prereqs_print_closeout_partial_hint(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    fake = object()

    def _fake_status(_root: object) -> tuple[str, object]:
        return "partial", fake

    monkeypatch.setattr("le_vibe.ide_packaging_paths.vscode_linux_build_status", _fake_status)
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs", "--print-closeout-commands"])
    assert launcher.main() == 0
    out = capsys.readouterr().out
    assert "partial build" in out
    assert "Partial tree" in out
    assert "./editor/use-node-toolchain.sh" in out
    assert "./editor/fetch-vscode-sources.sh" in out
    assert "(cd editor/vscodium && ./dev/build.sh)" in out


def test_ide_prereqs_path_only_json_rejected(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["launcher", "ide-prereqs", "--path-only", "branding", "--json"])
    with pytest.raises(SystemExit) as exc:
        launcher.main()
    assert exc.value.code == 2
    err = capsys.readouterr().err.lower()
    assert "not allowed" in err or "path-only" in err
