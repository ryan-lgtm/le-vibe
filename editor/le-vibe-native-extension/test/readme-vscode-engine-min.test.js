const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const packageJson = require('../package.json');

test('README.md documents engines.vscode minimum major.minor (task-n46-1)', () => {
  const range = packageJson.engines && packageJson.engines.vscode;
  assert.ok(typeof range === 'string' && range.length > 0, 'package.json should define engines.vscode');
  const match = range.match(/(\d+)\.(\d+)/);
  assert.ok(match, `engines.vscode should include major.minor, got: ${range}`);
  const majorMinor = `${match[1]}.${match[2]}`;
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(range), 'README.md should include engines.vscode literal range');
  assert.ok(readme.includes(`${majorMinor}+`), 'README.md should include major.minor+ floor');
  assert.ok(readme.includes('task-n46-1'), 'README should tag engines.vscode line for doc parity');
});
