"""STEP 7 / H4: reproducible Open VSX pins for Continue (``continue.continue@<semver>``) and YAML (``redhat.vscode-yaml@<semver>``).

Authority: ``docs/continue-extension-pin.md``; pin files ship as ``packaging/continue-openvsx-version`` and
``packaging/vscode-yaml-openvsx-version`` (under ``/usr/share/le-vibe/`` when installed from the stack ``.deb``).
"""

from __future__ import annotations

import os
import re
from pathlib import Path

_PIN_LINE_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$")


def resolve_vscode_yaml_openvsx_pin_path() -> Path:
    """
    Prefer ``LE_VIBE_VSCODE_YAML_PIN_FILE``, then packaged ``.deb`` path,
    then monorepo ``packaging/vscode-yaml-openvsx-version``.
    """
    env = os.environ.get("LE_VIBE_VSCODE_YAML_PIN_FILE", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    packaged = Path("/usr/share/le-vibe/vscode-yaml-openvsx-version")
    if packaged.is_file():
        return packaged
    dev = Path(__file__).resolve().parents[2] / "packaging" / "vscode-yaml-openvsx-version"
    return dev


def read_vscode_yaml_openvsx_version() -> str:
    """Return the first non-comment semver line from the YAML extension pin file."""
    path = resolve_vscode_yaml_openvsx_pin_path()
    if not path.is_file():
        raise FileNotFoundError(str(path))
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if _PIN_LINE_RE.fullmatch(s):
            return s
        raise ValueError(f"expected semver in {path}, got: {s!r}")
    raise ValueError(f"no semver line in {path}")


def resolve_continue_openvsx_pin_path() -> Path:
    """
    Prefer ``LE_VIBE_CONTINUE_PIN_FILE`` (same as ``install-continue-extension.sh``),
    then packaged ``.deb`` path, then monorepo ``packaging/continue-openvsx-version``.
    """
    env = os.environ.get("LE_VIBE_CONTINUE_PIN_FILE", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    packaged = Path("/usr/share/le-vibe/continue-openvsx-version")
    if packaged.is_file():
        return packaged
    dev = Path(__file__).resolve().parents[2] / "packaging" / "continue-openvsx-version"
    return dev


def read_continue_openvsx_version() -> str:
    """Return the first non-comment semver line from the pin file."""
    path = resolve_continue_openvsx_pin_path()
    if not path.is_file():
        raise FileNotFoundError(str(path))
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if _PIN_LINE_RE.fullmatch(s):
            return s
        raise ValueError(f"expected semver in {path}, got: {s!r}")
    raise ValueError(f"no semver line in {path}")
