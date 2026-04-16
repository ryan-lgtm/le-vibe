const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('README.md lists every package.json keywords[] entry (task-n34-1)', () => {
  const keywords = packageJson.keywords;
  assert.ok(Array.isArray(keywords) && keywords.length > 0, 'package.json should define keywords array');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  for (const kw of keywords) {
    assert.ok(typeof kw === 'string' && kw.length > 0, `invalid keyword entry: ${kw}`);
    assert.ok(readme.includes(kw), `README.md should document keyword: ${kw}`);
  }
  assert.ok(readme.includes('task-n34-1'), 'README should tag keywords line for doc parity');
});
