"""Contract: verify-step14-closeout.sh checks local §7.3 artifacts (STEP 14)."""

from __future__ import annotations

import fcntl
import json
import os
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _artifact_lock_fd() -> int:
    lock_path = _repo_root() / "le-vibe" / ".pytest-verify-step14-contract.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    return os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)


def _unlock_artifact_lock(fd: int) -> None:
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)


def _run_with_step14_contract_artifact_lock(fn: Callable[[], None]) -> None:
    """Serialize tests that share placeholder packaging/*.deb and fake editor bin/codium (xdist-safe)."""
    fd = _artifact_lock_fd()
    fcntl.flock(fd, fcntl.LOCK_EX)
    try:
        fn()
    finally:
        _unlock_artifact_lock(fd)


def test_verify_step14_contract_flock_lock_path_is_gitignored() -> None:
    """fcntl lock for parallel-safe JSON contract tests — path must stay out of version control."""
    gi = (_repo_root() / ".gitignore").read_text(encoding="utf-8")
    assert "le-vibe/.pytest-verify-step14-contract.lock" in gi


def test_verify_step14_closeout_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "verify-step14-closeout.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_verify_step14_closeout_script_documents_required_artifacts() -> None:
    text = (_repo_root() / "packaging" / "scripts" / "verify-step14-closeout.sh").read_text(encoding="utf-8")
    assert "0 -> 1 -> 14 -> 2-13 -> 15-17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "ci-editor-gate.sh" in text
    assert "verify-14c-local-binary.sh" in text
    assert "STEP 14.c failed" in text
    assert "vscode_linux_build:" in text
    assert "vscode_linux_bin_files" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "trigger-le-vibe-ide-linux-compile.sh" in text
    assert "download-vscodium-linux-compile-artifact.sh" in text
    assert "no VSCode-linux tree" in text
    assert "probe-vscode-linux-build.sh" in text
    assert "preflight-step14-closeout.sh" in text
    assert "ide-prereqs --print-closeout-commands" in text
    assert "packaging/le-vibe-ide_*.deb" in text
    assert "--require-stack-deb" in text
    assert "--apt-sim" in text
    assert "--skip-gate" in text
    assert "--json" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "desktop content contains `Name=Lé Vibe`" in text
    assert "Exec=/usr/lib/le-vibe/bin/codium %F" in text
    assert "Package: le-vibe-ide" in text
    assert "Architecture: amd64" in text
    assert "Package: le-vibe" in text
    assert "Architecture: all" in text
    assert "pick_latest_match" in text
    assert "sort -V" in text
    assert 'ide deb: $ide_deb_latest' in text
    assert 'stack deb: $stack_deb_latest' in text
    assert "search repo parent then repo root" in text
    assert "resolve-latest-le-vibe-stack-deb.sh" in text
    assert "assert_deb_contains" in text
    assert "assert_deb_contains_any" in text
    assert "assert_deb_field_equals" in text
    assert "assert_deb_file_contains" in text
    assert "assert_deb_path_is_executable" in text
    assert "desktop-file-validate" in text
    assert "le-vibe-desk-verify" in text
    assert "assert_apt_simulated_install" in text
    assert "dpkg-deb --contents" in text
    assert "dpkg-deb --field" in text
    assert "dpkg-deb --fsys-tarfile" in text
    assert "./usr/share/applications/le-vibe.desktop" in text
    assert "./usr/lib/le-vibe/bin/codium" in text
    assert "Name=Lé Vibe" in text
    assert "Exec=/usr/lib/le-vibe/bin/codium %F" in text
    assert "./usr/bin/lvibe" in text
    assert "./usr/share/doc/le-vibe/README.Debian" in text
    assert "./usr/share/doc/le-vibe/README.Debian.gz" in text
    assert "Package=le-vibe-ide, Architecture=amd64" in text
    assert "Package=le-vibe, Architecture=all" in text
    assert "apt-get -s install" in text
    assert "apt-get -s output follows" in text
    assert "held/broken packages" in text
    assert "skipped (use --apt-sim)" in text
    assert '"status": "ok"' in text
    assert '"vscode_linux_build":' in text
    assert '"codium_path":' in text
    assert '"ide_deb":' in text
    assert '"apt_sim_note":' in text
    assert "desktop_file_validate" in text
    assert "JSON success (--json)" in text
    assert "requested_without_stack_requirement" in text
    assert "build machine" in text
    assert "test host" in text
    assert "manual-step14-install-smoke.sh" in text
    assert "docs/apt-repo-releases.md" in text
    assert "Partial VSCode-linux" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "print-built-codium-path.sh" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text


