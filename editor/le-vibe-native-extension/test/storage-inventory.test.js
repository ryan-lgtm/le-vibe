const test = require('node:test');
const assert = require('node:assert/strict');

const { levibeNativeChatDir, PERSISTED_ARTIFACTS } = require('../storage-inventory');
const { transcriptDir } = require('../chat-transcript');
const { defaultStatePath: wizardStatePath } = require('../first-run-wizard');
const { handoffAuditPath } = require('../operator-handoff');
const {
  configDir: migrationConfigDir,
  defaultStatePath: migrationStatePath,
  migrationAuditPath,
} = require('../third-party-migration');
const { workspacePlanAuditPath } = require('../workspace-plan-exec');

test('levibeNativeChatDir matches all persisted path roots', () => {
  const root = levibeNativeChatDir();
  assert.equal(transcriptDir(), root);
  assert.equal(migrationConfigDir(), root);
  assert.ok(wizardStatePath().startsWith(root + '/') || wizardStatePath().startsWith(root + '\\'));
  assert.ok(handoffAuditPath().startsWith(root + '/') || handoffAuditPath().startsWith(root + '\\'));
  assert.ok(migrationStatePath().startsWith(root + '/') || migrationStatePath().startsWith(root + '\\'));
  assert.ok(migrationAuditPath().startsWith(root + '/') || migrationAuditPath().startsWith(root + '\\'));
  assert.ok(workspacePlanAuditPath().startsWith(root + '/') || workspacePlanAuditPath().startsWith(root + '\\'));
});

test('PERSISTED_ARTIFACTS has unique basenames (transcript glob allowed once)', () => {
  const names = PERSISTED_ARTIFACTS.map((a) => a.basename);
  const set = new Set(names);
  assert.equal(set.size, names.length);
});
