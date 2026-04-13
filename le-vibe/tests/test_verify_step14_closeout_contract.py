"""Contract: verify-step14-closeout.sh checks local §7.3 artifacts (STEP 14)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


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
    assert "packaging/le-vibe-ide_*.deb" in text
    assert "--require-stack-deb" in text
    assert "--skip-gate" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "pick_latest_match" in text
    assert "sort -V" in text
    assert 'ide deb: $ide_deb_latest' in text
    assert 'stack deb: $stack_deb_latest' in text
    assert "assert_deb_contains" in text
    assert "assert_deb_contains_any" in text
    assert "assert_deb_field_equals" in text
    assert "assert_deb_file_contains" in text
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
