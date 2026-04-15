# Task E1 Repro Audit — Fresh Install Continue Stabilization

## Task resolution and acceptance criteria

- Active epic resolved from `.lvibe/session-manifest.json`: `epic-fresh-install-continue-stabilization` (pending `task-e*` exists).
- Delegated task executed: `task-e1-reproduce-clean-install`.
- Manifest acceptance criterion: deterministic repro documented under `.lvibe/audit/` with environment details.
- Backlog Phase E1 acceptance criterion: capture extension list/state, extension host or `workbench.desktop.main.js` signals, and exact install path used.

## Environment

- Timestamp (UTC): 2026-04-15T05:52:30Z
- Host OS: Linux `6.17.0-20-generic`
- Repo: `/home/ryan/workspace/r-vibe`
- Install flow under test: `./packaging/scripts/install-le-vibe-local.sh --install --yes`

## Deterministic repro steps (clean-state flow)

1. Purge previously installed packages and local state:
   - `sudo apt remove --purge le-vibe le-vibe-ide`
   - `./packaging/scripts/uninstall-le-vibe-local.sh --yes --purge-user-data`
2. Run fresh install from repo root:
   - `./packaging/scripts/install-le-vibe-local.sh --install --yes`
3. Verify package install and launch path:
   - `dpkg -l le-vibe le-vibe-ide`
   - `lvibe --help`
   - launch one interactive IDE session (`lvibe .`) to trigger first-run extension activation.
4. Collect artifacts:
   - extension state cache: `~/.config/Lé Vibe/CachedProfilesData/__default__profile__/extensions.user.cache`
   - IDE logs root after launch: `~/.config/Lé Vibe/logs/*/window*/{renderer.log,exthost/exthost.log}`

## Evidence captured in this run/session

- Exact install path executed repeatedly in terminal history:
  - `./packaging/scripts/install-le-vibe-local.sh --install --yes`
- Successful historical install evidence present in session terminal output (same host/workspace):
  - stack package installed as `le-vibe 0.1.9`
  - IDE package installed as `le-vibe-ide 0.1.3`
- Extension state evidence (Lé Vibe profile cache):
  - `continue.continue` present, version `1.3.38`
  - source file: `~/.config/Lé Vibe/CachedProfilesData/__default__profile__/extensions.user.cache`
- Repro attempt from this non-interactive agent run failed at `sudo apt install ...` prompt in install script, which requires a TTY password entry:
  - `sudo: a terminal is required to read the password`
  - this prevents completing a full clean install inside this automation channel without operator interaction.

## Current gap vs E1 target signal

- Not yet captured in this run:
  - explicit `yaml.schemas` registration failure line from Lé Vibe `renderer.log`/`workbench.desktop.main.js`
  - first-launch visual symptom ("Continue gray box") screenshot or direct UI witness
- Reason:
  - full end-to-end fresh install + first interactive IDE launch requires operator-authenticated `sudo` and GUI interaction.

## Operator action needed to complete E1 evidence set

Run the same deterministic flow in an interactive terminal session (with sudo password prompt + one `lvibe .` launch), then append these artifacts:

1. `~/.config/Lé Vibe/logs/<latest>/window*/renderer.log`
2. `~/.config/Lé Vibe/logs/<latest>/window*/exthost/exthost.log`
3. `~/.config/Lé Vibe/CachedProfilesData/__default__profile__/extensions.user.cache`
4. Any screenshot showing the Continue gray-box state (if observed)

This will fully satisfy the backlog's "workbench.desktop.main.js + extension host" capture requirement for E1 on clean install.
