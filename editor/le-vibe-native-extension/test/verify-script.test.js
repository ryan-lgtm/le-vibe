const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');

test('package.json defines verify script chaining test and smoke', () => {
  const verify = packageJson.scripts && packageJson.scripts.verify;
  assert.ok(typeof verify === 'string' && verify.length > 0);
  assert.ok(verify.includes('npm test'), verify);
  assert.ok(verify.includes('smoke'), verify);
});

test('package.json test script uses node:test with test/*.test.js glob (task-n8-58)', () => {
  const testScript = packageJson.scripts && packageJson.scripts.test;
  assert.equal(testScript, 'node --test ./test/*.test.js');
});

test('package.json smoke script points at smoke-integration.js (task-n8-59)', () => {
  const smoke = packageJson.scripts && packageJson.scripts.smoke;
  assert.equal(smoke, 'node ./scripts/smoke-integration.js');
});
