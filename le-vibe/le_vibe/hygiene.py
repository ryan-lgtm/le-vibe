"""Maintainer checks for ``.lvibe/`` — manifest, session-manifest, storage-state, chunks.

Session JSON is expected to match ``schemas/session-manifest.v1.example.json`` (see
``docs/SESSION_ORCHESTRATION_SPEC.md``; STEP 5 / E4, PM map). Optional ``storage-state.json``
is checked for ``lvibe-storage-state.v1`` (PRODUCT_SPEC §5.4). Files under ``rag/refs/`` warn
when over ~128KiB (small-ref discipline). ``rag/refs/*.md`` / ``*.yaml`` should use optional YAML
frontmatter with ``title``, ``path`` (repo-relative), ``summary``, and ``updated`` (warnings if
missing). Use ``--seed-missing`` to idempotently add a missing
``session-manifest.json`` and agent ``skill.md`` files; ``--json`` for machine-readable reports.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from .session_orchestrator import SESSION_MANIFEST_FILENAME

# Loose ``path:`` capture in chunk YAML (single-line values).
_CHUNK_PATH_LINE = re.compile(r"^\s*path:\s*(.+?)\s*$", re.MULTILINE)


def _manifest_yaml_sanity(path: Path) -> str | None:
    """Return error string if ``manifest.yaml`` looks broken; None if OK or skip."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return f"manifest.yaml: cannot read ({e})"
    if not text.strip():
        return "manifest.yaml: empty"
    if "version:" not in text and "purpose:" not in text:
        return "manifest.yaml: expected keys like version/purpose (hub convention)"
    return None


