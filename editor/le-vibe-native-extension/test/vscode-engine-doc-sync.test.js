const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

/**
 * Documented VS Code minimum in README / OPERATOR must match engines.vscode (task-n8-20).
 */
test('README and OPERATOR include major.minor from package.json engines.vscode', () => {
  const vscodeEngine = packageJson.engines && packageJson.engines.vscode;
  assert.ok(typeof vscodeEngine === 'string');
  const m = vscodeEngine.match(/^\^(\d+)\.(\d+)\.\d+$/);
  assert.ok(m, `engines.vscode must use ^major.minor.patch (got ${vscodeEngine})`);
  const docVersion = `${m[1]}.${m[2]}`;

  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(
    operator.includes(docVersion),
    `OPERATOR.md should mention VS Code API minimum ${docVersion} (from engines.vscode)`
  );
  assert.ok(
    readme.includes(docVersion),
    `README.md should mention VS Code API minimum ${docVersion} (from engines.vscode)`
  );
});
