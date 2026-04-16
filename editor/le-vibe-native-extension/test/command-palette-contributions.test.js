const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('path');
const packageJson = require('../package.json');

test('every contributed command uses Lé Vibe Chat category + short title (task-n17-1)', () => {
  const commands = packageJson.contributes && packageJson.contributes.commands;
  assert.ok(Array.isArray(commands));
  for (const c of commands) {
    assert.equal(c.category, 'Lé Vibe Chat', `command ${c.command} category`);
    assert.ok(typeof c.title === 'string' && c.title.length > 0, `command ${c.command} title`);
    assert.ok(
      !c.title.includes('Lé Vibe Chat:'),
      `command ${c.command} title should not duplicate palette prefix (use short title only)`,
    );
    assert.ok(c.command && c.command.startsWith('leVibeNative.'), `command ${c.command} id`);
  }
});

test('README palette table lists every command id and palette label (task-n17-1)', () => {
  const readme = fs.readFileSync(path.join(__dirname, '..', 'README.md'), 'utf8');
  assert.ok(readme.includes('## Command palette and keyboard shortcuts (task-n17-1)'));
  const commands = packageJson.contributes.commands;
  for (const c of commands) {
    const label = `${c.category}: ${c.title}`;
    assert.ok(readme.includes(`\`${c.command}\``), `README table should mention ${c.command}`);
    assert.ok(readme.includes(label), `README table should include palette label "${label}"`);
  }
});
