# Lé Vibe Native Extension Product Track

**Owner:** Senior Product Management / Product Owner  
**Execution mode:** Senior engineering agents, iterative delivery, no prompt edits between passes  
**Primary objective:** Replace third-party gray-screen onboarding risk with a first-party Lé Vibe extension that is local-first, auditable, and storage-respectful.

## Product goals

1. `lvibe .` launches into an immediately usable agent surface (no gray dead-end).
2. Local Ollama is the default runtime with explicit health/status feedback.
3. Conversation and agent memory storage is bounded, user-visible, and opt-out/clearable.
4. Startup behavior is deterministic: clear success path or explicit remediation.
5. Every iteration is testable, auditable, and safe to ship incrementally.

## Non-negotiable constraints

- Local-first by default (no silent cloud fallback).
- No hidden writes of large chat history or embeddings outside declared locations.
- Must expose user controls for retention, export, and clear.
- Canonical UX/product name is **Lé Vibe Chat** for all user-facing surfaces.
- No unrelated refactors outside active task scope.
- If blocked on sudo/manual interaction, continue all other in-scope work and report under **USER FLAGGED ACTIONS REQUIRED**.

## Storage policy (required)

- **Chat transcript store:** bounded JSONL or sqlite under `~/.config/le-vibe/`.
- **Default retention:** rolling window + max size budget.
- **Compaction:** oldest-first with summary stub (never silent data loss).
- **Privacy controls:** `lvibe` command(s) to inspect usage, export, and clear.
- **Telemetry:** local structured logs only unless user explicitly opts in.

## Delivery model

- Work in small vertical slices.
- Each pass picks the **first `pending` task** in epic order.
- Update status and evidence in this file each pass.
- Keep a running section called **USER FLAGGED ACTIONS REQUIRED** for operator-only steps.

---

## Epic order and task board

### Epic N0 — Product framing and architecture baseline

- [x] `done` **task-n0-1**: Define extension boundary (what stays in launcher vs extension vs backend bridge).
  - Acceptance:
    - one-page architecture diagram and responsibilities
    - explicit API boundary for Ollama + workspace services
  - Evidence:
    - Added `docs/native-extension-boundary.md` with boundary diagram, deterministic startup contract, and explicit extension<->bridge, bridge<->Ollama, and bridge<->workspace API definitions.
- [x] `done` **task-n0-2**: Decide extension tech shape (native VS Code extension + webview view + command surface).
  - Acceptance:
    - scaffold approach selected
    - risks/trade-offs documented
  - Evidence:
    - Added `docs/native-extension-tech-shape.md` selecting `editor/le-vibe-native-extension` scaffold, initial command surface, webview view rationale, and explicit risks/trade-offs with mitigations.

### Epic N1 — Extension skeleton and deterministic startup

- [x] `done` **task-n1-1**: Create first-party extension package scaffold under `editor/` tree with Lé Vibe branding.
  - Acceptance:
    - extension activates
    - command appears in command palette
  - Evidence:
    - Added `editor/le-vibe-native-extension/` scaffold with branded command contribution (`leVibeNative.openAgentSurface` / `Lé Vibe: Open Agent Surface`), startup+command activation events, and passing targeted tests (`npm test` in extension folder).
- [x] `done` **task-n1-2**: Add startup readiness panel (not blank/gray) with explicit states:
  - `checking`, `ready`, `needs_ollama`, `needs_model`, `needs_auth_or_setup`.
  - Acceptance:
    - no blank panel state
    - every non-ready state has an actionable button/text
  - Evidence:
    - Implemented readiness webview panel in `editor/le-vibe-native-extension/extension.js` + `readiness.js` with all required states rendered, startup auto-open, and non-ready action buttons (`openOllamaSetupHelp`, `openModelPullHelp`, `openWorkspaceSetup`); targeted tests pass via `npm test` (6/6).

### Epic N2 — Local Ollama integration MVP

