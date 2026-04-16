const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const packageJson = require('../package.json');

test('README.md documents activationEvents count + startup literal (task-n50-1)', () => {
  const activationEvents = packageJson.activationEvents;
  assert.ok(Array.isArray(activationEvents), 'package.json should define activationEvents array');

  const startupEvent = 'onStartupFinished';
  assert.ok(activationEvents.includes(startupEvent), 'activationEvents should include onStartupFinished');

  const commandEvents = activationEvents.filter((entry) => entry.startsWith('onCommand:'));
  const totalCount = activationEvents.length;
  const commandCount = commandEvents.length;

  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('task-n50-1'), 'README should tag activationEvents line for doc parity');
  assert.ok(readme.includes('activationEvents'), 'README should mention activationEvents key');
  assert.ok(readme.includes(startupEvent), 'README should include startup event literal');
  assert.ok(readme.includes(`\`${totalCount}\``), 'README should include derived activationEvents count');
  assert.ok(readme.includes(`\`${commandCount}\``), 'README should include derived onCommand count');
});
