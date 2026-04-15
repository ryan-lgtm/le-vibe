# Lé Vibe Native Extension Tech Shape (N0-2)

This decision record selects the technical shape for the first-party Lé Vibe extension.

## Decision

Use a native VS Code extension under `editor/` with:

- Extension host entrypoint for activation and command registration.
- A dedicated webview view for deterministic readiness + chat surface.
- A small typed command surface for startup, remediation, and storage controls.

Selected scaffold target:

```text
editor/le-vibe-native-extension/
  package.json
  src/extension.ts
  src/commands/
  src/readiness/
  src/bridge/
  src/storage/
  media/
  test/
```

## Why this shape

- Fits `lvibe .` startup requirement: extension activates in-editor and can always render a non-blank state.
- Supports local-first Ollama integration cleanly from extension host (`127.0.0.1:11434` default).
- Enables storage-respectful persistence controls through explicit command palette actions and panel actions.
- Keeps API boundary explicit between UI state machine, bridge calls, and persistence.

## Command surface (initial)

Minimum commands to scaffold in N1/N2:

- `leVibe.openAgentSurface` — focus/open readiness + chat UI.
- `leVibe.retryReadinessCheck` — re-run startup checks and state resolution.
- `leVibe.openOllamaSetupHelp` — open local remediation instructions.
- `leVibe.showChatUsage` — show bounded storage usage summary.
- `leVibe.exportChatHistory` — user-initiated export only.
- `leVibe.clearChatHistory` — explicit destructive clear with confirmation.

## Webview view choice

Use a `WebviewViewProvider` instead of command-only transient panels:

- Persistent, deterministic anchor in the workbench (no hidden dead-end state).
- Cleaner state transitions for `checking` -> terminal readiness states.
- Supports progressive enhancement (streaming output, cancel button, status diagnostics).

## Trade-offs and risks

1. Webview complexity vs native tree/chat UI:
   - Risk: more front-end plumbing and message passing.
   - Mitigation: keep a small typed message protocol and render state from a single source-of-truth model.

2. Startup race conditions during activation:
   - Risk: blank UI if checks run before view is bound.
   - Mitigation: precompute readiness snapshot in extension host and hydrate view on first resolve.

3. Ollama availability variance across machines:
   - Risk: repeated failures degrade UX.
   - Mitigation: explicit error taxonomy and actionable remediation states (`needs_ollama`, `needs_model`).

4. Storage growth risk:
   - Risk: local history can exceed budgets.
   - Mitigation: bounded store under `~/.config/le-vibe/`, max-size enforcement, oldest-first compaction with summary stubs.

5. Packaging path under `editor/`:
   - Risk: confusion with existing `editor/le-vibe-settings-extension`.
   - Mitigation: keep first-party agent extension isolated as `editor/le-vibe-native-extension` and document ownership.

## Alternatives considered

- Reuse/expand `editor/le-vibe-settings-extension`:
  - Rejected for this track because it is settings/help oriented and not structured for deterministic readiness/chat lifecycle.
- External app/window separate from VS Code extension host:
  - Rejected because it weakens `lvibe .` in-editor determinism and increases orchestration complexity.
- Third-party extension dependency:
  - Rejected due to gray-screen risk, weaker auditability, and local-first control gaps.

## Exit criteria mapping for N0-2

- Scaffold approach selected: yes (native extension + webview view + command surface, with target tree).
- Risks/trade-offs documented: yes (five concrete risks with mitigations, plus alternatives).