- [x] `done` **task-n2-1**: Implement Ollama health probe + model list integration.
  - Acceptance:
    - extension can read health/model state
    - failures mapped to explicit remediation copy
  - Evidence:
    - Added `editor/le-vibe-native-extension/ollama.js` and wired live startup probe in `readiness.js`/`extension.js` using local endpoint (`http://127.0.0.1:11434` default), model-list state mapping (`ready` vs `needs_model`), and explicit error remediation copy for probe failures (`needs_ollama`); targeted tests pass (`npm test`, 10/10).
- [x] `done` **task-n2-2**: Implement basic prompt/response streaming in panel.
  - Acceptance:
    - send prompt
    - receive streaming response
    - cancel in-flight request
  - Evidence:
    - Added local Ollama prompt streaming path in `editor/le-vibe-native-extension/ollama.js`, chat lifecycle controller in `chat.js`, and panel send/cancel UI wiring in `extension.js` (stream token updates + cancel handling); targeted tests pass via `npm test` (13/13).

### Epic N3 — Conversation persistence with storage controls

- [x] `done` **task-n3-1**: Add bounded chat persistence with configurable cap.
  - Acceptance:
    - max size enforced
    - old messages compacted predictably
  - Evidence:
    - Added `editor/le-vibe-native-extension/chat-transcript.js` (JSONL under `~/.config/le-vibe/levibe-native-chat/`, `leVibeNative.chatTranscriptMaxBytes` / `chatTranscriptMaxMessages`, oldest-first compaction with explicit system stub), wired from `extension.js` on each user/assistant turn; tests in `test/transcript.test.js`; `npm test` 17/17.
- [x] `done` **task-n3-2**: Add user-facing controls (`view usage`, `export`, `clear`).
  - Acceptance:
    - controls wired
    - docs for behavior and paths
  - Evidence:
    - Panel buttons + Command Palette commands: `leVibeNative.viewChatUsage`, `exportChatTranscript`, `clearChatTranscript` (`extension.js`, `package.json`); `chat-transcript.js` helpers `getTranscriptStats`, `readTranscriptRaw`, `clearTranscript`; README table for paths under `~/.config/le-vibe/levibe-native-chat/`; `npm test` 18/18.

### Epic N4 — Workspace/operator integration

- [x] `done` **task-n4-1**: Integrate workspace context picker and safe file references.
  - Acceptance:
    - selected file context included in prompt payload
    - clear token-budget rules
  - Evidence:
    - Added workspace context utilities in `editor/le-vibe-native-extension/workspace-context.js` and wired panel/palette controls (`pickContextFile`, `clearContextFiles`) in `extension.js`/`package.json`; selected file excerpts are clipped and injected into outbound prompt payload; token-budget rules shown in panel + documented in `README.md`; tests pass via `npm test` (21/21).
- [x] `done` **task-n4-2**: Add operator handoff contract from extension to `lvibe` environment orchestration.
  - Acceptance:
    - reproducible handoff event format
    - local audit log evidence
  - Evidence:
    - Added `editor/le-vibe-native-extension/operator-handoff.js` with contract `lvibe.operator_handoff.v1` and JSONL append helper; wired panel + command palette action `leVibeNative.emitOperatorHandoff` in `extension.js`/`package.json`; local audit log path `~/.config/le-vibe/levibe-native-chat/operator-handoff-audit.jsonl`; targeted tests pass (`npm test`, 23/23).

### Epic N5 — Reliability and UX hardening

- [x] `done` **task-n5-1**: Add resilient retries and timeout UX for Ollama/API calls.
  - Acceptance:
    - no hard hangs
    - user gets retry + diagnostics
  - Evidence:
    - Added `retry-helpers.js` and wired exponential retries for streaming (`chat.js`) plus `listModels` in `ollama.js`; stream stall/max-duration timers in `ollama.js`; panel diagnostics + **Retry last prompt** (`extension.js`); settings `ollamaMaxRetries`, `ollamaRetryBackoffMs`, `ollamaStreamStallMs`, `ollamaStreamMaxMs`; README + tests (`npm test` extended).
