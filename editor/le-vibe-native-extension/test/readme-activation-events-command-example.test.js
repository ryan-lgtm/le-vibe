const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const packageJson = require('../package.json');

test('README.md documents concrete activationEvents onCommand literal (task-n52-1)', () => {
  const activationEvents = packageJson.activationEvents;
  assert.ok(Array.isArray(activationEvents), 'package.json should define activationEvents array');

  const commandEventLiteral = activationEvents.find((entry) =>
    entry === 'onCommand:leVibeNative.openAgentSurface',
  );
  assert.ok(commandEventLiteral, 'activationEvents should include onCommand:leVibeNative.openAgentSurface');

  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n52-1'), 'README should tag activation event example line for doc parity');
  assert.ok(readme.includes('activationEvents'), 'README should mention activationEvents key');
  assert.ok(readme.includes(commandEventLiteral), 'README should include derived concrete onCommand literal');
});
