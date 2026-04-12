"""Contract: IDE extension `editor/le-vibe-settings-extension` matches `schemas/user-settings.v1.example.json`."""

from __future__ import annotations

import json
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_le_vibe_settings_extension_package_matches_schema_keys():
    pkg = _repo_root() / "editor" / "le-vibe-settings-extension" / "package.json"
    raw = json.loads(pkg.read_text(encoding="utf-8"))
    cmds = raw["contributes"].get("commands", [])
    assert any(c.get("command") == "leVibe.showChatCommandsHelp" for c in cmds)
    help_md = _repo_root() / "editor" / "le-vibe-settings-extension" / "help-chat-commands.md"
    assert help_md.is_file()
    assert "setup-workspace.md" in help_md.read_text(encoding="utf-8")
    props = raw["contributes"]["configuration"][0]["properties"]
    assert "leVibe.lvibeCapMbDefault" in props
    assert "leVibe.model.useRecommended" in props
    assert "leVibe.model.overrideTag" in props
    assert "leVibe.model.allowPullIfDiskOk" in props
    assert "leVibe.ide.showChatCommandsHelp" in props
    assert "leVibe.ide.showNewWorkspaceHints" in props

    ex = _repo_root() / "schemas" / "user-settings.v1.example.json"
    example = json.loads(ex.read_text(encoding="utf-8"))
    assert example["schema_version"] == "user-settings.v1"
    assert "lvibe_cap_mb_default" in example
    assert set(example["model"].keys()) == {
        "use_recommended",
        "override_tag",
        "allow_pull_if_disk_ok",
    }
    assert set(example["ide"].keys()) == {
        "show_chat_commands_help",
        "show_new_workspace_hints",
        "help_show_command_id",
    }
    assert example["ide"]["help_show_command_id"] == "leVibe.showChatCommandsHelp"
    meta = example.get("meta", {})
    assert "contract_tests" in meta
    assert "orchestration_doc" in meta
    assert "AGENT_MODE_ORCHESTRATION" in meta["orchestration_doc"]
