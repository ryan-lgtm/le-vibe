const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('.vscodeignore does not exclude CHANGELOG.md (task-n22-1)', () => {
  const p = path.join(__dirname, '..', '.vscodeignore');
  const text = fs.readFileSync(p, 'utf8');
  const lines = text.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
  const excludesChangelog = lines.some(
    (line) => line === 'CHANGELOG.md' || line.endsWith('/CHANGELOG.md'),
  );
  assert.ok(!excludesChangelog, '.vscodeignore must not list CHANGELOG.md so it ships in the VSIX');
});
