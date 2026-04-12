"""H4: ``packaging/continue-openvsx-version`` must pin a semver for reproducible installs."""

from __future__ import annotations

import re
from pathlib import Path

# Relaxed semver: core x.y.z optional pre-release suffix.
_PIN_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?")


def _pin_file() -> Path:
    return Path(__file__).resolve().parents[2] / "packaging" / "continue-openvsx-version"


def test_continue_openvsx_pin_file_exists_and_semver():
    p = _pin_file()
    assert p.is_file(), f"missing {p}"
    line = ""
    for raw in p.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        line = s
        break
    assert line, "no version line in continue-openvsx-version"
    assert _PIN_RE.fullmatch(line.strip()), f"not a semver pin: {line!r}"
