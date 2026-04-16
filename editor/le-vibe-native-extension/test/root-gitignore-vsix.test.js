const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('monorepo root .gitignore ignores *.vsix (task-n16-2)', () => {
  const gitignore = path.join(__dirname, '..', '..', '..', '.gitignore');
  assert.ok(fs.existsSync(gitignore), 'expected repo root .gitignore');
  const text = fs.readFileSync(gitignore, 'utf8');
  assert.ok(text.includes('*.vsix'), 'root .gitignore should ignore packaged VSIX files');
});