def _verify_step14_closeout_json_mode_outputs_parseable_payload_impl() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "verify-step14-closeout.sh"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        stub_dir = tmp_root / "bin"
        stub_dir.mkdir()
        packaging_dir = root / "packaging"
        stack_deb = root.parent / "le-vibe_9999.0.0_all.deb"
        ide_deb = packaging_dir / "le-vibe-ide_9999.0.0_amd64.deb"
        fake_codium = root / "editor" / "vscodium" / "VSCode-linux-x64" / "bin" / "codium"
        fake_codium.parent.mkdir(parents=True, exist_ok=True)
        fake_codium.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        os.chmod(fake_codium, 0o755)
        stack_deb.write_bytes(b"placeholder")
        ide_deb.write_bytes(b"placeholder")
        try:
            (stub_dir / "dpkg-deb").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
if [[ "$1" == "--contents" ]]; then
  cat <<'EOF'
-rwxr-xr-x root/root         0 2026-01-01 00:00 ./usr/lib/le-vibe/bin/codium
-rwxr-xr-x root/root         0 2026-01-01 00:00 ./usr/bin/lvibe
-rw-r--r-- root/root         0 2026-01-01 00:00 ./usr/share/applications/le-vibe.desktop
-rw-r--r-- root/root         0 2026-01-01 00:00 ./usr/share/doc/le-vibe/README.Debian
EOF
  exit 0
fi
if [[ "$1" == "--field" ]]; then
  deb_path="$2"
  field="$3"
  if [[ "$field" == "Package" ]]; then
    if [[ "$deb_path" == *"le-vibe-ide_"* ]]; then
      printf 'le-vibe-ide\\n'
    else
      printf 'le-vibe\\n'
    fi
    exit 0
  fi
  if [[ "$field" == "Architecture" ]]; then
    if [[ "$deb_path" == *"le-vibe-ide_"* ]]; then
      printf 'amd64\\n'
    else
      printf 'all\\n'
    fi
    exit 0
  fi
fi
if [[ "$1" == "--fsys-tarfile" ]]; then
  cat <<'EOF'
dummy-tar-stream
EOF
  exit 0
fi
echo "unexpected dpkg-deb args: $*" >&2
exit 1
""",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "dpkg-deb", 0o755)
            (stub_dir / "tar").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
cat <<'EOF'
[Desktop Entry]
Name=Lé Vibe
Exec=/usr/lib/le-vibe/bin/codium %F
EOF
""",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "tar", 0o755)
            (stub_dir / "desktop-file-validate").write_text(
                "#!/usr/bin/env bash\n# Contract stub: real validator may reject minimal fake .desktop.\nexit 0\n",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "desktop-file-validate", 0o755)
            result = subprocess.run(
                [str(script), "--skip-gate", "--require-stack-deb", "--json"],
                cwd=str(root),
                capture_output=True,
                text=True,
                env={
                    "PATH": str(stub_dir) + ":" + str(Path("/usr/bin")) + ":" + str(Path("/bin")),
                },
            )
            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            assert payload["status"] == "ok"
            assert payload["vscode_linux_build"] == "ready"
            assert payload["stack_deb_required"] is True
            assert payload["apt_sim_requested"] is False
            assert payload["apt_sim_ran"] is False
            assert payload["apt_sim_note"] == "not_requested"
            assert payload["desktop_file_validate"] == "ran"
            assert payload["ide_deb"].endswith("le-vibe-ide_9999.0.0_amd64.deb")
            assert payload["stack_deb"].endswith("le-vibe_9999.0.0_all.deb")
            assert payload["codium_path"].endswith("editor/vscodium/VSCode-linux-x64/bin/codium")
            assert "==> STEP 14 gate: skipped (--skip-gate)" in result.stderr
        finally:
            fake_codium.unlink(missing_ok=True)
            ide_deb.unlink(missing_ok=True)
            stack_deb.unlink(missing_ok=True)


