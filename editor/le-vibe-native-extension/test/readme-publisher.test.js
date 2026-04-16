const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('README.md documents package.json publisher (task-n32-1)', () => {
  const publisher = packageJson.publisher;
  assert.ok(publisher && typeof publisher === 'string', 'package.json should define publisher');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(publisher), 'README.md should include package.json publisher');
  assert.ok(readme.includes('task-n32-1'), 'README should tag publisher line for doc parity');
});