- [x] `done` **task-n5-2**: Add onboarding wizard and first-run checkpoints.
  - Acceptance:
    - first-run path ends in actionable ready state
    - no ambiguous gray panel
  - Evidence:
    - Added `first-run-wizard.js` (persisted checkpoints under `~/.config/le-vibe/levibe-native-chat/first-run-wizard.json`), `firstRunWizardHtml` + message handlers in `extension.js` (next/finish/skip → `beginMainReadiness()`), setting `leVibeNative.showFirstRunWizard`; tests `test/first-run-wizard.test.js` + scaffold assertion for wizard HTML; README section; `npm test` in extension folder.

### Epic N6 — Test and release contracts

- [x] `done` **task-n6-1**: Add unit tests for state machine + storage bounds.
  - Acceptance:
    - deterministic tests for each non-ready state
    - persistence limits tested
  - Evidence:
    - Exported `getConfiguredState` from `readiness.js` for contract tests; added `test/readiness-state-machine.test.js` (per-state `getStateContent`, remediation action ids, dev-override `resolveStartupSnapshot` for all `STARTUP_STATES`, invalid config fallback); added `test/transcript-persistence-bounds.test.js` (appendEntry load/stress within `maxMessages`/`maxBytes`, compaction stub text); README section; `npm test` 37/37 in `editor/le-vibe-native-extension`.
- [x] `done` **task-n6-2**: Add integration smoke path (`lvibe .` + extension ready checks).
  - Acceptance:
    - automated smoke verifies panel is not blank
    - verifies local Ollama/model wiring
  - Evidence:
    - Added `editor/le-vibe-native-extension/scripts/smoke-integration.js` (`npm run smoke`): non-blank `panelHtml`/`firstRunWizardHtml` checks, live Ollama probe via `createOllamaClient` (non-fatal when daemon absent unless `LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=1`), `packaging/bin/lvibe` launcher string contract for `lvibe .`; `test/integration-smoke.test.js`; README section; `npm test` 38/38 + `npm run smoke` OK.

### Epic N7 — Rollout and migration

- [x] `done` **task-n7-1**: Introduce feature flag: first-party extension default with fallback controls.
  - Acceptance:
    - reversible rollout toggle
    - docs for rollback
  - Evidence:
    - Added `feature-flags.js` + `leVibeNative.enableFirstPartyAgentSurface` (default `true`) in `package.json`; `extension.js` gates `openAgentSurface` + startup auto-open; README rollback/restore; `test/feature-flags.test.js`; `npm test` in `editor/le-vibe-native-extension`.
- [x] `done` **task-n7-2**: Migrate users from third-party extension state.
  - Acceptance:
    - deterministic cleanup/remediation
    - migration notes + guardrails
  - Evidence:
    - Added `third-party-migration.js` (watchlist IDs, `third-party-migration-state.json` + `third-party-migration-audit.jsonl` under `~/.config/le-vibe/levibe-native-chat/`, migration Markdown guide, `runThirdPartyMigrationGuide` / `scheduleThirdPartyMigrationNudge`); command + panel action; `leVibeNative.showThirdPartyMigrationNudge`; README; `test/third-party-migration.test.js` + scaffold updates; `npm test` in `editor/le-vibe-native-extension`.

### Epic N8 — Operator runbook and release hygiene

- [x] `done` **task-n8-1**: Canonical verify entrypoint + ship checklist.
  - Acceptance:
    - single npm script runs tests + smoke
    - docs state expected “green” outcome
  - Evidence:
    - Added `npm run verify` (`npm test && npm run smoke`) in `editor/le-vibe-native-extension/package.json`; README section **Operator verification / ship checklist**; `test/verify-script.test.js`; `npm run verify` green in extension folder.
- [x] `done` **task-n8-2**: Bounded persistence inventory for operators.
  - Acceptance:
    - single documented list of persisted paths/patterns under `~/.config/le-vibe/`
    - guardrails visible (no silent unbounded growth beyond existing caps)
  - Evidence:
    - Added `storage-inventory.js` (`levibeNativeChatDir`, `PERSISTED_ARTIFACTS`); `test/storage-inventory.test.js` (paths for transcript, wizard, handoff, migration align on same directory); README table **Bounded persistence inventory**; `npm run verify` green.
