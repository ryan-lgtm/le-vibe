const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');

test('package.json repository points at monorepo subdirectory', () => {
  assert.ok(packageJson.repository);
  assert.equal(packageJson.repository.type, 'git');
  assert.ok(typeof packageJson.repository.url === 'string' && packageJson.repository.url.includes('github.com'));
  assert.equal(packageJson.repository.directory, 'editor/le-vibe-native-extension');
});

test('package.json homepage, bugs, and keywords for discovery (task-n8-12)', () => {
  assert.ok(packageJson.homepage && packageJson.homepage.includes('editor/le-vibe-native-extension'));
  assert.ok(packageJson.bugs && packageJson.bugs.url && packageJson.bugs.url.includes('github.com'));
  assert.ok(Array.isArray(packageJson.keywords) && packageJson.keywords.includes('levibe'));
});
