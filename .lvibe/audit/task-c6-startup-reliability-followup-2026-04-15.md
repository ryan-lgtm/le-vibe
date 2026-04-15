# Task C6 Follow-up — `lvibe .` startup reliability and Cline onboarding

## Trigger

Operator reported that:

- `lvibe .` intermittently exits with `Ollama API is not reachable ...`,
- `lvibe --force-first-run .` succeeds,
- Continue no longer loads, but initial Cline UI can appear gray/blank without clear guidance.

## Root cause

`_run_global_session_preamble` evaluated readiness before any managed Ollama recovery attempt.  
When `ensure_product_first_run` skipped (marker + model decision present), readiness could fail on a cold daemon, causing default launch to exit with code `8` before runtime startup path.

## Changes

1. `le-vibe/le_vibe/launcher.py`
   - Added one-shot managed Ollama recovery inside preamble when readiness failure contains
     `Ollama API is not reachable`.
   - Re-runs readiness check after successful recovery.

2. `le-vibe/le_vibe/cline_setup_auto.py`
   - Added one-time Cline onboarding hint (`.cline-onboarding-hint-shown`) when first-run is complete,
     Cline storage exists, and only `settings/cline_mcp_settings.json` is present (no visible auth state yet).
   - Hint directs user to complete Cline sign-in/provider setup if panel appears blank.

## Validation

- Targeted tests:
  - `pytest -q le-vibe/tests/test_launcher_session_preamble.py le-vibe/tests/test_cline_setup_auto.py le-vibe/tests/test_first_run.py`
  - Result: `16 passed`

## Expected operator-visible outcome

- `lvibe .` should no longer require manual `--force-first-run` solely to recover managed Ollama reachability.
- First launch with Cline installed but unauthenticated now emits explicit onboarding guidance instead of silent gray-state ambiguity.
