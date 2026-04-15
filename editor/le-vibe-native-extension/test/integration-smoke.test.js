const test = require('node:test');
const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const extRoot = path.join(__dirname, '..');

test('npm run smoke exits 0 (panel + launcher; Ollama non-strict)', () => {
  const r = spawnSync('npm', ['run', 'smoke', '--silent'], {
    cwd: extRoot,
    encoding: 'utf8',
    env: {
      ...process.env,
      // CI / dev machines often have no local Ollama — same default as smoke script
      LEVIBE_NATIVE_SMOKE_STRICT_OLLAMA: '0',
    },
  });
  assert.equal(r.status, 0, `stderr: ${r.stderr}\nstdout: ${r.stdout}`);
  assert.ok(
    r.stdout.includes('non-blank checks OK') || r.stdout.includes('smoke: done'),
    r.stdout,
  );
  assert.ok(
    r.stdout.includes('first-party persisted config dir:'),
    `expected storage-inventory log line in smoke stdout: ${r.stdout}`,
  );
});
