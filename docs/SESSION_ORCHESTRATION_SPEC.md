# Lé Vibe — session orchestration & PM-driven manifests

This document specifies the **session manifest JSON**, **SESSION STEPS**, **skill agents**, and how the **master orchestrator** uses **RAG-oriented context** so multiple agents coordinate like a modern SaaS product org.

**Cursor / build loop (same routing idea):** [`docs/MASTER_ITERATION_LOOP.md`](MASTER_ITERATION_LOOP.md) — one paste-ready prompt for **ENGINEER** ↔ **PRODUCT_MANAGER** with lean manuscript pointers and **new-agent** chats (`packaging/scripts/print-master-iteration-loop-prompt.py`).

It applies in **two places**:

| Context | Where it lives | Purpose |
|---------|----------------|---------|
| **Building Lé Vibe** (this repo) | `schemas/session-manifest.v1.example.json`, `schemas/session-manifest.step14-closeout.v1.example.json` (optional **STEP 14** backlog seed), `le-vibe/templates/agents/*.md` | Dogfood the same format while developing the product; CI and docs reference these paths. **STEP 14 autonomous engineer kit:** [`STEP14_AUTONOMOUS_ENGINEER_RUNBOOK.md`](STEP14_AUTONOMOUS_ENGINEER_RUNBOOK.md). |
| **User workspace** | `.lvibe/session-manifest.json`, `.lvibe/agents/<agent_id>/skill.md` | Same schema and agent skills; orchestrator and Continue/agent rules read from here. |

**Master orchestrator STEP 2 (PM session):** Seed **`session-manifest.json`** from **`schemas/session-manifest.v1.example.json`** when running from a clone (**`session_manifest_example_source_path`**), else the bundled example (same JSON — must match **`schemas/`**), copy **`le-vibe/templates/agents/*.md`** into **`.lvibe/agents/<agent_id>/skill.md`**, expose **`session_steps`** / **`product.epics`** iteration, and implement **`opening_intent` → skip → `workspace_scan`** via **`apply_opening_skip`** — **`le_vibe.session_orchestrator`** (**`ensure_pm_session_artifacts`** from workspace prepare). E1: **`le-vibe/tests/test_session_orchestrator.py`**. This is separate from **STEP 14** **H6** (**`editor/`** IDE shell); **`spec-phase2.md` §14** tracks IDE binary / build branding honesty.

