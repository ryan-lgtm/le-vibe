const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');

test('package.json verify script chains npm test then npm run smoke (task-n8-60)', () => {
  const verify = packageJson.scripts && packageJson.scripts.verify;
  assert.equal(verify, 'npm test && npm run smoke');
});

test('package.json test script uses node:test with test/*.test.js glob (task-n8-58)', () => {
  const testScript = packageJson.scripts && packageJson.scripts.test;
  assert.equal(testScript, 'node --test ./test/*.test.js');
});

test('package.json smoke script points at smoke-integration.js (task-n8-59)', () => {
  const smoke = packageJson.scripts && packageJson.scripts.smoke;
  assert.equal(smoke, 'node ./scripts/smoke-integration.js');
});
