# Lé Vibe Native Extension — operator quick reference

Use this sheet when validating or shipping the first-party extension (`editor/le-vibe-native-extension/`).

**Prerequisites:** **Node.js 18+** on your PATH to run **`npm run verify`** / **`npm test`** (uses `node:test`). The VS Code extension host ships its own runtime; the Node engine is for this package’s scripts and CI only. For installing or running the extension in an editor, match **`engines.vscode`** in `package.json` — currently **VS Code 1.85+** (or a compatible build such as **VSCodium** meeting the same API level). Contributor-oriented wording for the same Node and editor requirements is in **`README.md`** (*Prerequisites (developers)*).

`package.json` includes **`repository.directory`**, **`homepage`**, **`bugs`**, and **`keywords`** so tooling and registries can link to the monorepo path and issue tracker. It also declares **`publisher`** and **`license`** (SPDX string) for marketplace and CI identity.

**Extension host entry:** **`package.json`** **`main`** must be **`./extension.js`** (VS Code activation entry; required for packaging).

**Local-first:** the shipped defaults target **local Ollama** (see `leVibeNative.ollamaEndpoint`); the extension does **not** silently fall back to a cloud LLM.

**Default local Ollama URL:** **`http://127.0.0.1:11434`** — configure via **`leVibeNative.ollamaEndpoint`** (smoke’s default probe matches unless `LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT` is set).

**Default Ollama probe timeout:** **`2500` ms** — configure via **`leVibeNative.ollamaTimeoutMs`** (smoke override **`LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS`**; same default as the smoke table below).

**Default local model tag:** **`mistral:latest`** — **`leVibeNative.ollamaModel`** (used for streaming generate requests).

**Inline suggestions (beta, task-cp4-1):** **`leVibeNative.inlineSuggestionsEnabled`** default **`false`** — when enabled, registers a local-only inline completion provider for file editors (standard VS Code accept/dismiss keys); uses configured Ollama endpoint/model only.
**Inline suggestion debounce (task-cp4-2):** **`leVibeNative.inlineSuggestionsDebounceMs`** default **`150` ms** to suppress noisy repeated requests while typing.
**Inline latency budget (task-cp4-2):** operational target is **<= 1200 ms p95** time-to-first-suggestion for small single-line prefixes on local Ollama; above budget, provider should return empty result and keep editing responsive.
**Inline fallback quick-fix actions (task-cp4-3):** when inline suggestions are disabled/unavailable, selection assist remains available via editor context menu, selection CodeLens, and Quick Fix entries (`Ask`, `Explain`, `Refactor`, `Generate tests`) that open/populate Lé Vibe Chat.

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

**@file / @folder (task-n14-1):** Palette **`leVibeNative.addContextAtFile`** / **`leVibeNative.addContextAtFolder`** — **`vscode.workspace.findFiles`** with bounded scan + folder QuickPick cap; excerpts/listings clipped per **`contextMax*`**; implementation **`at-mention-context.js`**.

**Outline (task-n14-2):** Palette **`leVibeNative.addCurrentFileOutlineToContext`** — **`vscode.executeDocumentSymbolProvider`** on the **active file** only; bounded symbol expansion + **`contextMax*`** clipping; **not** a cross-repo or cloud index (see README *Current-file outline only* vs Cursor-class cloud retrieval).

**Selection → chat (task-n12-1):** Palette / context menu **`leVibeNative.askChatAboutSelection`** + CodeLens on selection — opens agent surface if needed; pushes path + clipped selection into context; **`selection-chat-context.js`**.

**Quick action templates (task-n12-2):** Panel **Explain / Refactor selection / Generate tests** — inserts `QUICK_ACTION_TEMPLATES` from **`chat-quick-actions.js`**; Ollama only on **Send Prompt** (local endpoint).

