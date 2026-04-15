const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

/**
 * Documented Node minimum in README / OPERATOR must match engines.node (task-n8-21).
 */
test('README and OPERATOR include Node.js N+ from package.json engines.node', () => {
  const nodeEngine = packageJson.engines && packageJson.engines.node;
  assert.ok(typeof nodeEngine === 'string');
  const m = String(nodeEngine).match(/>=\s*(\d+)/);
  assert.ok(m, `engines.node must use >=N form for doc sync (got ${nodeEngine})`);
  const n = m[1];
  const expectedPhrase = `Node.js ${n}+`;

  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(
    operator.includes(expectedPhrase),
    `OPERATOR.md should document ${expectedPhrase} (from engines.node)`
  );
  assert.ok(
    readme.includes(expectedPhrase),
    `README.md should document ${expectedPhrase} (from engines.node)`
  );
});
