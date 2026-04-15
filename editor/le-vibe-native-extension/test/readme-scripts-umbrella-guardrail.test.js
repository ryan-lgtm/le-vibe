const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README.md documents scripts literal umbrella guardrail test (task-n8-65)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(text.includes('Scripts literal umbrella'));
  assert.ok(text.includes('package-json-all-scripts-doc-literal-sync.test.js'));
});