- [x] `done` **task-n8-3**: Operator quick-reference document.
  - Acceptance:
    - single bookmarkable file for verify commands and persistence pointers
    - linked from extension README
  - Evidence:
    - Added `editor/le-vibe-native-extension/OPERATOR.md` (verify, smoke env table, persistence + workflow pointers); README link; `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-4**: Smoke prints canonical persisted config directory.
  - Acceptance:
    - integration smoke output includes the same path contract as `storage-inventory.js`
    - operator docs mention the line
  - Evidence:
    - `scripts/smoke-integration.js` logs `levibeNativeChatDir()` before `smoke: done`; `OPERATOR.md` updated; `test/smoke-inventory-line.test.js`; `npm run verify` green.
- [x] `done` **task-n8-5**: Package metadata for monorepo traceability.
  - Acceptance:
    - `package.json` declares git repository + subdirectory for this extension
    - operator doc notes the field
  - Evidence:
    - `package.json` `repository` (`url` + `directory: editor/le-vibe-native-extension`); `OPERATOR.md` sentence; `test/package-metadata.test.js`; `npm run verify` green.
- [x] `done` **task-n8-6**: Integration test asserts smoke prints persisted-dir line.
  - Acceptance:
    - subprocess smoke output contract-tested (not only static script grep)
  - Evidence:
    - `test/integration-smoke.test.js` asserts `first-party persisted config dir:` in stdout; `npm run verify` green.
- [x] `done` **task-n8-7**: README ↔ `PERSISTED_ARTIFACTS` contract test.
  - Acceptance:
    - automated check prevents operator table drift from `storage-inventory.js`
  - Evidence:
    - `test/readme-storage-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-8**: Smoke env vars documented and contract-tested vs `OPERATOR.md`.
  - Acceptance:
    - operator table matches smoke script (including timeout override)
    - automated test prevents OPERATOR / smoke drift
  - Evidence:
    - `OPERATOR.md` row for `LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS`; smoke script file header lists all env vars; `test/smoke-env-doc-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-9**: Monorepo root README pointer to native extension.
  - Acceptance:
    - discoverability from repo landing page
    - test prevents accidental removal of links
  - Evidence:
    - Root `README.md` bullet under *Documentation & project depth*; `test/root-readme-pointer.test.js`; `npm run verify` green.
- [x] `done` **task-n8-10**: Maintainer docs index (`docs/README.md`) links native extension.
  - Acceptance:
    - discoverability from `docs/README.md` table
    - contract test prevents accidental removal
  - Evidence:
    - `docs/README.md` table row for first-party native extension; `test/docs-readme-pointer.test.js`; `npm run verify` green.
- [x] `done` **task-n8-11**: Declare Node engine for extension package scripts.
  - Acceptance:
    - `package.json` `engines.node` for `npm test` / `npm run verify`
    - operator doc states prerequisite
  - Evidence:
    - `engines.node: ">=18"` in `editor/le-vibe-native-extension/package.json`; `OPERATOR.md` prerequisites; `test/package-engines.test.js`; `npm run verify` green.
- [x] `done` **task-n8-12**: Package discovery metadata (`homepage`, `bugs`, `keywords`).
  - Acceptance:
    - `package.json` links to monorepo subtree and issue tracker
    - operator doc mentions fields
  - Evidence:
    - `package.json` `homepage`, `bugs.url`, `keywords`; `OPERATOR.md` note; `test/package-metadata.test.js` extended; `npm run verify` green.
- [x] `done` **task-n8-13**: README developer prerequisites (Node 18+).
  - Acceptance:
    - extension README states Node requirement aligned with `engines.node`
    - contract test prevents removal
  - Evidence:
    - `README.md` *Prerequisites (developers)*; `test/readme-prerequisites.test.js`; `npm run verify` green.
- [x] `done` **task-n8-14**: Operator-doc test covers `package.json` discovery fields.
  - Acceptance:
    - `OPERATOR.md` contract includes homepage / bugs / keywords alongside repository
  - Evidence:
    - `test/operator-doc.test.js` extended; `npm run verify` green.
- [x] `done` **task-n8-15**: Package `homepage` / `bugs` consistency with `repository`.
  - Acceptance:
    - automated check that `homepage` embeds `repository.directory`
    - `bugs.url` same host as `repository.url`
  - Evidence:
    - `test/package-homepage-consistency.test.js`; `npm run verify` green.
- [x] `done` **task-n8-16**: Package identity — `license` (SPDX) and `publisher`.
  - Acceptance:
    - `package.json` declares non-empty `publisher` and SPDX `license`
    - `OPERATOR.md` mentions these fields for operators
    - contract tests prevent accidental removal
  - Evidence:
    - `OPERATOR.md` sentence; `test/package-metadata.test.js` + `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-17**: Operator prerequisites include **`engines.vscode`** (minimum editor API).
  - Acceptance:
    - `OPERATOR.md` states VS Code–compatible minimum aligned with `package.json` `engines.vscode`
    - tests assert `engines.vscode` semver caret and OPERATOR text contract
  - Evidence:
    - `OPERATOR.md` prerequisites; `test/package-engines.test.js` + `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-18**: Extension README prerequisites include **`engines.vscode`** (aligned with OPERATOR).
  - Acceptance:
    - developer README states minimum editor API alongside Node
    - contract test prevents accidental removal
  - Evidence:
    - `README.md` prerequisites; `test/readme-prerequisites.test.js`; `npm run verify` green.
- [x] `done` **task-n8-19**: OPERATOR cross-links **README** *Prerequisites (developers)*.
  - Acceptance:
    - runbook points contributors to README for the same Node / `engines.vscode` guidance
    - contract test prevents removal of the cross-link
  - Evidence:
    - `OPERATOR.md` prerequisites paragraph; `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-20**: Documented VS Code minimum stays aligned with **`engines.vscode`**.
  - Acceptance:
    - automated test derives major.minor from `package.json` and requires README + OPERATOR to mention it
    - prevents silent drift when `engines.vscode` is bumped
  - Evidence:
    - `test/vscode-engine-doc-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-21**: Documented Node minimum stays aligned with **`engines.node`**.
  - Acceptance:
    - automated test derives minimum major from `package.json` and requires README + OPERATOR to use `Node.js N+` prose
    - prevents silent drift when `engines.node` is bumped
  - Evidence:
    - `test/node-engine-doc-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-22**: OPERATOR documents **local-first** default (no silent cloud fallback).
  - Acceptance:
    - runbook states local Ollama as default runtime posture
    - contract test prevents removal of that operator-facing guarantee
  - Evidence:
    - `OPERATOR.md` product line; `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-23**: Extension **README** documents **local-first** (aligned with OPERATOR).
  - Acceptance:
    - developer README states local Ollama default and no silent cloud fallback
    - contract test + cross-reference to OPERATOR
  - Evidence:
    - `README.md` Local-first line; `test/readme-local-first.test.js`; `npm run verify` green.
- [x] `done` **task-n8-24**: **Local-first** doc parity between OPERATOR and README.
  - Acceptance:
    - automated test requires the same anti–cloud-fallback sentence in both files
    - both reference `leVibeNative.ollamaEndpoint`
  - Evidence:
    - `test/local-first-doc-parity.test.js`; `npm run verify` green.
- [x] `done` **task-n8-25**: OPERATOR documents **telemetry** (local logs; remote only on explicit opt-in).
  - Acceptance:
    - aligns with product track “Telemetry: local structured logs only unless user explicitly opts in”
    - contract test prevents removal
  - Evidence:
    - `OPERATOR.md` Telemetry line; `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-26**: Extension **README** documents **telemetry** (aligned with OPERATOR).
  - Acceptance:
    - developer README states local structured logs by default and explicit opt-in for remote
    - parity on shared “defaults” phrasing with OPERATOR
  - Evidence:
    - `README.md` Telemetry line; `test/readme-telemetry.test.js`; `npm run verify` green.
