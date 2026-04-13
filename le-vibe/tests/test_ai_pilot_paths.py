"""STEP 17: ``ai_pilot_paths`` manifest."""

from __future__ import annotations

from pathlib import Path

from le_vibe.ai_pilot_paths import H17_MANIFEST, iter_h17_paths


def test_h17_manifest_lists_three_paths():
    assert len(H17_MANIFEST) == 3
    rels = [m[1] for m in H17_MANIFEST]
    assert Path("docs/AI_PILOT_AND_CONTINUE.md") in rels


def test_iter_h17_paths_in_repo():
    root = Path(__file__).resolve().parents[2]
    rows = iter_h17_paths(root)
    assert len(rows) == 3
    assert all(ok for _l, _p, ok in rows)
