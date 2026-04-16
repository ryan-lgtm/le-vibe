const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('README.md includes package.json homepage (task-n26-1)', () => {
  const url = packageJson.homepage;
  assert.ok(url && typeof url === 'string', 'package.json should define homepage');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(url), 'README.md should document homepage for GitHub tree view');
  assert.ok(readme.includes('task-n26-1'), 'README should tag homepage line for doc parity');
});
