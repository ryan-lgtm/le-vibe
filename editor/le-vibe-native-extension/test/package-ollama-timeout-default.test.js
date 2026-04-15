const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('leVibeNative.ollamaTimeoutMs default matches OPERATOR smoke timeout default (task-n8-37)', () => {
  const props = packageJson.contributes.configuration[0].properties;
  const ms = props['leVibeNative.ollamaTimeoutMs'];
  assert.ok(ms);
  assert.equal(ms.default, 2500);

  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(operator.includes('LEVIBE_NATIVE_SMOKE_OLLAMA_TIMEOUT_MS'));
  assert.ok(operator.includes('default `2500`'));
});
