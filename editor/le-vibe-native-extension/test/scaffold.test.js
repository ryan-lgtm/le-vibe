const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

const packageJson = require('../package.json');
const extensionModule = require('../extension');

test('manifest contributes Lé Vibe Open Agent Surface command', () => {
  const commands = packageJson.contributes && packageJson.contributes.commands;
  assert.ok(Array.isArray(commands), 'contributes.commands must be an array');
  const command = commands.find((item) => item.command === 'leVibeNative.openAgentSurface');
  assert.ok(command, 'expected leVibeNative.openAgentSurface command contribution');
  assert.equal(command.title, 'Lé Vibe: Open Agent Surface');
});

test('manifest supports deterministic activation entrypoints', () => {
  const activationEvents = packageJson.activationEvents || [];
  assert.ok(
    activationEvents.includes('onCommand:leVibeNative.openAgentSurface'),
    'expected command activation event',
  );
  assert.ok(activationEvents.includes('onStartupFinished'), 'expected startup activation event');
});

test('extension exports activate/deactivate and command constant', () => {
  assert.equal(typeof extensionModule.activate, 'function');
  assert.equal(typeof extensionModule.deactivate, 'function');
  assert.equal(extensionModule.OPEN_AGENT_SURFACE_COMMAND, 'leVibeNative.openAgentSurface');
  assert.equal(path.basename(require.resolve('../extension')), 'extension.js');
});
