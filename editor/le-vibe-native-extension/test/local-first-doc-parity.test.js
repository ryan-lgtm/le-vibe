const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

/**
 * OPERATOR and README must agree on the no–silent-cloud-fallback sentence (task-n8-24).
 */
test('OPERATOR.md and README.md share local-first cloud-fallback sentence', () => {
  const shared =
    'the extension does **not** silently fall back to a cloud LLM';
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(operator.includes(shared), 'OPERATOR.md must keep shared local-first sentence');
  assert.ok(readme.includes(shared), 'README.md must keep shared local-first sentence');
  assert.ok(operator.includes('leVibeNative.ollamaEndpoint'));
  assert.ok(readme.includes('leVibeNative.ollamaEndpoint'));
});
