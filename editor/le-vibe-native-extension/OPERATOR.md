# Lé Vibe Native Extension — operator quick reference

Use this sheet when validating or shipping the first-party extension (`editor/le-vibe-native-extension/`).

**Prerequisites:** **Node.js 18+** on your PATH to run **`npm run verify`** / **`npm test`** (uses `node:test`). The VS Code extension host ships its own runtime; the Node engine is for this package’s scripts and CI only. For installing or running the extension in an editor, match **`engines.vscode`** in `package.json` — currently **VS Code 1.85+** (or a compatible build such as **VSCodium** meeting the same API level). Contributor-oriented wording for the same Node and editor requirements is in **`README.md`** (*Prerequisites (developers)*).

`package.json` includes **`repository.directory`**, **`homepage`**, **`bugs`**, and **`keywords`** so tooling and registries can link to the monorepo path and issue tracker. It also declares **`publisher`** and **`license`** (SPDX string) for marketplace and CI identity.

**Extension host entry:** **`package.json`** **`main`** must be **`./extension.js`** (VS Code activation entry; required for packaging).

**Local-first:** the shipped defaults target **local Ollama** (see `leVibeNative.ollamaEndpoint`); the extension does **not** silently fall back to a cloud LLM.

**Default local Ollama URL:** **`http://127.0.0.1:11434`** — configure via **`leVibeNative.ollamaEndpoint`** (smoke’s default probe matches unless `LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT` is set).

**Default Ollama probe timeout:** **`2500` ms** — configure via **`leVibeNative.ollamaTimeoutMs`** (smoke override **`LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS`**; same default as the smoke table below).

**Default local model tag:** **`mistral:latest`** — **`leVibeNative.ollamaModel`** (used for streaming generate requests).

**Ollama retries:** **`leVibeNative.ollamaMaxRetries`** default **`2`**, base backoff **`leVibeNative.ollamaRetryBackoffMs`** default **`400` ms** (transient `GET /api/tags` and streaming `POST /api/generate`).

**Ollama stream guards:** **`leVibeNative.ollamaStreamStallMs`** default **`60000` ms** (abort if no tokens/activity), **`leVibeNative.ollamaStreamMaxMs`** default **`120000` ms** (hard cap on wall time per `POST /api/generate`).

**Workspace context caps:** **`leVibeNative.contextMaxFiles`** default **`4`**, **`leVibeNative.contextMaxCharsPerFile`** default **`1200`**, **`leVibeNative.contextMaxLinesPerFile`** default **`80`**, **`leVibeNative.contextMaxTotalChars`** default **`3200`** (per-file and total character budget for prompt context; details in **`README.md`** *Workspace context picker*).

**Edit preview gate:** **`leVibeNative.requireEditPreviewBeforeApply`** default **`true`** — panel shows a unified diff before writing; when **`true`**, **Accept preview** is required before **Apply to file** (see **`README.md`** *Edit preview before apply*).

**Apply / undo (WorkspaceEdit):** Panel **Apply to file** uses **`vscode.workspace.applyEdit`** with **one** **`WorkspaceEdit` per Apply click** (`workspace-edit-apply.js`) — not raw `fs.writeFile` — so the active editor records a normal text undo. **Manual check (task-n9-3):** after Apply, focus the modified document and **Undo** once; the file should revert to its pre-apply contents for that operation.

**Partial selection apply (task-n9-4):** Palette **Lé Vibe Chat: Apply demo replace to selection** (`leVibeNative.applySelectionDemoReplace`) — **one** non-empty selection only; **multi-cursor / multiple selections** or **empty** selection → warning, no edit (`selection-apply.js`).

**Edit preview stale conflict (task-n9-5):** Panel **Apply to file** is blocked if workspace file bytes changed (or file vanished) since **Preview sample workspace edit** — content hash snapshot in **`edit-conflict.js`**; deterministic panel/toast copy, re-run preview.