**Terminal execution policy (task-n13-1):** **`leVibeNative.terminalExecutionEnabled`** default **`false`** (agent shell commands off until explicitly enabled). **`leVibeNative.terminalCommandAllowPatterns`** (default empty) and **`leVibeNative.terminalCommandDenyPatterns`** (shipped defaults include `rm -rf`, `sudo `, fork-bomb pattern, `| sh`, `curl | sh`) — deny wins; when enabled, an empty allow list blocks every command until you add patterns. Prefer **Workspace** scope for the master switch. Policy evaluation: **`terminal-execution-policy.js`**; full write-up **`TERMINAL_EXECUTION_POLICY.md`**.

**Terminal execution — visible integrated terminal (task-n13-2):** Palette **`leVibeNative.runCommandInIntegratedTerminal`** / panel **Run command in terminal…** — policy must allow the command; then a **modal confirms each batch** unless **`leVibeNative.terminalSkipBatchConfirmation`** is **`true`** (advanced) or the user chose session-skip in the modal. Commands are sent only to a visible terminal named **`Lé Vibe Chat`** (`terminal-exec.js` — not a hidden PTY). **`leVibeNative.clearTerminalSessionAllow`** resets session-skip; changing workspace folders also clears it.

**Startup / rollout (defaults):** **`leVibeNative.enableFirstPartyAgentSurface`** default **`true`** (first-party Lé Vibe Chat surface); **`leVibeNative.showFirstRunWizard`** default **`true`** (checkpointed wizard); **`leVibeNative.openPanelOnStartup`** default **`true`** (auto-open panel when the first-party surface is enabled). **Status bar (task-n17-3):** **`leVibeNative.showStatusBarEntry`** default **`false`** — optional subtle status item (Lé Vibe Chat + local Ollama reachability; click opens agent surface). Rollback semantics in **`README.md`** *Rollout and rollback*.

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

### Flake resistance (task-n18-2)

**Loop command used (2026-04-15):** from **`editor/le-vibe-native-extension/`**:

```bash
for i in $(seq 1 10); do npm run verify || exit 1; done
```

**Outcome:** **10/10** consecutive **`npm run verify`** runs passed (same machine, no failures). **Intentionally skipped tests:** none — **`npm test`** is fully offline; **`npm run smoke`** uses a **best-effort** local Ollama probe and does **not** fail CI when Ollama is absent unless **`LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=1`** (see *Smoke environment* below). Do **not** add network-dependent unit tests to the default **`npm test`** glob without an explicit product-track task and mocks.

Re-run this loop after large async/timer refactors or if CI-only flakes appear.

## Security notes (task-n18-1)

**Dependency audit:** from **`editor/le-vibe-native-extension/`**, run **`npm audit`** against the committed **`package-lock.json`** before releases or when bumping dependencies. Re-run **`npm run verify`** after any **`package.json`** / lockfile change.

**Last triage (2026-04-15):** **`npm audit`** reported **0 vulnerabilities** for the resolved tree (production: **`ignore`**; dev: **`@vscode/vsce`** and its transitive dependencies).

**`overrides` / `resolutions`:** this **`package.json`** does **not** define npm **`overrides`**. If a future audit surfaces a transitive issue with no direct upgrade path, add an **`overrides`** entry **only** with a short rationale in this section (CVE id, affected package range, why the override is safe for the extension host).

**Residual risk / tracking:** if **`npm audit`** reports issues later, file or link a tracker under **`https://github.com/ryan-lgtm/le-vibe/issues`** (see **`package.json`** **`bugs.url`**) and note the product-track follow-up; do not ship silent **`npm audit fix --force`** major jumps without **`npm run verify`** and a short note here.

### CI (GitHub Actions)

The repository workflow **`.github/workflows/le-vibe-native-extension-ci.yml`** runs on **push** and **pull request** to **`main`** and **`master`**: it executes **`npm ci`** then **`npm run verify`** in **`editor/le-vibe-native-extension`** on an **Ubuntu** runner (Node **18**). This is the automated ship gate for the extension package; failing steps should block merging once the check is marked **required** in GitHub branch protection (**Settings → Branches** for the default branch). Until your org wires that policy, treat a locally green **`npm run verify`** as the same bar before merging extension changes.

