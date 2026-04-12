"""Maintainer hygiene CLI for ``.lvibe/`` (STEP 5 — session-manifest.v1 vs ``schemas/``)."""

from __future__ import annotations

import json
from pathlib import Path

from le_vibe.hygiene import check_lvibe_workspace, main
from le_vibe.session_orchestrator import SESSION_MANIFEST_FILENAME
from le_vibe.workspace_hub import ensure_lvibe_workspace


def test_hygiene_ok_on_prepared_workspace(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    errs, warns = check_lvibe_workspace(tmp_path)
    assert errs == []
    assert main(["--workspace", str(tmp_path)]) == 0


def test_hygiene_fails_without_lvibe(tmp_path: Path):
    errs, warns = check_lvibe_workspace(tmp_path)
    assert any("no .lvibe/" in e for e in errs)
    assert main(["--workspace", str(tmp_path)]) == 1


def test_hygiene_module_docstring_points_at_schema_and_spec():
    import le_vibe.hygiene as h

    assert "schemas/session-manifest.v1.example.json" in (h.__doc__ or "")
    assert "SESSION_ORCHESTRATION_SPEC" in (h.__doc__ or "")


def test_hygiene_errors_on_bad_session_json(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    sm = tmp_path / ".lvibe" / SESSION_MANIFEST_FILENAME
    sm.write_text("{ not json", encoding="utf-8")
    errs, _ = check_lvibe_workspace(tmp_path)
    assert any("invalid JSON" in e for e in errs)
    assert main(["-w", str(tmp_path)]) == 1


def test_hygiene_seed_missing_restores_session_manifest(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    sm = tmp_path / ".lvibe" / SESSION_MANIFEST_FILENAME
    sm.unlink()
    assert not sm.exists()
    assert main(["--workspace", str(tmp_path), "--seed-missing"]) == 0
    assert sm.is_file()


def test_hygiene_seed_missing_skips_without_lvibe_dir(tmp_path: Path):
    code = main(["-w", str(tmp_path), "--seed-missing"])
    assert code == 1


def test_hygiene_warns_chunk_missing_path(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    chunk = tmp_path / ".lvibe" / "chunks" / "ref.yaml"
    chunk.write_text("path: ./does-not-exist-xyz\n", encoding="utf-8")
    errs, warns = check_lvibe_workspace(tmp_path)
    assert errs == []
    assert any("missing" in w.lower() for w in warns)
