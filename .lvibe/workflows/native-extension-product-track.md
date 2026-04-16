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
6. **Lé Vibe Chat** converges toward **Cursor / GitHub Copilot–class** editor integration: structured proposals, diff preview, safe apply/undo, multi-file agent plans, and guarded file/terminal operations — without breaking local-first or storage constraints above.

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
- [x] `done` **task-n8-39**: OPERATOR documents **`leVibeNative.ollamaTimeoutMs`** + smoke timeout env.
  - Acceptance:
    - runbook names 2500 ms default, VS Code setting, and `LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS`
    - parity heading stem with README (n8-38)
  - Evidence:
    - `OPERATOR.md`; `test/operator-doc.test.js`; `test/ollama-probe-timeout-doc-parity.test.js`; `npm run verify` green.
- [x] `done` **task-n8-40**: **`smoke-integration.js`** Ollama fallbacks match **`package.json`** defaults.
  - Acceptance:
    - automated test reads contributes defaults and asserts the same literals appear in smoke script fallbacks
  - Evidence:
    - `test/smoke-defaults-match-package.test.js`; `npm run verify` green.
- [x] `done` **task-n8-41**: **`createOllamaClient`** default **`timeoutMs`** matches **`package.json`**.
  - Acceptance:
    - runtime client constructed with only `endpoint` exposes `timeoutMs` equal to `leVibeNative.ollamaTimeoutMs` default
  - Evidence:
    - `test/ollama-client-defaults-match-package.test.js`; `npm run verify` green.
- [x] `done` **task-n8-42**: **`createOllamaClient`** default **`model`** matches **`leVibeNative.ollamaModel`**.
  - Acceptance:
    - client exposes resolved `model`; equals `package.json` contributes default
  - Evidence:
    - `ollama.js` return shape; `test/ollama-client-model-default.test.js`; `npm run verify` green.
- [x] `done` **task-n8-43**: OPERATOR + README document **default Ollama model** (`leVibeNative.ollamaModel`).
  - Acceptance:
    - runbook and developer README state `mistral:latest` and the Settings key
    - parity test on shared `mistral:latest` markdown stem
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/operator-doc.test.js`; `test/readme-ollama-model.test.js`; `test/ollama-model-doc-parity.test.js`; `npm run verify` green.
- [x] `done` **task-n8-44**: Documented **Ollama model** tag stays aligned with **`package.json`** default.
  - Acceptance:
    - test reads `leVibeNative.ollamaModel` default and requires it in both OPERATOR and README
  - Evidence:
    - `test/ollama-model-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-45**: Documented **Ollama endpoint URL** stays aligned with **`package.json`** default.
  - Acceptance:
    - test reads `leVibeNative.ollamaEndpoint` default and requires it in both OPERATOR and README
  - Evidence:
    - `test/ollama-endpoint-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-46**: Documented **Ollama probe timeout (ms)** stays aligned with **`package.json`** `leVibeNative.ollamaTimeoutMs` default.
  - Acceptance:
    - test reads numeric default and requires its decimal string in both OPERATOR and README
  - Evidence:
    - `test/ollama-timeout-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-47**: Documented **transcript retention defaults** (`chatTranscriptMaxBytes`, `chatTranscriptMaxMessages`) stay aligned with **`package.json`** in OPERATOR and README.
  - Acceptance:
    - docs state byte and message-count defaults; test reads contributes defaults and requires both literals in OPERATOR and README
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/transcript-caps-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-48**: Documented **Ollama retry defaults** (`ollamaMaxRetries`, `ollamaRetryBackoffMs`) stay aligned with **`package.json`** in OPERATOR and README.
  - Acceptance:
    - runbook and README state numeric defaults next to setting keys; test reads contributes defaults and asserts each appears within a short window after its key (avoids ambiguous `2` substring matches)
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/ollama-retry-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-49**: Documented **Ollama stream guard defaults** (`ollamaStreamStallMs`, `ollamaStreamMaxMs`) stay aligned with **`package.json`** in OPERATOR and README.
  - Acceptance:
    - runbook and README name full `leVibeNative.*` keys with ms defaults; test asserts backtick-wrapped defaults near each key (same pattern as task-n8-48)
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/ollama-stream-guards-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-50**: Documented **workspace context budget defaults** (`contextMaxFiles`, `contextMaxCharsPerFile`, `contextMaxLinesPerFile`, `contextMaxTotalChars`) stay aligned with **`package.json`** in OPERATOR and README.
  - Acceptance:
    - runbook lists all four keys with defaults; README uses bold `leVibeNative.*` + backtick defaults; test asserts each default appears near its key in both files
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/workspace-context-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-51**: Documented **startup / rollout boolean defaults** (`enableFirstPartyAgentSurface`, `showFirstRunWizard`, `openPanelOnStartup`) stay aligned with **`package.json`** in OPERATOR and README.
  - Acceptance:
    - runbook and README name full `leVibeNative.*` keys with backtick `true`/`false` defaults where stated; test reads contributes booleans and requires `\`true\`` near each key in both files
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/startup-rollout-boolean-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-52**: Documented **migration nudge + live readiness booleans** (`showThirdPartyMigrationNudge`, `useLiveOllamaReadiness`) stay aligned with **`package.json`** in OPERATOR and README.
  - Acceptance:
    - runbook and README name full `leVibeNative.*` keys with backtick `true` near each key; test reads contributes defaults and asserts for both files
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/migration-readiness-boolean-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-53**: Documented **`leVibeNative.devStartupState`** default enum string stays aligned with **`package.json`** in OPERATOR and README.
  - Acceptance:
    - runbook states default and allowed enum values; README ties default to development override flow; test reads contributes default and requires backtick value near the setting key in both files
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/dev-startup-state-doc-package-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-54**: **Settings inventory guardrail** — every **`leVibeNative.*`** key in **`package.json`** contributes is mentioned in **OPERATOR** and/or **README**.
  - Acceptance:
    - test enumerates `contributes.configuration[0].properties` keys with `leVibeNative.` prefix and asserts each appears in combined operator + README text
  - Evidence:
    - `test/package-leVibeNative-keys-doc-inventory.test.js`; `npm run verify` green.
