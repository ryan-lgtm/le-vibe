"""H4: ``packaging/continue-openvsx-version`` must pin a semver for reproducible installs."""

from __future__ import annotations

import re

from le_vibe.continue_pin import read_continue_openvsx_version, read_vscode_yaml_openvsx_version

# Relaxed semver: core x.y.z optional pre-release suffix.
_PIN_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?")


def test_continue_openvsx_pin_file_exists_and_semver():
    line = read_continue_openvsx_version()
    assert line, "no version line in continue-openvsx-version"
    assert _PIN_RE.fullmatch(line.strip()), f"not a semver pin: {line!r}"


def test_vscode_yaml_openvsx_pin_file_exists_and_semver():
    line = read_vscode_yaml_openvsx_version()
    assert line, "no version line in vscode-yaml-openvsx-version"
    assert _PIN_RE.fullmatch(line.strip()), f"not a semver pin: {line!r}"
