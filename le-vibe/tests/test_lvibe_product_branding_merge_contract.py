"""Contract: Lé Vibe product merge JSON for VSCodium prepare (STEP 14 / §7.3)."""

from __future__ import annotations

import json
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_product_branding_merge_has_lvibe_names():
    p = _repo_root() / "editor" / "le-vibe-overrides" / "product-branding-merge.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert data["nameShort"] == "Lé Vibe"
    assert data["nameLong"] == "Lé Vibe"
    assert data["linuxIconName"] == "le-vibe"
    assert data["product"]["nameShort"] == "Lé Vibe"
    assert data["product"]["nameLong"] == "Lé Vibe"
    assert data["product"]["linuxIconName"] == "le-vibe"