### Packaged VSIX (task-n16-2)

From **`editor/le-vibe-native-extension/`** after **`npm ci`**, run **`npm run package`**. That executes **`vsce package`** (**`package.json`** **`scripts.package`** = **`vsce package`**) and writes an installable **`le-vibe-native-extension-<version>.vsix`** in the **same directory** (for **`0.1.0`**, the file is **`le-vibe-native-extension-0.1.0.vsix`**). The monorepo root **`.gitignore`** ignores **`*.vsix`** so local builds are not committed. Install into a VS Code–compatible editor (CLI name may be **`code`** or **`codium`**):

```bash
code --install-extension ./le-vibe-native-extension-0.1.0.vsix
```

**Alternate CLI (task-n24-1):** if **`code`** is not on your **`PATH`** (e.g. **`which code`** fails), use **`codium`**, **`vscodium`**, or your distro’s VS Code–compatible launcher — keep the same **`--install-extension`** flag and the same **`.vsix`** path. Example: **`codium --install-extension ./le-vibe-native-extension-0.1.0.vsix`**.

**Manual spot-check (task-n23-1):** after a successful install, open the **Extensions** view in the editor (**View → Extensions**, or **Ctrl+Shift+X** / **Cmd+Shift+X**). Locate **Lé Vibe Native Agent** — that string is **`package.json`** **`displayName`** (publisher **`levibe`**). Confirm the **version** shown there matches **`package.json`** **`version`** (for the sample above, **0.1.0**). If the version does not match, you likely installed a different **`.vsix`** or an older cached build — re-run **`npm run package`** and install again.

No tokens or cloud secrets are embedded in this packaging path — the VSIX is a local archive of the extension tree plus production **`node_modules`** per **`@vscode/vsce`** defaults.

**`CHANGELOG.md` ships in the VSIX (task-n22-1):** **`CHANGELOG.md`** is **not** listed in **`.vscodeignore`** (that file excludes only dev-only paths such as **`test/**`**, **`scripts/smoke-integration.js`**, **`.vscode/**`, **`.vscode-test/**`**), so semver release notes are included in the **`.vsix`** archive for operators and users who inspect the package.

### Extension version vs monorepo / packaging (task-n16-3)

The **authoritative extension version** for **Lé Vibe Chat** is **`editor/le-vibe-native-extension/package.json`** **`version`** — it feeds **`@vscode/vsce`** output (**`le-vibe-native-extension-<version>.vsix`**) and what users see in the Extensions view. That semver string is **independent by default** from root **Debian** package versions (**`debian/changelog`**, **`le-vibe`** / **`le-vibe-ide`** `.deb` numbers): do **not** assume the IDE `.deb` and this **`package.json`** bump in lockstep unless you deliberately align them for a coordinated release. Monorepo **git tags** are also **manual for now** (no automation in this repo ties a tag only to the extension subtree); teams may use a dedicated tag pattern (e.g. **`levibe-native-extension-v0.2.0`**) or document the extension version in a broader release note.

**Version bump checklist (operators):**

1. Edit **`package.json`** **`version`** (semver: patch / minor / major as appropriate), then **`npm run verify`** in **`editor/le-vibe-native-extension/`**.
2. Run **`npm run package`** and confirm the generated **`le-vibe-native-extension-<version>.vsix`** matches the new **`version`** string.
3. Commit the **`package.json`** / lockfile change (if any) on **`main`** (or your release branch).
4. **Optional git tag** at the repo root: e.g. **`git tag -a levibe-native-extension-vX.Y.Z -m "Lé Vibe native extension X.Y.Z"`** then **`git push origin levibe-native-extension-vX.Y.Z`** — only if your release process uses tags; otherwise skip.
5. **Publish / hand off:** attach the **`.vsix`** to a **GitHub Release** (or your internal artifact store). Installers upgrading from an older VSIX get the new **`version`** without editing **`debian/`** unless you are also shipping a Debian-side change.
6. **CHANGELOG:** add a **`## [version]`** section to **`CHANGELOG.md`** summarizing user-visible changes (see *CHANGELOG (task-n19-1)* under *Product track*).

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

