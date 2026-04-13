"""STEP 10 / H3: resolve monorepo root and run ``packaging/scripts/ci-*.sh`` (``docs/ci-qa-hardening.md``)."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

SMOKE_REL = Path("packaging") / "scripts" / "ci-smoke.sh"
EDITOR_GATE_REL = Path("packaging") / "scripts" / "ci-editor-gate.sh"

EXIT_NO_MONOREPO = 125


def _walk_up_for_script(start: Path, rel: Path) -> Path | None:
    cur = start.resolve()
    for _ in range(64):
        if (cur / rel).is_file():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def find_monorepo_root() -> Path | None:
    """
    Locate the repository root that contains ``packaging/scripts/ci-smoke.sh``.

    Uses ``LE_VIBE_REPO_ROOT`` when set, else walks upward from the current working directory
    and from this package directory (so discovery works when ``lvibe`` runs from a subdirectory).
    """
    env = os.environ.get("LE_VIBE_REPO_ROOT", "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        hit = _walk_up_for_script(p, SMOKE_REL)
        if hit is not None:
            return hit
    for start in (Path.cwd(), Path(__file__).resolve().parent):
        hit = _walk_up_for_script(start, SMOKE_REL)
        if hit is not None:
            return hit
    return None


def run_ci_smoke(argv: list[str]) -> int:
    root = find_monorepo_root()
    if root is None:
        return EXIT_NO_MONOREPO
    script = root / SMOKE_REL
    if not script.is_file():
        return EXIT_NO_MONOREPO
    proc = subprocess.run(["bash", str(script), *argv], cwd=root)
    return int(proc.returncode)


def run_ci_editor_gate(argv: list[str]) -> int:
    root = find_monorepo_root()
    if root is None:
        return EXIT_NO_MONOREPO
    script = root / EDITOR_GATE_REL
    if not script.is_file():
        return EXIT_NO_MONOREPO
    proc = subprocess.run(["bash", str(script), *argv], cwd=root)
    return int(proc.returncode)


def run_ci_smoke_captured(argv: list[str]) -> tuple[int, str, str]:
    """
    Same as ``run_ci_smoke`` but capture stdout/stderr (``lvibe ci-smoke --json``).

    Returns ``(EXIT_NO_MONOREPO, "", "")`` when the monorepo or script is missing.
    """
    root = find_monorepo_root()
    if root is None:
        return EXIT_NO_MONOREPO, "", ""
    script = root / SMOKE_REL
    if not script.is_file():
        return EXIT_NO_MONOREPO, "", ""
    proc = subprocess.run(
        ["bash", str(script), *argv],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return int(proc.returncode), proc.stdout or "", proc.stderr or ""


def run_ci_editor_gate_captured(argv: list[str]) -> tuple[int, str, str]:
    """
    Same as ``run_ci_editor_gate`` but capture stdout/stderr (``lvibe ci-editor-gate --json``).

    Returns ``(EXIT_NO_MONOREPO, "", "")`` when the monorepo or script is missing.
    """
    root = find_monorepo_root()
    if root is None:
        return EXIT_NO_MONOREPO, "", ""
    script = root / EDITOR_GATE_REL
    if not script.is_file():
        return EXIT_NO_MONOREPO, "", ""
    proc = subprocess.run(
        ["bash", str(script), *argv],
        cwd=root,
        capture_output=True,
        text=True,
    )
    return int(proc.returncode), proc.stdout or "", proc.stderr or ""
