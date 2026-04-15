const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');

test('README documents telemetry as local structured logs with explicit opt-in (task-n8-26)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('Telemetry'));
  assert.ok(readme.includes('local structured logs'));
  assert.ok(readme.includes('explicitly opt in'));
  assert.ok(readme.includes('OPERATOR.md'));
});

test('README and OPERATOR share telemetry defaults phrasing', () => {
  const shared = 'defaults to **local structured logs only**';
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  const operator = fs.readFileSync(path.join(__dirname, '..', 'OPERATOR.md'), 'utf8');
  assert.ok(readme.includes(shared));
  assert.ok(operator.includes(shared));
});
