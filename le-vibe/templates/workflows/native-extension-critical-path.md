# Lé Vibe Chat Critical Path (No-Fluff Product Track)

**Outcome that matters:** ship Lé Vibe IDE with a first-party, in-app AI agent that works locally with Ollama and can safely create/edit/delete project files live (Cursor-like behavior).

## Scope filter (hard rule)

Only do work that directly improves one of these:
1. In-app chat + model interaction quality
2. Live workspace actions (create/edit/delete/move) with preview + undo + safety
3. Ollama local runtime reliability + latency + failure handling
4. Code completion/suggestion UX in-editor
5. Release readiness for shipping this as default in Lé Vibe IDE

Everything else is out-of-scope unless required to unblock one of the five.

---

## Epic CP0 — First-party runtime authority (remove third-party dependency)

**Narrative:** Lé Vibe Chat must be the default agent surface. Installer, readiness checks, and operator flows cannot depend on Continue/Cline.

- [x] `done` **task-cp0-1**: Replace installer runtime extension install step with first-party extension install/activation verification.
  - Acceptance:
    - `install-le-vibe-local.sh` validates first-party extension is installed/active
    - no runtime hard dependency on Continue/Cline installer scripts
  - Evidence (2026-04-15):
    - Updated `packaging/scripts/install-le-vibe-local.sh` to verify/install `levibe.le-vibe-native-extension` from local VSIX and removed runtime invocation of `install-cline-extension.sh`.
    - Updated `le-vibe/tests/test_install_le_vibe_local_script_contract.py` runtime contract assertions to first-party extension readiness semantics.
    - Verification: `python -m pytest le-vibe/tests/test_install_le_vibe_local_script_contract.py le-vibe/tests/test_uninstall_le_vibe_local_script_contract.py` (23 passed).
- [x] `done` **task-cp0-2**: Replace first-run readiness gate to check Lé Vibe Chat instead of third-party extension IDs.
  - Acceptance:
    - readiness passes with first-party extension only
    - tests updated for new extension ID/path
  - Evidence (2026-04-15):
    - Updated `le-vibe/le_vibe/first_run.py` readiness gate to require `levibe.le-vibe-native-extension` and removed third-party extension-ID gating.
    - Updated `le-vibe/tests/test_first_run.py` to validate readiness success with first-party extension presence and failure when first-party extension is missing.
    - Verification: `python -m pytest le-vibe/tests/test_first_run.py le-vibe/tests/test_install_le_vibe_local_script_contract.py` (28 passed).
- [x] `done` **task-cp0-3**: Add migration cleanup for prior Continue/Cline extension artifacts in fresh install path.
  - Acceptance:
    - documented and tested cleanup behavior
    - no stale third-party extension state after `--fresh-install`
  - Evidence (2026-04-15):
    - Updated `packaging/scripts/uninstall-le-vibe-local.sh` purge-agent-artifacts cleanup to remove stale third-party extension artifacts: extension directories (`continue.continue-*`, `saoudrizwan.claude-dev-*`) and legacy `globalStorage` state.
    - Updated `le-vibe/tests/test_uninstall_le_vibe_local_script_contract.py` to assert cleanup contract strings for third-party extension/artifact removal paths.
    - Verification: `python -m pytest le-vibe/tests/test_uninstall_le_vibe_local_script_contract.py le-vibe/tests/test_install_le_vibe_local_script_contract.py` (23 passed).

## Epic CP1 — Chat core loop quality (daily-driver usable)

**Narrative:** chat must be fast, clear, cancellable, and resilient with local Ollama.

- [x] `done` **task-cp1-1**: Harden streaming lifecycle (send, token stream, cancel, retry, timeout states).
  - Acceptance:
    - deterministic UI state machine; no stuck "loading"
    - tests for cancel/retry/timeout paths
  - Evidence (2026-04-15):
    - Updated `editor/le-vibe-native-extension/chat.js` with an explicit chat lifecycle state machine (`sending`, `streaming`, `retrying`, `cancelled`, `completed`, `error`, `idle`) and deterministic idle cleanup after success/cancel/error.
    - Updated `editor/le-vibe-native-extension/test/chat.test.js` to assert state transitions and coverage for cancel/retry/timeout paths, including final idle state to prevent stuck loading.
    - Verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 323 passed, smoke passed).
- [x] `done` **task-cp1-2**: Add conversation controls that matter in real use (new chat, restore recent, clear/export).
  - Acceptance:
    - bounded persistence unchanged
    - clear operator-visible paths/docs
  - Evidence (2026-04-15):
    - Updated `editor/le-vibe-native-extension/extension.js` and `editor/le-vibe-native-extension/package.json` to add new conversation controls: `leVibeNative.startNewChatSession` and `leVibeNative.restoreRecentPrompt`, plus panel buttons (`New chat`, `Restore recent…`) and transcript-backed recent prompt restore flow.
    - Updated `editor/le-vibe-native-extension/README.md` command/storage control docs and `editor/le-vibe-native-extension/test/scaffold.test.js` command/export/panel assertions for the new controls.
    - Verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 323 passed, smoke passed).
