const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

test('README.md links activation docs sequence back to quick index (task-n68-1)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n68-1'));
  assert.ok(readme.includes('Activation docs sequence (task-n60-1)'));
  assert.ok(readme.includes('Activation docs quick index (task-n62-1)'));
});