def test_verify_step14_closeout_json_mode_outputs_parseable_payload() -> None:
    _run_with_step14_contract_artifact_lock(_verify_step14_closeout_json_mode_outputs_parseable_payload_impl)


def _verify_step14_closeout_json_mode_apt_sim_ran_with_stack_requirement_impl() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "verify-step14-closeout.sh"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        stub_dir = tmp_root / "bin"
        stub_dir.mkdir()
        packaging_dir = root / "packaging"
        stack_deb = root.parent / "le-vibe_9999.0.4_all.deb"
        ide_deb = packaging_dir / "le-vibe-ide_9999.0.4_amd64.deb"
        fake_codium = root / "editor" / "vscodium" / "VSCode-linux-x64" / "bin" / "codium"
        fake_codium.parent.mkdir(parents=True, exist_ok=True)
        fake_codium.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        os.chmod(fake_codium, 0o755)
        stack_deb.write_bytes(b"placeholder")
        ide_deb.write_bytes(b"placeholder")
        try:
            (stub_dir / "dpkg-deb").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
if [[ "$1" == "--contents" ]]; then
  cat <<'EOF'
-rwxr-xr-x root/root         0 2026-01-01 00:00 ./usr/lib/le-vibe/bin/codium
-rwxr-xr-x root/root         0 2026-01-01 00:00 ./usr/bin/lvibe
-rw-r--r-- root/root         0 2026-01-01 00:00 ./usr/share/applications/le-vibe.desktop
-rw-r--r-- root/root         0 2026-01-01 00:00 ./usr/share/doc/le-vibe/README.Debian
EOF
  exit 0
fi
if [[ "$1" == "--field" ]]; then
  deb_path="$2"
  field="$3"
  if [[ "$field" == "Package" ]]; then
    if [[ "$deb_path" == *"le-vibe-ide_"* ]]; then
      printf 'le-vibe-ide\\n'
    else
      printf 'le-vibe\\n'
    fi
    exit 0
  fi
  if [[ "$field" == "Architecture" ]]; then
    if [[ "$deb_path" == *"le-vibe-ide_"* ]]; then
      printf 'amd64\\n'
    else
      printf 'all\\n'
    fi
    exit 0
  fi
fi
if [[ "$1" == "--fsys-tarfile" ]]; then
  cat <<'EOF'
dummy-tar-stream
EOF
  exit 0
fi
echo "unexpected dpkg-deb args: $*" >&2
exit 1
""",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "dpkg-deb", 0o755)
            (stub_dir / "tar").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
cat <<'EOF'
[Desktop Entry]
Name=Lé Vibe
Exec=/usr/lib/le-vibe/bin/codium %F
EOF
""",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "tar", 0o755)
            (stub_dir / "desktop-file-validate").write_text(
                "#!/usr/bin/env bash\nexit 0\n",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "desktop-file-validate", 0o755)
            (stub_dir / "apt-get").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
if [[ "$1" == "-s" && "$2" == "install" ]]; then
  exit 0
