const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');

test('package.json repository points at monorepo subdirectory', () => {
  assert.ok(packageJson.repository);
  assert.equal(packageJson.repository.type, 'git');
  assert.ok(typeof packageJson.repository.url === 'string' && packageJson.repository.url.includes('github.com'));
  assert.equal(packageJson.repository.directory, 'editor/le-vibe-native-extension');
});