def _session_manifest_checks(lvibe: Path, workspace: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    sm = lvibe / SESSION_MANIFEST_FILENAME
    if not sm.is_file():
        warnings.append(f"{SESSION_MANIFEST_FILENAME} missing (run lvibe . or sync from example)")
        return errors, warnings
    try:
        data = json.loads(sm.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"{SESSION_MANIFEST_FILENAME}: invalid JSON ({e})")
        return errors, warnings
    if data.get("schema_version") != "session-manifest.v1":
        warnings.append(
            f"{SESSION_MANIFEST_FILENAME}: schema_version is not session-manifest.v1 (got {data.get('schema_version')!r})"
        )
    if not isinstance(data.get("session_steps"), list) or not data["session_steps"]:
        errors.append(f"{SESSION_MANIFEST_FILENAME}: session_steps must be a non-empty array")
    product = data.get("product")
    if not isinstance(product, dict) or "epics" not in product:
        warnings.append(f"{SESSION_MANIFEST_FILENAME}: product.epics missing or malformed")
    # Skill files referenced from manifest
    agents = data.get("agents") or {}
    roles = agents.get("roles") or []
    if isinstance(roles, list):
        for r in roles:
            if not isinstance(r, dict):
                continue
            rel = r.get("skill_path")
            if isinstance(rel, str) and rel.startswith(".lvibe/"):
                clean = rel.removeprefix(".lvibe/").lstrip("/")
                target = lvibe / clean
                if not target.is_file():
                    warnings.append(f"skill_path not present: {rel} (sync agents or fix manifest)")
    return errors, warnings


def _chunk_path_references(lvibe: Path, workspace: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for sub in ("chunks", "rag"):
        subroot = lvibe / sub
        if not subroot.is_dir():
            continue
        for f in sorted(subroot.rglob("*")):
            if not f.is_file():
                continue
            if f.suffix.lower() not in (".yaml", ".yml", ".md"):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError as e:
                warnings.append(f"{f.relative_to(lvibe)}: read failed ({e})")
                continue
            for m in _CHUNK_PATH_LINE.finditer(text):
                raw = m.group(1).strip().strip("\"'")
                if not raw or raw.startswith("#"):
                    continue
                candidate = (workspace / raw).resolve()
                try:
                    workspace_resolved = workspace.resolve()
                except OSError:
                    workspace_resolved = workspace
                if not str(candidate).startswith(str(workspace_resolved)):
                    warnings.append(f"{f.relative_to(lvibe)}: path {raw!r} escapes workspace")
                    continue
                if not candidate.exists():
                    warnings.append(f"{f.relative_to(lvibe)}: referenced path missing: {raw}")
    return errors, warnings


_RAG_REF_OVERSIZE_BYTES = 128 * 1024
_RAG_REF_SCHEMA_KEYS = ("title", "path", "summary", "updated")
_INCREMENTAL_SOFT_WARN_BYTES = 64 * 1024

# Rough “looks like a secret literal” (PRODUCT_SPEC §8 — refs only, no values).
_SECRETISH_LINE = re.compile(
    r"(?i)(password|api_key|apikey|secret|client_secret|access_token)\s*[:=]\s*['\"]?[^\s'\"#]{16,}"
)


def _parse_md_frontmatter_keys(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    keys: dict[str, str] = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            for j in range(1, i):
                line = lines[j]
                if ":" not in line or line.strip().startswith("#"):
                    continue
                k, _, v = line.partition(":")
                keys[k.strip()] = v.strip().strip("\"'")
            return keys
    return None


def _top_level_yaml_scalar_keys(text: str, *, max_lines: int = 100) -> dict[str, str]:
    keys: dict[str, str] = {}
    for line in text.splitlines()[:max_lines]:
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("---"):
            break
        if s.startswith("-") or ":" not in s:
            continue
        k, _, v = line.partition(":")
        keys[k.strip()] = v.strip().strip("\"'")
    return keys


def _rag_refs_schema_warnings(lvibe: Path) -> list[str]:
    """Minimal ref shape: ``title``, ``path``, ``summary``, ``updated`` (warnings only)."""
    warnings: list[str] = []
    refs = lvibe / "rag" / "refs"
    if not refs.is_dir():
        return warnings
    for f in sorted(refs.rglob("*")):
        if not f.is_file():
            continue
        suf = f.suffix.lower()
        if suf not in (".yaml", ".yml", ".md", ".txt"):
            continue
        try:
            n = f.stat().st_size
        except OSError:
            continue
        if n > _RAG_REF_OVERSIZE_BYTES:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            warnings.append(f"{f.relative_to(lvibe)}: read failed ({e})")
            continue
        if _SECRETISH_LINE.search(text):
            warnings.append(
                f"{f.relative_to(lvibe)}: possible secret-like literal — use references only (PRODUCT_SPEC §8)"
            )
        rel = f.relative_to(lvibe)
        if suf == ".txt":
            warnings.append(
                f"{rel}: prefer .md or .yaml with optional frontmatter (title, path, summary, updated)"
            )
            continue
        if suf == ".md":
            fm = _parse_md_frontmatter_keys(text)
            if fm is None:
                if len(text.strip()) > 20:
                    warnings.append(
                        f"{rel}: add YAML frontmatter with title, path, summary, updated (Lé Vibe rag ref convention)"
                    )
                continue
            for key in _RAG_REF_SCHEMA_KEYS:
                if key not in fm or not str(fm.get(key, "")).strip():
                    warnings.append(f"{rel}: frontmatter missing or empty `{key}`")
            continue
        # .yaml / .yml
        keys = _top_level_yaml_scalar_keys(text)
        if not keys and text.strip():
            warnings.append(f"{rel}: expected top-level keys title, path, summary, updated")
            continue
        for key in _RAG_REF_SCHEMA_KEYS:
            if key not in keys or not str(keys.get(key, "")).strip():
                warnings.append(f"{rel}: missing or empty `{key}`")
    return warnings


def _incremental_size_warning(lvibe: Path) -> list[str]:
    warnings: list[str] = []
    inc = lvibe / "memory" / "incremental.md"
    if inc.is_file():
        n = inc.stat().st_size
        if n > 512 * 1024:
            warnings.append(f"memory/incremental.md is {n // 1024}KiB — consider summarizing (token efficiency)")
        elif n > _INCREMENTAL_SOFT_WARN_BYTES:
            warnings.append(
                f"memory/incremental.md is {n // 1024}KiB — keep individual entries short (~2KiB recommended)"
            )
    return warnings


def _rag_refs_oversize_warnings(lvibe: Path) -> list[str]:
    """Small-file discipline for ``rag/refs/`` (PRODUCT_SPEC §5.2 — token-efficient on-disk RAG)."""
    warnings: list[str] = []
    refs = lvibe / "rag" / "refs"
    if not refs.is_dir():
        return warnings
    for f in sorted(refs.rglob("*")):
        if not f.is_file():
            continue
        if f.suffix.lower() not in (".yaml", ".yml", ".md", ".txt"):
            continue
        n = f.stat().st_size
        if n > _RAG_REF_OVERSIZE_BYTES:
            warnings.append(
                f"{f.relative_to(lvibe)} is {n // 1024}KiB — split or summarize (rag ref size budget)"
            )
    return warnings


def _storage_state_checks(lvibe: Path) -> tuple[list[str], list[str]]:
    """Validate ``storage-state.json`` when present (PRODUCT_SPEC §5.4 — STEP 5 / E4)."""
    errors: list[str] = []
    warnings: list[str] = []
    p = lvibe / "storage-state.json"
    if not p.is_file():
        return errors, warnings
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"storage-state.json: invalid JSON ({e})")
        return errors, warnings
    if not isinstance(data, dict):
        errors.append("storage-state.json: root must be an object")
        return errors, warnings
    if data.get("schema") != "lvibe-storage-state.v1":
        warnings.append(
            f"storage-state.json: expected schema lvibe-storage-state.v1 (got {data.get('schema')!r})"
        )
    for key in ("cap_mb", "usage_bytes"):
        if key in data and not isinstance(data[key], int):
            warnings.append(f"storage-state.json: {key} should be int")
    return errors, warnings


def seed_missing_pm_artifacts(workspace_root: Path) -> list[str]:
    """
    If ``.lvibe/`` exists, seed ``session-manifest.json`` when absent and copy any missing
    ``agents/<id>/skill.md`` from templates (same as workspace prepare — STEP 2 / STEP 5).

    Does **not** create ``.lvibe/`` (consent/product flows own that).
    """
    from .session_orchestrator import (
        seed_session_manifest_if_missing,
        sync_agent_skills_from_templates,
    )

    lv = workspace_root / ".lvibe"
    if not lv.is_dir():
        return ["skip: no .lvibe/ (run lvibe . after consent, or create the hub first)"]
    messages: list[str] = []
    seeded = seed_session_manifest_if_missing(lv)
    if seeded is not None:
        messages.append(f"seeded {SESSION_MANIFEST_FILENAME}")
    written = sync_agent_skills_from_templates(lv)
    if written:
        messages.append(f"synced {len(written)} missing agent skill file(s)")
    if not messages:
        messages.append(f"{SESSION_MANIFEST_FILENAME} and agent skills already present")
    return messages


def check_lvibe_workspace(workspace_root: Path) -> tuple[list[str], list[str]]:
    """
    Validate ``workspace_root/.lvibe/`` for maintainer hygiene.
    Returns ``(errors, warnings)`` — non-empty errors should fail CI / exit 1.
    """
    errors: list[str] = []
    warnings: list[str] = []
    lvibe = workspace_root / ".lvibe"
    if not lvibe.is_dir():
        errors.append(f"no .lvibe/ under {workspace_root}")
        return errors, warnings

    mf = lvibe / "manifest.yaml"
    if mf.is_file():
        err = _manifest_yaml_sanity(mf)
        if err:
            errors.append(err)
    else:
        warnings.append("manifest.yaml missing")

    e1, w1 = _session_manifest_checks(lvibe, workspace_root)
    errors.extend(e1)
    warnings.extend(w1)

    e2, w2 = _chunk_path_references(lvibe, workspace_root)
    errors.extend(e2)
    warnings.extend(w2)
    warnings.extend(_incremental_size_warning(lvibe))
    warnings.extend(_rag_refs_oversize_warnings(lvibe))
    warnings.extend(_rag_refs_schema_warnings(lvibe))

    e3, w3 = _storage_state_checks(lvibe)
    errors.extend(e3)
    warnings.extend(w3)

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Lé Vibe: validate .lvibe/ manifest, session-manifest JSON (session-manifest.v1), "
            "and chunk path refs — see schemas/session-manifest.v1.example.json and SESSION_ORCHESTRATION_SPEC.md."
        ),
    )
    p.add_argument(
        "--workspace",
        "-w",
        type=Path,
        default=Path.cwd(),
        help="workspace root containing .lvibe/ (default: current directory)",
    )
    p.add_argument(
        "--seed-missing",
        action="store_true",
        help=(
            "If .lvibe/ exists, copy canonical session-manifest when missing and sync missing "
            "agent skill.md files from le-vibe/templates/agents/ (idempotent). Then run checks."
        ),
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Print errors and warnings as a JSON object on stdout (exit 1 if any errors).",
    )
    args = p.parse_args(argv)
    try:
        root = args.workspace.expanduser().resolve()
    except OSError as e:
        print(f"lvibe-hygiene: bad --workspace: {e}", file=sys.stderr)
        return 2
    seed_log: list[str] = []
    if args.seed_missing:
        seed_log = seed_missing_pm_artifacts(root)
        if not args.json:
            for line in seed_log:
                print(f"lvibe-hygiene: {line}", file=sys.stdout)
    errs, warns = check_lvibe_workspace(root)
    if args.json:
        payload: dict[str, object] = {"errors": errs, "warnings": warns}
        if seed_log:
            payload["seed"] = seed_log
        print(json.dumps(payload, indent=2, ensure_ascii=False), file=sys.stdout)
        return 1 if errs else 0
    for w in warns:
        print(f"warning: {w}", file=sys.stderr)
    for e in errs:
        print(f"error: {e}", file=sys.stderr)
    if errs:
        return 1
    print("lvibe-hygiene: OK", file=sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
