"""Contract: privacy + AI Pilot docs keep test_product_spec_section8 *Prioritization* Cargo cache strings."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_privacy_and_telemetry_table_lists_maintainer_full_product_deb_step14():
    """STEP 14: privacy index row points at PM deb doc + H1 vs §7.3 honesty."""
    text = (_repo_root() / "docs" / "privacy-and-telemetry.md").read_text(encoding="utf-8")
    assert "Maintainer stack + IDE" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "preflight-step14-closeout.sh" in text
    assert "ide-prereqs --print-closeout-commands" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "build machine" in text
    assert "test host" in text
    assert "Compile fail-fast" in text
    assert "packaging/scripts/ci-vscodium-bash-syntax.sh" in text
    assert "packaging/scripts/ci-editor-nvmrc-sync.sh" in text
    assert "packaging/scripts/ci-vscodium-linux-dev-build.sh" in text
    assert "./editor/smoke.sh" in text
    assert "linux_compile" in text
    assert "Partial VSCode-linux" in text
    assert "print-built-codium-path" in text
    assert "print-vsbuild-codium-path" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "build-le-vibe-ide-deb.sh --help" in text


def test_privacy_and_telemetry_e1_row_lists_linux_compile_cargo_cache():
    text = (_repo_root() / "docs" / "privacy-and-telemetry.md").read_text(encoding="utf-8")
    assert "test_product_spec_section8.py" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "actions/cache@v4" in text
    assert ".cargo" in text
    assert "spec-phase2.md" in text and "§14" in text


def test_ai_pilot_doc_lists_maintainer_full_product_deb_step14():
    """STEP 17 doc context: PM deb full-product vs default ci.yml le-vibe-deb."""
    text = (_repo_root() / "docs" / "AI_PILOT_AND_CONTINUE.md").read_text(encoding="utf-8")
    assert "Maintainer full-product" in text
    assert "PM_DEB_BUILD_ITERATION.md" in text
    assert "build-le-vibe-debs.sh --with-ide" in text
    assert "Full-product install" in text
    assert "preflight-step14-closeout.sh" in text
    assert "ide-prereqs --print-closeout-commands" in text
    assert "verify-step14-closeout.sh --require-stack-deb" in text
    assert "--apt-sim" in text
    assert "--json" in text
    assert "apt_sim_note" in text
    assert "le-vibe-deb" in text
    assert "apt-repo-releases.md" in text
    assert "H1 vs §7.3 .deb bundles" in text
    assert "build machine" in text
    assert "test host" in text
    assert "Compile fail-fast" in text
    assert "packaging/scripts/ci-vscodium-bash-syntax.sh" in text
    assert "packaging/scripts/ci-editor-nvmrc-sync.sh" in text
    assert "packaging/scripts/ci-vscodium-linux-dev-build.sh" in text
    assert "./editor/smoke.sh" in text
    assert "linux_compile" in text
    assert "Partial VSCode-linux" in text
    assert "print-built-codium-path" in text
    assert "print-vsbuild-codium-path" in text
    assert "print-step14-vscode-linux-bin-files.sh" in text
    assert "build-le-vibe-ide-deb.sh --help" in text


def test_ai_pilot_and_continue_table_lists_linux_compile_cargo_cache():
    text = (_repo_root() / "docs" / "AI_PILOT_AND_CONTINUE.md").read_text(encoding="utf-8")
    assert "test_product_spec_section8.py" in text
    assert "linux_compile" in text
    assert "ci-vscodium-bash-syntax.sh" in text
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "LEVIBE_SKIP_NODE_VERSION_CHECK" in text
    assert "fail fast" in text
    assert "vscodium-linux-build.tar.gz" in text
    assert "actions/cache@v4" in text
    assert ".cargo" in text
    assert "spec-phase2.md" in text and "§14" in text
