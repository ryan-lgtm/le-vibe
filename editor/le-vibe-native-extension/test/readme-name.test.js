const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const packageJson = require('../package.json');

test('README.md documents package.json name (task-n42-1)', () => {
  const packageName = packageJson.name;
  assert.ok(packageName && typeof packageName === 'string', 'package.json should define name');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(packageName), 'README.md should include package.json name');
  assert.ok(readme.includes('task-n42-1'), 'README should tag name line for doc parity');
});