- [x] `done` **task-n8-27**: **Lé Vibe Chat** documented as canonical user-facing chat name.
  - Acceptance:
    - OPERATOR + README state the product-track canonical name for palette/panel UX
    - parity test on shared sentence stem
  - Evidence:
    - `OPERATOR.md` + `README.md`; `test/canonical-product-name.test.js`; `npm run verify` green.
- [x] `done` **task-n8-28**: OPERATOR **bounded persistence** names transcript retention settings.
  - Acceptance:
    - runbook cites `chatTranscriptMaxBytes` / `chatTranscriptMaxMessages` and compaction behavior
    - contract test prevents accidental removal
  - Evidence:
    - `OPERATOR.md` *Bounded persistence*; `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-29**: README **bounded persistence** uses full **`leVibeNative.*`** transcript retention keys.
  - Acceptance:
    - developer doc matches OPERATOR setting IDs for JSONL caps
    - contract test scoped to *Bounded persistence inventory* section
  - Evidence:
    - `README.md`; `test/readme-storage-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-30**: **`package.json` `main`** entrypoint contract.
  - Acceptance:
    - `main` is `./extension.js` and the file exists (ship/packaging guardrail)
  - Evidence:
    - `test/package-main-entrypoint.test.js`; `npm run verify` green.
- [x] `done` **task-n8-31**: OPERATOR documents **`package.json` `main`** / `./extension.js` for packaging.
  - Acceptance:
    - runbook states the extension host entry path expected by VS Code / VSIX flow
    - contract test ties to n8-30 guardrail
  - Evidence:
    - `OPERATOR.md`; `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-32**: README documents **`main`** / **`./extension.js`** (aligned with OPERATOR).
  - Acceptance:
    - developer-facing intro names the VS Code activation entry and points to OPERATOR
    - contract test prevents removal
  - Evidence:
    - `README.md`; `test/readme-extension-entry.test.js`; `npm run verify` green.
- [x] `done` **task-n8-33**: Extension entry doc parity (OPERATOR ↔ README).
  - Acceptance:
    - automated test locks shared phrasing around `./extension.js` and VS Code activation entry
  - Evidence:
    - `test/extension-entry-doc-parity.test.js`; `npm run verify` green.
- [x] `done` **task-n8-34**: OPERATOR documents **default local Ollama URL** + **`leVibeNative.ollamaEndpoint`**.
  - Acceptance:
    - runbook states `http://127.0.0.1:11434` and ties smoke override env to the same default
    - contract test prevents removal
  - Evidence:
    - `OPERATOR.md`; `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-35**: README **default Ollama URL** + **`leVibeNative.ollamaEndpoint`** (aligned with OPERATOR).
  - Acceptance:
    - developer README states `http://127.0.0.1:11434`, setting key, and smoke override env
    - parity test on URL markdown stem shared with OPERATOR
  - Evidence:
    - `README.md`; `test/readme-ollama-default.test.js`; `test/ollama-default-doc-parity.test.js`; `npm run verify` green.