**Workspace plan (task-n10-1):** **`levibe.workspace_plan.v1`** — ordered steps (`create_file` / `apply_edit` / `delete_file` / `move_file`); validate via **`workspace-plan.js`** before execution — invalid plans return user-visible errors only (**`README.md`** *Workspace plan*).

**Workspace plan execution (task-n10-2):** panel **Run sample workspace plan** shows per-step **`Lé Vibe Chat: plan step N/M — …`** progress in the chat log; append-only audit JSONL **`workspace-plan-audit.jsonl`** under `levibe-native-chat/` (**`workspace-plan-exec.js`**). **Cancel plan run** skips remaining steps after the current step completes.

**Workspace plan rollback (task-n10-3):** if a step **fails** after prior steps succeeded, **Undo completed steps** runs best-effort inverse **`WorkspaceEdit`**s (same session); **`workspace_plan_rollback`** lines in **`workspace-plan-audit.jsonl`**. Cancel does not auto-rollback — see **`README.md`** / **`WORKSPACE_PLAN.v1.md`**.

**Workspace plan dry-run (task-n10-4):** panel **Dry-run sample plan** shows bounded per-step byte/token (÷4) estimates with **no writes**; implementation **`workspace-plan-dry-run.js`**.

**Workspace scaffold (task-n11-1):** Palette **Lé Vibe Chat: Create workspace file…** / **Create workspace folder…** and panel **Create file…** / **Create folder…** — workspace-relative paths only; blocked segments per **`workspace-fs-actions.js`**. **`leVibeNative.openDocumentAfterWorkspaceCreate`** default **`true`** (open new file after create).

**Workspace move/rename (task-n11-2):** Palette **Lé Vibe Chat: Move or rename workspace path…** + panel **Move / rename…** — **`WorkspaceEdit.renameFile`** when available (git-friendly rename); **no overwrite** if destination exists — explicit **`Lé Vibe Chat:`** errors; **`moveWorkspaceEntry`** in **`workspace-fs-actions.js`**.

**Workspace delete (task-n11-3):** Palette **Lé Vibe Chat: Delete workspace file or folder…** + panel **Delete file or folder…** — path prompt **then** modal confirm (never silent); **`deleteWorkspaceEntry`** + JSONL **`workspace-fs-ops-audit.jsonl`** (`lvibe.workspace_fs_ops_audit.v1`) via **`workspace-fs-ops-audit.js`**.

**Workspace context guards (task-n11-4):** **Add workspace context file** applies root **`.gitignore`**, per-file size cap vs **`leVibeNative.contextMaxCharsPerFile`**, and binary detection — deterministic **`Lé Vibe Chat: skipped …`** messages; **`context-file-guards.js`**.

**Selection → chat (task-n12-1):** Palette / context menu **`leVibeNative.askChatAboutSelection`** + CodeLens on selection — opens agent surface if needed; pushes path + clipped selection into context; **`selection-chat-context.js`**.

**Quick action templates (task-n12-2):** Panel **Explain / Refactor selection / Generate tests** — inserts `QUICK_ACTION_TEMPLATES` from **`chat-quick-actions.js`**; Ollama only on **Send Prompt** (local endpoint).

**Terminal execution policy (task-n13-1):** **`leVibeNative.terminalExecutionEnabled`** default **`false`** (agent shell commands off until explicitly enabled). **`leVibeNative.terminalCommandAllowPatterns`** (default empty) and **`leVibeNative.terminalCommandDenyPatterns`** (shipped defaults include `rm -rf`, `sudo `, fork-bomb pattern, `| sh`, `curl | sh`) — deny wins; when enabled, an empty allow list blocks every command until you add patterns. Prefer **Workspace** scope for the master switch. Policy evaluation: **`terminal-execution-policy.js`**; full write-up **`TERMINAL_EXECUTION_POLICY.md`**. Integrated-terminal execution wiring is **n13-2+**.

