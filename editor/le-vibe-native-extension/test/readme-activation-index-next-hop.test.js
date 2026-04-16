const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

test('README.md links activation quick index to sequence breadcrumb (task-n64-1)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n64-1'));
  assert.ok(readme.includes('Activation docs quick index (task-n62-1)'));
  assert.ok(readme.includes('Activation docs sequence (task-n60-1)'));
});
