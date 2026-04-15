const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');

test('package.json declares Node engine for test/verify scripts (task-n8-11)', () => {
  assert.ok(packageJson.engines);
  assert.ok(packageJson.engines.node, 'engines.node documents minimum for npm test / verify');
  assert.match(packageJson.engines.node, />=\s*18|^\^|>=/);
  assert.ok(packageJson.engines.vscode, 'vscode engine unchanged');
});
