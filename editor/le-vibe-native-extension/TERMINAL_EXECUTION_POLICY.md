# Terminal execution policy (Lé Vibe Chat, Epic N13)

**Status:** Policy and settings only (task-n13-1). Actual execution in the VS Code terminal is implemented in later tasks (n13-2+).

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

Implementation: [`terminal-execution-policy.js`](terminal-execution-policy.js) (`evaluateTerminalCommand`, `getTerminalExecutionPolicy`).

## Recommended workspace snippet

```json
{
  "leVibeNative.terminalExecutionEnabled": true,
  "leVibeNative.terminalCommandAllowPatterns": ["npm run test", "npm run lint", "git status"],
  "leVibeNative.terminalCommandDenyPatterns": ["rm -rf", "sudo ", "| sh", "curl | sh", ":(){ :|:& };:"]
}
```

Tune **allow** to the smallest set that fits your workflow. Extend **deny** for your threat model.
