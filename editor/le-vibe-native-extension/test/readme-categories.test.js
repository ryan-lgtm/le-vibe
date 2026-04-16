const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('README.md lists every package.json categories[] entry (task-n36-1)', () => {
  const categories = packageJson.categories;
  assert.ok(Array.isArray(categories) && categories.length > 0, 'package.json should define categories array');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const c of categories) {
    assert.ok(typeof c === 'string' && c.length > 0, `invalid categories entry: ${c}`);
    assert.ok(readme.includes(c), `README.md should document category: ${c}`);
  }
  assert.ok(readme.includes('task-n36-1'), 'README should tag categories line for doc parity');
});