**Terminal command audit (task-n13-3):** **`terminal-command-audit.jsonl`** — append-only **`lvibe.terminal_command_audit.v1`** lines (timestamp, cwd, command line; **`exit_code`** when **`onDidEndTerminalShellExecution`** matches). Same directory as other Lé Vibe Chat persistence; see **`terminal-command-audit.js`**.
**Orchestrator bridge audit (task-cp5-1):** **`orchestrator-events.jsonl`** — append-only **`lvibe.orchestrator_event.v1`** lines with event types **`chat_turn`**, **`edit_apply`**, **`plan_run`**, **`terminal_exec`** for operator/orchestrator consumption (local-only JSONL).
**Runbook diagnostics (task-cp5-2):** Palette **Lé Vibe Chat: Package runbook diagnostics (support)…** (`leVibeNative.packageRunbookDiagnostics`) writes a **local-only** folder under **`~/.config/le-vibe/levibe-native-chat/runbook-bundles/runbook-<timestamp>/`** (settings snapshot + recent audit/tail files + `README-runbook.txt`). No cloud upload; zip for support if needed.

## Product track

Workflow board: **`.lvibe/workflows/native-extension-product-track.md`** (Epic N8 — operator runbook).

**README: issues + GitHub source (task-n27-1):** **`package.json`** **`bugs.url`** and **`homepage`** (issue tracker + monorepo **tree** URL for this package) are written out in **`README.md`** *Issues / bugs (task-n25-1)* and *Source on GitHub (task-n26-1)* — use those sections for copy-paste URLs instead of opening **`package.json`**.

**README: monorepo clone (task-n29-1):** **`package.json`** **`repository`** **`url`** and **`directory`** (clone root + package path inside the monorepo) are written out in **`README.md`** *Monorepo clone (task-n28-1)* — use that section instead of assembling **`git`** clone + **`cd`** paths manually.

**README: SPDX license (task-n31-1):** **`package.json`** **`license`** (SPDX string; marketplace / CI identity alongside **`publisher`**) is written out in **`README.md`** *License (task-n30-1)* — use that section for the authoritative SPDX value instead of opening **`package.json`**.

**README: publisher (task-n33-1):** **`package.json`** **`publisher`** (marketplace namespace / VS Code extension id prefix **`<publisher>.<name>`**) is written out in **`README.md`** *Publisher (task-n32-1)* — use that section for the authoritative publisher string instead of opening **`package.json`**.

**README: keywords (task-n35-1):** **`package.json`** **`keywords`** (registry / marketplace search tags) are written out in **`README.md`** *Keywords (task-n34-1)* — use that section for the shipped tag list instead of opening **`package.json`**.

**README: categories (task-n37-1):** **`package.json`** **`categories`** (VS Code Marketplace extension category) are written out in **`README.md`** *Categories (task-n36-1)* — use that section for the shipped marketplace category instead of opening **`package.json`**.

**README: displayName (task-n39-1):** **`package.json`** **`displayName`** (Marketplace / Extensions UI listing title) is written out in **`README.md`** *Display name (task-n38-1)* — use that section for the shipped listing title instead of opening **`package.json`**.

**README: description (task-n41-1):** **`package.json`** **`description`** (Marketplace / Extensions UI summary blurb) is written out in **`README.md`** *Description (task-n40-1)* — use that section for the shipped summary text instead of opening **`package.json`**.

**README: package name (task-n43-1):** **`package.json`** **`name`** (npm/package identifier) is written out in **`README.md`** *Package name (task-n42-1)* — use that section for the shipped package id instead of opening **`package.json`**.

**README: version (task-n45-1):** **`package.json`** **`version`** (current shipped extension package version) is written out in **`README.md`** *Version (task-n44-1)* — use that section for the shipped version string instead of opening **`package.json`**.

