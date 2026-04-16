const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const packageJson = require('../package.json');

test('README.md explains onStartupFinished activation intent (task-n54-1)', () => {
  const activationEvents = packageJson.activationEvents;
  assert.ok(Array.isArray(activationEvents), 'package.json should define activationEvents array');

  const startupLiteral = activationEvents.find((entry) => entry === 'onStartupFinished');
  assert.ok(startupLiteral, 'activationEvents should include onStartupFinished');

  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n54-1'), 'README should tag startup intent line for doc parity');
  assert.ok(readme.includes(startupLiteral), 'README should include derived startup activation literal');
  assert.ok(readme.includes('deterministic'), 'README should explain deterministic startup intent');
});
