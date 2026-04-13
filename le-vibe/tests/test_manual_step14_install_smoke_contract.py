"""Contract: manual-step14-install-smoke.sh documents manual §7.3 Ubuntu validation."""

from __future__ import annotations

import json
import subprocess
import tempfile
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
    assert "--print-install-cmd" in text
    assert "--json" in text
    assert "sudo apt install" in text
    assert "lvibe --help" in text
    assert "codium --version" in text
    assert "/usr/share/applications/le-vibe.desktop" in text
    assert "/usr/share/doc/le-vibe/README.Debian" in text
    assert "lvibe open-welcome" in text
    assert "build artifacts first" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "apt_sim_note" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "build machine" in text
    assert "test host" in text
    assert "docs/apt-repo-releases.md" in text
    assert "Partial VSCode-linux tree" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "build-le-vibe-ide-deb.sh --help" in text
    assert "beside clone" in text
    assert "repo root" in text
    assert "resolve-latest-le-vibe-stack-deb.sh" in text


def test_session_manifest_step14_closeout_rag_notes_mentions_closeout_json() -> None:
    path = _repo_root() / "schemas" / "session-manifest.step14-closeout.v1.example.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    rag = payload["meta"]["rag_notes"]
    assert "verify-step14-closeout.sh --require-stack-deb" in rag
    assert "apt_sim_note" in rag
    assert "print-built-codium-path" in rag
    assert "print-vsbuild-codium-path" in rag
    assert "build-le-vibe-ide-deb.sh --help" in rag
    assert "Partial VSCode-linux" in rag
    assert "H1 vs §7.3 .deb bundles" in rag
    assert "packaging/scripts/ci-vscodium-bash-syntax.sh" in rag
    assert "packaging/scripts/ci-editor-nvmrc-sync.sh" in rag
    assert "packaging/scripts/ci-vscodium-linux-dev-build.sh" in rag
    assert "manual-step14-install-smoke.sh default STACK_DEB" in rag
    assert "resolve-latest-le-vibe-stack-deb.sh" in rag
    assert "Output paths (from repo root)" in rag


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
    assert "apt_sim_note" in err


def test_manual_step14_install_smoke_print_install_cmd_mode() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "manual-step14-install-smoke.sh"
    result = subprocess.run(
        [str(script), "--print-install-cmd"],
        cwd=str(root),
        capture_output=True,
        text=True,
        env={
            "PATH": str(Path("/usr/bin")) + ":" + str(Path("/bin")),
            "STACK_DEB": "/tmp/le-vibe_1.2.3_all.deb",
            "IDE_DEB": "/tmp/le-vibe-ide_1.2.3_amd64.deb",
        },
    )
    assert result.returncode == 2
    assert "build artifacts first" in result.stderr

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        stack = tmp_root / "le-vibe_1.2.3_all.deb"
        ide = tmp_root / "le-vibe-ide_1.2.3_amd64.deb"
        stack.write_bytes(b"placeholder")
        ide.write_bytes(b"placeholder")
        ok = subprocess.run(
            [str(script), "--print-install-cmd"],
            cwd=str(root),
            capture_output=True,
            text=True,
            env={
                "PATH": str(Path("/usr/bin")) + ":" + str(Path("/bin")),
                "STACK_DEB": str(stack),
                "IDE_DEB": str(ide),
            },
        )
        assert ok.returncode == 0
        assert ok.stdout.strip() == f'sudo apt install "{stack}" "{ide}"'


def test_manual_step14_install_smoke_json_mode() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "manual-step14-install-smoke.sh"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        stack = tmp_root / "le-vibe_9.9.9_all.deb"
        ide = tmp_root / "le-vibe-ide_9.9.9_amd64.deb"
        stack.write_bytes(b"placeholder")
        ide.write_bytes(b"placeholder")
        result = subprocess.run(
            [str(script), "--json"],
            cwd=str(root),
            capture_output=True,
            text=True,
            env={
                "PATH": str(Path("/usr/bin")) + ":" + str(Path("/bin")),
                "STACK_DEB": str(stack),
                "IDE_DEB": str(ide),
            },
        )
        assert result.returncode == 0
        payload = json.loads(result.stdout)
        assert payload["stack_deb"] == str(stack)
        assert payload["ide_deb"] == str(ide)
        assert payload["install_cmd"] == f'sudo apt install "{stack}" "{ide}"'


def test_manual_step14_install_smoke_json_mode_escapes_special_chars() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "manual-step14-install-smoke.sh"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        stack_dir = tmp_root / 'dir-with-"quotes"'
        stack_dir.mkdir()
        ide_dir = tmp_root / "dir-with-\\slashes"
        ide_dir.mkdir()
        stack = stack_dir / "le-vibe_9.9.9_all.deb"
        ide = ide_dir / "le-vibe-ide_9.9.9_amd64.deb"
        stack.write_bytes(b"placeholder")
        ide.write_bytes(b"placeholder")
        result = subprocess.run(
            [str(script), "--json"],
            cwd=str(root),
            capture_output=True,
            text=True,
            env={
                "PATH": str(Path("/usr/bin")) + ":" + str(Path("/bin")),
                "STACK_DEB": str(stack),
                "IDE_DEB": str(ide),
            },
        )
        assert result.returncode == 0
        payload = json.loads(result.stdout)
        assert payload["stack_deb"] == str(stack)
        assert payload["ide_deb"] == str(ide)
