const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('OPERATOR and README share extension entry stem for ./extension.js (task-n8-33)', () => {
  const shared = '**`./extension.js`** (VS Code activation entry;';
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(operator.includes(shared));
  assert.ok(readme.includes(shared));
});
