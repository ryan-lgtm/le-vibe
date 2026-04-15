const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README documents package.json main / extension.js for packaging (task-n8-32)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('Extension entry (packaging)'));
  assert.ok(readme.includes('./extension.js'));
  assert.ok(readme.includes('OPERATOR.md'));
  assert.ok(readme.includes('main'));
});
