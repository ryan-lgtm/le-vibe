"""Launcher default editor resolution (14.g — le-vibe-ide before codium)."""

from __future__ import annotations

import os

from le_vibe import launcher


def test_default_editor_respects_le_vibe_editor_env(monkeypatch):
    monkeypatch.setenv("LE_VIBE_EDITOR", "/opt/bin/editor")
    assert launcher._default_editor() == "/opt/bin/editor"


def test_default_editor_prefers_le_vibe_ide_on_disk(monkeypatch):
    monkeypatch.delenv("LE_VIBE_EDITOR", raising=False)

    def isfile(p):
        return str(p) == "/usr/bin/le-vibe-ide"

    def access(path, mode):
        return str(path) == "/usr/bin/le-vibe-ide"

    monkeypatch.setattr(os.path, "isfile", isfile)
    monkeypatch.setattr(os, "access", access)
    assert launcher._default_editor() == "/usr/bin/le-vibe-ide"


def test_default_editor_falls_back_to_codium_when_no_le_vibe_ide(monkeypatch):
    monkeypatch.delenv("LE_VIBE_EDITOR", raising=False)

    def isfile(p):
        return str(p) == "/usr/bin/codium"

    def access(path, mode):
        return str(path) == "/usr/bin/codium"

    monkeypatch.setattr(os.path, "isfile", isfile)
    monkeypatch.setattr(os, "access", access)
    assert launcher._default_editor() == "/usr/bin/codium"


def test_default_editor_string_codium_when_neither_present(monkeypatch):
    monkeypatch.delenv("LE_VIBE_EDITOR", raising=False)
    monkeypatch.setattr(os.path, "isfile", lambda p: False)
    monkeypatch.setattr(os, "access", lambda p, m: False)
    assert launcher._default_editor() == "codium"
