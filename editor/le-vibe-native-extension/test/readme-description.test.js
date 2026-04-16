const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('README.md documents package.json description (task-n40-1)', () => {
  const description = packageJson.description;
  assert.ok(description && typeof description === 'string', 'package.json should define description');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(description), 'README.md should include package.json description');
  assert.ok(readme.includes('task-n40-1'), 'README should tag description line for doc parity');
});
