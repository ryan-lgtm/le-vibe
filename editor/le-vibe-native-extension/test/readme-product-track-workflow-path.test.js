const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README.md documents Product track workflow path under Operator verification (task-n8-67)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(text.includes('## Operator verification / ship checklist'));
  assert.ok(text.includes('**Workflow board:**'));
  assert.ok(text.includes('`.lvibe/workflows/native-extension-product-track.md`'));
  assert.ok(text.includes('Epic N8'));
});
