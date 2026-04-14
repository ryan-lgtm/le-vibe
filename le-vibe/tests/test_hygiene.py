"""Maintainer hygiene CLI for ``.lvibe/`` (STEP 5 — session-manifest.v1 vs ``schemas/``)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

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


def test_hygiene_warns_rag_ref_incomplete_yaml(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    ref = tmp_path / ".lvibe" / "rag" / "refs" / "topic.yaml"
    ref.write_text("path: ./README.md\n", encoding="utf-8")
    errs, warns = check_lvibe_workspace(tmp_path)
    assert errs == []
    assert any("title" in w and "topic.yaml" in w for w in warns)


def test_hygiene_warns_rag_ref_md_without_frontmatter(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    ref = tmp_path / ".lvibe" / "rag" / "refs" / "note.md"
    ref.write_text("# Title\n\nSome prose without frontmatter block.\n", encoding="utf-8")
    errs, warns = check_lvibe_workspace(tmp_path)
    assert errs == []
    assert any("frontmatter" in w.lower() and "note.md" in w for w in warns)


def test_hygiene_warns_oversize_rag_ref(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    huge = tmp_path / ".lvibe" / "rag" / "refs" / "big.yaml"
    huge.write_bytes(b"x" * (128 * 1024 + 1))
    errs, warns = check_lvibe_workspace(tmp_path)
    assert errs == []
    assert any("big.yaml" in w and "KiB" in w for w in warns)


def test_hygiene_warns_chunk_missing_path(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    chunk = tmp_path / ".lvibe" / "chunks" / "ref.yaml"
    chunk.write_text("path: ./does-not-exist-xyz\n", encoding="utf-8")
    errs, warns = check_lvibe_workspace(tmp_path)
    assert errs == []
    assert any("missing" in w.lower() for w in warns)


def test_hygiene_errors_on_bad_storage_state_json(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    st = tmp_path / ".lvibe" / "storage-state.json"
    st.write_text("{", encoding="utf-8")
    errs, _ = check_lvibe_workspace(tmp_path)
    assert any("storage-state.json" in e and "JSON" in e for e in errs)


def test_hygiene_warns_storage_state_wrong_schema(tmp_path: Path):
    ensure_lvibe_workspace(tmp_path)
    st = tmp_path / ".lvibe" / "storage-state.json"
    st.write_text(
        '{"schema":"other","cap_mb":50,"usage_bytes":0}',
        encoding="utf-8",
    )
    errs, warns = check_lvibe_workspace(tmp_path)
    assert errs == []
    assert any("lvibe-storage-state.v1" in w for w in warns)


def test_hygiene_json_mode_ok(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    ensure_lvibe_workspace(tmp_path)
    assert main(["--workspace", str(tmp_path), "--json"]) == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["errors"] == []
    assert "warnings" in data
