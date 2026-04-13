"""STEP 14: ide_packaging_paths — §7.3 touchpoints in a checkout."""

from __future__ import annotations

from pathlib import Path

from le_vibe.ide_packaging_paths import (
    find_vscode_linux_tree,
    iter_ide_prereq_paths,
    static_prereq_repo_files_ok,
    vscode_linux_build_status,
)


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


def test_static_prereq_repo_files_ok_in_clone():
    assert static_prereq_repo_files_ok(_root())


def test_vscode_tree_row_matches_find():
    root = _root()
    vs = find_vscode_linux_tree(root)
    st, pth = vscode_linux_build_status(root)
    first = iter_ide_prereq_paths(root)[0]
    assert "VSCode-linux" in first[0]
    if st == "ready":
        assert vs is not None and first[2] and first[1] == vs == pth
    elif st == "partial":
        assert vs is None and not first[2] and "partial" in first[0].lower() and first[1] == pth
    else:
        assert vs is None and not first[2] and st == "absent"


def test_vscode_linux_build_status_absent(tmp_path: Path) -> None:
    (tmp_path / "editor" / "vscodium").mkdir(parents=True)
    st, p = vscode_linux_build_status(tmp_path)
    assert st == "absent"
    assert p is None


def test_vscode_linux_build_status_partial(tmp_path: Path) -> None:
    bindir = tmp_path / "editor" / "vscodium" / "VSCode-linux-x64" / "bin"
    bindir.mkdir(parents=True)
    (bindir / "codium-tunnel").write_text("x", encoding="utf-8")
    st, p = vscode_linux_build_status(tmp_path)
    assert st == "partial"
    assert p == tmp_path / "editor" / "vscodium" / "VSCode-linux-x64"


def test_vscode_linux_build_status_ready(tmp_path: Path) -> None:
    bindir = tmp_path / "editor" / "vscodium" / "VSCode-linux-x64" / "bin"
    bindir.mkdir(parents=True)
    c = bindir / "codium"
    c.write_text("#!/bin/sh\n", encoding="utf-8")
    c.chmod(0o755)
    st, p = vscode_linux_build_status(tmp_path)
    assert st == "ready"
    assert p == tmp_path / "editor" / "vscodium" / "VSCode-linux-x64"
