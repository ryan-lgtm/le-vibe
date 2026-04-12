"""Contract: spec-phase2.md §14 table + honesty paragraph stay aligned with STEP 14 (14.j)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_spec_phase2_section14_ide_row_honesty_strings():
    text = (_repo_root() / "spec-phase2.md").read_text(encoding="utf-8")
    assert "## 14." in text or "§14" in text
    assert "STEP 14.j" in text
    assert "linux_compile" in text
    assert "linux_compile-cargo" in text
    assert "actions/cache@v4" in text
    assert ".cargo/registry" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "14.j" in text
    assert "test_spec_phase2_section14_snapshot_contract.py" in text
    assert "test_editor_build_md_contract.py" in text
    assert "test_continue_extension_pin_doc_step14_contract.py" in text
    assert "test_vscodium_fork_le_vibe_branding_contract.py" in text
    assert "CHANGELOG.md" in text
    assert "test_launcher_default_editor.py" in text
    assert "/usr/bin/le-vibe-ide" in text
    assert "build-env.sh.example" in text
