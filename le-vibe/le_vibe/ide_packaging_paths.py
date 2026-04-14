"""STEP 14 / H6: paths for §7.3 IDE packaging — VSCode-linux tree, branding, Linux + workbench icons, staging scripts.

Freedesktop ``.desktop`` QA (packaged or installed): see ``preflight-step14-closeout.sh``,
``verify-step14-closeout.sh``, ``build-le-vibe-ide-deb.sh``, and test-host
``manual-step14-install-smoke.sh --verify-only`` (``desktop-file-validate`` when available).
``ide_deb_hicolor_icon_status`` / ``lvibe ide-prereqs --json`` field ``hicolor_icon_in_deb`` match
preflight/verify hicolor payload checks on ``packaging/le-vibe-ide_*.deb``.

Maintainer brand gate: ``sync-linux-icon-assets.sh --check`` (invoked from ``ci-editor-gate.sh`` when
``LEVIBE_EDITOR_GATE_ASSERT_BRAND=1`` and a ``VSCode-linux-*`` tree exists) needs ``cmp``, ``sed``, and
``mktemp`` on ``PATH`` — ``editor/BUILD.md`` (*Linux icons*).
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Literal

VscodeLinuxBuildStatus = Literal["ready", "partial", "absent"]
HicolorIdeDebStatus = Literal["none", "ok", "missing", "unknown"]

# Same path string as ``preflight-step14-closeout.sh`` / ``verify-step14-closeout.sh`` (§7.3 Freedesktop icon).
_IDE_DEB_HICOLOR_NEEDLE = "./usr/share/icons/hicolor/scalable/apps/le-vibe.svg"


def vscode_linux_build_status(root: Path) -> tuple[VscodeLinuxBuildStatus, Path | None]:
    """
    Classify the local VSCode-linux output under ``editor/vscodium/``.

    * **ready** — ``VSCode-linux-*/bin/codium`` exists and is executable (14.c complete).
    * **partial** — a ``VSCode-linux-*`` directory exists but ``bin/codium`` is missing
      (incomplete compile; see ``editor/BUILD.md`` *Partial tree*).
    * **absent** — no usable tree (fresh submodule or no build yet).
    """
    vsc = root / "editor" / "vscodium"
    if not vsc.is_dir():
        return "absent", None
    for p in sorted(vsc.glob("VSCode-linux-*")):
        codium = p / "bin" / "codium"
        if p.is_dir() and codium.is_file() and codium.stat().st_mode & 0o111:
            return "ready", p.resolve()
    for p in sorted(vsc.glob("VSCode-linux-*")):
        if p.is_dir():
            return "partial", p.resolve()
    return "absent", None


def find_vscode_linux_tree(root: Path) -> Path | None:
    """Return ``editor/vscodium/VSCode-linux-*`` when it contains ``bin/codium``."""
    st, p = vscode_linux_build_status(root)
    return p if st == "ready" else None


def vscode_linux_bin_filenames(vs_tree: Path | None) -> list[str] | None:
    """
    Filenames in ``VSCode-linux-*/bin`` when a tree path is known (partial or ready).

    ``None`` when there is no ``VSCode-linux-*`` directory; empty list when ``bin/`` is missing
    or empty. Helps diagnose **partial** trees (e.g. only ``codium-tunnel``).
    """
    if vs_tree is None:
        return None
    bin_dir = vs_tree / "bin"
    if not bin_dir.is_dir():
        return []
    return sorted(p.name for p in bin_dir.iterdir() if p.is_file())


def iter_ide_prereq_paths(root: Path) -> list[tuple[str, Path, bool]]:
    """
    Return ``(label, absolute_path, exists)`` for §7.3 packaging touchpoints.

    The VSCode-linux tree is **optional** until ``dev/build.sh`` completes — reported distinctly.
    """
    out: list[tuple[str, Path, bool]] = []

    st, vs = vscode_linux_build_status(root)
    if st == "ready":
        out.append(("VSCode-linux tree (for le-vibe-ide .deb)", vs, True))
    elif st == "partial":
        out.append(
            (
                "VSCode-linux tree — partial (bin/codium missing); editor/BUILD.md *Partial tree* / 14.c",
                vs,
                False,
            )
        )
    else:
        pending = (root / "editor" / "vscodium").resolve()
        out.append(("VSCode-linux tree (for le-vibe-ide .deb) — run editor/BUILD.md", pending, False))

    fixed: tuple[tuple[str, Path], ...] = (
        ("Branding merge (§7.3)", Path("editor/le-vibe-overrides/product-branding-merge.json")),
        ("Linux icon sync", Path("editor/le-vibe-overrides/sync-linux-icon-assets.sh")),
        (
            "VSCodium linux le-vibe.svg (after sync; LEVIBE_EDITOR_GATE_ASSERT_BRAND)",
            Path("editor/vscodium/src/stable/resources/linux/le-vibe.svg"),
        ),
        (
            "Workbench code-icon.svg stable (after sync; §7.3 window chrome)",
            Path("editor/vscodium/src/stable/src/vs/workbench/browser/media/code-icon.svg"),
        ),
        ("Canonical app icon (stack)", Path("packaging/icons/hicolor/scalable/apps/le-vibe.svg")),
        ("Stage IDE → deb staging", Path("packaging/scripts/stage-le-vibe-ide-deb.sh")),
        ("Build le-vibe-ide .deb", Path("packaging/scripts/build-le-vibe-ide-deb.sh")),
        ("Full-product stack + IDE", Path("packaging/scripts/build-le-vibe-debs.sh")),
        ("IDE debian metadata", Path("packaging/debian-le-vibe-ide/debian/control")),
        ("Freedesktop desktop entry (§7.3)", Path("packaging/debian-le-vibe-ide/debian/le-vibe.desktop")),
    )
    for label, rel in fixed:
        p = (root / rel).resolve()
        out.append((label, p, p.is_file()))
    return out


# Relative paths for ``lvibe ide-prereqs --path-only KEY`` (except ``vscode`` — use ``find_vscode_linux_tree``).
IDE_PREREQ_PATH_ONLY: dict[str, Path] = {
    "branding": Path("editor/le-vibe-overrides/product-branding-merge.json"),
    "sync-icons": Path("editor/le-vibe-overrides/sync-linux-icon-assets.sh"),
    "vsc-linux-svg": Path("editor/vscodium/src/stable/resources/linux/le-vibe.svg"),
    "workbench-icon": Path("editor/vscodium/src/stable/src/vs/workbench/browser/media/code-icon.svg"),
    "svg": Path("packaging/icons/hicolor/scalable/apps/le-vibe.svg"),
    "desktop": Path("packaging/debian-le-vibe-ide/debian/le-vibe.desktop"),
    "stage": Path("packaging/scripts/stage-le-vibe-ide-deb.sh"),
    "build-ide-deb": Path("packaging/scripts/build-le-vibe-ide-deb.sh"),
    "build-debs": Path("packaging/scripts/build-le-vibe-debs.sh"),
    "control": Path("packaging/debian-le-vibe-ide/debian/control"),
}

# Keys for ``static_prereq_files_ok`` in ``lvibe ide-prereqs --json``: repo-shipped §7.3 inputs only.
# ``vsc-linux-svg`` is produced by sync-linux-icon-assets.sh before dev/build.sh — omit from the static gate.
IDE_PREREQ_STATIC_OK_KEYS: tuple[str, ...] = (
    "branding",
    "sync-icons",
    "svg",
    "desktop",
    "stage",
    "build-ide-deb",
    "build-debs",
    "control",
)


def static_prereq_repo_files_ok(root: Path) -> bool:
    """True when every committed packaging / override file needed for §7.3 automation exists."""
    return all((root / IDE_PREREQ_PATH_ONLY[k]).is_file() for k in IDE_PREREQ_STATIC_OK_KEYS)


def pick_latest_le_vibe_ide_deb(root: Path) -> Path | None:
    """
    Newest ``packaging/le-vibe-ide_*.deb`` using ``sort -V`` on basenames — parity with bash close-out scripts.
    """
    packaging = root / "packaging"
    if not packaging.is_dir():
        return None
    paths = list(packaging.glob("le-vibe-ide_*.deb"))
    if not paths:
        return None
    if len(paths) == 1:
        return paths[0]
    proc = subprocess.run(
        ["sort", "-V"],
        input="\n".join(p.name for p in paths),
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    if not lines:
        return paths[0]
    last_name = lines[-1]
    for p in paths:
        if p.name == last_name:
            return p
    return paths[-1]


def ide_deb_hicolor_icon_status(root: Path) -> HicolorIdeDebStatus:
    """
    Whether the newest ``packaging/le-vibe-ide_*.deb`` lists the §7.3 hicolor icon path in ``dpkg-deb --contents``.

    Values match ``preflight-step14-closeout.sh --json`` field ``hicolor_icon_in_deb``:
    ``none`` (no IDE ``.deb``), ``ok`` / ``missing``, or ``unknown`` (no ``dpkg-deb`` or read failure).
    """
    deb = pick_latest_le_vibe_ide_deb(root)
    if deb is None:
        return "none"
    if shutil.which("dpkg-deb") is None:
        return "unknown"
    proc = subprocess.run(
        ["dpkg-deb", "--contents", str(deb)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        return "unknown"
    return "ok" if _IDE_DEB_HICOLOR_NEEDLE in proc.stdout else "missing"


def vscode_linux_compile_gate_progress(root: Path) -> dict[str, object]:
    """
    Weighted **0–100** progress toward ``VSCode-linux-*/bin/codium`` under ``editor/vscodium/``.

    This is the **Linux compile / CI tarball vendor** slice of STEP 14 only — not §7.3 branding
    checks, static packaging files, or built ``.deb`` artifacts. Use
    ``packaging/scripts/preflight-step14-closeout.sh`` for a broader maintainer gap list.
    """
    vsc = root / "editor" / "vscodium"
    milestones: list[dict[str, object]] = []
    score = 0

    ok = vsc.is_dir()
    w = 10
    if ok:
        score += w
    milestones.append(
        {
            "id": "vscodium_dir",
            "label": "editor/vscodium/ directory exists",
            "weight": w,
            "done": ok,
        }
    )

    pj = vsc / "product.json"
    ok = pj.is_file()
    w = 15
    if ok:
        score += w
    milestones.append(
        {
            "id": "product_json",
            "label": "editor/vscodium/product.json (submodule / checkout)",
            "weight": w,
            "done": ok,
        }
    )

    vs_tree: Path | None = None
    if vsc.is_dir():
        for p in sorted(vsc.glob("VSCode-linux-*")):
            if p.is_dir():
                vs_tree = p.resolve()
                break
    ok = vs_tree is not None
    w = 35
    if ok:
        score += w
    milestones.append(
        {
            "id": "vscode_linux_tree",
            "label": "VSCode-linux-* output directory exists",
            "weight": w,
            "done": ok,
        }
    )

    bin_dir = vs_tree / "bin" if vs_tree is not None else None
    bin_files: list[str] = []
    if bin_dir is not None and bin_dir.is_dir():
        bin_files = sorted(x.name for x in bin_dir.iterdir() if x.is_file())
    ok = bool(bin_files)
    w = 10
    if ok:
        score += w
    milestones.append(
        {
            "id": "bin_populated",
            "label": "VSCode-linux-*/bin/ has at least one file",
            "weight": w,
            "done": ok,
        }
    )

    codium_path = vs_tree / "bin" / "codium" if vs_tree is not None else None
    ok = codium_path is not None and codium_path.is_file() and codium_path.stat().st_mode & 0o111
    w = 30
    if ok:
        score += w
    milestones.append(
        {
            "id": "codium_binary",
            "label": "VSCode-linux-*/bin/codium exists and is executable (compile gate complete)",
            "weight": w,
            "done": ok,
        }
    )

    st, st_path = vscode_linux_build_status(root)
    return {
        "vscode_linux_build": st,
        "vscode_linux_path": str(st_path) if st_path is not None else None,
        "compile_gate_pct": min(100, score),
        "compile_gate_milestones": milestones,
    }
