"""Global first-run + Continue preamble runs before subcommand dispatch (desktop + CLI parity)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

from le_vibe import launcher


def test_session_preamble_skipped_when_env_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LE_VIBE_SKIP_SESSION_PREAMBLE", "1")
    assert launcher._run_global_session_preamble(["lvibe", "hygiene"]) is None


def test_session_preamble_skipped_on_non_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LE_VIBE_SKIP_SESSION_PREAMBLE", raising=False)
    monkeypatch.setattr(sys, "platform", "darwin")
    assert launcher._run_global_session_preamble(["lvibe", "hygiene"]) is None


def test_session_preamble_skips_help_argv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LE_VIBE_SKIP_SESSION_PREAMBLE", raising=False)
    monkeypatch.setattr(sys, "platform", "linux")
    assert launcher._run_global_session_preamble(["lvibe", "--help"]) is None


def test_session_preamble_returns_exit_8_when_default_launch_not_agent_ready(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("LE_VIBE_SKIP_SESSION_PREAMBLE", raising=False)
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr("le_vibe.launcher.ensure_product_first_run", lambda **_k: (0, "ok"))
    monkeypatch.setattr("le_vibe.launcher.maybe_auto_setup_cline_after_first_run", lambda _cfg: None)
    monkeypatch.setattr(
        "le_vibe.launcher.evaluate_first_run_agent_readiness",
        lambda **_k: (False, "not ready"),
    )
    rc = launcher._run_global_session_preamble(["lvibe"])
    assert rc == 8


def test_launcher_subcommands_frozen_matches_dispatch() -> None:
    """Guard: new ``lvibe <cmd>`` dispatch branches must update ``_LAUNCHER_SUBCOMMANDS``."""
    src = Path(launcher.__file__).read_text(encoding="utf-8")
    dispatched = set(
        re.findall(r'if len\(sys\.argv\) >= 2 and sys\.argv\[1\] == "([^"]+)"', src)
    )
    assert dispatched == set(launcher._LAUNCHER_SUBCOMMANDS)
