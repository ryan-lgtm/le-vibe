const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

test('README.md links activationEvents count breakdown to startup rationale (task-n58-1)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n58-1'));
  assert.ok(readme.includes('Activation events (task-n50-1)'));
  assert.ok(readme.includes('Startup activation intent (task-n54-1)'));
});
