const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('extension README documents Node prerequisite for verify (task-n8-13)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('Prerequisites (developers)'));
  assert.ok(readme.includes('18') && readme.includes('npm run verify'));
  assert.ok(readme.includes('engines.node'));
});

test('extension README documents vscode engine prerequisite aligned with package.json (task-n8-18)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('engines.vscode'));
  assert.ok(readme.includes('1.85'));
  assert.ok(readme.includes('VSCodium'));
});
