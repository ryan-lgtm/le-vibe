const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

test('README.md links activation event example to command table (task-n56-1)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n56-1'));
  assert.ok(readme.includes('Activation event example (task-n52-1)'));
  assert.ok(readme.includes('Command palette and keyboard shortcuts (task-n17-1)'));
});
