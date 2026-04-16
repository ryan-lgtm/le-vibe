const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const packageJson = require('../package.json');

test('e2e-acceptance script is registered and source exists (task-cp6-1)', () => {
  assert.equal(
    packageJson.scripts['e2e-acceptance'],
    'node ./scripts/e2e-acceptance.js',
  );
  const src = path.join(__dirname, '..', 'scripts', 'e2e-acceptance.js');
  assert.ok(fs.existsSync(src));
  const body = fs.readFileSync(src, 'utf8');
  assert.ok(body.includes('e2e-acceptance: RESULT=PASS'));
  assert.ok(body.includes('e2e-acceptance: RESULT=FAIL'));
});

test('E2E_ACCEPTANCE.md lists automated command and packaging wrapper (task-cp6-1)', () => {
  const doc = path.join(__dirname, '..', 'docs', 'E2E_ACCEPTANCE.md');
  assert.ok(fs.existsSync(doc));
  const text = fs.readFileSync(doc, 'utf8');
  assert.ok(text.includes('npm run e2e-acceptance'));
  assert.ok(text.includes('levibe-chat-e2e-acceptance.sh'));
  assert.ok(text.includes('LEVIBE_E2E_ACCEPTANCE_STRICT_OLLAMA'));
});
