"""Contract: editor/smoke-lvibe-editor.sh + ci-editor-gate keep STEP 14.c (lvibe ↔ binary smoke)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_smoke_lvibe_editor_script_contract():
    text = (_repo_root() / "editor" / "smoke-lvibe-editor.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "14.c" in text or "STEP 14" in text
    assert "le_vibe.launcher" in text
    assert "--skip-first-run" in text
    assert "--editor" in text
    assert "--version" in text
    assert "LE_VIBE_EDITOR" in text
    assert "ollama" in text
    assert "managed Ollama" in text
    assert "print-built-codium-path.sh" in text
    assert "not an executable file" in text
    assert "editor not on PATH" in text
    assert "python3 not on PATH" in text
    assert "exit 2" in text
    assert "exit 3" in text
    assert "exit 4" in text
    assert "exit 5" in text


def test_ci_editor_gate_bash_n_smoke_lvibe_editor():
    text = (_repo_root() / "packaging" / "scripts" / "ci-editor-gate.sh").read_text(encoding="utf-8")
    assert "smoke-lvibe-editor.sh" in text
    assert "bash -n" in text
    assert "use-node-toolchain.sh" in text
    assert "verify-14c-local-binary.sh" in text
    assert "smoke-built-codium-lvibe.sh" in text
    assert "print-built-codium-path.sh" in text
    assert "print-vsbuild-codium-path.sh" in text
    assert "print-ci-tarball-codium-path.sh" in text


def test_smoke_built_codium_lvibe_chains_print_built_and_smoke():
    root = _repo_root()
    text = (root / "editor" / "smoke-built-codium-lvibe.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "14.c" in text or "STEP 14" in text
    assert "python3 not on PATH" in text
    assert "exit 5" in text
    assert "print-built-codium-path.sh" in text
    assert "smoke-lvibe-editor.sh" in text
    assert (root / "editor" / "smoke-built-codium-lvibe.sh").is_file()


def test_14c_smoke_and_print_scripts_bash_syntax() -> None:
    root = _repo_root()
    for rel in (
        "editor/smoke-lvibe-editor.sh",
        "editor/smoke-built-codium-lvibe.sh",
        "editor/print-built-codium-path.sh",
        "editor/verify-14c-local-binary.sh",
    ):
        script = root / rel
        assert script.is_file(), script
        subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_print_built_codium_path_documents_14c():
    text = (_repo_root() / "editor" / "print-built-codium-path.sh").read_text(encoding="utf-8")
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "14.c" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "LE_VIBE_EDITOR" in text
    assert "smoke-lvibe-editor.sh" in text
    assert "print-built-codium-path: expected editor/vscodium" in text
    assert 'exec "${ROOT}/editor/print-vsbuild-codium-path.sh"' in text


def test_verify_14c_local_binary_script_contract():
    root = _repo_root()
    text = (root / "editor" / "verify-14c-local-binary.sh").read_text(encoding="utf-8")
    assert "--help" in text
    assert "unexpected argument" in text
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text
    assert "14.c" in text or "STEP 14" in text
    assert "print-built-codium-path.sh" in text
    assert "BUILD.md" in text
    assert "smoke-built-codium-lvibe.sh" in text
    assert "verify-14c-local-binary: (14.c) No built tree yet" in text
    assert "verify-14c-local-binary: (14.c) Incomplete VSCode-linux tree" in text
    assert "use-node-toolchain.sh" in text
    assert "fetch-vscode-sources.sh" in text
    assert "dev/build.sh" in text
    assert (root / "editor" / "verify-14c-local-binary.sh").is_file()
