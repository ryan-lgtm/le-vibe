"""Contract: editor/le-vibe-overrides/build-env.sh.example stays aligned with H6 compile path (STEP 14)."""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_build_env_example_documents_upstream_dev_build_and_policy():
    text = (
        _repo_root() / "editor" / "le-vibe-overrides" / "build-env.sh.example"
    ).read_text(encoding="utf-8")
    assert "ci-vscodium-linux-dev-build.sh" in text
    assert "dev/build.sh" in text
    assert "APP_NAME" in text and "BINARY_NAME" in text
    assert "PRODUCT_SPEC" in text and ("§7.3" in text or "§7.2" in text)
    assert "USER RESPONSE REQUIRED" in text
    assert "linux_compile" in text
    assert "H6" in text
