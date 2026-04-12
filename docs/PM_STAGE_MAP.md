# PM stage map — orchestrator queue → product management docs

Engineers and **auto-style** agents **open the listed PM doc first** for the **stage** they are executing, then implementation files. This keeps work **aligned** with product intent and avoids orphan code.

**Rule:** **`docs/PRODUCT_SPEC.md`** wins on conflict unless a stage note says otherwise.

**Spec index:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §9 (*Relationship to existing specs*) lists **`PROMPT_BUILD_LE_VIBE.md`**, **`SESSION_ORCHESTRATION_SPEC.md`**, **`PRODUCT_SPEC_SECTION8_EVIDENCE.md`**, **`AI_PILOT_AND_CONTINUE.md`**, and this map—use it when navigating across authority docs.

**E1 (STEP 1):** [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md) is the **§1** (naming / **H8**) + §5–§10 audit; run **[`le-vibe/tests/`](../le-vibe/tests/)** in a clone. **Full E1 module roster** — root [`README.md`](../README.md) *Tests* / **E1 mapping**; [`spec-phase2.md`](../spec-phase2.md) §14 *Honesty vs CI*. [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md) (intro) and [`AI_PILOT_AND_CONTINUE.md`](AI_PILOT_AND_CONTINUE.md) (§4) name representative contract tests alongside orchestration intent.

**E1 (STEP 12 — H8):** Editing **[`.github/workflows/ci.yml`](../.github/workflows/ci.yml)**, **[`.github/dependabot.yml`](../.github/dependabot.yml)**, or **[`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/)** (incl. **[`config.yml`](../.github/ISSUE_TEMPLATE/config.yml)** **`#` H8** comments) — refresh **[`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md)** §10 (*Roadmap H8* checklist), **[`docs/README.md`](README.md)** *Product surface*, and **[`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §10** opening regression paragraph (issue-template / **`pytest`** honesty) so **PRODUCT_SPEC** / **§9** / **`README.Debian`** / **§14** pointers stay accurate; keep **`privacy-and-telemetry`** (*E1 contract tests*) + **[`SECURITY.md`](../SECURITY.md)** *Related docs* in sync — including the optional **[`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md)** pointer (*RAG / embeddings*, non-canonical; **`spec-phase2.md`**) — (**`pytest`** does not cover YAML intros).

**Maintainer index (Roadmap H1–H8):** [`README.md`](README.md) (per **`PRODUCT_SPEC` §9** *Maintainer index*) — distribution, trust, and product-surface guides referenced by this map’s H rows.

**`.deb` / `apt`:** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) installs as **`/usr/share/doc/le-vibe/README.Debian`** — operator-facing summary when work intersects packaged installs (post-install, **§5** **`.lvibe/`** consent).

**Phase 2 vs this repo:** **[`spec-phase2.md`](../spec-phase2.md) §14** — **monorepo:** **`editor/`** (**H6**) + **`le-vibe/`** stack; **H7** may stay SKIPPED. **STEP 13** = Flatpak policy; **STEP 14** = **`editor/`** IDE shell—not an external repository.

