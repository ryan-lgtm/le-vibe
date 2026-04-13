"""§7.3 / STEP 14: ``./editor/smoke.sh`` must pass (same gate as ``lvibe ci-editor-gate``)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_editor_smoke_sh_exits_zero():
    """Vendor/layout + bash syntax + nvmrc sync — no full Electron compile required."""
    root = _repo_root()
    script = root / "editor" / "smoke.sh"
    assert script.is_file(), f"missing {script}"
    r = subprocess.run(
        ["bash", str(script)],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=120,  # editor gate is fast; cap hangs in CI
    )
    assert r.returncode == 0, r.stdout + r.stderr
    out = r.stdout + r.stderr
    assert "ci-editor-gate" in out or "ci-vscodium-bash-syntax" in out
