const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('README.md documents package.json license SPDX string (task-n30-1)', () => {
  const license = packageJson.license;
  assert.ok(license && typeof license === 'string', 'package.json should define license');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(license), 'README.md should include package.json license string');
  assert.ok(readme.includes('task-n30-1'), 'README should tag license line for doc parity');
  assert.ok(readme.includes('SPDX'), 'README should note SPDX for license line');
});
