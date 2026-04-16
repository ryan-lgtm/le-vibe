const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

test('README.md includes activation docs sequence breadcrumb (task-n60-1)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n60-1'));
  assert.ok(readme.includes('Activation events (task-n50-1)'));
  assert.ok(readme.includes('Activation event example (task-n52-1)'));
  assert.ok(readme.includes('Activation example lookup (task-n56-1)'));
});
