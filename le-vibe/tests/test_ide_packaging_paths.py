"""STEP 14: ide_packaging_paths — §7.3 touchpoints in a checkout."""

from __future__ import annotations

from pathlib import Path

from le_vibe.ide_packaging_paths import (
    find_vscode_linux_tree,
    ide_deb_hicolor_icon_status,
    iter_ide_prereq_paths,
    pick_latest_le_vibe_ide_deb,
    static_prereq_repo_files_ok,
    vscode_linux_bin_filenames,
    vscode_linux_build_status,
    vscode_linux_compile_gate_progress,
)


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_ide_packaging_paths_module_doc_mentions_freedesktop_closeout_chain() -> None:
    import le_vibe.ide_packaging_paths as m

    assert m.__doc__ is not None
    assert "manual-step14-install-smoke" in m.__doc__
    assert "desktop-file-validate" in m.__doc__
    assert "hicolor_icon_in_deb" in m.__doc__
    assert "sync-linux-icon-assets.sh --check" in m.__doc__
    assert "mktemp" in m.__doc__
    assert "LEVIBE_EDITOR_GATE_ASSERT_BRAND" in m.__doc__


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


def test_vscode_linux_build_status_codium_not_executable_is_partial(tmp_path: Path) -> None:
    bindir = tmp_path / "editor" / "vscodium" / "VSCode-linux-x64" / "bin"
    bindir.mkdir(parents=True)
    c = bindir / "codium"
    c.write_text("#!/bin/sh\n", encoding="utf-8")
    c.chmod(0o644)
    st, p = vscode_linux_build_status(tmp_path)
    assert st == "partial"
    assert p == tmp_path / "editor" / "vscodium" / "VSCode-linux-x64"


def test_vscode_linux_bin_filenames_none_when_no_tree() -> None:
    assert vscode_linux_bin_filenames(None) is None


def test_vscode_linux_bin_filenames_empty_when_no_bin_dir(tmp_path: Path) -> None:
    vs = tmp_path / "VSCode-linux-x64"
    vs.mkdir(parents=True)
    assert vscode_linux_bin_filenames(vs) == []


def test_vscode_linux_compile_gate_partial_tunnel_is_70_pct(tmp_path: Path) -> None:
    """Weights 10+15+35+10 = 70 until bin/codium exists."""
    bindir = tmp_path / "editor" / "vscodium" / "VSCode-linux-x64" / "bin"
    bindir.mkdir(parents=True)
    (bindir / "codium-tunnel").write_text("x", encoding="utf-8")
    (tmp_path / "editor" / "vscodium" / "product.json").write_text("{}", encoding="utf-8")
    d = vscode_linux_compile_gate_progress(tmp_path)
    assert d["compile_gate_pct"] == 70
    assert d["vscode_linux_build"] == "partial"
    assert len(d["compile_gate_milestones"]) == 5


def test_vscode_linux_compile_gate_ready_is_100_pct(tmp_path: Path) -> None:
    bindir = tmp_path / "editor" / "vscodium" / "VSCode-linux-x64" / "bin"
    bindir.mkdir(parents=True)
    (tmp_path / "editor" / "vscodium" / "product.json").write_text("{}", encoding="utf-8")
    c = bindir / "codium"
    c.write_text("#!/bin/sh\n", encoding="utf-8")
    c.chmod(0o755)
    d = vscode_linux_compile_gate_progress(tmp_path)
    assert d["compile_gate_pct"] == 100
    assert d["vscode_linux_build"] == "ready"


def test_pick_latest_le_vibe_ide_deb_sort_v_prefers_higher_version(tmp_path: Path) -> None:
    pkg = tmp_path / "packaging"
    pkg.mkdir(parents=True)
    (pkg / "le-vibe-ide_0.1.0_amd64.deb").write_bytes(b"x")
    (pkg / "le-vibe-ide_0.2.0_amd64.deb").write_bytes(b"x")
    assert pick_latest_le_vibe_ide_deb(tmp_path) == pkg / "le-vibe-ide_0.2.0_amd64.deb"


def test_ide_deb_hicolor_icon_status_none_without_deb(tmp_path: Path) -> None:
    (tmp_path / "packaging").mkdir()
    assert ide_deb_hicolor_icon_status(tmp_path) == "none"


def test_ide_deb_hicolor_icon_status_clone_is_valid_enum() -> None:
    st = ide_deb_hicolor_icon_status(_root())
    assert st in ("none", "ok", "missing", "unknown")


def test_vscode_linux_bin_filenames_lists_bin_files(tmp_path: Path) -> None:
    bindir = tmp_path / "editor" / "vscodium" / "VSCode-linux-x64" / "bin"
    bindir.mkdir(parents=True)
    (bindir / "codium-tunnel").write_text("x", encoding="utf-8")
    c = bindir / "codium"
    c.write_text("#!/bin/sh\n", encoding="utf-8")
    c.chmod(0o755)
    st, p = vscode_linux_build_status(tmp_path)
    assert st == "ready"
    assert vscode_linux_bin_filenames(p) == ["codium", "codium-tunnel"]
