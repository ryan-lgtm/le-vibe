"""Contract: manual-step14-install-smoke.sh documents manual §7.3 Ubuntu validation."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_manual_step14_install_smoke_script_exists_and_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "manual-step14-install-smoke.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_manual_step14_install_smoke_script_documents_install_and_verify() -> None:
    text = (_repo_root() / "packaging" / "scripts" / "manual-step14-install-smoke.sh").read_text(
        encoding="utf-8"
    )
    assert "STEP 14" in text
    assert "--verify-only" in text
    assert "sudo apt install" in text
    assert "lvibe --help" in text
    assert "codium --version" in text
    assert "/usr/share/applications/le-vibe.desktop" in text
    assert "/usr/share/doc/le-vibe/README.Debian" in text
    assert "lvibe open-welcome" in text
    assert "build artifacts first" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text


def test_pm_deb_build_iteration_points_to_manual_step14_install_smoke_script() -> None:
    text = (_repo_root() / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "manual-step14-install-smoke.sh" in text


def test_manual_step14_install_smoke_missing_artifacts_prints_recovery_commands() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "manual-step14-install-smoke.sh"
    result = subprocess.run(
        [str(script)],
        cwd=str(root),
        capture_output=True,
        text=True,
        env={
            "PATH": str(Path("/usr/bin")) + ":" + str(Path("/bin")),
            "STACK_DEB": "/definitely/missing/stack.deb",
            "IDE_DEB": "/definitely/missing/ide.deb",
        },
    )
    assert result.returncode == 2
    err = result.stderr
    assert "missing stack deb" in err
    assert "build artifacts first" in err
    assert "build-le-vibe-debs.sh --with-ide" in err
    assert "verify-step14-closeout.sh --require-stack-deb" in err