**Execution order ([`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) Master orchestrator):** **0 → 1 → 14 → 2–13 → 15–17** — the **Lé Vibe IDE** (`editor/`) is **next after baseline regression** until STEP 14 is satisfied or explicitly gated.

| Master orchestrator STEP | Primary PM / product doc | Also read |
|---------------------------|---------------------------|-----------|
| 0 — MUST baseline | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §§1–8, §10 | [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md) |
| 1 — E1 regression | [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md), [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §10 | Tests under `le-vibe/tests/`; root [`README.md`](../README.md) *Tests* / **E1 mapping**; [`spec-phase2.md`](../spec-phase2.md) §14 *Honesty vs CI* |
| **14 — H6 IDE** | [`vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md), [`editor/README.md`](../editor/README.md), [`editor/BUILD.md`](../editor/BUILD.md), [`editor/VENDORING.md`](../editor/VENDORING.md), [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) *Prioritization* | [`editor/le-vibe-overrides/README.md`](../editor/le-vibe-overrides/README.md) (**E1:** [`test_editor_le_vibe_overrides_readme_contract.py`](../le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py)); **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** (**E1:** [`test_build_le_vibe_ide_workflow_contract.py`](../le-vibe/tests/test_build_le_vibe_ide_workflow_contract.py) — **`ide-ci-metadata.txt`**, Actions run **Summary** **Pre-binary artifact** / **`le_vibe_editor_docs`** ↔ **`LE_VIBE_EDITOR`**); [`spec-phase2.md`](../spec-phase2.md) §2 + §14; [`ci-qa-hardening.md`](ci-qa-hardening.md) (**H6** — **`./editor/smoke.sh`** vs stack **`ci-smoke.sh`**); **[`build-linux.yml`](../.github/workflows/build-linux.yml)** (alias → **`build-le-vibe-ide`**) |
| 2 — PM session | [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md), [`schemas/session-manifest.v1.example.json`](../schemas/session-manifest.v1.example.json) | `le_vibe/session_orchestrator.py` |
| 3 — Continue / `.lvibe/` | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5–7, [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md) §5 | `le_vibe/continue_workspace.py` |
| 4 — In-editor welcome | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §4 | `le_vibe/continue_workspace.py`, `editor_welcome.py` |
| 5 — Maintainer hygiene | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5 | `le_vibe/hygiene.py` |
| 6 — Observability | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §7, [`privacy-and-telemetry.md`](privacy-and-telemetry.md) | `le_vibe/structured_log.py`, `README.md` |
| 7 — H4 Continue pin | [`continue-extension-pin.md`](continue-extension-pin.md) | `packaging/scripts/` |
| 8 — H1 releases | [`apt-repo-releases.md`](apt-repo-releases.md), [`CHANGELOG.md`](../CHANGELOG.md) | `.github/workflows/` |
| 9 — H2 SBOM / audit | [`sbom-signing-audit.md`](sbom-signing-audit.md) | CI workflow (**H8** in **`ci.yml`** header); [`.github/dependabot.yml`](../.github/dependabot.yml) (weekly **pip** / **Actions** PRs; **H8** in YAML header) |
| 10 — H3 QA CI | [`ci-qa-hardening.md`](ci-qa-hardening.md) | `packaging/scripts/ci-smoke.sh` |
| 11 — H5 brand | [`brand-assets.md`](brand-assets.md) | `packaging/icons/`; [`screenshots/README.md`](screenshots/README.md) (optional marketing captures); **§1** + **H8** **`.github/`** copy (*Naming (must ship)* in **brand-assets**) |
| 12 — H8 product surface | [`README.md`](../README.md) (docs index), this folder | **`.github/`** — workflows, **Dependabot**, **`ISSUE_TEMPLATE/`** + **`config.yml`** **`#` H8**; `docs/privacy-and-telemetry.md` |
| 13 — H7 Flatpak/AppImage | [`flatpak-appimage.md`](flatpak-appimage.md) | Policy: often **SKIPPED** in-repo |
| 15 — `.lvibe/` governance | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §5.1–5.6 | `le_vibe/workspace_hub.py`, consent paths |
| **16** — PM map + doc-locked loop | **This file** [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md), [`AI_PILOT_AND_CONTINUE.md`](AI_PILOT_AND_CONTINUE.md) | [`PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md) |
| **17** — AI Pilot & Continue (contracts) | [`AI_PILOT_AND_CONTINUE.md`](AI_PILOT_AND_CONTINUE.md), [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §7 | Continue rules, `README.md` UX copy |
| **Any STEP** — user gate | [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) **§7.2**, [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md) **§5.1** | Halt + **`USER RESPONSE REQUIRED`** + numbered Q&A |

---

*Update this table when STEPs or docs change.*

**STEP 16 — example JSON:** [`schemas/session-manifest.v1.example.json`](../schemas/session-manifest.v1.example.json) includes optional **`meta.continue_construction_note`** / **`meta.ai_pilot_note`** (documented in [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md) §3.1).
