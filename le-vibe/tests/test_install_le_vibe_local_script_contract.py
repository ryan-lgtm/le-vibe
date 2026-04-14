"""packaging/scripts/install-le-vibe-local.sh — canonical local full-product orchestrator (STEP 14 / §7.3)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_install_le_vibe_local_script_exists_bash_syntax_executable():
    script = _root() / "packaging" / "scripts" / "install-le-vibe-local.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_install_le_vibe_local_script_header_step14_contracts():
    text = (_root() / "packaging" / "scripts" / "install-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "verify-step14-closeout.sh" in text
    assert "build-le-vibe-debs.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "manual-step14-install-smoke.sh" in text
    assert "test_install_le_vibe_local_script_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text


def test_install_le_vibe_local_script_asserts_deb_artifacts_when_install():
    text = (_root() / "packaging" / "scripts" / "install-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "Explicit artifact gate" in text or "artifact gate" in text.lower()
    assert "stack package .deb missing" in text
    assert "IDE package .deb missing" in text


def test_install_le_vibe_local_usage_documents_flags_and_exit_codes():
    text = (_root() / "packaging" / "scripts" / "install-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "--preflight-only" in text
    assert "LOCAL_INSTALL_ONE_SHOT.md" in text
    assert "--install" in text and "--yes" in text
    assert "--force-editor-build" in text
    assert "--skip-editor-build" in text
    assert "--skip-compile-failfast" in text
    assert "--json" in text
    assert "--apt-sim" in text
    assert "--skip-gate" in text
    assert "--log-file" in text
    assert "Exit codes:" in text
    assert "install-le-vibe-local.sh --install --yes" in text
    assert "mutually exclusive" in text


def test_install_le_vibe_local_mutually_exclusive_flags_exit_2():
    r = subprocess.run(
        [
            "bash",
            str(_root() / "packaging" / "scripts" / "install-le-vibe-local.sh"),
            "--skip-editor-build",
            "--force-editor-build",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2
    assert "mutually exclusive" in (r.stderr or "")


def test_pm_deb_build_iteration_doc_lists_install_le_vibe_local_invocation():
    text = (_root() / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "install-le-vibe-local.sh" in text
    assert "Local install from source" in text or "canonical local" in text.lower()


def test_editor_build_md_lists_canonical_local_installer():
    text = (_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "install-le-vibe-local.sh" in text


def test_root_readme_mentions_canonical_local_install_path():
    text = (_root() / "README.md").read_text(encoding="utf-8")
    assert "install-le-vibe-local.sh" in text
    assert "LOCAL_INSTALL_ONE_SHOT.md" in text
    assert "SHIP_REPORT_LOCAL_INSTALL.md" in text
    assert "Full local install (one command)" in text


def test_local_install_one_shot_doc_exists():
    p = _root() / "docs" / "LOCAL_INSTALL_ONE_SHOT.md"
    assert p.is_file()
    t = p.read_text(encoding="utf-8")
    assert "install-le-vibe-local.sh" in t
    assert "verify-step14-closeout.sh" in t


def test_ship_report_local_install_doc_exists():
    p = _root() / "docs" / "SHIP_REPORT_LOCAL_INSTALL.md"
    assert p.is_file()
    assert "SHIPPED" in p.read_text(encoding="utf-8")
