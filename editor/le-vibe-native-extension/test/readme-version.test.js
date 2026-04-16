const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const packageJson = require('../package.json');

test('README.md documents package.json version (task-n44-1)', () => {
  const version = packageJson.version;
  assert.ok(version && typeof version === 'string', 'package.json should define version');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(version), 'README.md should include package.json version');
  assert.ok(readme.includes('task-n44-1'), 'README should tag version line for doc parity');
});
