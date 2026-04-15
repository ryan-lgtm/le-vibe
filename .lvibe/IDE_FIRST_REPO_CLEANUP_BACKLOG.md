# IDE-first repository cleanup — engineering backlog

**Owner:** Senior Project Management  
**Goal:** Refocus this repository as a **single product**: the **Lé Vibe IDE** (Code OSS–class editor), **managed Ollama**, **Continue + embedded agent/orchestration**, and **self-install / setup**—not a generic “monorepo umbrella” or an **`r-vibe`-named parent** mental model.

**Authority:** Engineers may use **any git commands** needed (`git mv`, `git filter-repo` only if explicitly approved in a task, branch/rebase/cherry-pick, submodule updates, etc.). Prefer **`git mv`** for renames so history stays traceable.

**Constraints:**

- Do not land drive-by refactors unrelated to path/layout/docs updates required by the restructure.
- After each task: **tests green** (`pytest` from repo root per `pytest.ini` / existing docs), and **document** what moved in the task notes or a short `.lvibe/decisions/` entry when behavior or public paths change.
- **Push policy:** follow `agents.defaults.engineer_completion_protocol` in `session-manifest.json` (clean scoped commits; push and report status unless blocked).
- **Strict epic priority (no ambiguity):** complete **Phase E / `epic-fresh-install-continue-stabilization`** first. Engineers must not start new A/B/C/D cleanup tasks while any `task-e*` remains `pending`, unless the operator explicitly overrides in-session.

---

## Phase A — Inventory and target shape (decision-ready)

| ID | Task | Done when |
|----|------|-----------|
| **A1** | **Tree inventory** — List top-level directories and *primary* purpose (`editor/`, `le-vibe/`, `debian/`, `packaging/`, `docs/`, `schemas/`, `.github/`, etc.). Note duplicate packaging trees (e.g. root `debian/` vs `packaging/debian-le-vibe-ide/`) and submodule anchors (`editor/vscodium`). | Markdown table + links to “source of truth” docs per area; no code moves yet. |
| **A2** | **Target layout RFC** — Propose **one** target directory tree and naming story: IDE + stack as first-class, no “wrapper repo” framing. Options may include: (i) keep physical layout, fix narrative + clone dirname only; (ii) limited `git mv` consolidation; (iii) larger flattening—each option lists **risk**, **CI impact**, and **rollback**. | `.lvibe/decisions/IDE_FIRST_LAYOUT_RFC.md` (create `decisions/` if needed) with **recommended** option + rationale. |
| **A3** | **Stakeholder strings audit** — Grep for `r-vibe`, “monorepo”, and legacy parent-folder assumptions in `README*`, `docs/`, `.github/`, `packaging/`, `le-vibe/`, `editor/` (scope: user-facing + CI). | Spreadsheet or checklist of files/lines to update in later phases (attach path list to A2 or a `.lvibe/audit/` file). |

---

## Phase B — Naming and documentation (no risky moves)

| ID | Task | Done when |
|----|------|-----------|
| **B1** | **Canonical repo identity** — Align **clone URL placeholder**, **default directory name after clone**, and **README** quick-start with PM-approved naming (replace instructional `cd r-vibe` with product/repo name; keep technical paths like `le-vibe/` package dir where required). | `README.md` + key install docs updated; links verified. |
| **B2** | **PRODUCT_SPEC / PM_STAGE_MAP alignment** — Update monorepo-vs-single-product language where PM directs “IDE-first single focus” (minimal edit: truth tables and prioritization, not a rewrite). | Docs consistent with A2 decision; cross-links still valid. |
| **B3** | **Contributor / maintainer index** — `docs/README.md`, `docs/MONOREPO_DEVELOPER_REFERENCE.md` (or successor title): frame as **one IDE product repo**, adjust titles only as needed. | No broken doc graph from moves in B (paths may still point to pre-Phase C locations). |

---

## Phase C — Structural moves (git mv + mechanical updates)

Execute **only after A2 is accepted**. Split into small PR-sized commits per subsystem.

| ID | Task | Done when |
|----|------|-----------|
| **C1** | **Packaging / debian consolidation (if RFC requires)** — Apply accepted layout to `debian/` and `packaging/debian-le-vibe-ide/` (or document explicit non-consolidation). | `dpkg-buildpackage` / project scripts still documented; staging paths updated. |
| **C2** | **Application code path updates** — `le-vibe/`, `editor/` scripts, `packaging/scripts/*.sh`, env samples: fix relative paths, `PYTHONPATH`, and CI workflow `working-directory` after any `git mv`. | Grep for old paths returns clean in scoped dirs; CI green. |
| **C3** | **Tests and contracts** — Update `le-vibe/tests/`, packaging contract tests, and any path-anchored assertions. | Full pytest pass from repo root. |
| **C4** | **Submodules & editor vendoring** — If layout touches `editor/` or submodule paths, run documented submodule sync; update `install-le-vibe-local.sh` and `editor/BUILD.md` paths. | Submodule status clean; build doc steps reproducible. |

