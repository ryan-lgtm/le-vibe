const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const packageJson = require('../package.json');

test('package.json main points to existing extension entrypoint (task-n8-30)', () => {
  assert.equal(packageJson.main, './extension.js');
  const resolved = path.join(__dirname, '..', packageJson.main);
  assert.ok(fs.existsSync(resolved), `main file missing: ${packageJson.main}`);
  const stat = fs.statSync(resolved);
  assert.ok(stat.isFile());
});
