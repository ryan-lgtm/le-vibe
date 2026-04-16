# Terminal execution policy (Lé Vibe Chat, Epic N13)

**Status:** Policy + **visible integrated-terminal execution** (task-n13-2). Commands are sent with `Terminal.sendText` into a named terminal (**`Lé Vibe Chat`**) — not a hidden `child_process` PTY. Structured audit logging is **n13-3**.

## Principles

1. **Off by default** — no agent-driven shell commands unless the user explicitly enables them.
2. **Per-workspace opt-in** — enable execution in **Workspace** settings (`.vscode/settings.json` or the Workspace tab in Settings UI) so each repository opts in deliberately. User-level enable is possible but discouraged for high-risk flows.
3. **Allow-list + deny-list** — when enabled, a proposed command must match at least one **allow** pattern and must not match any **deny** pattern. Empty allow list means **no commands are permitted** until you add patterns.
4. **Local-first** — policy evaluation runs in the extension host; patterns are not sent to remote services by this module.

## Settings keys (`package.json`)

| Key | Purpose |
|-----|---------|
| `leVibeNative.terminalExecutionEnabled` | Master switch (default **`false`**). |
| `leVibeNative.terminalCommandAllowPatterns` | String array — at least one substring/glob must match the normalized command (case-insensitive substring; `*` for simple glob). |
| `leVibeNative.terminalCommandDenyPatterns` | String array — if any pattern matches, the command is blocked regardless of allow list. |
| `leVibeNative.terminalSkipBatchConfirmation` | Advanced — default **`false`**. When **`true`**, skip the confirmation modal before each batch (still visible terminal only). |

Implementation: [`terminal-execution-policy.js`](terminal-execution-policy.js) (`evaluateTerminalCommand`, `getTerminalExecutionPolicy`). Execution entrypoints: [`terminal-exec.js`](terminal-exec.js) (`runCommandInVisibleTerminal`), palette **Lé Vibe Chat: Run command in integrated terminal…**, panel **Run command in terminal…**.

### Confirmation (task-n13-2)

Unless **`terminalSkipBatchConfirmation`** is **true** or you already chose **Run and skip further prompts (this session)** in the modal, you must **confirm each command batch** before it is sent. Session skip is cleared when workspace folders change or via **Lé Vibe Chat: Clear terminal session allow (re-enable confirmations)**.

## Recommended workspace snippet

```json
{
  "leVibeNative.terminalExecutionEnabled": true,
  "leVibeNative.terminalCommandAllowPatterns": ["npm run test", "npm run lint", "git status"],
  "leVibeNative.terminalCommandDenyPatterns": ["rm -rf", "sudo ", "| sh", "curl | sh", ":(){ :|:& };:"]
}
```

Tune **allow** to the smallest set that fits your workflow. Extend **deny** for your threat model.
