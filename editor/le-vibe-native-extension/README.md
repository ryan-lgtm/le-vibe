# Lé Vibe Native Agent Extension (scaffold)

This package is the first-party extension scaffold for the Lé Vibe native extension track.

## Scope for task-n1-1

- Extension host entrypoint exists (`extension.js`).
- Lé Vibe branded command is contributed:
  - `leVibeNative.openAgentSurface`
  - Command palette title: `Lé Vibe: Open Agent Surface`
- Activation events include startup and command-triggered activation.

## Startup readiness panel (task-n1-2)

The extension now renders a deterministic readiness panel with explicit states:

- `checking`
- `ready`
- `needs_ollama`
- `needs_model`
- `needs_auth_or_setup`

Every non-ready state includes at least one remediation action button:

- Ollama setup help
- local model install steps
- workspace setup workflow opener

During `n1-2`, readiness state is driven by `leVibeNative.devStartupState` so UX behavior is deterministic before live health wiring in `n2`.

## Prompt streaming (task-n2-2)

The panel includes a basic local prompt test surface:

- Send prompt to local Ollama streaming endpoint.
- Render streaming token output directly in the panel.
- Cancel in-flight request with a dedicated button.

## Bounded chat transcript (task-n3-1)

- Transcripts are stored as JSONL under `~/.config/le-vibe/levibe-native-chat/transcript-<workspaceKey>.jsonl` (workspace key is a short hash of the workspace folder URI).
- Settings `leVibeNative.chatTranscriptMaxBytes` and `leVibeNative.chatTranscriptMaxMessages` cap storage.
- When over budget, oldest messages are removed first and a **system** line records how many were compacted (explicit, not silent loss).

## Storage controls (task-n3-2)

**Lé Vibe Chat** exposes:

| Control | Where | Behavior |
|--------|--------|----------|
| **View usage** | Agent surface panel + Command Palette (`Lé Vibe Chat: View transcript usage`) | Shows line count, on-disk bytes, and absolute JSONL path. |
| **Export transcript** | Panel + Palette (`Lé Vibe Chat: Export transcript`) | Save dialog writes a copy of the current workspace JSONL (local-only). |
| **Clear transcript** | Panel + Palette (`Lé Vibe Chat: Clear transcript`) | Modal confirmation, then deletes that workspace’s JSONL file. |

All paths stay under `~/.config/le-vibe/levibe-native-chat/` unless the user chooses another location during export.

## Workspace context picker (task-n4-1)

- Add context files from panel (`Add context file`) or Command Palette (`Lé Vibe Chat: Add workspace context file`).
- Selected files are read from the current workspace only, path-checked to block traversal/absolute references, and clipped before prompt injection.
- Context is injected into prompt payload before the user prompt section, so Ollama receives local file excerpts plus the user message.

Token-budget rules (configurable in Settings):

- `leVibeNative.contextMaxFiles` (default `4`)
- `leVibeNative.contextMaxCharsPerFile` (default `1200`)
- `leVibeNative.contextMaxLinesPerFile` (default `80`)
- `leVibeNative.contextMaxTotalChars` (default `3200`)

## Operator handoff contract (task-n4-2)

- Command: `Lé Vibe Chat: Emit operator handoff event` (`leVibeNative.emitOperatorHandoff`), also available as a panel action.
- Contract version: `lvibe.operator_handoff.v1`.
- Event includes reproducible fields: `workspace_uri`, `startup_state`, `diagnostics`, Ollama endpoint/model, selected context paths, context budget, and transcript path/caps.
- Local audit log evidence is appended as JSONL at:
  - `~/.config/le-vibe/levibe-native-chat/operator-handoff-audit.jsonl`

## Reliability: retries and timeouts (task-n5-1)

- **Automatic retries** for transient local Ollama failures (`ollamaMaxRetries`, exponential backoff from `ollamaRetryBackoffMs`) apply to readiness `GET /api/tags` and to streaming `POST /api/generate`.
- **Stream guards**: `ollamaStreamStallMs` aborts if no tokens/activity for too long; `ollamaStreamMaxMs` caps total stream wall time (prevents hard hangs).
- **UX**: panel shows structured diagnostics on failure (`[error code] message (endpoint: …)`), retry progress during auto-retry, and a **Retry last prompt** button (manual resend without duplicating the user line in the transcript).

## First-run onboarding (task-n5-2)

- On first open, a **checkpointed wizard** runs before the full readiness + chat surface so the panel is never an empty gray view.
- State is stored at `~/.config/le-vibe/levibe-native-chat/first-run-wizard.json` (schema `first_run_wizard.v1`).
- **Next checkpoint** advances; **Finish and open agent surface** completes the wizard and runs the normal readiness flow; **Skip onboarding** marks completion and opens the same surface.
- Setting: `leVibeNative.showFirstRunWizard` (default `true`). Set to `false` to go straight to the readiness panel.

## Unit tests: readiness state machine + storage bounds (task-n6-1)

- **Readiness:** `test/readiness-state-machine.test.js` asserts deterministic `getStateContent` for every startup state, stable remediation action ids for `needs_*` states, invalid `devStartupState` fallback, and `resolveStartupSnapshot` dev overrides for each state (no network).
- **Transcript persistence:** `test/transcript-persistence-bounds.test.js` exercises `appendEntry` under sustained load so on-disk messages never exceed configured `maxMessages` / `maxBytes`, and verifies compaction emits an explicit system stub (no silent truncation).
- Run: `npm test` in this folder.

## Integration smoke (`lvibe .` contract + Ollama wiring) (task-n6-2)

- Command: `npm run smoke` (also exercised by `test/integration-smoke.test.js`).
- **Panel / wizard:** Asserts every readiness `panelHtml` state and each first-run wizard step produce substantial HTML with Lé Vibe markers and chat controls (no blank webview).
- **Ollama:** Uses `createOllamaClient` from `ollama.js` with the same endpoint defaults as the extension; if the daemon is down, the smoke **passes** unless `LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=1` (use on a machine with Ollama to fail closed). Override endpoint with `LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT` if needed.
- **`lvibe .`:** When this package lives under the r-vibe repo, verifies `packaging/bin/lvibe` execs `python3 -m le_vibe.launcher` (the `lvibe .` entry). Set `LEVIBE_SMOKE_SKIP_LVIBE_LAUNCHER=1` if you only have the extension subtree.

## Rollout and rollback (task-n7-1)

- **Feature flag:** `leVibeNative.enableFirstPartyAgentSurface` (default **true**). This is the supported switch for first-party Lé Vibe Chat rollout; toggling it does not delete data under `~/.config/le-vibe/`.
- **Rollback:** set `enableFirstPartyAgentSurface` to **false** in Settings (JSON: `"leVibeNative.enableFirstPartyAgentSurface": false`). Effects:
  - Startup no longer auto-opens the readiness panel (even if `openPanelOnStartup` is true).
  - Command **Lé Vibe: Open Agent Surface** shows a message with **Open Settings** to flip the flag back; the webview panel is not created while disabled.
- **Restore:** set the same key back to **true** (or remove the override). Palette commands for transcript export/clear and operator handoff remain available for recovery workflows while the panel is disabled.
