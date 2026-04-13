"""STEP 14: ide_packaging_paths — §7.3 touchpoints in a checkout."""

from __future__ import annotations

from pathlib import Path

from le_vibe.ide_packaging_paths import find_vscode_linux_tree, iter_ide_prereq_paths


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_fixed_prereq_files_exist_in_repo():
    root = _root()
    rows = iter_ide_prereq_paths(root)
    # All file-backed rows except the first (VSCode-linux) must be OK when tree missing.
    # VSCodium-staged le-vibe.svg is optional until sync-linux-icon-assets.sh (editor/BUILD.md).
    for label, path, ok in rows[1:]:
        if "VSCodium linux le-vibe.svg" in label:
            continue
        assert ok, f"{label}: {path}"


def test_vscode_tree_row_matches_find():
    root = _root()
    vs = find_vscode_linux_tree(root)
    first = iter_ide_prereq_paths(root)[0]
    assert "VSCode-linux" in first[0]
    assert first[2] is (vs is not None)
    if vs is not None:
        assert first[1] == vs