- [x] `done` **task-n8-36**: **`package.json`** default **`leVibeNative.ollamaEndpoint`** matches docs.
  - Acceptance:
    - automated test asserts contributes default is `http://127.0.0.1:11434` (same as OPERATOR/README)
  - Evidence:
    - `test/package-ollama-endpoint-default.test.js`; `npm run verify` green.
- [x] `done` **task-n8-37**: **`leVibeNative.ollamaTimeoutMs`** default matches OPERATOR smoke timeout.
  - Acceptance:
    - `package.json` contributes default is `2500` (ms)
    - OPERATOR smoke table still documents `default \`2500\`` for `LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS`
  - Evidence:
    - `test/package-ollama-timeout-default.test.js`; `npm run verify` green.
- [x] `done` **task-n8-38**: README documents **default Ollama probe timeout** (`leVibeNative.ollamaTimeoutMs` / smoke env).
  - Acceptance:
    - developer README states 2500 ms default, setting key, and `LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS`
    - contract test prevents removal
  - Evidence:
    - `README.md`; `test/readme-ollama-timeout.test.js`; `npm run verify` green.

---

## Per-pass completion checklist (engineering agents)

1. Implement only active task scope.
2. Add/update targeted tests.
3. Run relevant tests/verification commands.
4. Update this file task status + short evidence note.
5. Record any operator-only blockers under **USER FLAGGED ACTIONS REQUIRED**.
6. Create clean scoped commit(s), push, report status.

## USER FLAGGED ACTIONS REQUIRED

- _None currently._