**Startup / rollout (defaults):** **`leVibeNative.enableFirstPartyAgentSurface`** default **`true`** (first-party Lé Vibe Chat surface); **`leVibeNative.showFirstRunWizard`** default **`true`** (checkpointed wizard); **`leVibeNative.openPanelOnStartup`** default **`true`** (auto-open panel when the first-party surface is enabled). Rollback semantics in **`README.md`** *Rollout and rollback*.

**Third-party migration nudge:** **`leVibeNative.showThirdPartyMigrationNudge`** default **`true`**. **Ollama readiness source:** **`leVibeNative.useLiveOllamaReadiness`** default **`true`** (live local probes; for development overrides, set **`leVibeNative.useLiveOllamaReadiness`** to **`false`** and use **`leVibeNative.devStartupState`**). Migration flow in **`README.md`** *Third-party agent migration*.

**Development readiness override:** **`leVibeNative.devStartupState`** default **`needs_auth_or_setup`** (string enum: `checking`, `ready`, `needs_ollama`, `needs_model`, `needs_auth_or_setup`; used when **`leVibeNative.useLiveOllamaReadiness`** is **`false`**).

**Telemetry:** defaults to **local structured logs only**; there is **no** remote telemetry unless the user **explicitly opts in**.

**Canonical user-facing name (chat UX):** **Lé Vibe Chat** — palette titles and panel copy use this name for the agent surface (per product track).

## Verify (canonical)

From this directory:

```bash
npm run verify
```

Runs **`npm test`** then **`npm run smoke`**. The **`package.json`** **`scripts.verify`** string is exactly **`npm test && npm run smoke`**. Underlying script entries: **`scripts.test`** = **`node --test ./test/*.test.js`**; **`scripts.smoke`** = **`node ./scripts/smoke-integration.js`**. Green = all unit tests pass; smoke confirms non-blank panel HTML, optional `lvibe` launcher string check when the full monorepo is present, a best-effort local Ollama probe (non-fatal if Ollama is down unless strict mode is on), and prints the **canonical first-party persisted config directory** (from `storage-inventory.js`) before `smoke: done`.

### Smoke environment (optional)

| Variable | Effect |
|----------|--------|
| `LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=1` | Fail smoke if Ollama is unreachable (use on a machine with Ollama). |
| `LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT` | Override default `http://127.0.0.1:11434`. |
| `LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS` | Override Ollama probe timeout (default `2500`). |
| `LEVIBE_SMOKE_SKIP_LVIBE_LAUNCHER=1` | Skip `packaging/bin/lvibe` check (extension-only tree). |

## Bounded persistence

All extension-owned files live under **`~/.config/le-vibe/levibe-native-chat/`**. See **`README.md`** (section *Bounded persistence inventory*) and **`storage-inventory.js`** (`levibeNativeChatDir`, `PERSISTED_ARTIFACTS`).

Chat transcript JSONL is capped by **`leVibeNative.chatTranscriptMaxBytes`** (default **524288** bytes) and **`leVibeNative.chatTranscriptMaxMessages`** (default **200** JSONL rows) (oldest-first compaction with an explicit system stub when limits are hit — details in README).

## Product track

Workflow board: **`.lvibe/workflows/native-extension-product-track.md`** (Epic N8 — operator runbook).

**Settings disclosure guardrail:** **`npm test`** runs **`test/package-leVibeNative-keys-doc-inventory.test.js`**, which fails if any **`leVibeNative.*`** key in **`package.json`** contributes is absent from this runbook and/or **`README.md`** (add the key to operator or developer docs before shipping).

**Scripts literal umbrella:** **`npm test`** runs **`test/package-json-all-scripts-doc-literal-sync.test.js`**, which fails if any **`package.json` `scripts`** value is absent from this runbook and/or **`README.md`** (keep **`scripts.test`**, **`scripts.smoke`**, **`scripts.verify`** literals documented when you change npm scripts).