**README: engines.vscode minimum (task-n47-1):** **`package.json`** **`engines.vscode`** minimum/API floor is written out in **`README.md`** *Editor API minimum (task-n46-1)* — use that section for the runtime baseline instead of opening **`package.json`**.

**README: engines.node minimum (task-n49-1):** **`package.json`** **`engines.node`** minimum/runtime floor is written out in **`README.md`** *Node runtime minimum (task-n48-1)* — use that section for the package-script baseline instead of opening **`package.json`**.

**README: activationEvents docs (task-n51-1):** **`package.json`** **`activationEvents`** startup + command-trigger intent is written out in **`README.md`** *Activation events (task-n50-1)* — use that section to verify activation behavior without opening **`package.json`**.

**README: activationEvents command example (task-n53-1):** **`package.json`** **`activationEvents`** concrete command-trigger literal is written out in **`README.md`** *Activation event example (task-n52-1)* — use that section to find a shipped **`onCommand:leVibeNative.*`** example without opening **`package.json`**.

**README: startup activation intent (task-n55-1):** **`package.json`** **`activationEvents`** startup rationale is written out in **`README.md`** *Startup activation intent (task-n54-1)* — use that section to verify why **`onStartupFinished`** is enabled.

**README: activation example lookup (task-n57-1):** the one-hop mapping from activation metadata to palette labels is written out in **`README.md`** *Activation example lookup (task-n56-1)* — use that section to jump from **`activationEvents`** literals to the command table quickly.

**README: activation count rationale lookup (task-n59-1):** the startup-count relationship is written out in **`README.md`** *Activation count rationale lookup (task-n58-1)* — use that section to explain why startup activation appears in the event breakdown quickly.

**README: activation docs quick index (task-n63-1):** the activation-doc cluster entrypoint is written out in **`README.md`** *Activation docs quick index (task-n62-1)* — use that section first when directing contributors through activation metadata docs.

**README: activation docs sequence (task-n61-1):** the intended activation-doc flow is written out in **`README.md`** *Activation docs sequence (task-n60-1)* — use that section when guiding contributors through activation metadata discovery.

**README: activation index next hop (task-n65-1):** the quick-index-to-sequence handoff is written out in **`README.md`** *Activation index next hop (task-n64-1)* — use that section to point contributors from index context into the guided breadcrumb flow.

**README: quick-index sequence token (task-n67-1):** **`README.md`** *Activation docs quick index (task-n62-1)* explicitly references *Activation docs sequence (task-n60-1)* — use that line to call out the built-in next step during handoff.

**README: activation sequence return hop (task-n69-1):** **`README.md`** *Activation sequence return hop (task-n68-1)* points sequence readers back to *Activation docs quick index (task-n62-1)* — use that line when redirecting contributors to the compact activation-doc entrypoint.

**CHANGELOG (task-n19-1):** **`CHANGELOG.md`** — semver release notes at the package root (Keep a Changelog–style). When you bump **`package.json`** **`version`**, add a **`## [x.y.z]`** section there (coordinate with *Extension version vs monorepo / packaging (task-n16-3)*). Epic-level history remains in the product-track file above.

**Security notes (task-n18-1):** see **`## Security notes (task-n18-1)`** above — **`npm audit`** triage, **`overrides`** policy, issue tracker pointer.

**Flake resistance (task-n18-2):** see **`### Flake resistance (task-n18-2)`** under **Verify (canonical)** — 10× **`npm run verify`** evidence and intentional-skip policy.

**Settings disclosure guardrail:** **`npm test`** runs **`test/package-leVibeNative-keys-doc-inventory.test.js`**, which fails if any **`leVibeNative.*`** key in **`package.json`** contributes is absent from this runbook and/or **`README.md`** (add the key to operator or developer docs before shipping).

