const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const packageJson = require('../package.json');

test('README.md documents engines.node minimum major (task-n48-1)', () => {
  const engineNode = packageJson.engines && packageJson.engines.node;
  assert.ok(engineNode && typeof engineNode === 'string', 'package.json should define engines.node');

  const majorMatch = engineNode.match(/(\d+)/);
  assert.ok(majorMatch, 'engines.node should include a numeric major');
  const major = majorMatch[1];

  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n48-1'), 'README should tag engines.node line for doc parity');
  assert.ok(readme.includes('engines.node'), 'README should mention engines.node key');
  assert.ok(readme.includes(engineNode), 'README should include literal engines.node value');
  assert.ok(readme.includes(`${major}+`), 'README should include derived Node.js major floor');
});
