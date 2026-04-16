# Lé Vibe Native Agent Extension (scaffold)

This package is the first-party extension scaffold for the Lé Vibe native extension track.

**Operators:** see **`OPERATOR.md`** for the canonical `npm run verify` command, smoke env vars, and persistence pointers.

**Issues / bugs (task-n25-1):** use the monorepo issue tracker — **`https://github.com/ryan-lgtm/le-vibe/issues`** (**`package.json`** **`bugs.url`**). Tag or title issues so maintainers can see they concern **`editor/le-vibe-native-extension`**.

**Changelog / release notes (task-n19-1):** see **`CHANGELOG.md`** — Keep a Changelog–style semver sections (**`[0.1.0]`** seeds the current shipped bar); update when bumping **`package.json`** **`version`**.

**Extension entry (packaging):** **`package.json`** **`main`** is **`./extension.js`** (VS Code activation entry; see **`OPERATOR.md`**).

**Prerequisites (developers):** **Node.js 18+** on your PATH to run **`npm run verify`** / **`npm test`** (see `package.json` **`engines.node`**). The installed VS Code extension host uses the editor’s runtime; the Node requirement applies to this package’s scripts and CI only. To install or run this extension in an editor, match **`engines.vscode`** in `package.json` — currently **VS Code 1.85+** or a compatible build (**VSCodium**, etc.) at the same API level.

**Local-first:** shipped defaults target **local Ollama** (`leVibeNative.ollamaEndpoint`); the extension does **not** silently fall back to a cloud LLM (same posture as **`OPERATOR.md`**).

**Default local Ollama URL:** **`http://127.0.0.1:11434`** — Settings **`leVibeNative.ollamaEndpoint`** (smoke defaults match unless **`LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT`** is set; see **`OPERATOR.md`**).

**Default Ollama probe timeout:** **`2500` ms** — Settings **`leVibeNative.ollamaTimeoutMs`** (smoke override **`LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS`**; see **`OPERATOR.md`**).

**Default local model tag:** **`mistral:latest`** — Settings **`leVibeNative.ollamaModel`** (streaming generate; see **`OPERATOR.md`**).

**Telemetry:** defaults to **local structured logs only**; no remote telemetry unless you **explicitly opt in** (same policy as **`OPERATOR.md`**).

**Canonical user-facing name (chat UX):** **Lé Vibe Chat** — palette titles and panel copy use this name for the agent surface (per product track; same line as **`OPERATOR.md`**).

## Command palette and keyboard shortcuts (task-n17-1)

Contributed commands use **`category`** **`Lé Vibe Chat`** and a short **`title`** in **`package.json`**. VS Code shows **`Lé Vibe Chat: <title>`** in the Command Palette (and Quick Access).

**Default keybindings:** none are shipped — built-in VS Code defaults vary by OS; contributing global shortcuts would risk clashes. Assign under **File → Preferences → Keyboard Shortcuts** (search **`leVibeNative`** or **Lé Vibe Chat**). If you add a user keybinding that overlaps a built-in command, the editor warns when saving.

