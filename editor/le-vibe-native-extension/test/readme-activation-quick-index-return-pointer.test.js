const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

test('README.md quick index references activation sequence return hop (task-n70-1)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n70-1'));
  assert.ok(readme.includes('Activation docs quick index (task-n62-1'));
  assert.ok(readme.includes('Activation sequence return hop (task-n68-1)'));
});
