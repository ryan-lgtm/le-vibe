const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const packageJson = require('../package.json');

test('README.md documents package.json displayName (task-n38-1)', () => {
  const displayName = packageJson.displayName;
  assert.ok(displayName && typeof displayName === 'string', 'package.json should define displayName');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(displayName), 'README.md should include package.json displayName');
  assert.ok(readme.includes('task-n38-1'), 'README should tag displayName line for doc parity');
});