| Command id | Shown in Command Palette | Default keybinding |
|------------|---------------------------|-------------------|
| `leVibeNative.openAgentSurface` | Lé Vibe Chat: Open Agent Surface | — |
| `leVibeNative.openOllamaSetupHelp` | Lé Vibe Chat: Open Ollama setup help | — |
| `leVibeNative.openModelPullHelp` | Lé Vibe Chat: Show local model install steps | — |
| `leVibeNative.openWorkspaceSetup` | Lé Vibe Chat: Open workspace setup workflow… | — |
| `leVibeNative.viewChatUsage` | Lé Vibe Chat: View transcript usage | — |
| `leVibeNative.exportChatTranscript` | Lé Vibe Chat: Export transcript | — |
| `leVibeNative.clearChatTranscript` | Lé Vibe Chat: Clear transcript | — |
| `leVibeNative.pickContextFile` | Lé Vibe Chat: Add workspace context file | — |
| `leVibeNative.clearContextFiles` | Lé Vibe Chat: Clear selected workspace context | — |
| `leVibeNative.emitOperatorHandoff` | Lé Vibe Chat: Emit operator handoff event | — |
| `leVibeNative.openThirdPartyMigrationGuide` | Lé Vibe Chat: Open third-party migration guide… | — |
| `leVibeNative.applySelectionDemoReplace` | Lé Vibe Chat: Apply demo replace to selection | — |
| `leVibeNative.createWorkspaceFile` | Lé Vibe Chat: Create workspace file… | — |
| `leVibeNative.createWorkspaceFolder` | Lé Vibe Chat: Create workspace folder… | — |
| `leVibeNative.moveWorkspacePath` | Lé Vibe Chat: Move or rename workspace path… | — |
| `leVibeNative.deleteWorkspacePath` | Lé Vibe Chat: Delete workspace file or folder… | — |
| `leVibeNative.askChatAboutSelection` | Lé Vibe Chat: Ask about selection… | — |
| `leVibeNative.runCommandInIntegratedTerminal` | Lé Vibe Chat: Run command in integrated terminal… | — |
| `leVibeNative.clearTerminalSessionAllow` | Lé Vibe Chat: Clear terminal session allow (re-enable confirmations) | — |
| `leVibeNative.addContextAtFile` | Lé Vibe Chat: @file — add workspace file to context… | — |
| `leVibeNative.addContextAtFolder` | Lé Vibe Chat: @folder — add folder listing to context… | — |
| `leVibeNative.addCurrentFileOutlineToContext` | Lé Vibe Chat: Add current file outline to context… | — |

## Accessibility (task-n17-2)

The readiness / chat **webview** (`extension.js` — `panelHtml`, `firstRunWizardHtml`) uses VS Code theme tokens (`var(--vscode-*)`) so colors follow the active theme, including **Dark Modern**, **Light Modern**, and **High Contrast** / **High Contrast Light** in VS Code **1.85+**. **Spot-check (Linux, Ubuntu):** panel text and controls remain readable when switching among those themes; buttons expose matching **`title`** and **`aria-label`** attributes; the prompt field has a visible **`<label>`** plus **`aria-label`**; status and chat log use **`aria-live`**; a **skip link** moves focus to the main panel region; **`prefers-reduced-motion`** is respected for scroll behavior.

**Known gaps (not automated in CI):** no substitute for full assistive-technology or screen reader QA on every control; the panel is long — **Tab** order follows DOM order (top to bottom), which is many stops; the edit-preview **`<pre>`** can be verbose when announced. File issues if you hit a blocking contrast or focus trap in a specific theme/OS combination.

## Scope for task-n1-1

- Extension host entrypoint exists (`extension.js`).
- Lé Vibe branded command is contributed:
  - `leVibeNative.openAgentSurface`
  - Command palette title: `Lé Vibe Chat: Open Agent Surface`
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

During `n1-2`, readiness state is driven by **`leVibeNative.devStartupState`** (default **`needs_auth_or_setup`**) so UX behavior is deterministic before live health wiring in `n2`.

## Prompt streaming (task-n2-2)

The panel includes a basic local prompt test surface:

- Send prompt to local Ollama streaming endpoint.
- Render streaming token output directly in the panel.
- Cancel in-flight request with a dedicated button.

## Bounded chat transcript (task-n3-1)

- Transcripts are stored as JSONL under `~/.config/le-vibe/levibe-native-chat/transcript-<workspaceKey>.jsonl` (workspace key is a short hash of the workspace folder URI).
- Settings **`leVibeNative.chatTranscriptMaxBytes`** (default **524288** bytes) and **`leVibeNative.chatTranscriptMaxMessages`** (default **200** JSONL rows) cap storage.
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

- **`leVibeNative.contextMaxFiles`** (default **`4`**)
- **`leVibeNative.contextMaxCharsPerFile`** (default **`1200`**)
- **`leVibeNative.contextMaxLinesPerFile`** (default **`80`**)
- **`leVibeNative.contextMaxTotalChars`** (default **`3200`**)

### Context read guards (task-n11-4)

