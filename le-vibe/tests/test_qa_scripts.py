"""STEP 10 / H3: monorepo discovery for ci-smoke / ci-editor-gate."""

from __future__ import annotations

from pathlib import Path

from le_vibe.qa_scripts import SMOKE_REL, find_monorepo_root


def test_find_monorepo_root_in_checkout():
    root = find_monorepo_root()
    assert root is not None
    assert (root / SMOKE_REL).is_file()


def test_le_vibe_repo_root_overrides(monkeypatch, tmp_path: Path):
    fake = tmp_path / "fake"
    fake.mkdir()
    (fake / "packaging" / "scripts").mkdir(parents=True)
    (fake / "packaging" / "scripts" / "ci-smoke.sh").write_text("#!/bin/sh\necho ok\n", encoding="utf-8")
    monkeypatch.setenv("LE_VIBE_REPO_ROOT", str(fake))
    assert find_monorepo_root() == fake.resolve()
