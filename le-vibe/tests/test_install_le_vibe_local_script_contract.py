"""packaging/scripts/install-le-vibe-local.sh — canonical local full-product orchestrator (STEP 14 / §7.3)."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_install_le_vibe_local_script_exists_bash_syntax_executable():
    script = _root() / "packaging" / "scripts" / "install-le-vibe-local.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)


def test_install_le_vibe_local_script_header_step14_contracts():
    text = (_root() / "packaging" / "scripts" / "install-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "sbom-signing-audit.md" in text
    assert "pip-audit" in text
    assert "STEP 9" in text
    assert "0 → 1 → 14 → 2–13 → 15–17" in text
    assert "PROMPT_BUILD_LE_VIBE.md" in text
    assert "PM_STAGE_MAP.md" in text
    assert "verify-step14-closeout.sh" in text
    assert "build-le-vibe-debs.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "manual-step14-install-smoke.sh" in text
    assert "test_install_le_vibe_local_script_contract.py" in text
    assert "test_verify_step14_closeout_contract.py" in text
    assert ".pytest-verify-step14-contract.lock" in text
    assert "git submodule update --init editor/vscodium" in text
    assert "Fresh clone (14.b)" in text


def test_install_le_vibe_local_script_asserts_deb_artifacts_when_install():
    text = (_root() / "packaging" / "scripts" / "install-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "Explicit artifact gate" in text or "artifact gate" in text.lower()
    assert "stack package .deb missing" in text
    assert "IDE package .deb missing" in text


def test_install_le_vibe_local_warns_on_dirty_vscodium_submodule():
    text = (_root() / "packaging" / "scripts" / "install-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "warn_if_vscodium_submodule_dirty" in text
    assert "VSCodium submodule state: DIRTY" in text
    assert "non-reproducible" in text


def test_install_le_vibe_local_preflight_json_includes_determinism_fields():
    text = (_root() / "packaging" / "scripts" / "install-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "\"submodule_state\"" in text
    assert "\"node_state\"" in text
    assert "\"disk_state\"" in text
    assert "\"remediation_hint\"" in text
    assert "preflight checks passed (see editor_host_deps/node_state/disk_state)" in text


def test_install_le_vibe_local_usage_documents_flags_and_exit_codes():
    text = (_root() / "packaging" / "scripts" / "install-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "--preflight-only" in text
    assert "LOCAL_INSTALL_ONE_SHOT.md" in text
    assert "--install" in text and "--yes" in text
    assert "--force-editor-build" in text
    assert "--skip-editor-build" in text
    assert "--skip-compile-failfast" in text
    assert "--json" in text
    assert "--apt-sim" in text
    assert "--skip-gate" in text
    assert "--log-file" in text
    assert "Exit codes:" in text
    assert "install-le-vibe-local.sh --install --yes" in text
    assert "mutually exclusive" in text


def test_install_le_vibe_local_runtime_readiness_contract():
    text = (_root() / "packaging" / "scripts" / "install-le-vibe-local.sh").read_text(encoding="utf-8")
    assert "using existing ollama" in text
    assert "ollama missing on PATH; attempting install" in text
    assert "failed to install curl via apt-get" in text
    assert "sudo apt-get update && sudo apt-get install -y curl" in text
    assert "le-vibe/scripts/install_linux.sh" in text
    assert "BOOTSTRAP_YES" in text
    assert "expected /usr/bin/lvibe after --install" in text
    assert "Installing stack + IDE packages explicitly" in text
    assert "sudo apt-get install" in text
    assert "dpkg -s le-vibe-ide" in text
    assert "retrying once after IDE artifact cleanup" in text
    assert "hash -r" in text
    assert "lvibe ." in text
    assert "LE_VIBE_AUTO_CONTINUE_SETUP" in text
    assert "\"runtime_ollama_state\"" in text
    assert "\"runtime_lvibe_state\"" in text
    assert "\"runtime_remediation_hint\"" in text
    assert "\"runtime_dependency_mode\"" in text
    assert "\"editor_build_mode\"" in text
    assert "\"install_readiness_state\"" in text
    assert "\"install_readiness_reasons\"" in text
    assert "\"install_readiness_summary\"" in text
    assert "not_applicable" in text
    assert "install_ollama_runtime" in text
    assert "repair_lvibe_install" in text
    assert "reused" in text
    assert "installed" in text
    assert "deferred" in text
    assert "compiled" in text
    assert "reused_existing_build" in text
    assert "skipped_by_flag" in text
    assert "ready_with_warnings" in text
    assert "runtime_dependency_deferred" in text
    assert "editor_build_skipped_by_flag" in text
    assert "runtime_ollama_not_ready" in text
    assert "runtime_lvibe_not_ready" in text
    assert "editor_build_not_ready" in text
    assert "codium_binary_not_ready" in text
    assert "deb_build_failed" in text
    assert "artifact_stack_missing" in text
    assert "artifact_ide_missing" in text
    assert "step14_verify_failed" in text
    assert "post_install_smoke_failed" in text
    assert "install ready with warnings" in text
    assert "install not ready" in text


def test_install_le_vibe_local_mutually_exclusive_flags_exit_2():
    r = subprocess.run(
        [
            "bash",
            str(_root() / "packaging" / "scripts" / "install-le-vibe-local.sh"),
            "--skip-editor-build",
            "--force-editor-build",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2
    assert "mutually exclusive" in (r.stderr or "")


def test_install_le_vibe_local_preflight_json_emits_remediation_hint_key():
    r = subprocess.run(
        [
            "bash",
            str(_root() / "packaging" / "scripts" / "install-le-vibe-local.sh"),
            "--preflight-only",
            "--json",
        ],
        capture_output=True,
        text=True,
    )
    assert r.returncode in (0, 2), r.stderr
    payload = json.loads((r.stdout or "").strip())
    assert "remediation_hint" in payload
    assert payload["remediation_hint"] in (
        "none",
        "align_node_toolchain",
        "free_disk_space",
        "install_editor_build_deps_before_recompile",
        "install_editor_build_deps",
        "install_python3",
    )


def test_install_le_vibe_local_emit_final_json_array_shape_contract():
    script = _root() / "packaging" / "scripts" / "install-le-vibe-local.sh"
    cmd = (
        "source \"$SCRIPT_PATH\" && "
        "emit_final_json "
        "'ok' 'done' 'all steps passed' "
        "'ready' '/tmp/codium' '/tmp/stack.deb' '/tmp/ide.deb' "
        "'true' 'false' 'false' "
        "'ready' 'not_applicable' 'none' 'deferred' 'reused_existing_build' "
        "'ready_with_warnings' 'runtime_dependency_deferred,editor_build_skipped_by_flag' "
        "'install ready with warnings: runtime_dependency_deferred, editor_build_skipped_by_flag'"
    )
    r = subprocess.run(
        ["bash", "-lc", cmd],
        env={
            **os.environ,
            "LEVIBE_INSTALL_LOCAL_SOURCE_ONLY": "1",
            "SCRIPT_PATH": str(script),
        },
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads((r.stdout or "").strip())
    assert payload["install_readiness_state"] == "ready_with_warnings"
    assert payload["install_readiness_reasons"] == [
        "runtime_dependency_deferred",
        "editor_build_skipped_by_flag",
    ]
    assert payload["install_readiness_summary"].startswith("install ready with warnings:")


def test_install_le_vibe_local_emit_final_json_error_summary_contract():
    script = _root() / "packaging" / "scripts" / "install-le-vibe-local.sh"
    cmd = (
        "source \"$SCRIPT_PATH\" && "
        "emit_final_json "
        "'error' 'runtime' 'ollama runtime prerequisite not ready' "
        "'ready' '/tmp/codium' '/tmp/stack.deb' '/tmp/ide.deb' "
        "'true' 'true' 'true' "
        "'error' 'ready' 'install_ollama_runtime' 'installed' 'compiled' "
        "'error' 'runtime_ollama_not_ready' "
        "'install not ready: runtime_ollama_not_ready'"
    )
    r = subprocess.run(
        ["bash", "-lc", cmd],
        env={
            **os.environ,
            "LEVIBE_INSTALL_LOCAL_SOURCE_ONLY": "1",
            "SCRIPT_PATH": str(script),
        },
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads((r.stdout or "").strip())
    assert payload["status"] == "error"
    assert payload["install_readiness_state"] == "error"
    assert payload["install_readiness_reasons"] == ["runtime_ollama_not_ready"]
    assert payload["install_readiness_summary"] == "install not ready: runtime_ollama_not_ready"


def test_install_le_vibe_local_emit_final_json_reason_order_and_trim_contract():
    script = _root() / "packaging" / "scripts" / "install-le-vibe-local.sh"
    cmd = (
        "source \"$SCRIPT_PATH\" && "
        "emit_final_json "
        "'ok' 'done' 'all steps passed' "
        "'ready' '/tmp/codium' '/tmp/stack.deb' '/tmp/ide.deb' "
        "'true' 'false' 'false' "
        "'ready' 'not_applicable' 'none' 'deferred' 'reused_existing_build' "
        "'ready_with_warnings' ' runtime_dependency_deferred ,  editor_build_skipped_by_flag  ' "
        "'install ready with warnings: runtime_dependency_deferred, editor_build_skipped_by_flag'"
    )
    r = subprocess.run(
        ["bash", "-lc", cmd],
        env={
            **os.environ,
            "LEVIBE_INSTALL_LOCAL_SOURCE_ONLY": "1",
            "SCRIPT_PATH": str(script),
        },
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads((r.stdout or "").strip())
    assert payload["install_readiness_reasons"] == [
        "runtime_dependency_deferred",
        "editor_build_skipped_by_flag",
    ]


def test_install_le_vibe_local_emit_final_json_blank_reasons_fallback_contract():
    script = _root() / "packaging" / "scripts" / "install-le-vibe-local.sh"
    cmd = (
        "source \"$SCRIPT_PATH\" && "
        "emit_final_json "
        "'ok' 'done' 'all steps passed' "
        "'ready' '/tmp/codium' '/tmp/stack.deb' '/tmp/ide.deb' "
        "'true' 'false' 'false' "
        "'ready' 'not_applicable' 'none' 'reused' 'reused_existing_build' "
        "'ready' ' ,   , ' "
        "'install ready'"
    )
    r = subprocess.run(
        ["bash", "-lc", cmd],
        env={
            **os.environ,
            "LEVIBE_INSTALL_LOCAL_SOURCE_ONLY": "1",
            "SCRIPT_PATH": str(script),
        },
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads((r.stdout or "").strip())
    assert payload["install_readiness_state"] == "ready"
    assert payload["install_readiness_reasons"] == ["none"]
    assert payload["install_readiness_summary"] == "install ready"


def test_install_le_vibe_local_build_summary_unknown_state_contract():
    script = _root() / "packaging" / "scripts" / "install-le-vibe-local.sh"
    cmd = (
        "source \"$SCRIPT_PATH\" && "
        "build_install_readiness_summary 'unexpected_state' 'none'"
    )
    r = subprocess.run(
        ["bash", "-lc", cmd],
        env={
            **os.environ,
            "LEVIBE_INSTALL_LOCAL_SOURCE_ONLY": "1",
            "SCRIPT_PATH": str(script),
        },
        capture_output=True,
        text=True,
        check=True,
    )
    assert (r.stdout or "").strip() == "install readiness unknown"


def test_install_le_vibe_local_build_summary_warning_delimiter_contract():
    script = _root() / "packaging" / "scripts" / "install-le-vibe-local.sh"
    cmd = (
        "source \"$SCRIPT_PATH\" && "
        "build_install_readiness_summary "
        "'ready_with_warnings' "
        "'runtime_dependency_deferred,editor_build_skipped_by_flag'"
    )
    r = subprocess.run(
        ["bash", "-lc", cmd],
        env={
            **os.environ,
            "LEVIBE_INSTALL_LOCAL_SOURCE_ONLY": "1",
            "SCRIPT_PATH": str(script),
        },
        capture_output=True,
        text=True,
        check=True,
    )
    assert (r.stdout or "").strip() == (
        "install ready with warnings: runtime_dependency_deferred, editor_build_skipped_by_flag"
    )


def test_install_le_vibe_local_emit_final_json_unknown_summary_default_contract():
    script = _root() / "packaging" / "scripts" / "install-le-vibe-local.sh"
    cmd = (
        "source \"$SCRIPT_PATH\" && "
        "emit_final_json "
        "'ok' 'done' 'all steps passed' "
        "'unknown' '' '' '' "
        "'false' 'false' 'false' "
        "'unknown' 'unknown' 'none' 'unknown' 'unknown' "
        "'unknown' 'none'"
    )
    r = subprocess.run(
        ["bash", "-lc", cmd],
        env={
            **os.environ,
            "LEVIBE_INSTALL_LOCAL_SOURCE_ONLY": "1",
            "SCRIPT_PATH": str(script),
        },
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads((r.stdout or "").strip())
    assert payload["install_readiness_state"] == "unknown"
    assert payload["install_readiness_reasons"] == ["none"]
    assert payload["install_readiness_summary"] == "install readiness unknown"


def test_pm_deb_build_iteration_doc_lists_install_le_vibe_local_invocation():
    text = (_root() / "docs" / "PM_DEB_BUILD_ITERATION.md").read_text(encoding="utf-8")
    assert "install-le-vibe-local.sh" in text
    assert "Local install from source" in text or "canonical local" in text.lower()


def test_editor_build_md_lists_canonical_local_installer():
    text = (_root() / "editor" / "BUILD.md").read_text(encoding="utf-8")
    assert "install-le-vibe-local.sh" in text


def test_root_readme_mentions_canonical_local_install_path():
    text = (_root() / "README.md").read_text(encoding="utf-8")
    assert "install-le-vibe-local.sh" in text
    assert "LOCAL_INSTALL_ONE_SHOT.md" in text
    assert "SHIP_REPORT_LOCAL_INSTALL.md" in text
    assert "Full local install (one command)" in text


def test_local_install_one_shot_doc_exists():
    p = _root() / "docs" / "LOCAL_INSTALL_ONE_SHOT.md"
    assert p.is_file()
    t = p.read_text(encoding="utf-8")
    assert "install-le-vibe-local.sh" in t
    assert "verify-step14-closeout.sh" in t


def test_ship_report_local_install_doc_exists():
    p = _root() / "docs" / "SHIP_REPORT_LOCAL_INSTALL.md"
    assert p.is_file()
    assert "SHIPPED" in p.read_text(encoding="utf-8")