---

## Phase D — Verification and ship bar

| ID | Task | Done when |
|----|------|-----------|
| **D1** | **Install / smoke** — Run documented preflight + optional STEP 14 / manual smoke per `docs/LOCAL_INSTALL_ONE_SHOT.md` (as far as CI allows; note host-only steps). | Evidence recorded in task notes (log excerpt or “N/A CI-only”). |
| **D2** | **Session manifest** — Mark epic tasks `done` in `.lvibe/session-manifest.json`; update `meta.workspace_summary` one line. | JSON valid; manifest reflects reality. |
| **D3** | **Handoff** — Short “what moved / what to type” for operators in `README.md` or `docs/LOCAL_INSTALL_ONE_SHOT.md` only if still inaccurate post-change. | New clone instructions match Phase B/C outcomes. |

---

## Phase E — Fresh-install Continue stabilization (new epic prep)

Target issue after `install-le-vibe-local.sh --install --yes`: Continue appears as a gray box and logs show YAML schema registration failure (`yaml.schemas` not registered).

| ID | Task | Done when |
|----|------|-----------|
| **E1** | **Reproduce from clean state** — Run fresh-install flow in a clean environment and capture exact extension state + logs (`workbench.desktop.main.js`, extension host). | Repro notes committed under `.lvibe/audit/` with deterministic steps and observed versions. |
| **E2** | **Install-path guardrails** — Ensure YAML extension install is mandatory/verified before Continue schema writes (installer + first-run hooks). | No schema registration write is attempted until YAML config key is validly available. |
| **E3** | **Continue activation hardening** — Add fallback behavior when YAML extension is absent/late (retry/backoff/user-facing recovery command) and prevent broken gray-box state where feasible. | Continue loads or reports actionable remediation without silent failure. |
| **E4** | **Contract + smoke tests** — Add/extend tests for fresh install to assert YAML + Continue install/activation and no `yaml.schemas` write error path. | Test suite catches regression; smoke script records pass/fail evidence. |
| **E5** | **Operator docs + triage SOP** — Update install docs + Debian README with “what to verify after install” and explicit remediation command sequence. | Docs include validation checklist and known-good recovery flow. |

---

## Dependency order

```text
E1 → E2/E3 → E4 → E5, in parallel with A1/A2/A3 where staffing allows.
A1 → A2 → A3 → B* (parallel where safe) → C* (sequential by risk) → D*
```

---

## What task is delegated next? (no placeholder — engineer discovers it)

The copy/paste prompt below is **fixed**; engineers must **look up** the current assignment as follows:

1. **Open** `.lvibe/session-manifest.json` and locate **`product.epics`**.
2. **Determine active epic (strict order):**
   - If any `task-e*` is `pending`, active epic is **`epic-fresh-install-continue-stabilization`**.
   - Else active epic is **`epic-ide-first-repo-cleanup`**.
   - Operator/PM explicit in-session override can change this for that session only.
3. **Default next task:** inside the active epic, take the **first** task object whose **`"status"`** is **`"pending"`**.
4. **Override:** if operator/PM names a different task or narrower scope, that delegation wins.

Match the manifest task to this file’s phase rows by task intent and id prefix (e.g. `task-a1-*` ↔ **A1**, `task-e2-*` ↔ **E2**).

---

## Copy/paste prompt — engineer agent (same text every time)

```text
You are a senior software engineer working in the Lé Vibe repository.

Mission: Work the **single** delegated task that is next. Do not guess: open `.lvibe/session-manifest.json`, inspect `product.epics`, and apply strict priority: if any `task-e*` in `epic-fresh-install-continue-stabilization` is pending, work that epic first; only when all `task-e*` are done may you work `epic-ide-first-repo-cleanup`. Then take the active epic’s first task with `"status": "pending"` unless this session explicitly assigns a different task/scope.

Read this backlog file and any referenced RFC/decision (`.lvibe/decisions/IDE_FIRST_LAYOUT_RFC.md` and related notes) before changing production paths or docs.

Rules:
- You are authorized to use **any git commands** as needed (prefer `git mv` for moves; preserve clear commit history).
- Stay scoped to the delegated task: no unrelated refactors or extra documentation beyond what that task requires.
- If the task is blocked on a missing decision (e.g. layout RFC not accepted), stop and report precisely what is needed.
- Finish with: (1) what you changed, (2) test evidence (`pytest` or the verification named in the task), (3) git status and branch push result per `agents.defaults.engineer_completion_protocol` in the manifest.

Start by resolving **which** task you are executing (manifest + operator message), then confirm its acceptance criteria in this backlog and the manifest task entry.
```

---

## Suggested assignees (optional routing)

| Phase | Primary |
|-------|---------|
| A | `@prod` + `@be-eng` (inventory + RFC) |
| B | `@prod` + `@do-eng` (docs/CI wording) |
| C | `@be-eng` + `@do-eng` (moves + scripts) |
| D | `@do-eng` (smoke) + whoever owns manifest (`@prod`) |