fi
echo "unexpected apt-get args: $*" >&2
exit 1
""",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "apt-get", 0o755)
            result = subprocess.run(
                [str(script), "--skip-gate", "--require-stack-deb", "--apt-sim", "--json"],
                cwd=str(root),
                capture_output=True,
                text=True,
                env={
                    "PATH": str(stub_dir) + ":" + str(Path("/usr/bin")) + ":" + str(Path("/bin")),
                },
            )
            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            assert payload["status"] == "ok"
            assert payload["vscode_linux_build"] == "ready"
            assert payload["stack_deb_required"] is True
            assert payload["apt_sim_requested"] is True
            assert payload["apt_sim_ran"] is True
            assert payload["apt_sim_note"] == "ran"
            assert payload["desktop_file_validate"] == "ran"
        finally:
            fake_codium.unlink(missing_ok=True)
            ide_deb.unlink(missing_ok=True)
            stack_deb.unlink(missing_ok=True)


def test_verify_step14_closeout_json_mode_apt_sim_ran_with_stack_requirement() -> None:
    """--require-stack-deb + --apt-sim sets apt_sim_note=ran when apt-get -s succeeds."""
    _run_with_step14_contract_artifact_lock(_verify_step14_closeout_json_mode_apt_sim_ran_with_stack_requirement_impl)


def _verify_step14_closeout_json_mode_reports_apt_sim_requested_without_stack_requirement_impl() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "verify-step14-closeout.sh"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        stub_dir = tmp_root / "bin"
        stub_dir.mkdir()
        packaging_dir = root / "packaging"
        ide_deb = packaging_dir / "le-vibe-ide_9999.0.1_amd64.deb"
        fake_codium = root / "editor" / "vscodium" / "VSCode-linux-x64" / "bin" / "codium"
        fake_codium.parent.mkdir(parents=True, exist_ok=True)
        fake_codium.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        os.chmod(fake_codium, 0o755)
        ide_deb.write_bytes(b"placeholder")
        try:
            (stub_dir / "dpkg-deb").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
if [[ "$1" == "--contents" ]]; then
  cat <<'EOF'
-rwxr-xr-x root/root         0 2026-01-01 00:00 ./usr/lib/le-vibe/bin/codium
-rw-r--r-- root/root         0 2026-01-01 00:00 ./usr/share/applications/le-vibe.desktop
EOF
  exit 0
fi
if [[ "$1" == "--field" ]]; then
  field="$3"
  if [[ "$field" == "Package" ]]; then
    printf 'le-vibe-ide\\n'
    exit 0
  fi
  if [[ "$field" == "Architecture" ]]; then
    printf 'amd64\\n'
    exit 0
  fi
fi
if [[ "$1" == "--fsys-tarfile" ]]; then
  cat <<'EOF'
dummy-tar-stream
EOF
  exit 0
fi
echo "unexpected dpkg-deb args: $*" >&2
exit 1
""",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "dpkg-deb", 0o755)
            (stub_dir / "tar").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
