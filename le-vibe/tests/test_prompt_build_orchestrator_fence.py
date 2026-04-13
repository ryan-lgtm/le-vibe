"""`docs/PROMPT_BUILD_LE_VIBE.md` must retain an extractable Master orchestrator fence (STEP 16, print-master-orchestrator-prompt.py)."""

from __future__ import annotations

from pathlib import Path


def test_master_orchestrator_fence_extractable():
    root = Path(__file__).resolve().parents[2]
    text = (root / "docs" / "PROMPT_BUILD_LE_VIBE.md").read_text(encoding="utf-8")
    fence: str | None = None
    for part in text.split("```"):
        if part.lstrip().startswith("You are the senior engineer for Lé Vibe"):
            fence = part
            break
    assert fence is not None, (
        "Master orchestrator fenced block missing — "
        "see packaging/scripts/print-master-orchestrator-prompt.py"
    )
    assert "ORDERED WORK QUEUE" in fence
    assert "STEP 0" in fence and "STEP 17" in fence
    assert "USER RESPONSE REQUIRED" in fence
    assert "Rolling iteration — prefer continuation" in fence
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product maintainer `.deb`" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "preflight-step14-closeout.sh" in text
    assert "ide-prereqs --print-closeout-commands" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "build machine" in text
    assert "test host" in text
    assert "Partial VSCode-linux tree" in text
    assert "print-github-linux-compile-artifact-hint.sh" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "vscode_linux_bin_files" in text
    assert "print-built-codium-path" in text
    assert "print-vsbuild-codium-path" in text
    assert "build-le-vibe-ide-deb.sh --help" in text
    assert "Incomplete Linux build" in text
    assert "resolve-latest-le-vibe-stack-deb.sh" in text
    assert "probe-vscode-linux-build.sh" in text
    assert "dpkg-buildpackage" in text
    assert "Failure (`--with-ide`)" in text


def test_print_master_orchestrator_prompt_script_header_mentions_queue():
    root = Path(__file__).resolve().parents[2]
    text = (root / "packaging" / "scripts" / "print-master-orchestrator-prompt.py").read_text(encoding="utf-8")
    assert "0 -> 1 -> 14 -> 2-13 -> 15-17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
