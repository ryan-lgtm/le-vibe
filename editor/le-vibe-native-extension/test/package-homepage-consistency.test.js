const test = require('node:test');
const assert = require('node:assert/strict');
const packageJson = require('../package.json');

test('homepage path includes repository.directory; bugs host matches repo (task-n8-15)', () => {
  const { repository, homepage, bugs } = packageJson;
  assert.ok(homepage.includes(repository.directory), 'homepage should reference monorepo subdirectory');
  const repoUrl = new URL(repository.url);
  const bugsUrl = new URL(bugs.url);
  assert.equal(bugsUrl.hostname, repoUrl.hostname);
  assert.ok(bugsUrl.pathname.includes('issues') || bugsUrl.pathname.endsWith('/issues'));
});
