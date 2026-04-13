"""STEP 12 / H8: ``product_surface_paths`` manifest."""

from __future__ import annotations

from pathlib import Path

from le_vibe.product_surface_paths import H8_MANIFEST, iter_h8_paths


def test_h8_manifest_covers_checkout():
    root = Path(__file__).resolve().parents[2]
    rows = iter_h8_paths(root)
    assert len(rows) == len(H8_MANIFEST)
    for _label, path, ok in rows:
        assert ok, path


def test_h8_paths_include_github_and_docs():
    rels = {p for _l, p in H8_MANIFEST}
    assert Path(".github/workflows/ci.yml") in rels
    assert Path("docs/privacy-and-telemetry.md") in rels
