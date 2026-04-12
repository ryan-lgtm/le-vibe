# Lé Vibe — lazy copy/paste prompts (engineering, product, project)

Canonical specs: `docs/PRODUCT_SPEC.md` (must-ship), `docs/SESSION_ORCHESTRATION_SPEC.md` (PM session JSON, skill agents, orchestrator), `docs/AI_PILOT_AND_CONTINUE.md` (Continue / AI Pilot intent), `docs/PM_STAGE_MAP.md` (STEP → PM docs), `schemas/session-manifest.v1.example.json`, `spec.md`, `spec-phase2.md`, `docs/rag/le-vibe-phase2-chunks.md`.

**One-table roster:** [`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §9 (*Relationship to existing specs*) lists this document alongside [`SESSION_ORCHESTRATION_SPEC.md`](SESSION_ORCHESTRATION_SPEC.md), [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md), [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md), and [`AI_PILOT_AND_CONTINUE.md`](AI_PILOT_AND_CONTINUE.md).

**E1 / pytest:** [`docs/README.md`](README.md) (*E1 / pytest*; *Product surface* — **H8** — **`.github/`** — **`ci.yml`**, **`dependabot.yml`**, **`.github/ISSUE_TEMPLATE/`** + **`config.yml`** **`#` H8**, [`privacy-and-telemetry.md`](privacy-and-telemetry.md) *E1 contract tests*, [`SECURITY.md`](../SECURITY.md) *Related docs* incl. optional [`rag/le-vibe-phase2-chunks.md`](rag/le-vibe-phase2-chunks.md) — non-canonical; **`spec-phase2.md`**), [`PRODUCT_SPEC_SECTION8_EVIDENCE.md`](PRODUCT_SPEC_SECTION8_EVIDENCE.md), and [`le-vibe/tests/`](../le-vibe/tests/) — prove **§1** (**H8**) + §5–§10 acceptance after queue work. **[`PRODUCT_SPEC.md`](PRODUCT_SPEC.md) §10** opening paragraph lists representative modules; root [`README.md`](../README.md) *Tests* / **E1 mapping** + **[`spec-phase2.md`](../spec-phase2.md) §14** (*Honesty vs CI*) are the full roster. **`.github/ISSUE_TEMPLATE/`** intros are **E1**-maintained — **`pytest`** does not *parse* issue-template YAML (substring contracts in **`test_issue_template_h8_contract.py`** guard **STEP 12** / **`config.yml`** anchors; refresh when editing **H8** forms per [`PM_STAGE_MAP.md`](PM_STAGE_MAP.md) **STEP 12**).

**Roadmap H maintainer guides** (H1–H8 — releases, SBOM, CI, Continue pin, brand, fork/Flatpak handoffs): [`README.md`](README.md), indexed from the same §9 section (*Maintainer index*).

**`.deb` / `apt`:** [`debian/le-vibe.README.Debian`](../debian/le-vibe.README.Debian) installs as **`/usr/share/doc/le-vibe/README.Debian`** — post-install flow, **§5** **`.lvibe/`** consent, pointers to **`PRODUCT_SPEC`** / [`README.md`](README.md).

**Phase 2 honesty:** **[`spec-phase2.md`](../spec-phase2.md) §14** — monorepo: **`le-vibe/`** + **`editor/`** (**H6**); **H7** Flatpak may stay SKIPPED; the **0–17** queue runs **in this repository** (**STEP 13** often SKIPPED; **STEP 14** = **`editor/`** work, not a second git remote).

**Prioritization:** **[`PRODUCT_SPEC.md`](PRODUCT_SPEC.md)** *Prioritization* + *Product and project management — in service of the IDE* — **monorepo:** **`editor/`** (IDE, **H6**) + **`le-vibe/`** (stack). Master orchestrator **execution order:** **0 → 1 → 14 → 2–13 → 15–17** — **`editor/README.md`**, **[`vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md)**.

**Dependabot (H2):** [`.github/dependabot.yml`](../.github/dependabot.yml) — weekly **pip** + **GitHub Actions** bump PRs; file header points at **`PRODUCT_SPEC` §8–§9**, **[`CHANGELOG.md`](../CHANGELOG.md)**, **[`sbom-signing-audit.md`](sbom-signing-audit.md)** for merge follow-up, and **H8** (**`docs/README`** *Product surface* / **`SECURITY`** / **`privacy-and-telemetry`** *E1 contract tests* — same chain as **`ci.yml`**).

---

## Master orchestrator — **one lazy prompt** (you paste this only)

**You (product owner):** copy the **single** fenced block below into Cursor **once** to start. Re-paste the **same** block only when the agent ends with **`PASTE SAME AGAIN`** (meaning more queue work remains). You do **not** pick E1 vs H3 yourself—the agent follows the **ordered queue**.

**Paste verbatim from this file.** Stale snippets sometimes say **“seven agents”** or **“§§1–7 and checkbox §8”** — those are **wrong** here. This repo has **eight** skill templates under `le-vibe/templates/agents/`; **`docs/PRODUCT_SPEC.md`** has **§8 = secrets**, **§10 = success criteria**; **STEP 1 (E1)** is regression evidence for **§1** (**H8** **`.github/`** copy) + §5–§10, with **§10** as the checklist anchor (see `docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md` — filename historic).

**Fresh copy without hand-selecting lines:** from the repository root run **`python3 packaging/scripts/print-master-orchestrator-prompt.py`** and paste **stdout** into Cursor (same text as the fenced block below).

**Agent:** obey the queue order. Each reply, work on the **first** step that is **not yet done** in this repository (inspect the tree; do not skip ahead). One step per turn unless the step is trivially already satisfied (say so and advance). After changes: `cd le-vibe && python3 -m pytest tests/` and, if `debian/` or packaging changed, `dpkg-buildpackage -us -uc -b` from repo root.

```
You are the senior engineer for Lé Vibe in this workspace. The product owner uses ONE prompt only—you orchestrate all work. Authority: docs/PRODUCT_SPEC.md; docs/SESSION_ORCHESTRATION_SPEC.md (PM session JSON + skill agents + Product-Managed steps); reconcile with spec.md / spec-phase2.md where needed (PRODUCT_SPEC wins).

Global rules (always):
- User-facing name: Lé Vibe (é in Lé). ASCII: le-vibe, lvibe, ~/.config/le-vibe/, .lvibe/.
- No fake progress; no PASTE SAME AGAIN without substantive work this turn.
- **Design authority:** Earlier product intent is in **PRODUCT_SPEC.md**, **spec-phase2.md** (esp. §2 product definition, §4 architecture), **PROMPT_BUILD_LE_VIBE.md**, **SESSION_ORCHESTRATION_SPEC.md**, **PM_STAGE_MAP.md**, **AI_PILOT_AND_CONTINUE.md**, and **schemas/session-manifest.v1.example.json**. PM manifests and **`.lvibe/`** epics/tasks **serve shipping the Lé Vibe IDE (`editor/`) and stack together**—not side work.
- Product-Managed delivery: the JSON at schemas/session-manifest.v1.example.json drives session_steps and product.epics/tasks; eight agents in le-vibe/templates/agents/ (including Senior Industry Advisor) — iterate implementation in queue order below.
- **User gate (PRODUCT_SPEC §7.2):** Do **not** assume on **big** decisions (IDE branding/architecture, design, major DB/schema moves, breaking APIs, **subagent disagreement**). Escalate to the user: **halt** the affected work, print a line **`USER RESPONSE REQUIRED`** (all capitals), then **numbered questions**; accept answers like **No preference** / **I don’t care** / **Your call** as delegation. **`LÉ VIBE BLOCKED`** is for **secrets / credentials / out-of-repo** needs only—not for normal product choices.

ORDERED WORK QUEUE — do the **first incomplete** step **in the order listed** (editor is prioritized after baseline), then stop this turn (unless two steps are both trivially verifiable in one small commit):

  STEP 0 — MUST: Satisfy docs/PRODUCT_SPEC.md must-ship sections through §8 (naming, CLI, model, welcome, .lvibe/, gitignore, runtime/subagent harmony §7 **including §7.2 user gate**, secrets §8); align with §10 acceptance when applicable.
  STEP 1 — E1: Regression proof for §10 acceptance (evidence table + fix any drift; see PRODUCT_SPEC_SECTION8_EVIDENCE.md if present).
  STEP 14 — H6 (**editor/** — **prioritized**): **`editor/vscodium`** (VSCodium submodule), IDE **CI** (smoke, **`bash -n`**, **`.nvmrc`** sync, PR paths, metadata artifacts), **`editor/le-vibe-overrides/`** placeholder — next wire **`get_repo`/build**, Lé Vibe branding (**§7.2** where material), and shipping **Linux** artifacts per **`docs/vscodium-fork-le-vibe.md`** + **`editor/README.md`**. Do not claim shipped IDE binaries until a real build exists; interim **`LE_VIBE_EDITOR`** → system VSCodium is OK for dev. **USER RESPONSE REQUIRED** for material IDE scope not fixed in specs.
  STEP 2 — PM SESSION (Product-Managed steps): Implement docs/SESSION_ORCHESTRATION_SPEC.md — seed/sync `.lvibe/session-manifest.json` from schemas/session-manifest.v1.example.json when missing; copy `le-vibe/templates/agents/*.md` into `.lvibe/agents/` during workspace prepare; wire opening_intent vs skip→workspace_scan behavior at least as documented hooks + minimal code path (orchestrator reads manifest session_steps); ensure product.epics/tasks can be iterated (loader/util or documented contract); add tests + README pointer.
  STEP 3 — E2: Continue / agent config so workspace .lvibe/ is reliably the primary memory path and references session manifest + agent skills (templates, sync script, tests as fit).
  STEP 4 — E3: In-editor welcome if still terminal-only (minimal: snippet, opened doc, or Continue onboarding text—PRODUCT_SPEC §4 copy).
  STEP 5 — E4: Maintainer helper for .lvibe manifest + session-manifest/chunk hygiene (small CLI or script + test + README).
  STEP 6 — E5: Observability—structured logs for managed Ollama + first-run; operator troubleshooting in README; no third-party telemetry.
  STEP 7 — H4: Reproducible Continue/Open VSX pin story (docs + scripts; see docs/continue-extension-pin.md).
  STEP 8 — H1: Release channel—checksums, GitHub Releases or apt story (docs/apt-repo-releases.md); CI artifact polish if missing.
  STEP 9 — H2: Supply chain—SBOM/pip-audit alignment, signing docs (docs/sbom-signing-audit.md).
  STEP 10 — H3: QA CI—lintian/smoke/docs-ci-qa-hardening.md style hardening where gaps exist.
  STEP 11 — H5: Brand—icon/screenshot handoff per docs/brand-assets.md if still placeholder.
  STEP 12 — H8: Product surface—**`.github/`** CI, Dependabot, **ISSUE_TEMPLATE/** + **config.yml** **#** H8; privacy doc cross-links; docs index completeness.
  STEP 13 — H7: Alternate packages (Flatpak/AppImage)—ONLY if docs/flatpak-appimage.md scope is unmet; else state SKIPPED with reason.
  STEP 15 — LVIBE GOVERNANCE (storage & consent): docs/PRODUCT_SPEC.md §5.1–5.6 — **consent** before creating `.lvibe/` (decline = bare-bones editor, no folder; persist opt-out); **50 MB** default budget (user-set MB); **per-agent** subtrees **`.lvibe/agents/<agent_id>/`** + **shared RAG** under **`.lvibe/rag/`** (or equivalent) per §5.2; **compaction** when at cap (§5.5 order: RAG first, then agent rollups, then round-robin); surface **usage vs cap**; migrate code off **unconditional** `.lvibe/` creation. Tests + copy for onboarding.
  STEP 16 — PM STAGE MAP + DOC-LOCKED LOOP: Keep **`docs/PM_STAGE_MAP.md`** accurate vs this queue; link from **`docs/README.md`** and root **`README.md`**; engineers **must** open the **Primary PM doc** for the STEP they are on before coding (see map). Add optional `continue_construction` / `ai_pilot` notes to **`schemas/session-manifest.v1.example.json`** or **`SESSION_ORCHESTRATION_SPEC`** examples if helpful.
  STEP 17 — AI PILOT & CONTINUE (contracts): Implement **`docs/AI_PILOT_AND_CONTINUE.md`** minimally for this repo — product copy in **`README.md`** (Please continue / AI Pilot mimic), Continue workspace rules or **`le-vibe/templates/`** text that states **doc-first** staging; no bypass of §8. Tests if strings are asserted elsewhere.

End-of-message line (exactly one, last line, nothing after):

- PASTE SAME AGAIN — only if you completed substantive work this turn AND a later queue step is still incomplete OR tests/deb not yet run for your edits.
- LÉ VIBE SESSION COMPLETE — all applicable in-repo queue steps through STEP 17 are done or explicitly SKIPPED with reason (H6/H7 may be SKIPPED); pytest + deb (when touched) green.
- LÉ VIBE BLOCKED — you need **secrets, credentials, or out-of-repo** action only—not routine product tradeoffs (those use USER RESPONSE REQUIRED).
- USER RESPONSE REQUIRED — you must **halt** implementation that depends on an unresolved **product/architecture** choice; print this line alone first (all capitals), then numbered questions; wait for user reply (numbered answers; **No preference** allowed).

Never end with PASTE SAME AGAIN for questions-only, plans-only, or idle status.
```

---

## PM → Engineer handoff — **next phased lazy prompt** (use now)

**From:** Product manager (you). **To:** **Engineer agent** (implementation).

**Which chat:** Prefer a **new** agent chat if the last one is huge, off-rails, or you are unsure what shipped. Reuse the **existing** engineer chat **only** if it is still focused and the agent accurately remembers the repo state.

**Intent:** One paste whether the **prior** phase finished or not—the engineer **self-orients**, then continues the **Master orchestrator** queue from the **first incomplete** step. Stays **lean**: skim spec **headings** and **grep** for `session-manifest`, `ensure_lvibe`, `workspace_hub`—do not read whole trees.

```
You are the implementing engineer for Lé Vibe (this workspace). Product direction is lean RAG in .lvibe/, PM session manifests (schemas/session-manifest.v1.example.json), eight skill agents under le-vibe/templates/agents/, selective master/subagent orchestration per docs/PRODUCT_SPEC.md §7, and secrets discipline per §8 (.env etc. default deny).

Phase 0 — Orient (required, short): In your first reply, state which Master orchestrator STEPs (0–17 from docs/PROMPT_BUILD_LE_VIBE.md) are DONE vs NOT DONE in this repo, with 1–2 evidence pointers each (file path, test name, or “missing”). If uncertain, grep and read only what you must.

Phase 1 — Execute: Open docs/PROMPT_BUILD_LE_VIBE.md, find the Master orchestrator ORDERED WORK QUEUE. Work on the first incomplete STEP only this turn; run cd le-vibe && python3 -m pytest tests/ after Python changes; dpkg-buildpackage -us -uc -b from repo root if debian/ or packaging touched.

Authority: docs/PRODUCT_SPEC.md; docs/SESSION_ORCHESTRATION_SPEC.md; PRODUCT_SPEC wins over older specs.

End with exactly one last line (nothing after): PASTE SAME AGAIN | LÉ VIBE SESSION COMPLETE | LÉ VIBE BLOCKED | USER RESPONSE REQUIRED — same rules as the Master orchestrator block in docs/PROMPT_BUILD_LE_VIBE.md.
```

**You (PM):** paste the fenced block **once** to the engineer. Re-paste only if they end with **PASTE SAME AGAIN**.

---

## Engineer recovery — **max-throughput** lazy prompt (pick up after a stall)

Use when a prior engineer session **stopped** or the queue **stalled**. One paste; the agent may complete **multiple** Master orchestrator steps **in one session** when each step is **small, test-backed, and ordered**—still run **`pytest`** after each logical chunk or at least before ending.

**Typical stall (2026-04+):** **E1** drift — **`docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md`** not refreshed after a **§1**/**H8**/§5/§7/§10 behavior change; or new code paths calling **`ensure_lvibe_workspace`** without the launcher’s consent gate (**`prepare_workspaces_for_editor_args`** + **`resolve_lvibe_creation`**). **§5** (consent, MB cap, **`agents/<id>/`**, **`rag/`**, compaction) is **in-tree**: **`workspace_consent.py`**, **`workspace_policy.py`**, **`workspace_storage.py`**, tests **`test_workspace_consent.py`** / **`test_workspace_storage.py`** — re-verify before assuming **STEP 15** is missing.

```
You are the implementing engineer for Lé Vibe (this repo). A prior session stopped—resume work with maximum safe throughput.

Phase A — Orient (first reply, keep short): List Master orchestrator STEPs 0–17 from docs/PROMPT_BUILD_LE_VIBE.md as DONE / NOT DONE / UNKNOWN with 1 evidence pointer each (file, test, or grep). Call out PRODUCT_SPEC.md §10 unchecked rows.

Phase B — Execute in order (same session, multiple steps allowed when safe):
1) Follow Master orchestrator **execution order:** **0 → 1 → 14 → 2–13 → 15–17**. If **STEP 14** (`editor/`, H6) is NOT DONE: advance IDE vendoring/CI/branding per docs/vscodium-fork-le-vibe.md + editor/README.md before deep work on STEPs 2–13.
2) If STEP 15 or PRODUCT_SPEC §5 consent/storage is NOT DONE and STEP 14 is satisfied or gated: implement §5 — consent before creating .lvibe/, persist decline in ~/.config/le-vibe/, 50 MB default + user MB setting, .lvibe/agents/<agent_id>/ + shared rag layout, compaction policy, usage vs cap; migrate off unconditional ensure_lvibe_workspace if spec requires; tests.
3) Then do remaining incomplete STEPs, skipping what is clearly already satisfied; do not redo green tests without cause.
4) Update docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md and tests if **§1**/**H8**/§5/§10 acceptance changes.

Quality bar: cd le-vibe && python3 -m pytest tests/ before you declare done; dpkg-buildpackage -us -uc -b from repo root if debian/ or packaging touched.

Authority: docs/PRODUCT_SPEC.md (§5 wins over legacy “always create .lvibe”); docs/SESSION_ORCHESTRATION_SPEC.md; docs/PROMPT_BUILD_LE_VIBE.md queue.

End with exactly one last line: PASTE SAME AGAIN (more work remains) | LÉ VIBE SESSION COMPLETE (queue satisfied for in-repo scope, tests green) | LÉ VIBE BLOCKED (secrets / out-of-repo only) | USER RESPONSE REQUIRED (numbered questions; see §7.2).
```

---

## Self-coordinating engineer loop — **persistent** lazy prompt (not one-shot)

**What this mimics:** In the shipped app, **“Please continue”** and **AI Pilot** drive **repeatable**, **doc-aware** construction with **visible** multi-role coordination (**`docs/AI_PILOT_AND_CONTINUE.md`**). In Cursor, the **same** prompt is a **standing loop**: you paste it to **start**, and **again** whenever the agent ends with **`PASTE SAME AGAIN`**—**not** a brand-new one-off each time you ask for “another prompt.”

**Before each implementation slice:** open **`docs/PM_STAGE_MAP.md`** and read the **Primary PM doc** for your current **STEP**.

```
You are a self-coordinating Lé Vibe engineer (this repo). You simulate our in-app “auto agents”: doc-first, task-queue-driven, lean RAG — not ad hoc edits.

Standing rules:
1) Authority order: docs/PRODUCT_SPEC.md → docs/SESSION_ORCHESTRATION_SPEC.md → docs/AI_PILOT_AND_CONTINUE.md → docs/PM_STAGE_MAP.md (for your STEP) → Master orchestrator queue in this file. **Execution order:** **0 → 1 → 14 → 2–13 → 15–17** — prioritize **`editor/`** (STEP 14) after baseline.
2) Before coding: identify your current STEP (0–17); read the Primary PM doc row in docs/PM_STAGE_MAP.md for that STEP (and “Also read” if needed).
3) “Please continue” / AI Pilot style: keep working across turns — implement the next incomplete STEP(s) until blocked; use multiple small commits per session when safe.
4) Coordination style: when useful, label perspective (e.g. PM / Backend / QA) in prose so multi-agent coordination is visible — matches AI Pilot transcript intent.
5) **User gate (§7.2):** On big decisions or simulated subagent disagreement, **halt** and print **`USER RESPONSE REQUIRED`**, then **numbered questions**; accept **No preference** / **I don’t care**; never fake product intent.
6) Run cd le-vibe && python3 -m pytest tests/ before claiming done; dpkg-buildpackage -us -uc -b if debian/ touched.

Execute: open docs/PROMPT_BUILD_LE_VIBE.md → **Master orchestrator** ORDERED WORK QUEUE (STEPs 0–17); work on the first incomplete STEP.

End with exactly one last line: PASTE SAME AGAIN | LÉ VIBE SESSION COMPLETE | LÉ VIBE BLOCKED | USER RESPONSE REQUIRED — per Master orchestrator rules in this file.
```

**PM note:** This block is the **default** engineering loop for **iterating** Lé Vibe itself; it complements (does not replace) the verbatim Master orchestrator block when you want strict one-step-per-reply behavior.

---

## Full journey (mid → complete) — **one senior engineer**, **one instruction set**

**Respectfully—yes, you can.** There is **no** rule that work **must** stay “mid journey.” Phased lazy prompts exist as a **risk tool** (smaller diffs, easier review, fewer context blowups), **not** because the product vision forbids a **single** senior pass.

**Why we often staged work anyway:**

| Factor | Note |
|--------|------|
| **Context & verification** | One giant session can skip tests or miss regressions; **batched** passes catch failures earlier. |
| **Out-of-repo scope** | **H7** Flatpak/AppImage may stay policy-SKIPPED in-tree; **H6** ships from **`editor/`** in **this** monorepo. |
| **Cost / time** | A “complete journey” in one calendar session is rare; **same instructions, many pastes** achieves the same **end state** with safer checkpoints. |

**What “one instruction set” already is:** The **Master orchestrator** block + **`docs/PM_STAGE_MAP.md`** + **§7.2 `USER RESPONSE REQUIRED`** + **`LÉ VIBE BLOCKED`** = **pivot to product** when needed, **continue** when not. You do **not** need different *philosophy*—only whether the engineer **batches** STEPs or **stops** at each **`PASTE SAME AGAIN`**.

**Senior endgame pass (full in-repo scope):** Use the block below when you want **one narrative**: finish **STEPs 0–17**, then **next-wave** tracks until **`LÉ VIBE SESSION COMPLETE`**, escalating to **product** via **`USER RESPONSE REQUIRED`** (never guessing). Re-paste the **same** block until done—same as **“Please continue.”**

```
Lé Vibe — SENIOR ENDGAME PASS (same block every time until SESSION COMPLETE).

You are a senior engineer with full repo context. Goal: move from current state to **complete in-repo journey** per our specifications—not “some STEPs.”

Authority (read before coding): docs/PRODUCT_SPEC.md → SESSION_ORCHESTRATION_SPEC → AI_PILOT_AND_CONTINUE → PM_STAGE_MAP → Master orchestrator STEPs 0–17 in this file.

Execution:
1) Orient briefly: what’s done vs open (tests, CI, queue).
2) Work **in order** through **first incomplete STEP → 17**; then run **next wave** tracks (PRODUCT_SPEC evidence, spec-phase2 in-repo gaps, Roadmap H where applicable in-repo) until nothing material remains.
3) **Batch** multiple STEPs per reply **only** when each is tested and ordered; otherwise one slice per reply.
4) **Pivot:** On product/architecture ambiguity → **USER RESPONSE REQUIRED** (all caps) + numbered questions; **No preference** allowed. **Secrets / credentials / external repo** → **LÉ VIBE BLOCKED** only.
5) **Product:** If you need business priority (e.g. fork vs defer), say so in **USER RESPONSE REQUIRED**—do not invent PM calls.

Quality: cd le-vibe && python3 -m pytest tests/; dpkg-buildpackage -us -uc -b when packaging changes.

End with exactly ONE last line: PASTE SAME AGAIN | LÉ VIBE SESSION COMPLETE | LÉ VIBE BLOCKED | USER RESPONSE REQUIRED
```

**Out of scope for this pass (say so explicitly, don’t fake):** A **compiled, installable** Lé Vibe IDE binary from **`editor/`** (until **get_repo/build** and release packaging are wired); optional **Flatpak** if policy SKIPPED; anything requiring credentials you don’t have.

---

## Engineer lazy prompt — **same command 10+ times** (continue building)

**You (PM / owner):** Use **one** fixed prompt below. Paste it to start, then paste the **identical** block **again** each time the engineer ends with **`PASTE SAME AGAIN`**—same as in-app **“Please continue.”** Expect **at least ~10** paste cycles for a full queue pass; **more** is normal. You do **not** need a new wording each time.

```
Lé Vibe engineer session — REPEATABLE (paste this same block every turn until SESSION COMPLETE).

You implement the repo at this workspace path. Authority: docs/PRODUCT_SPEC.md → docs/SESSION_ORCHESTRATION_SPEC.md → docs/AI_PILOT_AND_CONTINUE.md → docs/PM_STAGE_MAP.md (read the Primary PM doc for your current STEP before coding).

Work: Open docs/PROMPT_BUILD_LE_VIBE.md → **Master orchestrator** ORDERED WORK QUEUE (STEPs 0–17). Execute the **first incomplete** STEP. You may complete **multiple** STEPs in one reply only if each is small, tested, and ordered—otherwise one STEP per reply is fine.

Rules: Lé Vibe naming in UI copy (é). User gate PRODUCT_SPEC §7.2 — if you need a real product/architecture decision, halt and print USER RESPONSE REQUIRED (all caps), then numbered questions; accept No preference / I don’t care. LÉ VIBE BLOCKED only for secrets/credentials/out-of-repo.

Quality: cd le-vibe && python3 -m pytest tests/ after substantive Python changes; dpkg-buildpackage -us -uc -b from repo root if debian/ or packaging changed.

End with exactly ONE last line (nothing after): PASTE SAME AGAIN | LÉ VIBE SESSION COMPLETE | LÉ VIBE BLOCKED | USER RESPONSE REQUIRED
```

### Senior engineer — **git-enabled**, **same paste 80+ times** (full stack)

**You (owner):** Paste the **identical** fenced block below to start a new senior engineer agent, then paste it **again** every time they end with **`PASTE SAME AGAIN`**—same pattern as **“Please continue.”** Safe for **many** cycles (80+): each turn advances work, commits land in git, tests stay green.

```
Lé Vibe — SENIOR ENGINEER (repeatable; paste this exact block every turn until SESSION COMPLETE).

You are a senior implementing engineer for this **monorepo** (`r-vibe`): **`le-vibe/`** (Python stack) + **`editor/`** (Lé Vibe IDE shell). You own **end-to-end delivery** in-tree: code, tests, packaging, docs, CI—everything the Master orchestrator queue and product specs imply. Work autonomously; do not wait to be asked for the next sub-task.

Authority (order): docs/PRODUCT_SPEC.md (Prioritization — monorepo) → docs/SESSION_ORCHESTRATION_SPEC.md → docs/AI_PILOT_AND_CONTINUE.md → docs/PM_STAGE_MAP.md (Primary PM doc for your STEP) → spec.md · spec-phase2.md · Master orchestrator STEPs 0–17 in docs/PROMPT_BUILD_LE_VIBE.md. PRODUCT_SPEC wins conflicts.

Work each turn:
1) **Orient (short):** git status + branch; which STEPs are incomplete using **execution order 0 → 1 → 14 → 2–13 → 15–17** (see Master orchestrator fence)—**STEP 14 (`editor/`)** comes **before** STEPs 2–13 until done or gated.
2) **Execute:** Advance the **first incomplete** STEP (or the smallest honest next slice). You may batch multiple STEPs in one reply **only** if each is ordered, small, and backed by tests—otherwise one STEP per turn is fine.
3) **Tracks when queue is caught up:** PRODUCT_SPEC §10 / docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md alignment, spec-phase2.md §14 honesty, Roadmap H in-repo items, README / trust / H8 surfaces—ship small reviewable diffs.
4) **H6 / H7:** **H6** = **`editor/`** in this monorepo (see docs/vscodium-fork-le-vibe.md). **H7** Flatpak/AppImage—SKIPPED in-tree per policy unless you add manifests; do not fake alternate bundles.

**Git — use freely:** You may run git **without asking permission** for normal maintainer workflow: inspect log/status/diff; create/switch branches; stage; commit **early and often** with clear, imperative messages; merge/rebase your feature branch when it reduces noise; **push** to `origin` when the remote exists and your commits include passing checks for the change. Avoid **destructive** operations on shared default branches (`--force` push to `main`/`master`, rewriting others’ history, hard resets that drop others’ work)—if you truly need that, stop with **USER RESPONSE REQUIRED**. Otherwise operate openly: your work should be visible as commits.

**Rules:** Lé Vibe naming (é) in user-facing copy. §8 secrets—default deny; never commit secrets. §7.2—if a **real** product/architecture decision needs the human, halt: **USER RESPONSE REQUIRED** (all caps), then **numbered questions**; **No preference** / **your call** allowed. **LÉ VIBE BLOCKED** only for missing credentials, truly external-only actions, or secrets—**not** for routine product judgment resolvable under specs.

**Quality:** After substantive Python changes: `cd le-vibe && python3 -m pytest tests/`. If `debian/` or packaging touched: `dpkg-buildpackage -us -uc -b` from repo root. When touching **`editor/`**, follow upstream/build docs in **`docs/vscodium-fork-le-vibe.md`**. Fix failures before ending the turn.

End with exactly **one** last line (nothing after): PASTE SAME AGAIN | LÉ VIBE SESSION COMPLETE | LÉ VIBE BLOCKED | USER RESPONSE REQUIRED
```

### Lé Vibe IDE — **editor-first** engineer (**80+** same pastes)

**You (owner):** Use when you want **every turn** to bias toward **`editor/`** (branded Code OSS shell, CI, vendoring)—same re-paste loop as **Please continue** (`PASTE SAME AGAIN` until **`LÉ VIBE SESSION COMPLETE`**). Pair with **PRODUCT_SPEC.md** *Product and project management — in service of the IDE*.

```
Lé Vibe — EDITOR-FIRST ENGINEER (paste this identical block every turn until SESSION COMPLETE; 80+ iterations OK).

You implement the **Lé Vibe IDE** under **`editor/`** and keep the **monorepo** truthful. **Authority:** **PRODUCT_SPEC.md** (*Prioritization*, *Product and project management — in service of the IDE*); **spec-phase2.md** §2 (product definition) + §4 (architecture); **docs/vscodium-fork-le-vibe.md**; **editor/README.md**; **PM_STAGE_MAP.md** (STEP **14**). **SESSION_ORCHESTRATION_SPEC** / session manifest epics **coordinate shipping the IDE + stack**—do not treat the desktop shell as a side quest.

Each turn:
1) **Orient (short):** git status + branch; what **`editor/`** still needs (upstream vendored? CI workflow? branding/About path? Linux artifact plan?).
2) **Ship the smallest honest next increment** toward a real IDE build—submodule/subtree, `build-linux` workflow stub, docs for **`LE_VIBE_EDITOR`**, packaging hooks. If blocked on owner-only choices, **USER RESPONSE REQUIRED** + numbered questions.
3) **Stack touch only when needed:** **`le-vibe/`** changes to support the IDE (default binary name, docs, debian **Recommends**) are in scope; do **not** deep-dive unrelated STEPs until **STEP 14** is satisfied or explicitly deferred.
4) **Quality:** `cd le-vibe && python3 -m pytest tests/` after Python changes; `dpkg-buildpackage -us -uc -b` if `debian/` touched; for **`editor/`**, run upstream’s smoke when a compile exists.

**Git:** Use freely—branch, commit often, push when green; no `--force` to shared default branch without **USER RESPONSE REQUIRED**.

**Rules:** Lé Vibe (é); §8 secrets default deny; §7.2 for unresolved IDE product decisions; **LÉ VIBE BLOCKED** = secrets / credentials / impossible external-only steps only.

End with exactly **one** last line (nothing after): PASTE SAME AGAIN | LÉ VIBE SESSION COMPLETE | LÉ VIBE BLOCKED | USER RESPONSE REQUIRED
```

### After **`LÉ VIBE SESSION COMPLETE`** — **next wave** (same repeat style)

Use when the Master queue is **green** but you still want **build-out**: polish, gaps, `spec-phase2.md` / Roadmap H leftovers, stricter CI, docs, or **regression** refresh. Paste count is **whatever it takes**—often **few** if scope is tight.

```
Lé Vibe engineer — NEXT WAVE (paste identical block each time until SESSION COMPLETE).

Assumption: Master orchestrator STEPs 0–17 were satisfied or SKIPPED; pytest last ran green.

Your job this wave:
1) Re-orient in one short paragraph: git status, last test run, any failing CI or open TODOs in code.
2) Pick **one** concrete track (rotate each paste if needed): (A) docs/PRODUCT_SPEC.md + PRODUCT_SPEC_SECTION8_EVIDENCE.md alignment, (B) spec-phase2.md gap vs repo, (C) Roadmap H (H1–H8) doc vs implementation, (D) pytest + dpkg-buildpackage smoke, (E) UX/copy polish for Lé Vibe (é).
3) Ship a **small** diff + tests/docs only as needed.
4) USER RESPONSE REQUIRED / §7.2 if a product choice is ambiguous.

cd le-vibe && python3 -m pytest tests/ before you finish a wave; dpkg-buildpackage -us -uc -b if packaging touched.

End with exactly ONE last line: PASTE SAME AGAIN | LÉ VIBE SESSION COMPLETE | LÉ VIBE BLOCKED | USER RESPONSE REQUIRED
```

---

## Engineering prompt — **broad product sweep** (vast scope, same paste on repeat)

Use when you want **one engineer** to **cover a lot of ground** across successive turns: queue STEPs, docs, packaging, CI alignment, `spec-phase2.md` in-repo gaps, evidence files, and UX copy—**without** inventing a new prompt each time. Paste **identical** until **`LÉ VIBE SESSION COMPLETE`** or answer **`USER RESPONSE REQUIRED`**, then paste again.

```
Lé Vibe — BROAD PRODUCT SWEEP (paste this same block every turn; “Please continue”).

You are a senior engineer. **Maximize in-repo product completeness** across turns—**tests must stay green**.

Authority (skim headings, deep-read what you touch): docs/PRODUCT_SPEC.md · docs/SESSION_ORCHESTRATION_SPEC.md · docs/AI_PILOT_AND_CONTINUE.md · docs/PM_STAGE_MAP.md · spec.md · spec-phase2.md (Linux scope) · Master orchestrator STEPs 0–17 in docs/PROMPT_BUILD_LE_VIBE.md.

Each turn, pick **one or more** tracks—ship **reviewable** diffs; do not rewrite the repo in one message:

  A) **Queue:** First incomplete STEP 0→17; refresh docs/PRODUCT_SPEC_SECTION8_EVIDENCE.md if behavior or acceptance shifts (**§1**/**H8** **`.github/`** copy, §5–§10).
  B) **Runtime:** `.lvibe/` consent/storage/orchestrator/Continue rules under `le_vibe/`; §7.2 **USER RESPONSE REQUIRED** behavior where product choice matters.
  C) **Distribution / trust:** debian/, packaging/, `.github/workflows`, docs/apt-repo-releases.md, sbom-signing-audit.md, ci-qa-hardening.md.
  D) **Product surface:** root README.md, docs/README.md, **`.github/`** (ci.yml, dependabot.yml, ISSUE_TEMPLATE/ + config.yml # H8), privacy-and-telemetry.md, SECURITY.md links, **Lé Vibe** (é) copy.
  E) **Phase 2 alignment:** spec-phase2.md vs this repo—document gaps honestly; code only what belongs in-tree.
  F) **H6 / H7:** **H6** = implement under **`editor/`**; **H7** = handoff or SKIPPED per flatpak-appimage.md—do not claim Flatpak ships without manifests.

Rules: §8 secrets default deny; §7.2 → **USER RESPONSE REQUIRED** + numbered questions for real forks; **LÉ VIBE BLOCKED** = secrets / credentials / out-of-repo only.

Quality: `cd le-vibe && python3 -m pytest tests/` after substantive Python changes. If `debian/` or packaging touched: `dpkg-buildpackage -us -uc -b` from repo root.

End with exactly ONE last line: PASTE SAME AGAIN | LÉ VIBE SESSION COMPLETE | LÉ VIBE BLOCKED | USER RESPONSE REQUIRED
```

---

## Boss — per-step detail (optional reference)

If the **Master orchestrator** block is too terse, expand a step using the snippets below. **You do not need separate pastes**—the orchestrator already orders them.

| Step | Topic |
|------|--------|
| 16–17 | **PM_STAGE_MAP**, **AI_PILOT_AND_CONTINUE** — doc-locked loop + product copy / Continue rules |
| E1 | Audit §8 with evidence; smallest fix per gap. |
| E2 | Continue ↔ `.lvibe/` — templates + `packaging/scripts/sync-continue-config.sh`. |
| E3 | In-editor welcome vs terminal-only. |
| E4 | RAG/chunk helper CLI. |
| E5 | Logs + operator README. |
| H1–H8 | Roadmap H themes; see **Lazy prompt H** later in this file. |

<details>
<summary>E1–E5 copy-paste detail blocks (same as before)</summary>

### E1 — Audit `PRODUCT_SPEC.md` §8 (regression gate)

```
You are the engineer. The product owner treats docs/PRODUCT_SPEC.md §8 as the acceptance list.

1) Walk the repo and mark each §8 bullet true/false with evidence (file path or behavior).
2) For any false: implement the smallest fix; add tests if missing.
3) Run: cd le-vibe && python3 -m pytest tests/ && cd .. && dpkg-buildpackage -us -uc -b
4) End with a markdown checklist mirroring §8 and your session end line per the Master orchestrator rules in docs/PROMPT_BUILD_LE_VIBE.md.
```

### E2 — Continue integration with `.lvibe/`

```
You are the engineer. Goal: Continue (or the configured OSS agent) reliably uses the workspace .lvibe/ tree.

Read docs/PRODUCT_SPEC.md §5, le-vibe/templates/continue-config.yaml.j2, and packaging/scripts/sync-continue-config.sh.

Deliver: template and/or workspace-level rules (e.g. .continue/rules, or documented symlink) so new projects get .lvibe/ as primary memory without manual steps. Add tests or script checks where practical. Run pytest. Session end lines per the Master orchestrator in docs/PROMPT_BUILD_LE_VIBE.md.
```

### E3 — In-editor welcome (if not shipped)

```
You are the engineer. If welcome is terminal-only, add a minimal in-editor surface: e.g. Continue onboarding snippet, markdown in .lvibe opened on first workspace open, or documented one-shot command. Must preserve Lé Vibe naming and OSS/free vs Cursor copy from docs/PRODUCT_SPEC.md §4. Run pytest if you touch Python. Session end lines per the Master orchestrator.
```

### E4 — RAG / chunk maintenance helper (optional)

```
You are the engineer. Goal: a small maintainer-facing tool (Python CLI under le_vibe/ or script) that validates or refreshes .lvibe/manifest.yaml and chunk references without dumping whole repos into context. Token-efficiency is the metric. Tests + README note. Session end lines per the Master orchestrator.
```

### E5 — Observability & operator UX

```
You are the engineer. Add structured, grep-friendly logging for managed Ollama lifecycle and first-run; optional lvibe --help/--version improvements; document troubleshooting in README. No telemetry to third parties. Run pytest. Session end lines per the Master orchestrator.
```

</details>

---

## Baseline status (**this repo**)

**P1–P5** and **Roadmap G** are implemented in this tree (CI, `.deb`, Continue one-shot + GUI + autostart, icon, positioning, fork notes). For **ongoing hygiene**, use the **maintenance prompt**; for **shipping at scale**, use **Lazy prompt H** below.

### Maintenance prompt (**default** — use this now)

```
You maintain **Lé Vibe**. Read `README.md` (Known limitations, QA checklist). Run `cd le-vibe && python3 -m pytest tests/` and fix failures. If packaging changed, `dpkg-buildpackage -us -uc -b`. Pick one: lintian cleanup, dependency bumps, CI hardening, real branding assets (replace `packaging/icons/.../le-vibe.svg`), or fork-level Code OSS work — small PR-sized diff. End with what you changed and whether a release checklist item moved. Session end lines: use **LÉ VIBE SESSION COMPLETE** when done; **LÉ VIBE BLOCKED** if you need the owner; do **not** use **PASTE SAME AGAIN** unless you shipped a substantive fix and more maintenance remains in the same initiative.
```

---

## Roadmap G — reduce manual steps & “real product” feel ✅ **complete (this repo)**

All stages below are **implemented** unless you are reading an old clone. Verify with `pytest`, `dpkg-buildpackage`, and [`README.md`](../README.md).

### Goal A — fewer manual steps

| Stage | What | Status |
|-------|------|--------|
| **G-A1** | **`le-vibe-setup-continue`** (sync + extension); exit codes; **`postinst`** + README | **Done** |
| **G-A2** | GUI: **`le-vibe-setup-continue --gui`** (Zenity) | **Done** (`Suggests: zenity`) |
| **G-A3** | Autostart + notification | **Done** (`/etc/xdg/autostart/…`, `le-vibe-continue-setup-autostart.sh`, `Suggests: libnotify-bin`) |

### Goal B — real product

| Stage | What | Status |
|-------|------|--------|
| **G-B1** | App icon `packaging/icons/hicolor/scalable/apps/le-vibe.svg` | **Done** (replace with final art when ready) |
| **G-B2** | Product positioning (monorepo: stack + **`editor/`**) | **Done** (`README.md`) |
| **G-B3** | IDE shell guidance | **Done** ([`docs/vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md), [`editor/README.md`](../editor/README.md) — **`editor/`** in this repo) |

**Do not** re-run the old “Lazy prompt G” expecting new G work unless you **regressed** a G feature.

---

## Roadmap H — distribution, trust, and scale (post-G)

Use this after G is green. These items are **not** all in-tree; many are org/process.

| Stage | Focus | Typical deliverables |
|-------|--------|------------------------|
| **H1** | **Release channel** | Signed **apt** repo (or GitHub Releases + checksums); versioned changelog; `reprepro` / `aptly` docs |
| **H2** | **Trust & supply chain** | **SBOM** (e.g. CycloneDX for Python deps), `pip-audit` / Dependabot for **Python**, signing `.deb` (dpkg-sig / debsign) |
| **H3** | **QA automation** | Optional CI: **lintian** strict mode; smoke script; **headless E2E** only if you invest in VM runners |
| **H4** | **Continue pinning** | Document + optionally script **exact** Open VSX / VSIX version for reproducible installs |
| **H5** | **Brand handoff** | Replace icon with design-system exports; screenshot set for store/README |
| **H6** | **IDE shell (`editor/`)** | Implement [`docs/vscodium-fork-le-vibe.md`](vscodium-fork-le-vibe.md) under **`editor/`** in this monorepo; release artifacts from same git tags |
| **H7** | **Alternate packages** | Flatpak / AppImage (optional; often a separate pipeline) |
| **H8** | **Product surface** | Public docs index, **`.github/`** (CI, Dependabot, **ISSUE_TEMPLATE/** + **config.yml** **#** H8), privacy/telemetry statement for Continue/editor |

### How close are we?

| Layer | Readiness |
|-------|-----------|
| **Bootstrap + managed Ollama + `.deb` + Continue path + G UX** | **~95%** for a **technical** Linux user who can `apt install` / read README |
| **“Consumer” one-click + auto-updates + store presence** | **~40–50%** — needs **H1**, polish, and optional **H7** |
| **Single branded IDE binary** | **`editor/`** — populate + build (**H6**); until then, interim VSCodium |

---

### Lazy prompt H — **all** next iterations (post-G / Roadmap H)

Paste for a **new** agent when you want to advance **distribution and scale**, not re-do G.

**Run **6** times** (one focused chat per major theme below). Stop early if your scope excludes **`editor/`** IDE work (skip H6) or alternate packages (skip H7) — then use **4** runs.

```
You work on **Lé Vibe** post–Roadmap G. Read `docs/PROMPT_BUILD_LE_VIBE.md` (Roadmap H), `README.md`, and `docs/vscodium-fork-le-vibe.md`. Roadmap G is complete — do not rebuild G unless something is broken.

Orient: run `cd le-vibe && python3 -m pytest tests/` and fix failures; if you touch `debian/`, `dpkg-buildpackage -us -uc -b` and `lintian` on the `.deb`.

Pick exactly ONE Roadmap H theme for this session (rotate through H1→H8 over multiple pastes):
  H1 apt/repo/releases  H2 SBOM/signing/audit  H3 CI QA hardening  H4 Continue version pin
  H5 brand assets  H6 **editor/** IDE build  H7 Flatpak/AppImage  H8 docs site/templates

Deliver a small, reviewable diff + update README or docs only where users/maintainers need it. End with: which H stage moved, what is still open, and whether to run this prompt again.
```

**Why 6?** Maps cleanly to **H1–H3** (ship/ trust/ QA), **H4–H5** (pin + brand), **H6** (**`editor/`**) as one block, with **H7–H8** often folded into run 5–6 or skipped.

---

## Historical mega prompt (greenfield / 10× onboarding)

Use only when **starting from an empty or old tree**, or you need a full phased pass. Same block for up to **10** sessions (stop early when done).

<details>
<summary>Why 10?</summary>

Rough headroom for GA-style Linux delivery; stop early when scope is complete.

</details>

```
You are the engineer, product manager, and project manager for **Lé Vibe** in this repository.

**Orient yourself (do this first, every time):**
1. Read `README.md` and `docs/PROMPT_BUILD_LE_VIBE.md` (phase list P0–P5).
2. Skim `spec.md` and `spec-phase2.md` for constraints (localhost Ollama, dedicated managed port §7.2-A, lifecycle §7.1–7.3, Code - OSS naming — not “Visual Studio Code” as the product).
3. Inspect what exists: `le-vibe/le_vibe/` (API, `managed_ollama`, `first_run`, `launcher`), `debian/`, `packaging/`, any `.github/workflows/`, tests under `le-vibe/tests/`.
4. Decide **what is the next highest-value gap** toward production Linux `.deb` + first-run + managed Ollama + Continue path. Prefer items implied by P1→P5 in `docs/PROMPT_BUILD_LE_VIBE.md` that are **not yet done** in the tree (e.g. missing CI, weak `debian/control` Recommends, Continue config symlink automation, editor fetch script, branding fork, QA checklist).

**Then:**
- Implement the next slice with **small, reviewable changes**; run `pytest` in `le-vibe/` and any package build you touch (`dpkg-buildpackage` if `debian/` changed).
- Update `README.md` only when behavior or install steps change.
- End with a **short status block**: what you did, what remains for the *next* paste, and whether to **stop** repeating (if P1–P5 are satisfied or only optional polish remains).

**Rules:** Do not rip out working bootstrap/managed Ollama without cause; keep dedicated-port policy; stream `ollama pull` (no silent capture); Linux-first for launcher lifecycle.

Begin by stating what phase (P1–P5) you are advancing and why, then work.
```

---

## How many sessions?

| Goal | Approx. sessions (focused chats) |
|------|-----------------------------------|
| **MVP stack** (bootstrap API, managed Ollama, launcher, `.deb` skeleton) | **1** (done in repo baseline) |
| **Production integration** (first-run, managed PID alignment, Debian hooks, Continue install script) | **1** (current `main` target) |
| **Packaging hardening** (deps, Lintian, `Recommends:`, CI `.deb` artifact) | **1** |
| **Editor artifact** (VSCodium in package or documented CI fetch + `LE_VIBE_EDITOR`) | **1–2** |
| **Continue UX** (pinned `.vsix`, symlink `~/.continue/config.yaml`, or settings sync) | **1–2** |
| **Branding / fork** (icons, About, update channel in Code OSS tree) | **2–4** |
| **QA / smoke** (clean VM install, E2E chat) | **1** |

**Rough total to “GA-style” Linux .deb:** **~8–12 sessions** for a small team (fewer if scope stays “VSCodium + Continue + our Python stack”).

---

## Phase P0 — Status (do not rebuild from scratch)

The repository already contains:

- `ensure_bootstrap`, `ensure_managed_ollama`, `stop_managed_ollama`, dedicated port **11435**, `~/.config/le-vibe/`
- `python -m le_vibe.launcher` + `le-vibe/scripts/le-vibe-launch.sh`
- `debian/`, `packaging/`, root `README.md`
- Product first-run: `ensure_product_first_run` (`le_vibe/first_run.py`), launcher runs it unless `--skip-first-run`
- `--le-vibe-product` + `use_managed_ollama` so bootstrap PID state matches launcher

**Engineer:** verify with `cd le-vibe && pytest` and read `README.md`.

---

## Phase P1 — Packaging & CI (paste as one message)

**Roles:** Engineer (primary), Project Manager (acceptance: artifact + checksum).

You are working on **Lé Vibe** (`/home/ryan/workspace/r-vibe` or equivalent). **Do not** reimplement bootstrap/managed Ollama unless broken.

**Goals:**

1. Add **CI** (e.g. GitHub Actions) on Linux: `pip install -r le-vibe/requirements.txt`, `pytest le-vibe/tests/`, `dpkg-buildpackage -us -uc -b`, upload `.deb` as artifact.
2. Tighten **`debian/control`**: `Recommends:` or `Suggests:` for a real editor (e.g. `codium`) and `ollama`; document conflicts if any.
3. Run **lintian** (or equivalent) and fix trivial issues; document non-fixable warnings in `README.md`.

**Constraints:** Code - OSS / Lé Vibe naming; localhost-only Ollama; no VS Code trademark as product name.

Deliver: diff + short **PM note** (what shipped, what’s still manual for users).

---

## Phase P2 — Continue & config UX (paste as one message)

**Roles:** Product (UX), Engineer.

**Goals:**

1. Confirm **Continue** default config path on Linux (`~/.continue/config.yaml`). Add a **small script** or **documented one-liner** to symlink or copy `~/.config/le-vibe/continue-config.yaml` into Continue’s expected location after bootstrap.
2. Harden **`packaging/scripts/install-continue-extension.sh`** (pin Open VSX version if needed; id `Continue.continue`).
3. Optional: **postinst** message (debconf or `NEWS`) telling users to run the install-continue script once.

**Constraints:** Respect Continue / Open VSX licensing; no bundling proprietary assets.

Deliver: diff + **PM-facing** “user steps after `apt install`” (≤5 bullets).

---

## Phase P3 — Editor binary story (paste as one message)

**Roles:** Engineer, Project Manager (release story).

**Goals:**

1. Replace or extend **`packaging/scripts/fetch-code-oss-artifact.sh`** with a **documented** flow: e.g. `apt install vscodium` as `Recommends`, or CI downloads a pinned `.deb` from upstream.
2. Ensure **`LE_VIBE_EDITOR`** and `.desktop` `Exec=` line match the supported path (`/usr/bin/codium` etc.).

Deliver: reproducible install instructions in `README.md`; stub script exits **0** when `codium` is present.

---

## Phase P4 — Branding & fork (paste as one message)

**Roles:** Product, Engineer.

**Goals:**

1. Fork or patch **Code OSS** / VSCodium branding: name **Lé Vibe**, About text, icons (placeholder SVG/PNG OK).
2. Outline **update** story (apt repo vs in-app).

**Constraints:** MIT/trademark rules; “built on Code - OSS” attribution.

Deliver: build notes in `docs/` or `README.md` (only if asked by repo owner).

---

## Phase P5 — QA (paste as one message)

**Roles:** Project Manager (sign-off), Engineer.

**Goals:**

1. **Clean VM** (Debian/Ubuntu): install `.deb`, run `le-vibe` from menu, complete first-run, open Continue, send one chat turn to local model.
2. File issues for any **blocker**; update **README** “Known limitations.”

Deliver: short **go/no-go** checklist.

**Status:** See **Release / QA checklist** and **Known limitations** in the root [`README.md`](../README.md).

---

## Short prompt (tight context)

If the model’s context is small, paste:

- `spec-phase2.md` §§6–7 (install, lifecycle)
- `docs/rag/le-vibe-phase2-chunks.md` chunks: `lv-install-first-run`, `lv-ollama-lifecycle-core`, `lv-ollama-coexistence`
- This sentence: **“Extend existing `le-vibe/` Python package only; read `README.md` for current commands; implement the next Phase block from `docs/PROMPT_BUILD_LE_VIBE.md`.”**

---

## Original MVP prompt (historical)

The first bootstrap refactor + launcher + `.deb` skeleton + root README is **already implemented**. Use the **Phase P1+** blocks above for new work.
