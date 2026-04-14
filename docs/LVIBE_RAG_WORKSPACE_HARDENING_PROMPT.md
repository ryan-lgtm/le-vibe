# One-shot engineer prompt — `.lvibe/` RAG workspace hardening (repeatable)

**Audience:** Senior shipping engineers (human or agent).  
**Paste everything below the `---` into a new session.**  
**Authority:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5–§8, [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md), [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) (STEP 15 / orchestration touchpoints).

---

You are a senior shipping engineer for **Lé Vibe**. Your mission is to **solidify and harden** the **`.lvibe/`** workspace layer so that—**only when the user has opted in**—project memory, **RAG-shaped retrieval discipline**, **agent coordination**, and **sync of new project facts** are **correct, bounded, testable, and aligned with industry best practices**. Treat this as **product-critical**: behavior must be **predictable** under stress (large repos, cap pressure, non-interactive CI, secrets nearby).

## Non-negotiable product facts

1. **`.lvibe/` is consent-gated** ([`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5.1). No folder without accept; decline persists; reversible later.
2. **Default cap** (~50 MB per workspace) and **compaction order** are policy ([`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5.4–5.5). Implementation exists in `le_vibe/workspace_storage.py`—**verify, extend tests, and close gaps** vs spec (e.g. manifest protection, user-visible failure modes).
3. **Separation of concerns:** per-agent (`agents/<id>/skill.md`) vs shared retrieval (`rag/refs/`, `chunks/`) vs incremental narrative (`memory/incremental.md`) vs orchestration spine (`session-manifest.json`)—**must remain distinct** in code and docs.
4. **Continue** loads workspace rules from **`.continue/rules/`** (`le_vibe/continue_workspace.py`). Rules must stay **tight, accurate, and safe** (§7.2 user gate, §8 secrets default deny).
5. **“RAG” in this product** means **token-efficient, inspectable on-disk discipline** (small refs + rules + bounded incremental memory). **Vector/embeddings pipelines** may be **future-facing**; do not block shipping on a full embedding service, but **design extension points** (clear interfaces, no monolithic dumps in `.lvibe/`).

---

## Objectives (ship bar)

| # | Objective |
|---|-----------|
| O1 | **Consistency:** Every code path that mutates or reads `.lvibe/` agrees on layout, consent, and caps. |
| O2 | **Hardened RAG discipline:** Refs are **validated** where possible (paths exist, no secret material); **sync** of “new project facts” is **append-safe** and **idempotent** where applicable. |
| O3 | **Operator ↔ subagent coordination:** `session-manifest.json` + `agents/*/skill.md` + rules text **match** runtime behavior (`session_orchestrator`, launcher prepare path). |
| O4 | **Best practices:** Least privilege for secrets; deterministic compaction; structured logging for compaction/consent; **no silent data loss** without policy alignment ([`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5.5). |
| O5 | **Testability:** Contract tests cover consent, seeding, hygiene, storage, compaction edge cases, and Continue rule content anchors. |
| O6 | **Operator UX:** When `.lvibe/` appears, users can understand **what happened** (docs in-tree + optional CLI output). Non-interactive behavior is **explicit** (no mystery empty consent). |

---

## Scope — IN

Implement, refine, or add **as needed** (audit first):

1. **`le_vibe/workspace_consent.py`** — Prompt copy, env overrides, persistence, non-TTY behavior, structured logs.
2. **`le_vibe/workspace_hub.py`** — Seeding order, directory layout, `ensure_gitignore_has_lvibe`, integration with session + Continue + welcome.
3. **`le_vibe/workspace_storage.py`** — Metering, `storage-state.json`, compaction vs [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5.5; **harden** edge cases (empty tree, permission errors, still-over-cap warning).
4. **`le_vibe/workspace_policy.py`** — Caps, per-workspace overrides, env (`LE_VIBE_LVIBE_CAP_MB` etc.) documented and tested.
5. **`le_vibe/continue_workspace.py`** — Rule bodies: memory anchor, welcome, **RAG/agent/session** instructions; **remove drift** vs `PRODUCT_SPEC`; ensure **§7.2** / **§8** strings remain contract-tested.
6. **`le_vibe/session_orchestrator.py`** — Manifest seeding, `iter_tasks_in_epic_order`, skill sync; **no overwrite** of user edits.
7. **`le_vibe/hygiene.py`** — Validates manifests, session JSON, chunk path refs; extend if new RAG ref schema added.
8. **Launcher integration** — `launcher.py` paths that call `prepare_workspaces_for_editor_args`; ensure consent + prepare run **once** per open, correct roots.
9. **Documentation** — Short **user-facing** note in packaged / repo docs: when `.lvibe/` appears, what’s inside, cap, gitignore—**without** bloating root [`README.md`](../README.md) (use [`le-vibe/README.md`](../le-vibe/README.md) or [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) as appropriate).
10. **Optional “sync” helper (if justified)** — e.g. CLI or library function to **append** a small verified fact to `memory/incremental.md` or a ref file under `rag/refs/` with **schema validation**; must be **idempotent** or **explicitly duplicate-safe** per product decision.

---

## Scope — OUT (unless blocker)

- Apt/repo publishing, `install-le-vibe-local.sh`, IDE compile pipeline.
- Replacing Continue with another chat stack.
- Full managed embedding service / cloud vector DB (stub interfaces OK).

---

## Industry best practices to apply

1. **Data minimization** — Only store what agents need; **references** not secret values ([`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §8).
2. **Explicit consent & transparency** — User knows folder exists, size budget, and how to remove/disable.
3. **Integrity** — Hygiene checks for JSON/YAML; invalid files **surface errors**, not silent skip.
4. **Deterministic compaction** — Document order; log actions; **never delete** `session-manifest.json` without replacement policy compliance.
5. **Idempotency** — Seeding commands safe to re-run; no duplicate corrupt state.
6. **Defense in depth** — Rules + runtime paths + tests aligned.
7. **Observability** — Use existing `structured_log` for consent, compaction, and storage events (no third-party telemetry).

---

## RAG / “project sync” hardening (concrete)

1. **Define or tighten a minimal ref format** for `rag/refs/` (e.g. frontmatter: `title`, `path` (repo-relative), `summary`, `updated`)—**small files only**; reject or warn on oversize in hygiene.
2. **`memory/incremental.md`** — Document max recommended entry size; optional warning in `lvibe-hygiene` when file exceeds threshold.
3. **Agent skill files** — Templates in `le-vibe/templates/agents/` stay **bounded**; compaction behavior documented.
4. **Session manifest** — Schema alignment with `schemas/session-manifest.v1.example.json`; contract tests on invalid manifest handling.

---

## Testing requirements

- Extend **`le-vibe/tests/`** with focused tests: consent matrix (TTY/non-TTY/env), compaction edge cases, hygiene on bad refs, Continue rule snapshots where appropriate.
- Run **`cd le-vibe && python3 -m pytest tests/`** — **all green** before ship.
- Update **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** *Last verified* / relevant rows if behavior or acceptance shifts (E1 bar).

---

## Loop / stop control

- **Loop:** audit → implement → pytest → fix → repeat.
- **Max 3** fix attempts per **distinct** failure class; then stop with evidence and **numbered questions** for product.
- **Stop when:** O1–O6 satisfied, tests green, docs updated, and you can write a **Ship note** (below). **Do not** start unrelated epics.

---

## Deliverables (must paste back)

1. **Delta summary** — Files touched, rationale.
2. **Test transcript** — `pytest` command + pass summary.
3. **Ship note** — “`.lvibe/` RAG workspace hardening: SHIPPED” with:
   - consent behavior summary
   - cap/compaction summary
   - RAG ref + incremental memory rules
   - known limitations / follow-ups
4. **Risk list** — What is **not** vector-RAG yet; what a future embedding layer would plug into.

---

## Start

Begin with a **read-only audit** (half page): map current behavior vs [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5–§5.6 and list gaps. Then implement in **small commits** (or one logical PR), tests first where TDD helps.

**Session complete only when** the Ship note criteria are met and pytest is green.

---

*This file is the canonical copy of the prompt; paste from here into engineer/agent sessions.*