**Scripts literal umbrella:** **`npm test`** runs **`test/package-json-all-scripts-doc-literal-sync.test.js`**, which fails if any **`package.json` `scripts`** value is absent from this runbook and/or **`README.md`** (keep **`scripts.test`**, **`scripts.smoke`**, **`scripts.verify`** literals documented when you change npm scripts).

**Command palette inventory (task-n17-1):** **`README.md`** *Command palette and keyboard shortcuts (task-n17-1)* — table of **`leVibeNative.*`** command id → **Command Palette** label (**`Lé Vibe Chat:`** + **`title`**) → default keybinding (**none** shipped; bind in Keyboard Shortcuts).

**Panel accessibility (task-n17-2):** **`README.md`** *Accessibility (task-n17-2)* — webview skip link, **`main`** landmark, button **`title`** / **`aria-label`**, live regions for status/log; theme spot-check notes and known gaps.

**Status bar entry (task-n17-3):** **`leVibeNative.showStatusBarEntry`** — see **Startup / rollout** above and **`README.md`** *Rollout and rollback*; implementation **`status-bar-entry.js`** (disposes on deactivate via **`ExtensionContext.subscriptions`**).

## E2E agentic editor release checklist (Epic N15, task-n15-1)

Run **after** **`npm run verify`** is green. This is a **manual** gate for agentic-editor flows (edit preview, multi-step workspace plan, cancellation). **Sign off** each release in the table at the end (tag, VSIX version, or internal build id).

### Prerequisites

- Open a **folder workspace** (not a single untitled buffer only) so demos can write under **`.lvibe/`** in that folder.
- **Ollama** is **not** required for these panel demos (they use the built-in sample paths and **`WorkspaceEdit`**).

### A — Preview → accept → apply → undo (edit proposal demo)

1. **Lé Vibe Chat: Open Agent Surface** — panel shows readiness + chat controls (not a blank/gray webview).
2. Click **Preview sample workspace edit** — a **unified diff** appears for **`.lvibe/.levibe-edit-preview-demo.txt`**.
3. With **`leVibeNative.requireEditPreviewBeforeApply`** at default **`true`**: click **Accept preview**, then **Apply to file**. Optionally confirm **Reject** dismisses the preview **without** applying.
4. Focus the modified file and use editor **Undo** once (**Ctrl+Z** / **Cmd+Z**) — contents revert for that **Apply** (one undo transaction per **Apply**, same manual contract as **task-n9-3** above).

### B — Multi-step workspace plan → cancel mid-flight

1. Click **Run sample workspace plan** — chat log shows **`Lé Vibe Chat: plan step N/M — …`** for **three** steps (sample **create_file** → **apply_edit** → **move_file** under **`.lvibe/`**).
2. While **Cancel plan run** is enabled, click **Cancel plan run**.
3. **Expected:** status indicates cancellation after the **in-flight** step finishes; **remaining steps are not run** (partial completion is explicit). **Cancel** does **not** auto-rollback completed steps — clean up with editor/SCM if needed (see **`WORKSPACE_PLAN.v1.md`**).

### Sign-off (per release)

| Release (tag or VSIX version) | Date (YYYY-MM-DD) | Sign-off (name or initials) | Notes |
|-------------------------------|-------------------|------------------------------|-------|
| _e.g. extension 0.x / git tag_ | _e.g. 2026-04-15_ | | |

Add or update a row whenever you **tag**, **publish a VSIX**, or **bless an internal build** so agentic-editor releases stay auditable.

## Regression goldens (Epic N15, task-n15-2)

File-backed cases under **`test/fixtures/n15-2/`** — **`edit-proposal/`** pairs (`*.proposal.json` + `*.expected.json`) and **`workspace-edit/`** pairs (`*.proposal.json` + `*.meta.json`) — are exercised by **`test/n15-2-golden-regression.test.js`** as part of **`npm test`** / **`npm run verify`**. They lock **`validateEditProposal`** and the **`WorkspaceEdit`** op sequence from **`applyEditProposalBatchAsWorkspaceEdit`** (mocked VS Code API — **no network**).
