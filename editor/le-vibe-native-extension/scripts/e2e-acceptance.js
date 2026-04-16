#!/usr/bin/env node
'use strict';

/**
 * CP6 automated acceptance gate (task-cp6-1): runs the same bar as ship CI plus optional strict Ollama.
 *
 * Exit: 0 = PASS, 1 = FAIL.
 *
 * Env:
 * - LEVIBE_E2E_ACCEPTANCE_STRICT_OLLAMA=1 — after `npm run verify`, re-run smoke with
 *   LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA=1 so unreachable Ollama fails the gate (local release sign-off).
 */

const { execSync } = require('node:child_process');
const path = require('node:path');

function main() {
  const root = path.join(__dirname, '..');
  const strict = process.env.LEVIBE_E2E_ACCEPTANCE_STRICT_OLLAMA === '1';
  console.log(
    `e2e-acceptance: CP6 automated gate (verify${strict ? ' + strict Ollama' : ''})`,
  );
  try {
    execSync('npm run verify', { cwd: root, stdio: 'inherit', env: process.env });
    if (strict) {
      const env = { ...process.env, LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA: '1' };
      execSync('node ./scripts/smoke-integration.js', {
        cwd: root,
        stdio: 'inherit',
        env,
      });
    }
  } catch {
    console.error('e2e-acceptance: RESULT=FAIL');
    process.exit(1);
  }
  console.log('e2e-acceptance: RESULT=PASS');
  console.log(
    'e2e-acceptance: Manual CP6 checklist: docs/E2E_ACCEPTANCE.md (PASS/FAIL column)',
  );
}

main();
