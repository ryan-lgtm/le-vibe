# Task C6 Continue Runtime Inventory and Remediation Evidence

## Scope

- Task: `task-c6-release-readiness-closeout`
- Objective: close the C6 blocker where Continue-era UI state (gray rectangle) still appears after Cline install.

## Phase 1 — Reproduce and inventory active Continue sources

### Evidence commands

1. `"/usr/lib/le-vibe/bin/codium" --list-extensions`
2. `ls -la "/home/ryan/.vscode-oss/extensions"`
3. `rg "continue|Continue|continue\\.continue|Authentication provider continue" /home/ryan/workspace/r-vibe`

### Findings

- Active editor extension list initially included:
  - `continue.continue`
  - `redhat.vscode-yaml`
  - `saoudrizwan.claude-dev`
- User extension directory contained stale Continue install:
  - `/home/ryan/.vscode-oss/extensions/continue.continue-1.3.38-linux-x64`
- Runtime/install scripts still allowed stale Continue state to survive unless manually removed.

## Phase 2 — Eliminate Continue from runtime/install surface

### Implemented controls

- `packaging/scripts/install-cline-extension.sh` now:
  - detects and uninstalls disallowed extension id `continue.continue`,
  - removes stale Continue extension directories from common profile locations:
    - `~/.vscode-oss/extensions`
    - `~/.vscode/extensions`
    - `~/.config/VSCodium/extensions`
  - keeps behavior deterministic with explicit remediation on uninstall failure.

### Evidence command

- `bash packaging/scripts/install-cline-extension.sh`

### Outcome

- Installer output confirmed:
  - `uninstalling disallowed extension continue.continue`
  - `Extension 'continue.continue' was successfully uninstalled`

## Phase 3 — Startup enforcement and remediation

### Implemented controls

- `le-vibe/le_vibe/first_run.py` readiness gate now fails if a disallowed extension is active.
- Error is explicit and actionable:
  - `codium --uninstall-extension continue.continue`

### Runtime evidence

- After remediation:
  - `"/usr/lib/le-vibe/bin/codium" --list-extensions` shows only:
    - `redhat.vscode-yaml`
    - `saoudrizwan.claude-dev`
- Structured runtime log check:
  - `rg "continue|Continue|Authentication provider continue|continue\\.focusContinueInput" /home/ryan/.config/le-vibe/le-vibe.log.jsonl`
  - result: `No matches found`

## Closeout note

- Continue is no longer active in the default extension runtime path on this host.
- Cline remains present as the exclusive agent extension in the observed packaged editor profile.
