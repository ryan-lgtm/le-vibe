"""Contract: verify-product-branding-merge-parity.sh — read-only §7.3 jq merge check (STEP 14)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_verify_product_branding_merge_parity_script_bash_syntax() -> None:
    script = _repo_root() / "packaging" / "scripts" / "verify-product-branding-merge-parity.sh"
    assert script.is_file(), script
    assert script.stat().st_mode & 0o111, "script should be executable"
    subprocess.run(["bash", "-n", str(script)], check=True, capture_output=True)
    text = script.read_text(encoding="utf-8")
    assert "product-branding-merge.json" in text
    assert ".nameShort == \"Lé Vibe\"" in text
    assert ".linuxIconName == \"le-vibe\"" in text
