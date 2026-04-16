const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('README.md includes package.json bugs.url (task-n25-1)', () => {
  const url = packageJson.bugs && packageJson.bugs.url;
  assert.ok(url && typeof url === 'string', 'package.json should define bugs.url');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(url), 'README.md should document bugs.url for extension issues');
  assert.ok(readme.includes('task-n25-1'), 'README should tag bugs line for operator doc parity');
});