- Before a file is added as prompt context, Lé Vibe Chat applies **`.gitignore`** (workspace root `.gitignore` via [`ignore`](https://www.npmjs.com/package/ignore)), a **per-file size** check against **`leVibeNative.contextMaxCharsPerFile`** (disk bytes must not exceed that budget), and a **binary / non-text** probe (null-byte scan on an initial chunk). Skips use deterministic **`Lé Vibe Chat: skipped "path" — …`** strings (toast + no silent omission). Implementation: [`context-file-guards.js`](context-file-guards.js).

### @file / @folder picker (Epic N14, task-n14-1)

- **Palette:** **Lé Vibe Chat: @file — add workspace file to context…** (`leVibeNative.addContextAtFile`) and **Lé Vibe Chat: @folder — add folder listing to context…** (`leVibeNative.addContextAtFolder`); panel **@file…** / **@folder…** next to **Add context file**.
- **Discovery:** both use **`vscode.workspace.findFiles`** with the same exclude glob as the legacy picker and a **strict scan cap** (`FILE_PICKER_MAX_SCAN_URIS` in [`at-mention-context.js`](at-mention-context.js)). **@folder** builds folder candidates from parent paths of scanned files, capped at **`FOLDER_QUICKPICK_MAX_CANDIDATES`**, with **`.gitignore`** applied.
- **Budgets:** file excerpts and one-level folder listings respect **`leVibeNative.contextMaxCharsPerFile`** and **`leVibeNative.contextMaxLinesPerFile`**; the number of context slots still respects **`leVibeNative.contextMaxFiles`** and total injected size **`leVibeNative.contextMaxTotalChars`** via [`workspace-context.js`](workspace-context.js) (`### FOLDER:` blocks for directories).

### Current-file outline only (task-n14-2)

- **Palette:** **Lé Vibe Chat: Add current file outline to context…** (`leVibeNative.addCurrentFileOutlineToContext`); panel **Outline (file)…**.
- **Mechanism:** **`vscode.executeDocumentSymbolProvider`** on the **active editor** document (language / outline providers — same family as the **Outline** view). Text is **clipped** with **`contextMaxCharsPerFile`** / **`contextMaxLinesPerFile`**; symbol expansion is capped (**`OUTLINE_MAX_SYMBOL_NODES`** / depth in [`outline-context.js`](outline-context.js)).
- **Limitations vs Cursor-style cloud index:** Lé Vibe Chat does **not** build a **cross-repo embedding index**, **remote** symbol graph, or **semantic** search over the whole workspace. It only pulls **structured outline symbols for one open file** from the local editor APIs — **bounded**, **local-first**, **no default full-repo indexing**. Cursor-class products may combine **cloud-scale** retrieval and **multi-file** intelligence; this extension stays within explicit **storage and context budgets** (see *Bounded persistence inventory*).

## Inline assistant — selection → chat (Epic N12, task-n12-1)

- **Command Palette / editor context menu:** **Lé Vibe Chat: Ask about selection…** (`leVibeNative.askChatAboutSelection`) — requires a **non-empty** selection in a **workspace file** (`file` scheme). Opens the Lé Vibe Chat panel (same as **Lé Vibe Chat: Open Agent Surface**) if it was closed, then injects **workspace-relative path**, **0-based selection bounds** (surfaced in the context excerpt header), and a **clipped text excerpt** into prompt context, and **prefills** the prompt box with a short template line.
- **CodeLens:** when text is selected, a lens **Ask Lé Vibe Chat about this selection** appears on the selection range and runs the same command.
- Helpers: [`selection-chat-context.js`](selection-chat-context.js) (`buildSelectionContextEntry`, `prefillPromptForSelection`).

### Quick actions — templated prompts (task-n12-2)

- **Panel strip** under *Local prompt test*: **Explain…**, **Refactor selection…**, **Generate tests…** — each inserts a **fixed template** into the prompt box. **No HTTP** runs until you click **Send Prompt** (then only the configured **local Ollama** endpoint, same as any other chat message).
- Templates (see [`chat-quick-actions.js`](chat-quick-actions.js) `QUICK_ACTION_TEMPLATES`):
  - **`explain`** — *Explain the following code or notes in plain language. Call out assumptions and edge cases.*
  - **`refactor_selection`** — *Refactor the code below for clarity…* (behavior-preserving; preserve public APIs unless noted.)
  - **`generate_tests`** — *Generate focused unit tests…* (minimal mocks; note gaps.)

## Terminal execution policy (Epic N13, task-n13-1)

Agent-driven shell commands are **high risk**; see [`TERMINAL_EXECUTION_POLICY.md`](TERMINAL_EXECUTION_POLICY.md), [`terminal-execution-policy.js`](terminal-execution-policy.js).

- **`leVibeNative.terminalExecutionEnabled`** — default **`false`** (off until you opt in; use **Workspace** settings for per-repo opt-in).
- **`leVibeNative.terminalCommandAllowPatterns`** — default **empty**; when execution is enabled, you must add at least one allow pattern or **no** commands pass (allow-list mode).
- **`leVibeNative.terminalCommandDenyPatterns`** — shipped **deny** defaults block common destructive / pipe-to-shell patterns; **deny** is evaluated before **allow**.

### Visible integrated terminal (task-n13-2)

Approved commands run only via the **integrated terminal** (named **`Lé Vibe Chat`**) using `Terminal.sendText` — **no hidden PTY**. Palette **Lé Vibe Chat: Run command in integrated terminal…** and the panel **Run command in terminal…** prompt for a one-line command. You **confirm each batch** in a modal unless you choose **Run and skip further prompts (this session)**, or set the advanced **`leVibeNative.terminalSkipBatchConfirmation`** to **`true`**. Session skip clears when workspace folders change or via **Lé Vibe Chat: Clear terminal session allow (re-enable confirmations)**. Implementation: [`terminal-exec.js`](terminal-exec.js).

### Terminal command audit (task-n13-3)

Each successful send appends a structured JSONL record under **`~/.config/le-vibe/levibe-native-chat/terminal-command-audit.jsonl`** (`lvibe.terminal_command_audit.v1`): **timestamp**, **cwd**, **command_line**, **`exit_code: null`** on dispatch. When the editor exposes **`window.onDidEndTerminalShellExecution`** and the event matches the same command line, a second line records **`exit_code`** (may be `null` if the shell did not report a code). See [`terminal-command-audit.js`](terminal-command-audit.js).

## Edit preview before apply (Epic N9)

- **`leVibeNative.requireEditPreviewBeforeApply`** (default **`true`**) — for the panel **Preview sample workspace edit** flow, a unified diff is shown first; when **`true`**, you must click **Accept preview** before **Apply to file** (no silent whole-file overwrite from preview alone). Set to **`false`** only if you accept **Apply to file** immediately after the diff is shown (the preview is still displayed for that demo path).
- Proposal shape: [`EDIT_PROPOSAL.v1.md`](EDIT_PROPOSAL.v1.md) · [`edit-proposal.js`](edit-proposal.js) · diff/gate helpers [`edit-preview.js`](edit-preview.js).
- Apply path: [`workspace-edit-apply.js`](workspace-edit-apply.js) — one **`WorkspaceEdit`** per **Apply** (VS Code undo stacks coalesce that transaction per buffer).

### Partial selection apply (Epic N9)

- Command Palette: **Lé Vibe Chat: Apply demo replace to selection** (`leVibeNative.applySelectionDemoReplace`) — replaces the **single** non-empty editor selection with a short demo line via **`WorkspaceEdit.replace`** (Undo reverts). Use this to validate partial-apply wiring before model-driven `range_replace` proposals.
- **When selection is missing or ambiguous:** no active editor, **empty** selection (caret only), or **more than one** selection (multi-cursor) → a **warning** only; **no** workspace edit. Multiple regions are **not** merged — use one range or whole-file preview in the panel.
- Helper: [`selection-apply.js`](selection-apply.js) (`resolveSingleSelectionForPartialApply`).
- **Stale file conflict:** [`edit-conflict.js`](edit-conflict.js) stores a **SHA-256** of the file’s UTF-8 bytes at **Preview sample workspace edit** time. If the file changes or disappears before **Apply to file**, apply is **blocked** and the panel shows a fixed **Lé Vibe Chat:** remediation string (re-run preview).

## Workspace plan (Epic N10)

- Multi-step orchestration uses **`levibe.workspace_plan.v1`** — ordered **`steps`** with **`op`**: `create_file`, `apply_edit` (same `edit` shapes as [`EDIT_PROPOSAL.v1.md`](EDIT_PROPOSAL.v1.md)), `delete_file`, `move_file`. Validate with [`workspace-plan.js`](workspace-plan.js) (`validateWorkspacePlan`) **before** execution so invalid plans surface a single **`Lé Vibe Chat: workspace plan invalid — …`** string (no partial writes). Human summary: [`WORKSPACE_PLAN.v1.md`](WORKSPACE_PLAN.v1.md).
- **Execution (task-n10-2):** the panel **Run sample workspace plan** demo streams **`Lé Vibe Chat: plan step N/M — …`** lines into the chat log; each phase also appends structured JSONL under **`workspace-plan-audit.jsonl`** (see *Bounded persistence inventory*). **Cancel plan run** stops before the next step (the in-flight step completes first). Implementation: [`workspace-plan-exec.js`](workspace-plan-exec.js).
- **Rollback (task-n10-3):** if a step **fails** after earlier steps succeeded, the chat log explains the **partial state** and enables **Undo completed steps** (same VS Code session). Rollback applies inverse **`WorkspaceEdit`** operations in reverse order (best-effort: restore prior bytes, delete newly created files, reverse renames). A `workspace_plan_rollback` line is appended to **`workspace-plan-audit.jsonl`**. Cancel mid-run does not auto-rollback; semantics are documented in [`WORKSPACE_PLAN.v1.md`](WORKSPACE_PLAN.v1.md).
- **Dry-run (task-n10-4):** **Dry-run sample plan** prints per-step rough **byte** and **token (÷4) estimates** into the chat log with **no disk writes** (read-only sizing where needed). Output is **line-capped** for bounded UX; see [`workspace-plan-dry-run.js`](workspace-plan-dry-run.js).

## Workspace scaffold — create file / folder (Epic N11, task-n11-1)

- **Panel:** **Create file…** / **Create folder…** · **Command Palette:** **Lé Vibe Chat: Create workspace file…** (`leVibeNative.createWorkspaceFile`), **Lé Vibe Chat: Create workspace folder…** (`leVibeNative.createWorkspaceFolder`).
- Paths must be **workspace-relative** (no `..` segments, no absolute paths). **Blocked path segments:** `.git`, `.ssh`, `.gnupg`, `node_modules`, `.env` (see [`workspace-fs-actions.js`](workspace-fs-actions.js)).
- **`leVibeNative.openDocumentAfterWorkspaceCreate`** (default **`true`**) — open the new file in the editor after a successful **create file** (set **`false`** to create without focusing an editor tab).

### Move / rename (task-n11-2)

- **Panel:** **Move / rename…** · **Command Palette:** **Lé Vibe Chat: Move or rename workspace path…** (`leVibeNative.moveWorkspacePath`). Two workspace-relative paths (source, then destination); same validation and blocked segments as create.
- **Git-friendly behavior:** moves use **`WorkspaceEdit.renameFile`** when the API is available so the workbench (and source-control providers) can treat the operation as a **rename** rather than delete+add when possible.
- **Conflict handling (no silent overwrite):** if the **source is missing**, or the **destination already exists**, or **`applyEdit` is rejected**, the user gets an explicit **`Lé Vibe Chat:`** message and nothing is overwritten. Implementation: [`moveWorkspaceEntry`](workspace-fs-actions.js) (`overwrite: false`).

### Delete file or folder (task-n11-3)

- **Panel:** **Delete file or folder…** · **Command Palette:** **Lé Vibe Chat: Delete workspace file or folder…** (`leVibeNative.deleteWorkspacePath`). **Two-step UX:** workspace-relative path (`showInputBox`), then a **modal** confirmation — nothing is deleted until **Delete** is chosen (never silent).
- **Audit:** each confirmed attempt (success or failure after confirm) appends one JSONL line to **`workspace-fs-ops-audit.jsonl`** under `~/.config/le-vibe/levibe-native-chat/` (`lvibe.workspace_fs_ops_audit.v1`). Implementation: [`deleteWorkspaceEntry`](workspace-fs-actions.js), [`workspace-fs-ops-audit.js`](workspace-fs-ops-audit.js).

## Operator handoff contract (task-n4-2)

- Command: `Lé Vibe Chat: Emit operator handoff event` (`leVibeNative.emitOperatorHandoff`), also available as a panel action.
- Contract version: `lvibe.operator_handoff.v1`.
- Event includes reproducible fields: `workspace_uri`, `startup_state`, `diagnostics`, Ollama endpoint/model, selected context paths, context budget, and transcript path/caps.
- Local audit log evidence is appended as JSONL at:
  - `~/.config/le-vibe/levibe-native-chat/operator-handoff-audit.jsonl`

## Reliability: retries and timeouts (task-n5-1)

- **Automatic retries** for transient local Ollama failures — **`leVibeNative.ollamaMaxRetries`** (default **`2`**), exponential backoff from **`leVibeNative.ollamaRetryBackoffMs`** (default **`400` ms**) — apply to readiness `GET /api/tags` and to streaming `POST /api/generate`.
- **Stream guards:** **`leVibeNative.ollamaStreamStallMs`** (default **`60000` ms**) aborts if no tokens/activity for too long; **`leVibeNative.ollamaStreamMaxMs`** (default **`120000` ms**) caps total stream wall time (prevents hard hangs).
- **Readiness source:** **`leVibeNative.useLiveOllamaReadiness`** (default **`true`**) — use live local Ollama probes for startup snapshot; set **`false`** and choose a **`leVibeNative.devStartupState`** string (default **`needs_auth_or_setup`**) for development overrides (see **`test/readiness-state-machine.test.js`**).
- **UX**: panel shows structured diagnostics on failure (`[error code] message (endpoint: …)`), retry progress during auto-retry, and a **Retry last prompt** button (manual resend without duplicating the user line in the transcript).

## First-run onboarding (task-n5-2)

- On first open, a **checkpointed wizard** runs before the full readiness + chat surface so the panel is never an empty gray view.
- State is stored at `~/.config/le-vibe/levibe-native-chat/first-run-wizard.json` (schema `first_run_wizard.v1`).
- **Next checkpoint** advances; **Finish and open agent surface** completes the wizard and runs the normal readiness flow; **Skip onboarding** marks completion and opens the same surface.
- Setting: **`leVibeNative.showFirstRunWizard`** (default **`true`**). Set to **`false`** to go straight to the readiness panel.

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

- **Feature flag:** **`leVibeNative.enableFirstPartyAgentSurface`** (default **`true`**). This is the supported switch for first-party Lé Vibe Chat rollout; toggling it does not delete data under `~/.config/le-vibe/`.
- **Startup panel:** **`leVibeNative.openPanelOnStartup`** (default **`true`**) — when the first-party surface is enabled, open the readiness panel at editor startup (wizard may run first per **`leVibeNative.showFirstRunWizard`**).
- **Status bar (optional, task-n17-3):** **`leVibeNative.showStatusBarEntry`** (default **`false`**) — when **`true`**, registers a **subtle** status bar entry (right-aligned, low priority) for **Lé Vibe Chat** with periodic local **Ollama** reachability text; **click** runs **Lé Vibe Chat: Open Agent Surface**. Off by default to avoid clutter.
- **Rollback:** set **`leVibeNative.enableFirstPartyAgentSurface`** to **false** in Settings (JSON: `"leVibeNative.enableFirstPartyAgentSurface": false`). Effects:
  - Startup no longer auto-opens the readiness panel (even if **`leVibeNative.openPanelOnStartup`** is **`true`**).
  - Command **Lé Vibe Chat: Open Agent Surface** shows a message with **Open Settings** to flip the flag back; the webview panel is not created while disabled.
- **Restore:** set the same key back to **true** (or remove the override). Palette commands for transcript export/clear and operator handoff remain available for recovery workflows while the panel is disabled.

## Third-party agent migration (task-n7-2)

- **Goal:** Move from common third-party chat/agent extensions (e.g. Continue, Cline) to **Lé Vibe Chat** without silent cross-extension writes.
- **Command:** **Lé Vibe Chat: Open third-party migration guide…** — opens a Markdown checklist in the editor and optional follow-up actions.
- **Guardrails:** The extension does **not** uninstall other extensions or delete their data. It only writes migration state and JSONL audit lines under `~/.config/le-vibe/levibe-native-chat/` (`third-party-migration-state.json`, `third-party-migration-audit.jsonl`).
- **Detection:** A small watchlist of marketplace extension IDs (see `third-party-migration.js`) is used to suggest the guide. If **`leVibeNative.showThirdPartyMigrationNudge`** (default **`true`**) is on and a watchlist extension is present while migration status is still **pending**, a one-time notification offers the guide; **Not now** records status **skipped** (no further auto nudges).
- **Remediation:** Disable or uninstall conflicting extensions manually from the Extensions view, keep `leVibeNative.enableFirstPartyAgentSurface` **true**, then verify **Lé Vibe Chat: Open Agent Surface**.

## Operator verification / ship checklist (task-n8-1)

- **E2E agentic editor (Epic N15, task-n15-1):** before tagging or publishing, run the manual **E2E agentic editor release checklist** in **`OPERATOR.md`** — **Preview sample workspace edit** → **Accept preview** → **Apply to file** → editor **Undo**; then **Run sample workspace plan** and **Cancel plan run** mid-flight — and record a row in the **Sign-off (per release)** table there.
- **Workflow board:** **`.lvibe/workflows/native-extension-product-track.md`** (Epic N8 — task order for this extension; operator runbook references the same path under **`OPERATOR.md`** *Product track*).
- **Canonical command:** from `editor/le-vibe-native-extension/`, run **`npm run verify`** (runs **`npm test`** then **`npm run smoke`**; **`package.json`** **`scripts.verify`** = **`npm test && npm run smoke`**).
- **Underlying scripts:** **`package.json`** **`scripts.test`** = **`node --test ./test/*.test.js`**; **`scripts.smoke`** = **`node ./scripts/smoke-integration.js`**; **`scripts.package`** = **`vsce package`** (see **`OPERATOR.md`** *Packaged VSIX* for **`npm run package`** output path and **`code --install-extension`**).
- **Green means:** all unit tests pass; smoke confirms non-blank panel/wizard HTML, `lvibe` launcher string contract when the monorepo layout is present, and a best-effort local Ollama probe (non-fatal if the daemon is absent unless `LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=1`).
- **Settings disclosure guardrail:** **`npm test`** runs **`test/package-leVibeNative-keys-doc-inventory.test.js`**, which fails if any **`leVibeNative.*`** key in **`package.json`** contributes is missing from **`OPERATOR.md`** and/or this README (document new settings before shipping; see **`OPERATOR.md`** *Product track*).
- **Scripts literal umbrella:** **`npm test`** runs **`test/package-json-all-scripts-doc-literal-sync.test.js`**, which fails if any **`package.json` `scripts`** value is missing from **`OPERATOR.md`** and/or this README (see **`OPERATOR.md`** *Product track*).
- Use this before tagging or packaging the extension; CI can mirror the same script.

## Bounded persistence inventory (task-n8-2)

All first-party on-disk state for this extension lives under **`~/.config/le-vibe/levibe-native-chat/`** (see `storage-inventory.js` for the canonical helper). Retention caps apply to chat JSONL via Settings (**`leVibeNative.chatTranscriptMaxBytes`**, **`leVibeNative.chatTranscriptMaxMessages`**).

| Artifact | Role |
|----------|------|
| `first-run-wizard.json` | First-run wizard checkpoints (`first_run_wizard.v1`). |
| `transcript-<hash>.jsonl` | Per-workspace bounded chat transcript (one file per workspace key). |
| `operator-handoff-audit.jsonl` | Append-only operator handoff records (`lvibe.operator_handoff.v1`). |
| `third-party-migration-state.json` | Third-party migration status (`third_party_migration.v1`). |
| `third-party-migration-audit.jsonl` | Append-only migration actions (`lvibe.third_party_migration.v1`). |
| `workspace-plan-audit.jsonl` | Append-only workspace plan step records (`lvibe.workspace_plan_audit.v1`). |
| `workspace-fs-ops-audit.jsonl` | Append-only destructive workspace FS operations (`lvibe.workspace_fs_ops_audit.v1`). |
| `terminal-command-audit.jsonl` | Append-only integrated terminal command audit (`lvibe.terminal_command_audit.v1` — timestamp, cwd, command; exit code when shell integration reports `onDidEndTerminalShellExecution`). |

No embeddings or unbounded cloud sync are written by this extension; export/clear remain user-driven.
