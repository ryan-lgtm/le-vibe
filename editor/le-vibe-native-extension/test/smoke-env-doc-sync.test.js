const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

/** Every env var smoke-integration reads; must stay documented in OPERATOR.md. */
const SMOKE_ENV_VARS = [
  'LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA',
  'LEVIBE_NATIVE_SMOKE_OLLAMA_ENDPOINT',
  'LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS',
  'LEVIBE_SMOKE_SKIP_LVIBE_LAUNCHER',
];

test('OPERATOR.md documents each smoke env var used by smoke-integration.js', () => {
  const smoke = fs.readFileSync(path.join(__dirname, '..', 'scripts', 'smoke-integration.js'), 'utf8');
  const op = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  for (const v of SMOKE_ENV_VARS) {
    assert.ok(smoke.includes(v), `smoke-integration.js should reference ${v}`);
    assert.ok(op.includes(v), `OPERATOR.md should document ${v}`);
  }
});