cat <<'EOF'
[Desktop Entry]
Name=Lé Vibe
Exec=/usr/lib/le-vibe/bin/codium %F
EOF
""",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "tar", 0o755)
            (stub_dir / "desktop-file-validate").write_text(
                "#!/usr/bin/env bash\nexit 0\n",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "desktop-file-validate", 0o755)
            result = subprocess.run(
                [str(script), "--skip-gate", "--apt-sim", "--json"],
                cwd=str(root),
                capture_output=True,
                text=True,
                env={
                    "PATH": str(stub_dir) + ":" + str(Path("/usr/bin")) + ":" + str(Path("/bin")),
                },
            )
            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            assert payload["status"] == "ok"
            assert payload["vscode_linux_build"] == "ready"
            assert payload["stack_deb_required"] is False
            assert payload["stack_deb"] is None
            assert payload["apt_sim_requested"] is True
            assert payload["apt_sim_ran"] is False
            assert payload["apt_sim_note"] == "requested_without_stack_requirement"
            assert payload["desktop_file_validate"] == "ran"
        finally:
            fake_codium.unlink(missing_ok=True)
            ide_deb.unlink(missing_ok=True)


def test_verify_step14_closeout_json_mode_reports_apt_sim_requested_without_stack_requirement() -> None:
    _run_with_step14_contract_artifact_lock(
        _verify_step14_closeout_json_mode_reports_apt_sim_requested_without_stack_requirement_impl
    )


def _verify_step14_closeout_json_mode_escapes_special_chars_in_paths_impl() -> None:
    root = _repo_root()
    script = root / "packaging" / "scripts" / "verify-step14-closeout.sh"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_root = Path(tmp_dir)
        stub_dir = tmp_root / "bin"
        stub_dir.mkdir()
        packaging_dir = root / "packaging"
        stack_deb = root.parent / 'le-vibe_9999.0.2_"quotes"_all.deb'
        ide_deb = packaging_dir / 'le-vibe-ide_9999.0.2_"quotes"_amd64.deb'
        fake_codium = root / "editor" / "vscodium" / "VSCode-linux-x64" / "bin" / "codium"
        fake_codium.parent.mkdir(parents=True, exist_ok=True)
        fake_codium.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
        os.chmod(fake_codium, 0o755)
        stack_deb.write_bytes(b"placeholder")
        ide_deb.write_bytes(b"placeholder")
        try:
            (stub_dir / "dpkg-deb").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
if [[ "$1" == "--contents" ]]; then
  cat <<'EOF'
-rwxr-xr-x root/root         0 2026-01-01 00:00 ./usr/lib/le-vibe/bin/codium
-rwxr-xr-x root/root         0 2026-01-01 00:00 ./usr/bin/lvibe
-rw-r--r-- root/root         0 2026-01-01 00:00 ./usr/share/applications/le-vibe.desktop
-rw-r--r-- root/root         0 2026-01-01 00:00 ./usr/share/doc/le-vibe/README.Debian
EOF
  exit 0
fi
if [[ "$1" == "--field" ]]; then
  deb_path="$2"
  field="$3"
  if [[ "$field" == "Package" ]]; then
    if [[ "$deb_path" == *"le-vibe-ide_"* ]]; then
      printf 'le-vibe-ide\\n'
    else
      printf 'le-vibe\\n'
    fi
    exit 0
  fi
  if [[ "$field" == "Architecture" ]]; then
    if [[ "$deb_path" == *"le-vibe-ide_"* ]]; then
      printf 'amd64\\n'
    else
      printf 'all\\n'
    fi
    exit 0
  fi
fi
if [[ "$1" == "--fsys-tarfile" ]]; then
  cat <<'EOF'
dummy-tar-stream
EOF
  exit 0
fi
echo "unexpected dpkg-deb args: $*" >&2
exit 1
""",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "dpkg-deb", 0o755)
            (stub_dir / "tar").write_text(
                """#!/usr/bin/env bash
set -euo pipefail
cat <<'EOF'
[Desktop Entry]
Name=Lé Vibe
Exec=/usr/lib/le-vibe/bin/codium %F
EOF
""",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "tar", 0o755)
            (stub_dir / "desktop-file-validate").write_text(
                "#!/usr/bin/env bash\nexit 0\n",
                encoding="utf-8",
            )
            os.chmod(stub_dir / "desktop-file-validate", 0o755)
            result = subprocess.run(
                [str(script), "--skip-gate", "--require-stack-deb", "--json"],
                cwd=str(root),
                capture_output=True,
                text=True,
                env={
                    "PATH": str(stub_dir) + ":" + str(Path("/usr/bin")) + ":" + str(Path("/bin")),
                },
            )
            assert result.returncode == 0, result.stderr
            payload = json.loads(result.stdout)
            assert payload["vscode_linux_build"] == "ready"
            assert Path(payload["stack_deb"]).resolve() == stack_deb.resolve()
            assert payload["ide_deb"] == str(ide_deb)
            assert payload["apt_sim_note"] == "not_requested"
            assert payload["desktop_file_validate"] == "ran"
        finally:
            fake_codium.unlink(missing_ok=True)
            ide_deb.unlink(missing_ok=True)
            stack_deb.unlink(missing_ok=True)


def test_verify_step14_closeout_json_mode_escapes_special_chars_in_paths() -> None:
    _run_with_step14_contract_artifact_lock(_verify_step14_closeout_json_mode_escapes_special_chars_in_paths_impl)
