const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README.md Operator verification points to OPERATOR E2E checklist (task-n15-1)', () => {
  const text = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(text.includes('## Operator verification / ship checklist'));
  assert.ok(text.includes('task-n15-1'));
  assert.ok(text.includes('**`OPERATOR.md`**'));
  assert.ok(text.includes('E2E agentic editor release checklist'));
});
