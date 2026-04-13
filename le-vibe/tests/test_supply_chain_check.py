"""STEP 9 / H2: ``supply_chain_check`` paths."""

from __future__ import annotations

from le_vibe.supply_chain_check import requirements_txt_path


def test_requirements_txt_path_in_git_clone():
    p = requirements_txt_path()
    assert p.name == "requirements.txt"
    assert p.is_file(), f"expected {p} in repository checkout"
    assert (p.parent / "le_vibe").is_dir()