- [x] `done` **task-cp1-3**: Add prompt context controls in-panel (`@file`, `@folder`, selection explain/refactor/tests).
  - Acceptance:
    - strict token/file caps respected
    - visible skip reasons for disallowed/large/binary files
  - Evidence (2026-04-15):
    - Existing in-panel context controls were already wired (`@file`, `@folder`, selection quick actions explain/refactor/tests) with strict `contextMax*` cap enforcement in `workspace-context.js`, `context-file-guards.js`, and `at-mention-context.js`.
    - Updated `editor/le-vibe-native-extension/at-mention-context.js` and `editor/le-vibe-native-extension/extension.js` so `@file/@folder` guard failures return and surface explicit in-panel skip messages (`Lé Vibe Chat: skipped …`) instead of relying on toast-only visibility.
    - Added targeted tests in `editor/le-vibe-native-extension/test/at-mention-context.test.js` for visible skip-message returns; verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 325 passed, smoke passed).

## Epic CP2 — Cursor-like live edits (propose → preview → apply → undo)

**Narrative:** this is the core trust loop; no silent destructive writes.

- [x] `done` **task-cp2-1**: Structured edit proposals with schema validation and user-visible parse errors.
  - Acceptance:
    - invalid proposals never write to disk
  - Evidence (2026-04-15):
    - Updated `editor/le-vibe-native-extension/extension.js` panel flow to add explicit in-panel JSON proposal validation (`validateEditProposalJson`) with parse-error messaging (`Lé Vibe Chat: edit proposal parse error — …`) and schema validation messaging before any preview/apply path.
    - Updated `editor/le-vibe-native-extension/edit-proposal.js` to add `formatEditProposalValidationForUser()` for deterministic, user-visible invalid-proposal summaries.
    - Added regression coverage in `editor/le-vibe-native-extension/test/edit-proposal.test.js` (invalid-summary formatting/truncation) and `editor/le-vibe-native-extension/test/scaffold.test.js` (panel includes proposal validation controls).
    - Verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 327 passed, smoke passed).
- [x] `done` **task-cp2-2**: Diff preview and explicit accept/reject/apply actions as default path.
  - Acceptance:
    - preview required by default before apply
  - Evidence (2026-04-15):
    - Updated `editor/le-vibe-native-extension/edit-preview.js` with deterministic `reducePreviewUiState()` reducer for explicit preview actions (`preview_shown`, `accept`, `reject`) so the default `requireEditPreviewBeforeApply=true` path keeps Apply disabled until Accept and always disables Apply after Reject.
    - Updated `editor/le-vibe-native-extension/extension.js` to enforce explicit action handling with active-session checks: Accept/Reject without a pending preview now surface clear in-panel status and never enable apply.
    - Added coverage in `editor/le-vibe-native-extension/test/edit-preview.test.js` for default-path gating, reject clear behavior, and no-session accept blocking.
    - Verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 330 passed, smoke passed).
- [x] `done` **task-cp2-3**: WorkspaceEdit apply with single undo transaction per accepted batch.
  - Acceptance:
    - one undo reverts batch
  - Evidence (2026-04-15):
    - Hardened `editor/le-vibe-native-extension/workspace-edit-apply.js` to explicitly reject empty proposal batches before any write call and preserve a single `workspace.applyEdit` call for each accepted validated batch.
    - Added focused regression tests in `editor/le-vibe-native-extension/test/workspace-edit-apply.test.js` for mixed full-file + range edits in one batch (`getApplyCount() === 1`) and for empty-batch rejection without any `applyEdit` call.
    - Verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 332 passed, smoke passed).
- [x] `done` **task-cp2-4**: Stale-file conflict detection (version/hash/mtime) before apply.
  - Acceptance:
    - deterministic conflict remediation shown to user
  - Evidence (2026-04-15):
    - Updated `editor/le-vibe-native-extension/edit-conflict.js` preview revision contract to include metadata snapshot (`mtimeMs`, `sizeBytes`) alongside content hash and added deterministic metadata conflict copy (`EDIT_PREVIEW_METADATA_CONFLICT_MESSAGE`).
    - Updated `editor/le-vibe-native-extension/extension.js` preview capture to snapshot file stat metadata at preview time and pass it into `buildPreviewRevision(...)` so apply-time checks enforce mtime/size drift plus hash mismatch and missing-file remediation.
    - Added regression coverage in `editor/le-vibe-native-extension/test/edit-conflict.test.js` for mtime-drift and size-drift blocked apply behavior with deterministic remediation messages.
    - Verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 334 passed, smoke passed).

## Epic CP3 — Agentic file system operations (create/edit/delete/move)

**Narrative:** Lé Vibe Chat must perform project changes end-to-end safely.