**Product authority:** complements **`docs/PRODUCT_SPEC.md`**. Naming: **Lé Vibe** in prose; ASCII paths under **`.lvibe/`**. **Continue / AI Pilot** intent: **`docs/AI_PILOT_AND_CONTINUE.md`**. **Per-stage PM docs:** **`docs/PM_STAGE_MAP.md`**. **Spec index (orchestrator + E1 evidence):** **`docs/PRODUCT_SPEC.md` §9** — regression mapping and tests: **`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`** (**§1**/**H8** + §5–§10), **`le-vibe/tests/`** (e.g. **`test_session_orchestrator.py`**, **`test_session_orchestration_spec_step2_contract.py`** (this intro + **STEP 2**), **`test_continue_workspace.py`**, **`test_le_vibe_readme_e1_contract.py`**, **`test_editor_le_vibe_overrides_readme_contract.py`**, **`test_build_le_vibe_ide_workflow_contract.py`** — **STEP 14** / **H6**).

**Maintainer index (Roadmap H1–H8):** [`README.md`](README.md) — distribution / trust / product-surface guides, named from **`PRODUCT_SPEC` §9** (*Maintainer index*).

**H8 / trust (CI, Dependabot, ISSUE_TEMPLATE/ + config.yml # H8 & reporting):** [`docs/README.md`](README.md) *Product surface* — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** ([`config.yml`](../.github/ISSUE_TEMPLATE/config.yml) **`#` H8** maintainer lines), [`privacy-and-telemetry.md`](privacy-and-telemetry.md) (*E1 contract tests*), [`SECURITY.md`](../SECURITY.md) (*Related docs*, incl. optional [`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md) for *RAG / embeddings* — non-canonical; **[`spec-phase2.md`](../spec-phase2.md)**); **[`docs/PM_STAGE_MAP.md`](PM_STAGE_MAP.md) STEP 12** *E1* when editing reporter intros or workflow headers.

**`.deb` / `apt`:** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) installs as **`/usr/share/doc/le-vibe/README.Debian`** — post-install flow and **§5** workspace memory consent before **`.lvibe/`** on packaged hosts.

**Maintainer full-product `.deb` (STEP 14 / §7.3):** **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** — **`packaging/scripts/build-le-vibe-debs.sh --with-ide`** prints **Full-product install** on success; **preflight (optional):** **`packaging/scripts/preflight-step14-closeout.sh --require-stack-deb`** or **`lvibe ide-prereqs --print-closeout-commands`** — **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Preflight (all gaps)*); **local close-out gate:** **`packaging/scripts/verify-step14-closeout.sh --require-stack-deb`** (add **`--apt-sim`** for explicit dependency simulation, **`--json`** for machine-readable close-out output — **`apt_sim_note`**, **`desktop_file_validate`** (`ran` \| `skipped` on packaged **`le-vibe.desktop`**) — **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*`--json` close-out payload*)); default **[`ci.yml`](../.github/workflows/ci.yml)** artifact **`le-vibe-deb`** is **stack-only** — **[`apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package*); **[`PM_STAGE_MAP.md`](PM_STAGE_MAP.md)** (*H1 vs §7.3 .deb bundles*). **Ordering:** **build machine** close-out, **test host** install/smoke — **[`apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package*); on the test host after **`apt install`**, **`packaging/scripts/manual-step14-install-smoke.sh --json`** (**`desktop_file_validate_on_path`**) and **`manual-step14-install-smoke.sh --verify-only`** (optional **`desktop-file-validate`** on **`le-vibe.desktop`**) — **[`apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package*), **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Success output (`--with-ide`)*). **Compile fail-fast:** **`packaging/scripts/ci-vscodium-bash-syntax.sh`** → **`packaging/scripts/ci-editor-nvmrc-sync.sh`** → **`packaging/scripts/ci-vscodium-linux-dev-build.sh`** (same as **`./editor/smoke.sh`** / **`linux_compile`**) — **[`apt-repo-releases.md`](apt-repo-releases.md)** (*IDE package*), **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Compile fail-fast*). **Partial VSCode-linux** (missing **`bin/codium`**) — **[`editor/BUILD.md`](../editor/BUILD.md)** (*Partial tree*, **14.c**); **[`PM_DEB_BUILD_ITERATION.md`](PM_DEB_BUILD_ITERATION.md)** (*Partial VSCode-linux tree*); **`./editor/print-built-codium-path.sh`**, **`./editor/print-vsbuild-codium-path.sh`**, **`./packaging/scripts/print-step14-vscode-linux-bin-files.sh`** (**`--help`**; **`vscode_linux_bin_files`** vs **`lvibe ide-prereqs --json`**); **`./packaging/scripts/build-le-vibe-ide-deb.sh --help`** (triage + **`verify-step14-closeout.sh`**).

**Phase 2 vs this tree:** Session manifests and agents apply to **workspace** **`.lvibe/`** and **Continue** in this document. The **Lé Vibe IDE** desktop shell (Code OSS / **VSCodium** build, CI, packaging) is owned under **`editor/`** — **[`editor/README.md`](../editor/README.md)**, **[`editor/BUILD.md`](../editor/BUILD.md)**, **[`docs/vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md)** (**H6**); **H7** templates (**`packaging/flatpak/`**, **`packaging/appimage/`**, **[`docs/flatpak-appimage.md`](flatpak-appimage.md)**) — **[`spec-phase2.md`](../spec-phase2.md) §14**. PM epics that ship the **shell** alongside the stack should treat **`editor/`** work as **P0** with **`le-vibe/`** — local **H6** smoke (no Electron compile): **`./editor/smoke.sh`** from the monorepo root; stack vs IDE CI split — **[`docs/ci-qa-hardening.md`](ci-qa-hardening.md)** (*IDE smoke*). **14.d:** [`branding-staging.checklist.md`](../editor/le-vibe-overrides/branding-staging.checklist.md) — read *PRODUCT_SPEC §7.2 (read before overrides)* first ([**`PRODUCT_SPEC.md`**](PRODUCT_SPEC.md) §7.2); fast smoke ≠ Lé Vibe–visible IDE branding; **[`editor/README.md`](../editor/README.md)** *14.c vs 14.d*. **GitHub:** **[`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml)** (pre-binary **`ide-ci-metadata.txt`** on the default **`linux` job**; optional **`linux_compile`** — not default on **`pull_request`** — runs **`ci-vscodium-bash-syntax.sh`** + **`ci-editor-nvmrc-sync.sh`** before **`ci-vscodium-linux-dev-build.sh`** → **`dev/build.sh`** (fail fast — **`editor/BUILD.md`** *CI*; **`ci-vscodium-linux-dev-build.sh`** enforces **`node --version`** = **`editor/.nvmrc`** — **14.a** / **14.e**; **`LEVIBE_SKIP_NODE_VERSION_CHECK`**); may upload **`vscodium-linux-build.tar.gz`** — **14.e / 14.f** when opt-in) and manual **[`build-linux.yml`](../.github/workflows/build-linux.yml)** (**`uses:`** the same workflow). **E1 (overrides doc):** [`test_editor_le_vibe_overrides_readme_contract.py`](../le-vibe/tests/test_editor_le_vibe_overrides_readme_contract.py) — [`editor/le-vibe-overrides/README.md`](../editor/le-vibe-overrides/README.md) (**STEP 14** / **H6** launcher + workflow strings). **E1 (IDE workflow):** [`test_build_le_vibe_ide_workflow_contract.py`](../le-vibe/tests/test_build_le_vibe_ide_workflow_contract.py) — [`build-le-vibe-ide.yml`](../.github/workflows/build-le-vibe-ide.yml) **`ide-ci-metadata.txt`** **`le_vibe_editor_docs`** (**`LE_VIBE_EDITOR`** pointer), **`upload-artifact`** **`retention-days`** on the metadata upload, workflow **`permissions:`** **`contents: read`**, **`actions: write`**; GitHub Actions run **Summary** **Pre-binary artifact** line mirrors the same stack story (see **[`editor/README.md`](../editor/README.md)** *CI*).

---

## 1. Why this exists

- **Product managers** design **epics** and **tasks** once; the manifest is the machine- and human-readable backlog loop.
- **Session steps** are a **fixed vocabulary** of phases (opening, bootstrap, epic iteration). PMs configure **which** steps exist and **order**, not arbitrary code.
- **Skill agents** are roles (PM, DevOps, etc.) with **markdown** definitions—portable, diffable, and LLM-friendly.
- The **orchestrator** (master) routes steps, enables/disables agents, and grounds negotiation in **`.lvibe/`** RAG material (manifest, chunks, incremental memory—not monolithic repo dumps).

---

## 2. Skill agents (defaults)

All **nine** canonical roles are **enabled by default**. Each has a **markdown** file describing scope, responsibilities, and boundaries (modern SaaS org norms: clear ownership, escalation to PM/User, no silent scope creep).

| Agent `id` | Alias | File (template & workspace) | Role |
|------------|-------|-----------------------------|------|
| `subject_matter_industry_expert` | `@sme` | `…/subject-matter-industry-expert.md` → `.lvibe/agents/subject-matter-industry-expert/skill.md` | Deterministic domain and industry guidance for the workspace purpose. |
| `senior_product_operations` | `@props` | `…/senior-product-operations.md` → `.lvibe/agents/senior-product-operations/skill.md` | Delivery operations, sequencing, readiness, and execution governance. |
| `senior_product_management` | `@prod` | `…/senior-product-management.md` → `.lvibe/agents/senior-product-management/skill.md` | Outcomes, epics, priorities, and product tradeoffs. |
| `senior_backend_engineer` | `@be-eng` | `…/senior-backend-engineer.md` → `.lvibe/agents/senior-backend-engineer/skill.md` | APIs, data, services, performance, security backend. |
| `senior_frontend_engineer` | `@fe-eng` | `…/senior-frontend-engineer.md` → `.lvibe/agents/senior-frontend-engineer/skill.md` | UI/UX implementation, accessibility, client performance. |
| `senior_devops_engineer` | `@do-eng` | `…/senior-devops-engineer.md` → `.lvibe/agents/senior-devops-engineer/skill.md` | CI/CD, infra as code, observability, release safety. |
| `senior_marketing` | `@marketing` | `…/senior-marketing.md` → `.lvibe/agents/senior-marketing/skill.md` | Positioning, launch narrative, and communication readiness. |
| `senior_customer_success` | `@cs` | `…/senior-customer-success.md` → `.lvibe/agents/senior-customer-success/skill.md` | Adoption quality, onboarding clarity, supportability, and retention signals. |
| `senior_revenue` | `@rev` | `…/senior-revenue.md` → `.lvibe/agents/senior-revenue/skill.md` | Monetization impact, commercial risk, and revenue-oriented prioritization. |

**Paths:**

- **Templates (this repo):** `le-vibe/templates/agents/<name>.md`
- **Workspace (skill source files):** **`.lvibe/agents/<agent_id>/skill.md`** (PRODUCT_SPEC §5.2); session manifest **`skill_path`** entries point at these files (see `schemas/session-manifest.v1.example.json`).

**Storage & consent:** **`.lvibe/`** is **opt-in** after user consent (**PRODUCT_SPEC** §5.1); size budget and compaction apply per **§5.4–5.5**.

---

## 3. Session manifest JSON (`session-manifest.v1`)

**Single file** per active session configuration (iterate PM epics/tasks **and** drive session machinery).

### 3.1 Top-level shape

| Field | Type | Meaning |
|-------|------|---------|
| `schema_version` | string | e.g. `"session-manifest.v1"` |
| `meta` | object | ids, timestamps, optional `workspace_summary` / RAG pointers; optional `evidence_artifacts` registry (artifact ids that evidence entries must reference), optional `evidence_artifact_records` (artifact-to-session mapping for freshness checks), optional `goal_alignment_check.start` / `goal_alignment_check.end` records (session boundary alignment checks), optional `stop_condition_check` gate (`completion_allowed` only true at final milestone with product goals satisfied), optional `milestone_definition_of_done_checks` (per-milestone DoD pass/fail), optional `milestone_dependency_visibility` (dependency graph quality + missing refs), optional `progress_confidence_report` (confidence score + drift detection), optional `final_milestone_lock_criteria` (acceptance-evidence lock gate), optional `failure_mode_catalog` (active failure modes derived from readiness blockers), optional `release_readiness_summary` (derived readiness + blockers from checks/tasks), optional `remaining_gaps_report` (explicit pre-closeout gap list), plus optional **`continue_construction_note`** / **`ai_pilot_note`** (human hints; tie to **[`docs/AI_PILOT_AND_CONTINUE.md`](AI_PILOT_AND_CONTINUE.md)** and the Master queue in **[`docs/PROMPT_BUILD_LE_VIBE.md`](PROMPT_BUILD_LE_VIBE.md)**) |
| `session_steps` | array | Ordered **SESSION STEPS** designed by PM workflow (see §4) |
| `agents` | object | Which roles are on; paths to skill markdown |
| `product` | object | **Epics** and **tasks** (PM-owned backlog) |

### 3.2 `product.milestones` (formal schema)

- Each milestone includes:
  - `id`
  - `objective`
  - `acceptance` (array of acceptance statements)
  - `exit_tests` (array of test identifiers/paths)
  - `owners` (array of role aliases or owner ids)
- This schema defines milestone accountability before closeout checks.

### 3.2.1 Milestone definition-of-done checks (Task 62)

- Operator-consumable checks evaluate each milestone for required DoD fields:
  - non-empty `objective`
  - non-empty `acceptance`
  - non-empty `exit_tests`
  - non-empty `owners`
- Results are persisted in `meta.milestone_definition_of_done_checks` with per-milestone pass/fail and aggregate totals.

### 3.2.2 Cross-milestone dependency visibility (Task 63)

- Milestones may include `dependencies` as milestone-id references.
- Orchestrator computes `meta.milestone_dependency_visibility` with:
  - per-milestone dependency lists
  - missing dependency references
  - reverse dependents map
- Release and gap outputs include a blocker when dependency references are missing.

### 3.3 `product.epics`

- Each **epic** has `id`, `title`, optional `description`, and `tasks[]`.
- Each **task** has `id`, `title`, `status` (`pending` \| `in_progress` \| `done` \| `blocked`), optional `assignee_agent`, `notes`, `acceptance_criteria`.

The orchestrator **iterates** epics/tasks in order unless a step overrides (e.g. “current epic only”).

### 3.4 `agents`

- `defaults.all_enabled`: boolean — default **true** (all nine canonical roles on).
- `roles[]`: optional per-role overrides: `id`, `enabled`, `skill_path` (relative to `.lvibe/` or template root).
- Mentions may use shorthand aliases: `@sme`, `@props`, `@prod`, `@be-eng`, `@fe-eng`, `@do-eng`, `@marketing`, `@cs`, `@rev`.

---

## 4. SESSION STEPS (PM-designed)

Steps are **declarative** entries in `session_steps[]`. Each has at least `id`, `type`, `title`.

**Standard types** (v1):

| `type` | Meaning |
|--------|---------|
| `opening_intent` | First interaction: prompt user to **describe what they want to build**; skippable. |
| `workspace_scan` | Orchestrator builds **shared context** from existing repo (for every enabled agent) when user skips opening and a workspace exists. |
| `agent_bootstrap` | Load skill markdown + RAG refs; establish negotiation protocol for the session. |
| `epic_iteration` | Walk `product.epics` / tasks; agents coordinate per task until done or blocked. |
| `continue_construction` | **Resume** from current manifest / epic state (maps to user **“Please continue”** in **`docs/AI_PILOT_AND_CONTINUE.md`**). |
| `ai_pilot` | **Sustained** coordinated mode (prompt-gated); visible multi-agent style orchestration; same guards as **PRODUCT_SPEC** §5 / §8. |
| `retrospective` | Optional close-out (optional v1). |

**Opening rule:**

- **Prompt copy:** default title like **“Describe what you want to build”**; user may **skip**.
- **If skip** and **workspace root has meaningful files**: run **workspace scan** — orchestrator summarizes purpose, stack signals, and key paths; writes compact entries for **each** agent’s context (e.g. under `.lvibe/memory/` + chunk refs) so negotiation is **grounded**, not generic.

**If skip** and **empty workspace:** fall back to minimal bootstrap + PM asks for intent later.

---

## 5. Orchestration & RAG

- Agents **do not** each ingest the whole repo blindly. They use **`.lvibe/`** (manifest, `memory/incremental.md`, `chunks/`, `AGENTS.md`) per **`docs/PRODUCT_SPEC.md` §5**.
- **Session manifest** is part of that ground truth: epics/tasks + current step index (implementation may add `meta.current_step_id` or a sidecar state file—see example JSON).
- **Runtime alignment checks:** launcher runtime updates `meta.goal_alignment_check.start` after workspace prepare and `meta.goal_alignment_check.end` after editor exit so session boundaries always carry evidence.
- **Runtime stop condition check:** launcher runtime updates `meta.stop_condition_check` with `completion_allowed=false` by default, so completion stays blocked until product goals and final milestone are explicitly verified.
- **Phase 7 closeout invariant (Task 70):** `stop_condition_check.completion_allowed` stays **false** for all partial states and turns **true** only when product goals are satisfied and the current milestone equals the final milestone.
- **Release-readiness summary (Task 69):** orchestrator computes `meta.release_readiness_summary` from goal-alignment end status, stop-condition gate, and task status counts so release blockers are explicit and deterministic.
- **CI evidence parser (Task 59):** orchestrator parses pytest-style CI logs from `meta.ci_failure_log` / `meta.ci_failure_logs` into `meta.ci_evidence_summary` (`failure_count`, `error_count`, reported summary counts, and parsed failure entries) so subagents reason from actual failures.
- **CI evidence summary contract:** seeded manifest examples pin `meta.ci_evidence_summary` shape to: `sources`, `has_failures`, `failure_count`, `error_count`, `reported_failed_count`, `reported_error_count`, `failures`, `source`.
- **Remaining gaps report (Task 66):** orchestrator computes and persists `meta.remaining_gaps_report` from current blockers so milestone close explicitly lists unresolved gaps (`lvibe remaining-gaps`).
- **Milestone DoD checks (Task 62):** orchestrator computes `meta.milestone_definition_of_done_checks`; release/gap outputs include a `milestone_definition_of_done_incomplete` blocker when required milestone fields are missing.
- **Milestone dependency visibility (Task 63):** orchestrator computes `meta.milestone_dependency_visibility`; release/gap outputs include `milestone_dependency_missing_reference` when dependencies point to unknown milestone ids.
- **Progress confidence + drift (Task 64):** orchestrator computes `meta.progress_confidence_report`; release/gap outputs include `progress_drift_detected` when alignment claims are ahead of observable execution progress.
- **Final milestone lock criteria (Task 65):** orchestrator computes `meta.final_milestone_lock_criteria` and requires complete acceptance evidence (`goal_alignment_check.end.evidence` + `stop_condition_check.evidence`) before final milestone lock is satisfied.
- **Evidence provenance validation (Task 59):** final-milestone lock checks now require evidence entries to be traceable via `meta.evidence_artifacts`; untraceable evidence adds `final_milestone_evidence_untraceable` blocker and keeps lock unsatisfied.
- **Evidence freshness rule (Task 26):** evidence entries must also be fresh for current `meta.session_id` via `meta.evidence_artifact_records`; stale evidence adds `final_milestone_evidence_stale` and must be revalidated before lock.
- **Runtime artifact refresh (Task 26 follow-through):** runtime persistence helpers (`persist_goal_alignment_check` / `persist_stop_condition_check`) auto-upsert `meta.evidence_artifacts` and refresh `meta.evidence_artifact_records` for the active `meta.session_id`.
- **Runtime session-id guard:** those same persistence helpers repair missing/blank `meta.session_id` before writing evidence so artifact freshness tracking is always attachable to a concrete session.
- **Session-id repair audit logging:** when repair occurs, runtime emits structured `session_id_repaired` events (including check type and repaired id) so identity repairs are observable in logs.
- **Structured log event contract:** workspace orchestration events use `schema_version=workspace_event.v1`. Required fields:
  - All workspace events are emitted through a shared helper entrypoint (`_emit_workspace_event`) to centralize schema/version/workspace fields and required-field validation.
  - `session_id_repaired`: `workspace`, `check`, `repaired_session_id` (+ `phase` for goal-alignment repairs).
  - `goal_alignment_check_applied`: `workspace`, `phase`, `status`.
  - `stop_condition_check_applied`: `workspace`, `completion_allowed`.
  - Noop events (`*_noop_*`) emitted by opening-skip / goal-alignment / stop-condition / readiness / gaps include `workspace`.
  - Summary events include: `release_readiness_applied` (`workspace`, `ready`, `blockers`) and `remaining_gaps_applied` (`workspace`, `gap_count`).
  - Contract registry is centralized in `WORKSPACE_EVENT_REQUIRED_FIELDS`; test matrix enforces all listed events for both positive and missing-field paths.
  - Strict registration rule: `_emit_workspace_event` rejects unknown workspace event ids unless they are explicitly present in `WORKSPACE_EVENT_REQUIRED_FIELDS`.
  - Developer checklist when adding a workspace event: update `WORKSPACE_EVENT_REQUIRED_FIELDS`, emit through `_emit_workspace_event`, extend event-contract tests, and update this spec section.
  - Static parity guard: shared test utility parses `_emit_workspace_event` callsites and requires exact set parity with `WORKSPACE_EVENT_REQUIRED_FIELDS`.
  - Event id literals only: callsites must pass string-literal event ids to `_emit_workspace_event`; dynamic event-id composition is disallowed by contract tests.
  - Static diagnostics quality: violations report concrete `file:line:column` locations for non-literal event-id callsites, and scan recursively across `le_vibe/**/*.py` emitter modules.
  - Recursive-scan exclusion policy: skip paths containing `generated`, `vendor`, `third_party`, or `__pycache__`; exclusions are explicit in shared test utility with per-term rationale strings and covered by tests.
  - Policy-change guard: exclusion term set is pinned by test and must be intentionally updated alongside rationale + spec-contract text when terms change.
  - Safe update procedure: shared utility docstring lists required exclusion-update steps (reasons map, derived parts, spec text, contract assertions, and targeted test run).
  - Canonical helper-index tuple (`WORKSPACE_EVENT_HELPER_INDEX_SYMBOLS`) now includes `HELPER_INDEX_GOVERNANCE_ANCHOR_PREFIX` so exported-helper coverage is single-sourced.
  - Shared docstring index parser: helper `parse_exported_helper_index` parses only bullets under header constant `EXPORTED_HELPER_INDEX_HEADER` (the `Exported helper index` section; stops at the next section header) without capturing unrelated bullet lists. Parser edge cases are covered by table-driven tests with case ids via shared constant `PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS`, which mirrors canonical tuple `PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL` (`no_header`, `repeated_header_first_section_wins`, `empty_section`).
  - Parser edge-case id integrity guard: `PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS` stays non-empty, duplicate-free, and in canonical order (`no_header`, `repeated_header_first_section_wins`, `empty_section`).
  - Helper-constant index placement: `FAILURE_MODE_DIAGNOSTIC_GOVERNANCE_INVARIANTS` is pinned in `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS` as the trailing constant entry.
  - Helper-docstring index placement: `workspace_event_contract_utils` exported helper index keeps `FAILURE_MODE_DIAGNOSTIC_GOVERNANCE_INVARIANTS` as the trailing docstring bullet.
  - Governance test comment convention: use short `Guard #N:` and/or single-line intent comments above policy tests so each guard’s responsibility stays explicit and non-overlapping.
  - Marker adjacency checks are centralized in shared test utility helper `assert_marker_adjacent_to_target_tests` for reuse consistency.
- **Failure-mode cataloging (Task 58):** orchestrator computes `meta.failure_mode_catalog` from release blockers with id/severity/status entries so operators can triage closeout risks from a stable decision record. Severity assignment is pinned by explicit blocker policy map `FAILURE_MODE_SEVERITY_BY_BLOCKER` (not string heuristics); blocker `ci_failures_present` is cataloged as an active mode with `medium` severity by default.
- **Failure-mode policy derivation:** blocker policy is centralized in `FAILURE_MODE_BLOCKER_POLICY` (`blocker_id`, group, severity). `FAILURE_MODE_SEVERITY_BY_BLOCKER`, `RELEASE_READINESS_BASE_BLOCKER_IDS`, and `RELEASE_READINESS_EVIDENCE_BLOCKER_IDS` are derived from that single policy source. Group labels use named constants `BLOCKER_GROUP_BASE` and `BLOCKER_GROUP_EVIDENCE`.
- **Failure-mode policy shape guard:** contract tests require unique blocker ids in `FAILURE_MODE_BLOCKER_POLICY` and allow only group labels from `BLOCKER_GROUP_BASE` / `BLOCKER_GROUP_EVIDENCE`.
- **Failure-mode policy tuple schema guard:** policy entries are strict 3-tuples (`blocker_id`, group, severity), and severity values are constrained to the allowed taxonomy in `FAILURE_MODE_ALLOWED_SEVERITIES` (currently `high`, `medium`).
- **Failure-mode severity taxonomy integrity guard:** `FAILURE_MODE_ALLOWED_SEVERITIES` remains non-empty, duplicate-free, and in canonical order (`high`, `medium`) to keep deterministic policy semantics.
- **Failure-mode severity taxonomy parity guard:** helper `failure_mode_severity_taxonomy_diagnostics` reports `unknown_severities` and `unused_allowed_severities`; both must remain empty so policy severities match `FAILURE_MODE_ALLOWED_SEVERITIES`.
- **Failure-mode taxonomy diagnostics schema guard:** `failure_mode_severity_taxonomy_diagnostics` returns stable keys `allowed_severities`, `used_severities`, `unknown_severities`, and `unused_allowed_severities` as list fields for contract-friendly assertions.
- **Failure-mode taxonomy diagnostics ordering guard:** `allowed_severities` and `used_severities` are returned in sorted order for deterministic outputs and stable contract assertions.
- **Failure-mode taxonomy source-link guard:** diagnostics `allowed_severities` must equal `sorted(FAILURE_MODE_ALLOWED_SEVERITIES)` so helper output stays directly linked to the canonical severity constant.
- **Failure-mode taxonomy used-source guard:** diagnostics `used_severities` must equal `sorted({severity for _, _, severity in FAILURE_MODE_BLOCKER_POLICY})` so helper output stays directly linked to policy-declared severity usage.
- **Failure-mode diagnostics governance table:** a table-driven test verifies shape, list typing, ordering, source-link parity, and empty unknown/unused diagnostics in one labeled invariant matrix while focused tests remain as smoke checks.
- **Failure-mode diagnostics invariant labels:** governance matrix labels are pinned as `shape_keys`, `list_types`, `sorted_order`, `source_link_allowed`, `source_link_used`, and `parity_unknown_unused_empty`.
- **Parser edge-case canonical tuple visibility guard:** `PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL` is internal-only and must remain excluded from both `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS` and the `Exported helper index` docstring bullets to keep public helper index surface minimal.
- **Parser edge-case alias identity guard:** `PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS` must remain identity-linked to `PARSE_EXPORTED_HELPER_INDEX_EDGE_CASE_IDS_CANONICAL` (`is`, not copy-equal only) so table-test IDs stay single-sourced.
- **Helper internal-only constants registry guard:** `WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS` is the explicit registry for internal-only helper constants; it remains non-empty, duplicate-free, and in canonical sorted order, and each listed symbol must stay excluded from both `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS` and the exported helper docstring index. The registry is non-self-referential (`WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS` cannot list itself), and each listed symbol must resolve on `workspace_event_contract_utils` (`hasattr`) to prevent stale names. The registry symbol itself remains discoverable in both `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS` and the exported helper docstring index, with runtime evidence asserted by parsing `workspace_event_contract_utils` docstring through `parse_exported_helper_index`; runtime exclusion evidence verifies each internal-only member remains absent from parsed exported helper names, and runtime sorted-order evidence keeps the internal-only registry canonical. Registry integrity checks are centralized in shared helper `assert_internal_only_registry_integrity`, which must remain in the callable section (`WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS`) and out of the constant section; runtime doc-index ordering evidence keeps `assert_internal_only_registry_integrity` before `WORKSPACE_EVENT_HELPER_INTERNAL_ONLY_CONSTANT_SYMBOLS` and uses shared pair constant `INTERNAL_ONLY_REGISTRY_ORDERING_PAIR`, whose ordering pair remains a 2-tuple with distinct entries and both symbols present in parsed exported helper names. Ordering-pair integrity checks are centralized in shared helper `assert_ordering_pair_integrity`. Placement guard: `assert_ordering_pair_integrity` remains in callable surface (`WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS`), excluded from `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS`, and appears before constant section entries in parsed exported helper index. Callable-surface placement checks are centralized in shared helper `assert_callable_surface_membership`. Callable symbol resolution checks are centralized in shared helper `assert_callable_symbols_resolve`. Helper-index export coverage + callable resolution checks are centralized in shared helper `assert_helper_index_export_and_resolution_consistency`. Helper-governance spec phrase bundle is centralized via `HELPER_GOVERNANCE_SPEC_PHRASES`. Phrase-bundle integrity guard: `HELPER_GOVERNANCE_SPEC_PHRASES` remains non-empty, duplicate-free, and in canonical order. Phrase-bundle integrity checks are centralized in shared helper `assert_phrase_bundle_integrity`. Placement guard: `assert_phrase_bundle_integrity` remains in callable surface (`WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS`), excluded from `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS`, and appears before constant section entries in helper index. Callable placement governance source is centralized in `CALLABLE_PLACEMENT_GUARDED_HELPERS`, including `assert_helper_governance_runtime_consistency`. Expected tuple shape/order checks are centralized in shared helper `assert_expected_symbol_tuple`. Constant symbol discoverability checks are centralized in shared helper `assert_constant_symbol_discoverability`. Helper-governance phrase boundary pins are centralized via `HELPER_GOVERNANCE_SPEC_FIRST_PHRASE` and `HELPER_GOVERNANCE_SPEC_LAST_PHRASE`. Phrase-bundle boundary checks are centralized in shared helper `assert_phrase_bundle_boundaries_match_constants`. Phrase-bundle full integrity checks are centralized in shared helper `assert_phrase_bundle_full_integrity`. Placement guard: `assert_helper_governance_runtime_consistency` remains in callable surface (`WORKSPACE_EVENT_HELPER_CALLABLE_SYMBOLS`), excluded from `WORKSPACE_EVENT_HELPER_CONSTANT_SYMBOLS`, and appears before constant section entries in helper index. Helper-governance runtime consistency checks are centralized in shared helper `assert_helper_governance_runtime_consistency`.
- **Failure-mode severity coverage guard:** contract tests require every emitted release-readiness blocker id to be present in `FAILURE_MODE_SEVERITY_BY_BLOCKER`; blocker ids are centralized via `RELEASE_READINESS_BASE_BLOCKER_IDS` + `RELEASE_READINESS_EVIDENCE_BLOCKER_IDS` so new blockers must declare severity explicitly.
- **Negotiation:** orchestrator proposes next action from `session_steps` + current epic/task; agents respond per skill file; decisions recorded in incremental memory **in small, token-efficient** snippets.
- **Master vs subagents (product model):** The **in-app** primary model **grounds** on **`.lvibe/`** and manifest/task state; it **invokes** subagent roles **when appropriate** so their “learning” (summaries, decisions, chunk refs) is **reused**—see **`docs/PRODUCT_SPEC.md` §7**. Not every role runs on every turn; **selective** orchestration keeps latency and token use **lean**.
- **Session-long updates:** Even when the user is **not** chat-heavy, the product may **append bounded** updates to **`.lvibe/`** over an open session (**PRODUCT_SPEC** §5)—implementation must stay **safe** and **small-token**.
- **Secrets:** Do not ingest **`.env` / `.env.local`** etc. by default; follow **`docs/PRODUCT_SPEC.md` §8**. Subagent prompts must respect the same rules.

### 5.1 User gate — **USER RESPONSE REQUIRED** (coordinator authority)

When the **master orchestrator** lacks **product authority** or **clear** technical consensus among subagents on a **high-impact** decision, it **must not** proceed with assumptions (**`docs/PRODUCT_SPEC.md` §7.2**).

**Protocol (must ship in product behavior and in Cursor-style prompts):**

1. **Halt** execution of the affected epic/task/step until resolved.
2. Emit a single prominent line: **`USER RESPONSE REQUIRED`** (all capitals).
3. Below it, list **numbered questions** (1., 2., …) with **short** context each (what tradeoff, why it matters).
4. Instruct the user to answer **by number**. Accept **“No preference”**, **“I don’t care”**, **“Your call”**, **“Surprise me”**, or equivalent as **delegation** to the orchestrator + PM/Industry Advisor heuristics—not as empty permission to invent facts.
5. **Subagent disagreement:** If two or more roles conflict, the coordinator summarizes **positions** and **one** consolidated question set—no voting spam.
6. Resume only after user reply (or explicit delegation as above); record the outcome in **`.lvibe/`** incremental memory as a **short** decision stub (no essays).

**Examples** of gate triggers: major **DB** / persistence shape changes; **breaking** public API; **brand/design** forks; **security** posture changes; unresolved **multi-agent** dispute on approach.

---

## 6. Files to ship in-repo (building the app)

| Path | Role |
|------|------|
| `schemas/session-manifest.v1.example.json` | Canonical example + comments in spec |
| `le-vibe/templates/agents/*.md` | Default skill definitions (SaaS-style) |
| Workspace prepare (`le_vibe.workspace_hub` + `le_vibe.session_orchestrator`) | Seeds `.lvibe/session-manifest.json` when absent from **`schemas/session-manifest.v1.example.json`** in a monorepo checkout (`session_manifest_example_source_path`), else the bundled copy (must match — E1 `test_session_orchestrator`); copies `le-vibe/templates/agents/*.md` into `.lvibe/agents/` when missing; hooks in `session_orchestrator` for **opening_intent** skip → **workspace_scan** |

---

## 7. Success criteria (this spec)

- [x] Example JSON validates the mental model: **session_steps** + **product.epics** + **agents**.
- [x] Nine canonical agent markdown files exist with **Lé Vibe**-aligned, SaaS-realistic defaults and alias mapping (`@sme`, `@props`, `@prod`, `@be-eng`, `@fe-eng`, `@do-eng`, `@marketing`, `@cs`, `@rev`).
- [x] Opening / skip / workspace-scan behavior is documented for implementers (`le_vibe.session_orchestrator`: `resolve_next_step_after_opening_skip`, `apply_opening_skip`, `write_workspace_scan_stub`).
- [x] Same files conceptually reused under **`.lvibe/`** for end users.

---

*This spec is input to the Master orchestrator lazy prompt and to future `lvibe` / extension features.*
