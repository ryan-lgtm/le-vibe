const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');

test('package.json defines verify script chaining test and smoke', () => {
  const verify = packageJson.scripts && packageJson.scripts.verify;
  assert.ok(typeof verify === 'string' && verify.length > 0);
  assert.ok(verify.includes('npm test'), verify);
  assert.ok(verify.includes('smoke'), verify);
});
