const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  SCHEMA,
  matchWatchlist,
  buildMigrationGuideMarkdown,
  loadMigrationState,
  saveMigrationState,
  appendMigrationAudit,
  EXTENSION_WATCHLIST,
} = require('../third-party-migration');

test('EXTENSION_WATCHLIST has stable ids', () => {
  assert.ok(EXTENSION_WATCHLIST.length >= 2);
  assert.ok(EXTENSION_WATCHLIST.every((e) => e.id && e.label));
});

test('matchWatchlist returns deterministic matches', () => {
  const ids = ['Continue.continue', 'foo.bar'];
  const m = matchWatchlist(ids);
  assert.equal(m.length, 1);
  assert.equal(m[0].id, 'Continue.continue');
});

test('buildMigrationGuideMarkdown lists detected extensions', () => {
  const md = buildMigrationGuideMarkdown([
    { id: 'Continue.continue', label: 'Continue', isActive: true },
  ]);
  assert.ok(md.includes('Continue'));
  assert.ok(md.includes('Continue.continue'));
  assert.ok(md.includes('Guardrails'));
  assert.ok(md.includes('Remediation steps'));
});

test('migration state save and audit append round-trip', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-mig-'));
  const stateFile = path.join(dir, 'state.json');
  const auditFile = path.join(dir, 'audit.jsonl');
  const saved = saveMigrationState(
    { status: 'remediated', lastDetectedIds: ['Continue.continue'], updatedAt: '2026-01-01T00:00:00.000Z' },
    stateFile,
  );
  assert.equal(saved.status, 'remediated');
  assert.equal(saved.schema, SCHEMA);
  appendMigrationAudit(auditFile, { action: 'test', detectedIds: [] });
  const loaded = loadMigrationState(stateFile);
  assert.equal(loaded.status, 'remediated');
  const auditLines = fs.readFileSync(auditFile, 'utf8').trim().split('\n');
  assert.equal(auditLines.length, 1);
  const row = JSON.parse(auditLines[0]);
  assert.equal(row.action, 'test');
  assert.ok(row.ts);
});