- [x] `done` **task-cp3-1**: Create file/folder from chat with path traversal protection.
  - Acceptance:
    - workspace-relative only; deny-list enforced
  - Evidence (2026-04-15):
    - Hardened `editor/le-vibe-native-extension/workspace-fs-actions.js` path validation to enforce deny-list segments case-insensitively (e.g., `.GIT`, `Node_Modules`) in addition to existing workspace-relative traversal blocking.
    - Extended `editor/le-vibe-native-extension/test/workspace-fs-actions.test.js` with uppercase/mixed-case deny-list regression assertions to prove create-path guardrails reject bypass attempts.
    - Existing create flows in `editor/le-vibe-native-extension/extension.js` remain wired through `validateWorkspaceRelativeCreatePath(...)` + `createWorkspaceFile(...)` / `createWorkspaceFolder(...)` for interactive chat/panel entrypoints.
    - Verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 334 passed, smoke passed).
- [x] `done` **task-cp3-2**: Move/rename flow with conflict handling and git-friendly behavior.
  - Acceptance:
    - destination conflict path covered in tests
  - Evidence (2026-04-15):
    - Hardened `editor/le-vibe-native-extension/workspace-fs-actions.js` fallback move path to normalize destination-exists rename errors (`FileExists` / `EEXIST` / “exists” message) into the same deterministic no-overwrite conflict remediation used by the primary path.
    - Added focused tests in `editor/le-vibe-native-extension/test/workspace-fs-actions.test.js` to assert git-friendly behavior (`WorkspaceEdit.renameFile` invoked with `overwrite: false`) and destination-conflict handling in the fallback `workspace.fs.rename` path.
    - Verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 336 passed, smoke passed).
- [x] `done` **task-cp3-3**: Delete flow with explicit confirmation + audit log.
  - Acceptance:
    - no silent delete path exists
  - Evidence (2026-04-15):
    - Hardened `editor/le-vibe-native-extension/workspace-fs-actions.js` so `deleteWorkspaceEntry(...)` now requires explicit caller confirmation (`confirmedByUser: true`) and refuses execution otherwise, closing silent invocation paths.
    - Updated `editor/le-vibe-native-extension/extension.js` delete flow to pass explicit confirmation only after the modal `"Delete"` acknowledgment step, preserving two-step operator-visible delete behavior and existing audit append flow.
    - Added regression coverage in `editor/le-vibe-native-extension/test/workspace-fs-actions.test.js` for unconfirmed delete blocking (`task-cp3-3`) while retaining existing missing/success/failure delete-path tests.
    - Verification: `npm run verify` in `editor/le-vibe-native-extension/` (tests 337 passed, smoke passed).

## Epic CP4 — In-editor suggestions/completion (Copilot-like assist)

**Narrative:** optional but strategic parity: inline assistance, not only side-panel chat.

- [ ] `pending` **task-cp4-1**: Add inline suggestion provider (setting-gated beta) using local Ollama.
  - Acceptance:
    - suggestions can be accepted/dismissed with standard editor keys
    - no cloud fallback
- [ ] `pending` **task-cp4-2**: Add minimal suggestion ranking/debounce and cancellation to avoid noisy UX.
  - Acceptance:
    - measured latency budget documented
- [ ] `pending` **task-cp4-3**: Add fallback quick-fix actions when inline provider is disabled/unavailable.
  - Acceptance:
    - users still get selection-based assist from context menu/CodeLens

## Epic CP5 — Operator/orchestrator integration

**Narrative:** agent actions must cooperate with orchestrator flows and be observable.

- [ ] `pending` **task-cp5-1**: Standardize event contract between extension and operator/orchestrator (`chat_turn`, `edit_apply`, `plan_run`, `terminal_exec`).
  - Acceptance:
    - JSONL contracts documented + contract tests
- [ ] `pending` **task-cp5-2**: Add "runbook mode" command to package diagnostics for support (settings, logs, recent events).
  - Acceptance:
    - local-only bundle output path documented

## Epic CP6 — Release gate: done means shippable

**Narrative:** stop doc-only churn and enforce a product finish line.

- [ ] `pending` **task-cp6-1**: End-to-end acceptance script/checklist proving:
  - chat works with Ollama
  - agent creates/edits/deletes files in a sample project
  - apply/undo/conflict paths pass
  - optional inline suggestions work (or gracefully degrade)
  - Acceptance:
    - single operator command/checklist produces PASS/FAIL
- [ ] `pending` **task-cp6-2**: Make Lé Vibe Chat the default user path in installer and startup UX.
  - Acceptance:
    - no third-party chat path required for default happy path
- [ ] `pending` **task-cp6-3**: Product freeze marker (`track complete`) with explicit sign-off fields.
  - Acceptance:
    - workflow has final sign-off block (Product + Eng + QA)

---

## Execution policy

- Work top-down: always execute the first `pending` task.
- One task per pass, fully complete (code + tests + docs evidence).
- If blocked, record blocker + exact unblock command and continue with remaining in-scope work.
- Do not spend a pass on docs-only linking unless the active task explicitly requires it.