- [x] `done` **task-n8-55**: **OPERATOR** documents the **settings disclosure guardrail** (inventory test) under **Product track**.
  - Acceptance:
    - runbook tells operators that `npm test` runs `package-leVibeNative-keys-doc-inventory.test.js` and what failure means; `operator-doc.test.js` asserts key phrases
  - Evidence:
    - `OPERATOR.md`; `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-56**: **README** documents the same **settings disclosure guardrail** (inventory test) under *Operator verification / ship checklist*.
  - Acceptance:
    - developer README states `npm test` runs `package-leVibeNative-keys-doc-inventory.test.js` and cross-links OPERATOR *Product track*; dedicated README contract test
  - Evidence:
    - `README.md`; `test/readme-settings-disclosure-guardrail.test.js`; `npm run verify` green.
- [x] `done` **task-n8-57**: **Doc parity** — OPERATOR *Product track* and README *Operator verification* both name the **settings disclosure guardrail** and **`package-leVibeNative-keys-doc-inventory.test.js`**.
  - Acceptance:
    - parity test fails if either file drops the shared stem or inventory test path
  - Evidence:
    - `test/settings-disclosure-guardrail-doc-parity.test.js`; `npm run verify` green.
- [x] `done` **task-n8-58**: **`package.json` `scripts.test`** contract — **`node --test ./test/*.test.js`** (deterministic runner + glob).
  - Acceptance:
    - `verify-script.test.js` asserts exact `scripts.test` string so CI/agents cannot silently drop `*.test.js` discovery
  - Evidence:
    - `test/verify-script.test.js`; `npm run verify` green.
- [x] `done` **task-n8-59**: **`package.json` `scripts.smoke`** contract — **`node ./scripts/smoke-integration.js`** (deterministic smoke entrypoint).
  - Acceptance:
    - `verify-script.test.js` asserts exact `scripts.smoke` string
  - Evidence:
    - `test/verify-script.test.js`; `npm run verify` green.
- [x] `done` **task-n8-60**: **`package.json` `scripts.verify`** contract — **`npm test && npm run smoke`** (canonical ship gate).
  - Acceptance:
    - `verify-script.test.js` asserts exact `scripts.verify` string (replaces loose substring checks)
  - Evidence:
    - `test/verify-script.test.js`; `npm run verify` green.
- [x] `done` **task-n8-61**: **OPERATOR** + **README** include the exact **`package.json` `scripts.verify`** literal (**`npm test && npm run smoke`**).
  - Acceptance:
    - docs name `scripts.verify` alongside the verify UX; test reads `package.json` and requires the same string in both markdown files
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/verify-script-doc-literal-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-62**: **OPERATOR** + **README** include exact **`package.json` `scripts.test`** and **`scripts.smoke`** literals (aligned with **n8-58** / **n8-59**).
  - Acceptance:
    - runbook and developer README quote the full command strings; test reads `package.json` and requires both literals in each file
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/package-scripts-test-smoke-doc-literal-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-63**: **Umbrella doc sync** — **OPERATOR** + **README** contain every exact **`package.json` `scripts`** value (`test`, `smoke`, `verify`).
  - Acceptance:
    - single test iterates `package.json` `scripts` entries and requires each string literal in both markdown files
  - Evidence:
    - `test/package-json-all-scripts-doc-literal-sync.test.js`; `npm run verify` green.
- [x] `done` **task-n8-64**: **OPERATOR** + **README** document the **scripts literal umbrella** test (**n8-63**) under verification / **Product track**.
  - Acceptance:
    - runbook and developer README name `package-json-all-scripts-doc-literal-sync.test.js` and shared “Scripts literal umbrella” stem; parity + `operator-doc` contract tests
  - Evidence:
    - `OPERATOR.md`; `README.md`; `test/scripts-umbrella-guardrail-doc-parity.test.js`; `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-65**: **README-only** contract test for **scripts literal umbrella** (mirrors **n8-56** pattern for settings disclosure).
  - Acceptance:
    - `readme-scripts-umbrella-guardrail.test.js` asserts stem + umbrella test filename in README
  - Evidence:
    - `test/readme-scripts-umbrella-guardrail.test.js`; `npm run verify` green.
- [x] `done` **task-n8-66**: **OPERATOR** contract — **Product track** section cites the workflow board path **`.lvibe/workflows/native-extension-product-track.md`**.
  - Acceptance:
    - `operator-doc.test.js` asserts exact path string + “Product track” / Epic N8 context
  - Evidence:
    - `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n8-67**: **README** contract — *Operator verification / ship checklist* cites the same **Product track** workflow board path (**`.lvibe/workflows/native-extension-product-track.md`**); parity with OPERATOR.
  - Acceptance:
    - `readme-product-track-workflow-path.test.js` asserts path + section context in README
    - `product-track-workflow-doc-parity.test.js` asserts the exact path string appears in both **OPERATOR.md** and **README.md**
  - Evidence:
    - `README.md`; `test/readme-product-track-workflow-path.test.js`; `test/product-track-workflow-doc-parity.test.js`; `npm run verify` green.

### Epic N9 — Cursor/Copilot-like editor actions: apply, diff, undo

Product intent: users expect **Lé Vibe Chat** to drive the editor the way **Cursor** and **GitHub Copilot Chat** do: proposed edits are visible as diffs, applied safely, and reversible.

- [x] `done` **task-n9-1**: Define an **edit proposal contract** (JSON schema) for assistant output: target URI(s), replacement ranges or full-file content, rationale, and confidence flags.
  - Acceptance:
    - schema documented under `editor/le-vibe-native-extension/` (or `docs/`)
    - unit tests validate parse + reject malformed proposals
  - Evidence:
    - `schemas/levibe.edit-proposal.v1.json`; `EDIT_PROPOSAL.v1.md`; `edit-proposal.js` (`validateEditProposal`); `test/edit-proposal.test.js`; `npm run verify` green.
- [x] `done` **task-n9-2**: Implement **preview diff** before apply (side-by-side or unified diff in editor or webview), with explicit **Accept** / **Reject** / **Apply to file** actions.
  - Acceptance:
    - no silent whole-file overwrite without preview when setting requires preview (default on)
    - tests for accept/reject paths
  - Evidence:
    - `leVibeNative.requireEditPreviewBeforeApply` (default **true**); panel unified diff + **Accept preview** / **Reject** / **Apply to file**; `edit-preview.js` (`buildUnifiedDiff`, `canApplyAfterPreview`); `extension.js` sample path `.levibe-edit-preview-demo.txt`; `test/edit-preview.test.js`; `test/scaffold.test.js`; `README.md` / `OPERATOR.md`; `npm run verify` green.
- [x] `done` **task-n9-3**: Wire **WorkspaceEdit** / `TextEditorEdit` application with **single undo transaction** per accepted batch (VS Code undo stack behaves like one user action).
  - Acceptance:
    - one undo reverts entire accepted patch
    - integration test or manual checklist captured in OPERATOR
  - Evidence:
    - `workspace-edit-apply.js` (`applyEditProposalBatchAsWorkspaceEdit`, `applyFullFileAsSingleWorkspaceEdit`, `fullDocumentRange`); panel Apply uses `applyEdit` (not `fs.writeFile`); `test/workspace-edit-apply.test.js`; `OPERATOR.md` manual undo check; `README.md` / `EDIT_PROPOSAL.v1.md`; `npm run verify` green.
- [x] `done` **task-n9-4**: Support **partial selection apply** (apply only to highlighted range) and **multi-cursor safe** behavior (document limitations).
  - Acceptance:
    - documented behavior when selection missing or ambiguous
    - tests for at least single-selection happy path
  - Evidence:
    - `selection-apply.js` (`resolveSingleSelectionForPartialApply`, `SELECTION_APPLY_LIMITATIONS_MD`); palette command `leVibeNative.applySelectionDemoReplace`; `extension.js` demo `WorkspaceEdit.replace`; `test/selection-apply.test.js`; `README.md` / `OPERATOR.md`; `npm run verify` green.
- [x] `done` **task-n9-5**: Add **conflict detection** if file changed on disk since proposal generation (hash/mtime/version token); block apply with explicit remediation.
  - Acceptance:
    - deterministic conflict UX string in **Lé Vibe Chat** panel
    - test for stale-proposal path
  - Evidence:
    - `edit-conflict.js` (`buildPreviewRevision`, `checkDiskContentMatchesRevision`, stable `EDIT_PREVIEW_*` strings); `extension.js` apply gate + panel `chatUpdate`; `test/edit-conflict.test.js`; `README.md` / `OPERATOR.md` / `EDIT_PROPOSAL.v1.md`; `npm run verify` green.

### Epic N10 — Composer-style multi-file changes (plan → execute → verify)

Product intent: match **Cursor Composer** / multi-file Copilot flows: a single agent turn can touch several files with an ordered, auditable plan.

- [x] `done` **task-n10-1**: Introduce a **multi-step plan object** (ordered steps: create/apply/delete/move) produced by the model or orchestrator, validated before execution.
  - Acceptance:
    - invalid plans rejected with user-visible errors (no partial mystery writes)
    - schema + tests
  - Evidence:
    - `schemas/levibe.workspace-plan.v1.json`; `WORKSPACE_PLAN.v1.md`; `workspace-plan.js` (`validateWorkspacePlan`, `formatPlanValidationForUser`); `test/workspace-plan.test.js`; `README.md` / `OPERATOR.md`; `npm run verify` green.
- [x] `done` **task-n10-2**: Execute plan steps with **per-step progress** in **Lé Vibe Chat** (step N of M, file path, status).
  - Acceptance:
    - UI shows progress; logs structured events locally
    - cancel aborts remaining steps safely
  - Evidence:
    - `workspace-plan-exec.js` (`executeValidatedWorkspacePlan`, `lvibe.workspace_plan_audit.v1` JSONL at `workspace-plan-audit.jsonl`); panel **Run sample workspace plan** / **Cancel plan run** + `planRunUpdate` in `extension.js`; `storage-inventory.js` + README bounded table; tests `test/workspace-plan-exec.test.js`, `test/scaffold.test.js`, `test/storage-inventory.test.js`, `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n10-3**: **Rollback strategy**: on failure mid-plan, offer “undo applied steps” or leave workspace consistent with explicit partial state message.
  - Acceptance:
    - documented semantics + at least best-effort undo for same session
  - Evidence:
    - `workspace-plan-exec.js`: pre-step `capturePreStepSnapshot`, `inverseAfterSuccessfulStep`, failure returns `rollbackInverses`; `applyWorkspacePlanRollbackInverses` + `workspace_plan_rollback` audit; optional test hook `failStepAtIndex`; panel **Undo completed steps** + `planRollbackUpdate` in `extension.js`; `WORKSPACE_PLAN.v1.md` rollback section; README/OPERATOR; tests `test/workspace-plan-exec.test.js`, `test/scaffold.test.js`, `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n10-4**: Optional **dry-run** mode: list files that would change, with size/token estimates (bounded).
  - Acceptance:
    - dry-run output visible before commit to disk
  - Evidence:
    - `workspace-plan-dry-run.js` (`dryRunValidatedWorkspacePlan`, capped lines / read size); panel **Dry-run sample plan** before **Run sample workspace plan**; `buildSampleDemoWorkspacePlan` in `extension.js`; README / `WORKSPACE_PLAN.v1.md` / `OPERATOR.md`; tests `test/workspace-plan-dry-run.test.js`, `test/scaffold.test.js`, `test/operator-doc.test.js`; `pathLabelForStep` exported from `workspace-plan-exec.js`; `npm run verify` green.

### Epic N11 — File and workspace operations from chat (create / delete / rename)

Product intent: parity with Copilot/Cursor **agent** tools: create new files, scaffold folders, rename, delete with guardrails.

- [x] `done` **task-n11-1**: Implement **create file** and **create folder** actions with path validation (workspace-relative, no `..` escape, deny-list for sensitive roots).
  - Acceptance:
    - tests for path traversal rejection
    - open created file in editor on success (setting-gated)
  - Evidence:
    - `workspace-fs-actions.js` (`validateWorkspaceRelativeCreatePath`, `createWorkspaceFile`, `createWorkspaceFolder`); panel **Create file…** / **Create folder…** + commands `leVibeNative.createWorkspaceFile` / `leVibeNative.createWorkspaceFolder`; setting **`leVibeNative.openDocumentAfterWorkspaceCreate`** (default `true`); `test/workspace-fs-actions.test.js`, `test/scaffold.test.js`, `test/operator-doc.test.js`; README + `OPERATOR.md`; `npm run verify` green.
- [x] `done` **task-n11-2**: Implement **rename/move** with git-friendly behavior (optional: run through VS Code rename API).
  - Acceptance:
    - conflict handling documented
  - Evidence:
    - `workspace-fs-actions.js` (`moveWorkspaceEntry` — `WorkspaceEdit.renameFile` with `overwrite: false`, parent dirs for destination); panel **Move / rename…** + command **`leVibeNative.moveWorkspacePath`**; README *Move / rename* + `OPERATOR.md`; tests `test/workspace-fs-actions.test.js`, `test/scaffold.test.js`, `test/operator-doc.test.js`; `npm run verify` green.
- [x] `done` **task-n11-3**: Implement **delete file** behind explicit confirmation UX (never silent delete).
  - Acceptance:
    - confirmation modal or two-step confirm in panel
    - audit log line for destructive ops
  - Evidence:
    - Path prompt + modal **`showWarningMessage`** (`Delete` / cancel) before **`deleteWorkspaceEntry`**; panel **Delete file or folder…** + command **`leVibeNative.deleteWorkspacePath`**; JSONL **`workspace-fs-ops-audit.jsonl`** (`lvibe.workspace_fs_ops_audit.v1`) on success or failed delete after confirm; `workspace-fs-ops-audit.js`, `workspace-fs-actions.js`; README + `OPERATOR.md`; tests `workspace-fs-actions.test.js`, `workspace-fs-ops-audit.test.js`, `scaffold.test.js`, `operator-doc.test.js`, `storage-inventory.test.js`; `npm run verify` green.
- [x] `done` **task-n11-4**: **.gitignore / binary / large file** guards before reading/writing context (align with workspace context budget).
  - Acceptance:
    - deterministic skip reasons surfaced in UI
  - Evidence:
    - `context-file-guards.js` + `ignore` dependency — root `.gitignore`, `stat.size` vs `contextMaxCharsPerFile`, binary null-byte probe; `formatContextGuardUserMessage` strings; **`leVibeNative.pickContextFile`** filters QuickPick + `showWarningMessage` on skip; panel Workspace context copy; README + `OPERATOR.md`; `test/context-file-guards.test.js`, scaffold + `operator-doc` updates; `npm run verify` green.

### Epic N12 — “Inline assistant” affordances (Copilot-like)

Product intent: complement the chat panel with lightweight, Copilot-like triggers where appropriate (without duplicating full Copilot product).

- [x] `done` **task-n12-1**: Optional **CodeLens / lightbulb** entry: “Ask Lé Vibe Chat about this selection” → sends selection + file path into chat session.
  - Acceptance:
    - command registered; selection bounds passed correctly
    - works when panel closed (opens panel)
  - Evidence:
    - Command **`leVibeNative.askChatAboutSelection`** + editor context menu; CodeLens on selection range; `runAskChatAboutSelection` → `pendingSelectionContext` + **`executeCommand(openAgentSurface)`**; `flushPendingSelectionContext` pushes context + **`prefillPrompt`**; **`selection-chat-context.js`**; README + `OPERATOR.md`; tests `selection-chat-context.test.js`, scaffold, `operator-doc`; `npm run verify` green.
- [x] `done` **task-n12-2**: **Quick actions** strip in chat for common intents (explain, refactor selection, generate tests) as templated prompts (local-only).
  - Acceptance:
    - templates documented; no network calls beyond configured Ollama
  - Evidence:
    - Panel buttons **`quickActionExplain`** / **`quickActionRefactorSelection`** / **`quickActionGenerateTests`** → **`prefillPrompt`** + status; templates in **`chat-quick-actions.js`** (`explain`, `refactor_selection`, `generate_tests`); README lists exact template intents; **`OPERATOR.md`**; tests **`chat-quick-actions.test.js`**, scaffold + `operator-doc`; `npm run verify` green.

### Epic N13 — Terminal and command execution (Cursor-like, high risk — gated)

Product intent: Cursor-like agent runs can execute shell commands; this must be **opt-in**, obvious, and logged.

- [x] `done` **task-n13-1**: Design **terminal execution policy**: off by default; per-workspace opt-in; allow-list/deny-list patterns.
  - Acceptance:
    - written policy in docs + settings keys
  - Evidence:
    - `TERMINAL_EXECUTION_POLICY.md` + `terminal-execution-policy.js`; `package.json` contributes **`leVibeNative.terminalExecutionEnabled`** (default **false**), **`leVibeNative.terminalCommandAllowPatterns`**, **`leVibeNative.terminalCommandDenyPatterns`**; README + `OPERATOR.md`; `test/terminal-execution-policy.test.js`; `npm run verify` green in `editor/le-vibe-native-extension`.
- [x] `done` **task-n13-2**: If enabled, run commands in **VS Code terminal** with full user visibility (no hidden PTY).
  - Acceptance:
    - user must confirm each command batch unless an explicit “session allow” mode is enabled (advanced)
  - Evidence:
    - `terminal-exec.js` — `runCommandInVisibleTerminal` uses `Terminal.sendText` on a named visible terminal (`Lé Vibe Chat`); modal confirmation per batch; **Run and skip further prompts (this session)** + workspace-folder change + **`leVibeNative.clearTerminalSessionAllow`**; advanced **`leVibeNative.terminalSkipBatchConfirmation`**; palette + panel entrypoints; `test/terminal-exec.test.js`; README / `OPERATOR.md` / `TERMINAL_EXECUTION_POLICY.md`; `npm run verify` green.
- [x] `done` **task-n13-3**: Structured audit log for every executed command (timestamp, cwd, exit code).
  - Acceptance:
    - audit path documented next to other Lé Vibe Chat persistence
  - Evidence:
    - `terminal-command-audit.js` + `terminal-exec.js` append **`terminal-command-audit.jsonl`** (`lvibe.terminal_command_audit.v1`: `sent` line with timestamp/cwd/command; `shell_ended` line with **exit_code** when `onDidEndTerminalShellExecution` matches); `storage-inventory.js` / README bounded table / `OPERATOR.md`; `test/terminal-command-audit.test.js`, `terminal-exec.test.js`; `npm run verify` green.

### Epic N14 — Indexing & @-mentions (optional, bounded)

Product intent: Cursor-like **@file / @folder** context without unbounded embedding storage.

- [x] `done` **task-n14-1**: Implement **@file** / **@folder** picker backed by workspace file search (ripgrep or VS Code API), with strict caps.
  - Acceptance:
    - respects `contextMax*` settings; tests for cap enforcement
  - Evidence:
    - `at-mention-context.js` — `pickAtFileContext` / `pickAtFolderContext` (`findFiles` + `FILE_PICKER_MAX_SCAN_URIS`, folder QuickPick `FOLDER_QUICKPICK_MAX_CANDIDATES`, `.gitignore`); folder listing via `readDirectory` clipped with `contextMaxCharsPerFile` / `contextMaxLinesPerFile`; `workspace-context.js` `### FOLDER:` blocks; palette + panel commands; `test/at-mention-context.test.js` + `workspace-context.test.js`; README / `OPERATOR.md`; `npm run verify` green.
- [x] `done` **task-n14-2**: Optional **lightweight symbol index** (outline only) for current file — no full-repo embedding by default.
  - Acceptance:
    - documented limitations vs Cursor cloud index
  - Evidence:
    - `outline-context.js` — `fetchCurrentFileOutlineForContext` / `outlineTextFromSymbols` (`vscode.executeDocumentSymbolProvider`, caps `OUTLINE_MAX_SYMBOL_NODES` / depth, `contextMax*` via `clipTextByBudget`); `workspace-context.js` `### OUTLINE:`; palette + panel; README + `OPERATOR.md` limitations vs cloud index; `test/outline-context.test.js`; `npm run verify` green.

### Epic N15 — QA / parity gates for “agentic editor” releases

- [x] `done` **task-n15-1**: **E2E checklist** (manual or scripted): propose edit → preview → accept → undo → multi-file plan → cancel mid-flight.
  - Acceptance:
    - checklist lives in `OPERATOR.md` or extension README; signed off per release
  - Evidence:
    - Added **`OPERATOR.md`** section **E2E agentic editor release checklist (task-n15-1)** with steps A (Preview sample workspace edit → Accept preview → Apply to file → Undo) and B (Run sample workspace plan → Cancel plan run mid-flight) plus **Sign-off (per release)** table; **`README.md`** *Operator verification* cross-link; tests `test/operator-doc.test.js`, `test/readme-e2e-checklist-pointer.test.js`; `npm run verify` green.
- [x] `done` **task-n15-2**: **Regression tests** for proposal parser + WorkspaceEdit builder (golden files in `test/fixtures/`).
  - Acceptance:
    - `npm run verify` includes new tests; no flaky network
  - Evidence:
    - **`test/fixtures/n15-2/edit-proposal/`** + **`test/fixtures/n15-2/workspace-edit/`** golden JSON pairs; **`test/n15-2-golden-regression.test.js`**; shared mock **`test/mock-vscode-workspace-edit.js`** (used by **`workspace-edit-apply.test.js`**); **`OPERATOR.md`** *Regression goldens*; `npm run verify` green (no network).

### Epic N16 — CI, packaging, and install path

Product intent: **Lé Vibe Chat** is shippable from the monorepo with the same bar as the rest of the stack: automated verify in CI, reproducible VSIX/build artifacts, and docs for how `lvibe .` + installed extension line up.

- [x] `done` **task-n16-1**: Add a **repository CI job** (or extend an existing workflow) that runs `npm ci` + `npm run verify` in `editor/le-vibe-native-extension` on PR/push to `main` (Linux runner sufficient).
  - Acceptance:
    - workflow YAML checked in under `.github/workflows/` (or documented equivalent)
    - failing tests block merge (required check or documented manual gate if repo policy differs)
    - `OPERATOR.md` or root `README.md` mentions where CI runs extension verify
  - Evidence:
    - Added `.github/workflows/le-vibe-native-extension-ci.yml` (Ubuntu, Node 18, `npm ci` + `npm run verify` in `editor/le-vibe-native-extension`); **`OPERATOR.md`** *CI (GitHub Actions)* + root **`README.md`** pointer; branch-protection note for required checks; tests `test/ci-workflow-presence.test.js`, `operator-doc.test.js` (task-n16-1); `npm run verify` green.
- [x] `done` **task-n16-2**: **VSIX build script** + one-line docs: `npm run package` (or equivalent) produces an installable `.vsix`, with output path and `code --install-extension` example in `OPERATOR.md`.
  - Acceptance:
    - script exists in `editor/le-vibe-native-extension/package.json` `scripts`
    - `.gitignore` ignores `*.vsix` if written to disk
    - no secrets in VSIX build path
  - Evidence:
    - **`package.json`** **`scripts.package`** = **`vsce package`**; devDependency **`@vscode/vsce`**; **`.vscodeignore`** excludes **`test/`** and smoke script; root **`.gitignore`** **`*.vsix`**; **`LICENSE`** (MIT) for clean packaging; **`OPERATOR.md`** *Packaged VSIX* + **`README.md`** script literal; tests `verify-script.test.js`, `operator-doc.test.js`, `root-gitignore-vsix.test.js`; `npm run verify` green; local **`npm run package`** produces **`le-vibe-native-extension-0.1.0.vsix`**.
- [x] `done` **task-n16-3**: **Version alignment note** — `package.json` `version` vs git tags / deb packaging: single paragraph in `OPERATOR.md` describing how operators bump extension version for a release (even if “manual for now”).
  - Acceptance:
    - explicit bump checklist (edit version → tag? → attach VSIX?)
    - contract test optional; at minimum human-readable runbook
  - Evidence:
    - **`OPERATOR.md`** *Extension version vs monorepo / packaging (task-n16-3)* — **`package.json`** as source of truth, independence from **`debian/changelog`** / `.deb`, optional **`git tag`**, five-step **Version bump checklist** ending in **GitHub Release** / VSIX handoff; **`test/operator-doc.test.js`** (task-n16-3); `npm run verify` green.

### Epic N17 — UX polish and operator ergonomics

- [x] `done` **task-n17-1**: **Command palette audit** — ensure every user-facing **Lé Vibe Chat** command has a `category` and title consistent with canonical naming; add missing keybindings only where they do not conflict with VS Code defaults (document overrides in README).
  - Acceptance:
    - table in README or `OPERATOR.md`: command id → title → default keybinding (if any)
    - `npm run verify` green
  - Evidence:
    - **`package.json`** **`contributes.commands`**: **`category`** **`Lé Vibe Chat`**, short **`title`** (palette shows **`Lé Vibe Chat: <title>`**); no default **`keybindings`** (documented); **`README.md`** *Command palette and keyboard shortcuts (task-n17-1)* table (id → palette label → **—**); **`OPERATOR.md`** *Product track* pointer; **`third-party-migration.js`** / **`docs/native-extension-boundary.md`** strings aligned; tests `command-palette-contributions.test.js`, `operator-doc.test.js`, `scaffold.test.js`; `npm run verify` green.
- [x] `done` **task-n17-2**: **Panel accessibility pass** — focus order, button `title`/`aria` equivalents in webview HTML where applicable, and high-contrast theme spot-check (document known gaps).
  - Acceptance:
    - short **Accessibility** subsection in README with tested VS Code themes + OS
    - no regressions in `npm run verify`
  - Evidence:
    - **`extension.js`** `panelHtml` / `firstRunWizardHtml`: **`lang="en"`**, skip link, **`main`** landmark, **`nav`** for state pills, **`title`** + **`aria-label`** on buttons, labeled prompt **`textarea`**, **`aria-live`** status/log, edit-preview region labels; **`prefers-reduced-motion`**; **`README.md`** *Accessibility (task-n17-2)* (Linux / VS Code themes + gaps); **`OPERATOR.md`** pointer; tests **`panel-accessibility.test.js`**, **`operator-doc.test.js`**; `npm run verify` green.
- [x] `done` **task-n17-3**: **Status bar entry** (optional, setting-gated): show Ollama reachability or “Lé Vibe Chat” idle/active with link to open panel; default off or subtle to avoid noise.
  - Acceptance:
    - `leVibeNative.showStatusBarEntry` (or similar) in `package.json` contributes
    - clears on deactivate; tests for registration where mock allows
  - Evidence:
    - **`package.json`** **`leVibeNative.showStatusBarEntry`** (default **`false`**); **`status-bar-entry.js`** — right-aligned low-priority item, **`probeHealth`** refresh (90s interval, `maxRetries: 0`), click → **`leVibeNative.openAgentSurface`**; **`extension.js`** registers on activate; dispose clears item + interval + config listener via **`ExtensionContext.subscriptions`**; post-`await` **`!item`** guard avoids races on deactivate; **`README.md`** / **`OPERATOR.md`**; tests **`test/status-bar-entry.test.js`**, **`test/show-status-bar-entry-doc-sync.test.js`**, **`operator-doc.test.js`**; **`npm run verify`** green.

### Epic N18 — Hardening and tech debt (bounded)

- [x] `done` **task-n18-1**: **Dependency audit** — `npm audit` triage for `editor/le-vibe-native-extension`: document `overrides`/`resolutions` rationale or bump safe minors; record outcome in `OPERATOR.md` *Security notes*.
  - Acceptance:
    - committed lockfile/package updates if any
    - if vulnerabilities remain: documented risk + tracking issue link or internal id
  - Evidence:
    - **`npm audit`** (2026-04-15): **0 vulnerabilities** — no lockfile change required; production **`ignore`** @ **5.3.2** (latest **7.x** is a **major** bump; deferred absent audit findings — note in **`OPERATOR.md`** *Security notes*).
    - **`OPERATOR.md`** **`## Security notes (task-n18-1)`** — triage command, last outcome, **`overrides`** policy, **`bugs.url`** tracking pointer.
    - **`test/operator-doc.test.js`** (task-n18-1); **`npm run verify`** green.
- [x] `done` **task-n18-2**: **Flake hunt** — run `npm run verify` in a loop (e.g. 10× locally or in CI) and fix ordering/timing issues in tests; document any intentionally skipped cases.
  - Acceptance:
    - evidence note with command used and pass count
    - no new network-dependent tests in default verify
  - Evidence:
    - **`for i in $(seq 1 10); do npm run verify || exit 1; done`** from **`editor/le-vibe-native-extension/`** (2026-04-15): **10/10** passes; no ordering/timing fixes required this pass.
    - **`OPERATOR.md`** **`### Flake resistance (task-n18-2)`** — loop command, **10/10**, intentionally skipped tests **none**, policy against adding network-dependent tests to default **`npm test`** without explicit track + mocks.
    - **`test/operator-doc.test.js`** (task-n18-2); **`npm run verify`** green.

### Epic N19 — Post-track continuity (engineering backlog)

- [x] `done` **task-n19-1**: **CHANGELOG for native extension** — add **`editor/le-vibe-native-extension/CHANGELOG.md`** (Keep a Changelog–style: `## [version]` sections); seed **`## [0.1.0]`** with a short shipped-capabilities summary and pointer to this product-track file for full epic history; link from **`README.md`** and **`OPERATOR.md`**.
  - Acceptance:
    - `CHANGELOG.md` present at extension package root
    - README + OPERATOR cross-links
    - `operator-doc.test.js` (or equivalent) asserts the file exists / first section header
    - `npm run verify` green
  - Evidence:
    - **`editor/le-vibe-native-extension/CHANGELOG.md`** — **`# Changelog`**, **`## [0.1.0]`** (2026-04-15), Added bullets + product-track pointer; **`README.md`** / **`OPERATOR.md`** cross-links; version-bump step **6** in **`OPERATOR.md`** *Extension version vs monorepo / packaging*.
    - **`test/changelog-presence.test.js`**, **`operator-doc.test.js`** (task-n19-1); **`npm run verify`** green.

### Epic N20 — Post-track continuity (engineering backlog)

- [x] `done` **task-n20-1**: **Root README parity** — ensure the monorepo **root `README.md`** “Native extension” (or equivalent) subsection links to **`CHANGELOG.md`** as well as **`README.md`** / **`OPERATOR.md`** under **`editor/le-vibe-native-extension/`**, so release readers find semver notes from the repo landing page.
  - Acceptance:
    - root README diff only (no unrelated doc churn)
    - link to `editor/le-vibe-native-extension/CHANGELOG.md`
    - `npm run verify` in `editor/le-vibe-native-extension/` still green (extension tests unchanged or extended if a root-doc contract test is added at repo root)
  - Evidence:
    - **Root `README.md`** *Documentation & project depth* — added **semver release notes** link to **`editor/le-vibe-native-extension/CHANGELOG.md`** alongside README, OPERATOR, product track.
    - **`test/root-readme-pointer.test.js`** — **`monorepo root README links native extension CHANGELOG (task-n20-1)`**; **`npm run verify`** green.

### Epic N21 — Post-track continuity (engineering backlog)

- [x] `done` **task-n21-1**: **`docs/README.md` CHANGELOG parity** — extend **`docs/README.md`** first-party native extension bullet (or adjacent line) with the same **`editor/le-vibe-native-extension/CHANGELOG.md`** link so the maintainer index matches the repo landing page.
  - Acceptance:
    - `docs/README.md` only (plus product-track / tests if contract test added under `editor/le-vibe-native-extension/test/`)
    - link path matches root README
    - `npm run verify` green
  - Evidence:
    - **`docs/README.md`** maintainer table — **semver release notes** link to **`../editor/le-vibe-native-extension/CHANGELOG.md`** (path token **`editor/le-vibe-native-extension/CHANGELOG.md`** matches root **`README.md`**).
    - **`test/docs-readme-pointer.test.js`** — **`docs/README.md links native extension CHANGELOG (task-n21-1)`**; **`npm run verify`** green.

### Epic N22 — Post-track continuity (engineering backlog)

- [x] `done` **task-n22-1**: **OPERATOR VSIX note — CHANGELOG ships** — under **`OPERATOR.md`** *Packaged VSIX (task-n16-2)*, add one sentence that **`CHANGELOG.md`** is **not** listed in **`.vscodeignore`**, so semver release notes ship inside the **`.vsix`** alongside the extension sources operators expect.
  - Evidence:
    - **`OPERATOR.md`** *Packaged VSIX* — **`CHANGELOG.md ships in the VSIX (task-n22-1)`** paragraph (what **`.vscodeignore`** omits vs **`CHANGELOG.md`**).
    - **`test/operator-doc.test.js`** (task-n22-1); **`test/vscodeignore-changelog-ships.test.js`** — asserts **`.vscodeignore`** does not list **`CHANGELOG.md`**; **`npm run verify`** green.

### Epic N23 — Post-track continuity (engineering backlog)

- [x] `done` **task-n23-1**: **Manual VSIX install spot-check (OPERATOR)** — add one bullet under *Packaged VSIX (task-n16-2)* or the *E2E agentic editor release checklist*: after **`code --install-extension ./le-vibe-native-extension-<version>.vsix`**, confirm the Extensions view lists **Lé Vibe Native Agent** (or the **`displayName`** from **`package.json`**) at the expected **`version`**.
  - Acceptance:
    - **`OPERATOR.md`** only (short manual verification step)
    - **`operator-doc.test.js`** asserts the new bullet/heading token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** *Packaged VSIX* — **`Manual spot-check (task-n23-1)`** — Extensions view, **`displayName`** **Lé Vibe Native Agent**, publisher **`levibe`**, version matches **`package.json`** **`version`**.
    - **`test/operator-doc.test.js`** (task-n23-1); **`npm run verify`** green.

### Epic N24 — Post-track continuity (engineering backlog)

- [x] `done` **task-n24-1**: **OPERATOR Packaged VSIX — alternate CLI** — add one sentence after the **`code --install-extension`** example: if **`code`** is not on **`PATH`**, use **`codium`** or your editor’s equivalent (**`--install-extension`** path unchanged).
  - Evidence:
    - **`OPERATOR.md`** *Packaged VSIX* — **`Alternate CLI (task-n24-1)`** — **`which code`**, **`codium`** / **`vscodium`**, same **`--install-extension`** + **`.vsix`** path; example **`codium --install-extension …`**.
    - **`test/operator-doc.test.js`** (task-n24-1); **`npm run verify`** green.

### Epic N25 — Post-track continuity (engineering backlog)

- [x] `done` **task-n25-1**: **Extension README — issues / bugs link** — add a short line (e.g. under **Operators** or **Prerequisites**) with **`package.json`** **`bugs.url`** so contributors can file first-party extension issues without hunting **`package.json`**.
  - Acceptance:
    - **`editor/le-vibe-native-extension/README.md`** only (plus product-track / `operator-doc` or README contract test if you add one)
    - full **`https://github.com/ryan-lgtm/le-vibe/issues`** string (or derive from **`package.json`** in test)
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Issues / bugs (task-n25-1)`** with full **`bugs.url`** + note to tag extension path.
    - **`test/readme-bugs-url.test.js`** — asserts **`README.md`** contains **`package.json`** **`bugs.url`**; **`npm run verify`** green.

### Epic N26 — Post-track continuity (engineering backlog)

- [x] `done` **task-n26-1**: **Extension README — `homepage` link** — add one line (near **Issues** or **Operators**) with **`package.json`** **`homepage`** so contributors can open the GitHub **tree** view for this package without assembling the URL manually.
  - Acceptance:
    - **`README.md`** + contract test deriving URL from **`package.json`**
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Source on GitHub (task-n26-1)`** with full **`homepage`** URL + **`package.json`** key reference.
    - **`test/readme-homepage-url.test.js`**; **`npm run verify`** green.

### Epic N27 — Post-track continuity (engineering backlog)

- [x] `done` **task-n27-1**: **OPERATOR — README pointers for issues + source** — under **`OPERATOR.md`** *Product track* (or *Verify*), add one line cross-linking **`README.md`** *Issues / bugs (task-n25-1)* and *Source on GitHub (task-n26-1)* so operators land on the same **`bugs.url`** / **`homepage`** strings without opening **`package.json`**.
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token for the cross-link
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: issues + GitHub source (task-n27-1)`** under *Product track*; points to README section headings **`task-n25-1`** / **`task-n26-1`**.
    - **`test/operator-doc.test.js`** — **`task-n27-1`** token test; **`npm run verify`** green.

### Epic N28 — Post-track continuity (engineering backlog)

- [x] `done` **task-n28-1**: **Extension README — `repository` field** — add one line (near **Issues** / **Source on GitHub**) documenting **`package.json`** **`repository`** (**`type`**, **`url`**, **`directory`**) so contributors know the monorepo clone URL and subdirectory path without assembling it manually; include contract test deriving **`url`** + **`directory`** from **`package.json`**.
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Monorepo clone (task-n28-1)`** with **`git`** + **`url`** + **`directory`**.
    - **`test/readme-repository.test.js`**; **`npm run verify`** green.

### Epic N29 — Post-track continuity (engineering backlog)

- [x] `done` **task-n29-1**: **OPERATOR — README pointer for monorepo clone** — under **`OPERATOR.md`** *Product track*, add one line cross-linking **`README.md`** *Monorepo clone (task-n28-1)* for **`package.json`** **`repository`** (**`url`** + **`directory`**) so operators match the **`task-n27-1`** pattern (issues/source + clone path).
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: monorepo clone (task-n29-1)`** under *Product track*.
    - **`test/operator-doc.test.js`** — **`task-n29-1`** token test; **`npm run verify`** green.

### Epic N30 — Post-track continuity (engineering backlog)

- [x] `done` **task-n30-1**: **Extension README — SPDX `license`** — add one line (near **Operators** or **Monorepo clone**) documenting **`package.json`** **`license`** (SPDX string, aligned with **`OPERATOR.md`** *publisher and license*) so contributors see marketplace/CI identity without opening **`package.json`**; include contract test deriving the string from **`package.json`**.
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`License (task-n30-1)`** with SPDX + **`package.json`** **`license`**.
    - **`test/readme-license.test.js`**; **`npm run verify`** green.

### Epic N31 — Post-track continuity (engineering backlog)

- [x] `done` **task-n31-1**: **OPERATOR — README pointer for SPDX license** — under **`OPERATOR.md`** *Product track*, add one line cross-linking **`README.md`** *License (task-n30-1)* for **`package.json`** **`license`** so operators align with **`task-n27-1`** / **`task-n29-1`** doc-discovery pattern.
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: SPDX license (task-n31-1)`** under *Product track*.
    - **`test/operator-doc.test.js`** — **`task-n31-1`** token test; **`npm run verify`** green.

### Epic N32 — Post-track continuity (engineering backlog)

- [x] `done` **task-n32-1**: **Extension README — `publisher`** — add one line (near **License** or **Operators**) documenting **`package.json`** **`publisher`** (marketplace identity; pairs with **`license`**) so contributors see the extension id prefix without opening **`package.json`**; include contract test deriving the string from **`package.json`**.
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Publisher (task-n32-1)`** with **`package.json`** **`publisher`** + id-prefix note.
    - **`test/readme-publisher.test.js`**; **`npm run verify`** green.

### Epic N33 — Post-track continuity (engineering backlog)

- [x] `done` **task-n33-1**: **OPERATOR — README pointer for `publisher`** — under **`OPERATOR.md`** *Product track*, add one line cross-linking **`README.md`** *Publisher (task-n32-1)* for **`package.json`** **`publisher`** so operators align with **`task-n31-1`** doc-discovery pattern.
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: publisher (task-n33-1)`** under *Product track*.
    - **`test/operator-doc.test.js`** — **`task-n33-1`** token test; **`npm run verify`** green.

### Epic N34 — Post-track continuity (engineering backlog)

- [x] `done` **task-n34-1**: **Extension README — `keywords`** — add one line (near **Publisher** or **Operators**) documenting **`package.json`** **`keywords`** (registry/search hints) so contributors see the shipped tag list without opening **`package.json`**; include contract test asserting every **`keywords[]`** entry appears in **`README.md`** (or derive from **`package.json`** in test).
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Keywords (task-n34-1)`** listing all **`keywords`** entries.
    - **`test/readme-keywords.test.js`**; **`npm run verify`** green.

### Epic N35 — Post-track continuity (engineering backlog)

- [x] `done` **task-n35-1**: **OPERATOR — README pointer for `keywords`** — under **`OPERATOR.md`** *Product track*, add one line cross-linking **`README.md`** *Keywords (task-n34-1)* for **`package.json`** **`keywords`** so operators align with **`task-n33-1`** doc-discovery pattern.
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: keywords (task-n35-1)`** under *Product track*.
    - **`test/operator-doc.test.js`** — **`task-n35-1`** token test; **`npm run verify`** green.

### Epic N36 — Post-track continuity (engineering backlog)

- [x] `done` **task-n36-1**: **Extension README — marketplace `categories`** — add one line (near **Keywords** or **Publisher**) documenting **`package.json`** **`categories`** (VS Code marketplace extension category) so contributors see the shipped value without opening **`package.json`**; include contract test deriving the array from **`package.json`** (every category string appears in **`README.md`**).
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Categories (task-n36-1)`** with **`package.json`** **`categories`**.
    - **`test/readme-categories.test.js`**; **`npm run verify`** green.

### Epic N37 — Post-track continuity (engineering backlog)

- [x] `done` **task-n37-1**: **OPERATOR — README pointer for `categories`** — under **`OPERATOR.md`** *Product track*, add one line cross-linking **`README.md`** *Categories (task-n36-1)* for **`package.json`** **`categories`** so operators align with **`task-n35-1`** doc-discovery pattern.
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: categories (task-n37-1)`** under *Product track*.
    - **`test/operator-doc.test.js`** — **`task-n37-1`** token test; **`npm run verify`** green.

### Epic N38 — Post-track continuity (engineering backlog)

- [x] `done` **task-n38-1**: **Extension README — `displayName`** — add one line (near **Operators** or **Categories**) documenting **`package.json`** **`displayName`** (marketplace / Extensions UI title; distinct from **`name`**) so contributors see the shipped listing title without opening **`package.json`**; include contract test deriving the string from **`package.json`**.
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Display name (task-n38-1)`** with **`package.json`** **`displayName`**.
    - **`test/readme-display-name.test.js`**; **`npm run verify`** green.

### Epic N39 — Post-track continuity (engineering backlog)

- [x] `done` **task-n39-1**: **OPERATOR — README pointer for `displayName`** — under **`OPERATOR.md`** *Product track*, add one line cross-linking **`README.md`** *Display name (task-n38-1)* for **`package.json`** **`displayName`** so operators align with **`task-n37-1`** doc-discovery pattern.
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: displayName (task-n39-1)`** under *Product track*.
    - **`test/operator-doc.test.js`** — **`task-n39-1`** token test; **`npm run verify`** green.

### Epic N40 — Post-track continuity (engineering backlog)

- [x] `done` **task-n40-1**: **Extension README — `description`** — add one line (near **Display name** or **Operators**) documenting **`package.json`** **`description`** so contributors see the shipped marketplace summary text without opening **`package.json`**; include contract test deriving the string from **`package.json`**.
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Description (task-n40-1)`** with full **`package.json`** **`description`** text.
    - **`test/readme-description.test.js`**; **`npm run verify`** green.

### Epic N41 — Post-track continuity (engineering backlog)

- [x] `done` **task-n41-1**: **OPERATOR — README pointer for `description`** — under **`OPERATOR.md`** *Product track*, add one line cross-linking **`README.md`** *Description (task-n40-1)* for **`package.json`** **`description`** so operators align with **`task-n39-1`** doc-discovery pattern.
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: description (task-n41-1)`** under *Product track*.
    - **`test/operator-doc.test.js`** — **`task-n41-1`** token test; **`npm run verify`** green.

### Epic N42 — Post-track continuity (engineering backlog)

- [x] `done` **task-n42-1**: **Extension README — `name`** — add one line (near **Display name** / **Description**) documenting **`package.json`** **`name`** (npm/package identifier; distinct from **`displayName`**) so contributors see the shipped package id without opening **`package.json`**; include contract test deriving the string from **`package.json`**.
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Package name (task-n42-1)`** with **`package.json`** **`name`**.
    - **`test/readme-name.test.js`**; **`npm run verify`** green.

### Epic N43 — Post-track continuity (engineering backlog)

- [x] `done` **task-n43-1**: **OPERATOR — README pointer for `name`** — under **`OPERATOR.md`** *Product track*, add one line cross-linking **`README.md`** *Package name (task-n42-1)* for **`package.json`** **`name`** so operators align with **`task-n41-1`** doc-discovery pattern.
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: package name (task-n43-1)`** under *Product track*.
    - **`test/operator-doc.test.js`** — **`task-n43-1`** token test; **`npm run verify`** green.

### Epic N44 — Post-track continuity (engineering backlog)

- [x] `done` **task-n44-1**: **Extension README — `version`** — add one line (near **Package name** / **Changelog**) documenting **`package.json`** **`version`** so contributors can see the currently shipped extension package version without opening **`package.json`**; include contract test deriving the string from **`package.json`**.
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green
  - Evidence:
    - **`README.md`** — **`Version (task-n44-1)`** with **`package.json`** **`version`**.
    - **`test/readme-version.test.js`**; **`npm run verify`** green.

### Epic N45 — Post-track continuity (engineering backlog)

- [x] `done` **task-n45-1**: **OPERATOR — README pointer for `version`** — under **`OPERATOR.md`** *Product track*, add one line cross-linking **`README.md`** *Version (task-n44-1)* for **`package.json`** **`version`** so operators align with **`task-n43-1`** doc-discovery pattern.
  - Acceptance:
    - **`OPERATOR.md`** + **`operator-doc.test.js`** token
    - **`npm run verify`** green
  - Evidence:
    - **`OPERATOR.md`** — **`README: version (task-n45-1)`** under *Product track*.
    - **`test/operator-doc.test.js`** — **`task-n45-1`** token test; **`npm run verify`** green.

### Epic N46 — Post-track continuity (engineering backlog)

- [ ] `pending` **task-n46-1**: **Extension README — `engines.vscode` minimum** — add one line (near **Prerequisites**) documenting the current minimum editor API baseline from **`package.json`** **`engines.vscode`** so contributors can see the runtime floor without scanning JSON; include contract test deriving the major/minor from **`engines.vscode`**.
  - Acceptance:
    - **`README.md`** + targeted test
    - **`npm run verify`** green

---

## Board hygiene (engineering agents)

If **Protocol 1–2** reports **no** `[ ]` rows and **no** `` `pending` `` tasks, **stop** and add at least one new **`pending`** task under the next epic (or a new Epic N*) with acceptance criteria before closing the pass — or escalate to product. The board must never be “all done” without an explicit product decision to freeze the track.

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

