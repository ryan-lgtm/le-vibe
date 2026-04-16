const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('README.md documents package.json repository url + directory (task-n28-1)', () => {
  const repo = packageJson.repository;
  assert.ok(repo && typeof repo === 'object', 'package.json should define repository');
  assert.equal(repo.type, 'git');
  assert.ok(repo.url && typeof repo.url === 'string', 'repository.url');
  assert.ok(repo.directory && typeof repo.directory === 'string', 'repository.directory');
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes(repo.url), 'README.md should include repository.url');
  assert.ok(readme.includes(repo.directory), 'README.md should include repository.directory');
  assert.ok(readme.includes('task-n28-1'), 'README should tag repository line for doc parity');
});
