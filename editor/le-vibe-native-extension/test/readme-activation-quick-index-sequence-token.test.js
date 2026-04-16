const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

test('README.md quick index names activation docs sequence token (task-n66-1)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n66-1'));
  assert.ok(readme.includes('Activation docs quick index (task-n62-1'));
  assert.ok(readme.includes('Activation docs sequence (task-n60-1)'));
});
