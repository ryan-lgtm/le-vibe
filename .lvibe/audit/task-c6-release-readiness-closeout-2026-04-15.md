# Task C6 Closeout Audit — Release Readiness (Cline migration)

## Task resolution and acceptance target

- Active epic from `.lvibe/session-manifest.json`: `epic-cline-e2e-migration`.
- Delegated task executed: `task-c6-release-readiness-closeout`.
- Manifest acceptance criterion: evidence that fresh install launches Cline-ready Lé Vibe with Ollama/model checks passing.
- Backlog C6 scope: run full install/smoke closeout, record evidence in `.lvibe/audit/`, update manifest handoff notes.

## Environment

- Timestamp (UTC): 2026-04-15T17:17:24Z
- Host OS: Linux `6.17.0-20-generic`
- Repo: `/home/ryan/workspace/r-vibe`
- VSCodium submodule state observed by orchestrator: `DIRTY` (non-blocking warning)

## Commands executed

1. Full closeout attempt (with apt install):
   - `packaging/scripts/install-le-vibe-local.sh --install --yes --skip-compile-failfast --json --log-file .lvibe/audit/task-c6-release-readiness-closeout-2026-04-15.log`
2. Post-install payload verification on currently installed host state:
   - `dpkg -l le-vibe le-vibe-ide`
   - `/usr/bin/lvibe --help`
   - `packaging/scripts/manual-step14-install-smoke.sh --verify-only`
3. Closeout rerun without apt install (to complete runtime readiness checks):
   - `packaging/scripts/install-le-vibe-local.sh --skip-compile-failfast --json --log-file .lvibe/audit/task-c6-release-readiness-closeout-2026-04-15.log`

## Evidence captured

### A) Full closeout with `--install` failed at apt step (blocker)

- Build + STEP 14 closeout portions completed:
  - `verify_step14_closeout_passed: true`
  - `.deb` artifacts produced:
    - stack: `/home/ryan/workspace/r-vibe/../le-vibe_0.1.9_all.deb`
    - ide: `/home/ryan/workspace/r-vibe/packaging/le-vibe-ide_0.1.3_amd64.deb`
- Apt install failed because this automation context cannot provide sudo password:
  - `sudo: a terminal is required to read the password`
  - JSON result: `status=error`, `step=install`, `install_readiness_reasons=["apt_install_failed"]`

### B) Installed-state smoke checks passed

- Installed packages present:
  - `le-vibe 0.1.9`
  - `le-vibe-ide 0.1.3`
- `manual-step14-install-smoke.sh --verify-only` passed:
  - verifies `lvibe`, `/usr/lib/le-vibe/bin/codium`, desktop entry, and docs payloads.

### C) Closeout rerun without apt install passed runtime readiness checks

- `install-le-vibe-local.sh --skip-compile-failfast --json` result:
  - `status=ok`
  - `verify_step14_closeout_passed=true`
  - `runtime_ollama_state=ready` (existing `/usr/local/bin/ollama`)
  - Cline extension install succeeded:
    - `saoudrizwan.claude-dev@3.19.4`
    - `redhat.vscode-yaml@1.22.2026041108`
- Note: this successful run is build+verify+runtime readiness; it does not perform apt install (`install_performed=false`).

## Blocker report

- Blocker: non-interactive automation cannot satisfy `sudo apt-get install` password prompt during required full `--install` closeout path.
- Evidence: exact stderr from closeout attempt:
  - `sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper`
  - `sudo: a password is required`
- This blocks final acceptance wording tied to a fresh install execution in this session.

## Explicit unblock action

Run the following in an interactive terminal session with sudo auth available:

1. `packaging/scripts/install-le-vibe-local.sh --install --yes --skip-compile-failfast --json --log-file .lvibe/audit/task-c6-release-readiness-closeout-2026-04-15.log`
2. `packaging/scripts/manual-step14-install-smoke.sh --verify-only`
3. `lvibe .` (single launch smoke for agent-ready flow)

When those commands pass, update `task-c6` to `done` with the interactive run timestamp and JSON payload reference.
