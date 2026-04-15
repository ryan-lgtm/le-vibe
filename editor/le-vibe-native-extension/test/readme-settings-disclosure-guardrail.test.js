const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README.md documents settings disclosure guardrail test (task-n8-56)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(text.includes('Settings disclosure guardrail'));
  assert.ok(text.includes('package-leVibeNative-keys-doc-inventory.test.js'));
  assert.ok(text.includes('leVibeNative.*'));
});
