const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  buildOperatorHandoffEvent,
  appendOperatorHandoffAudit,
  loadAuditEvents,
} = require('../operator-handoff');

test('handoff event contract is reproducible and versioned', () => {
  const event = buildOperatorHandoffEvent({
    workspaceUri: 'file:///workspace/demo',
    startupState: 'ready',
    diagnostics: { modelCount: 1 },
    ollamaEndpoint: 'http://127.0.0.1:11435',
    ollamaModel: 'mistral:latest',
    selectedContextPaths: ['README.md'],
    contextBudget: { maxFiles: 4 },
    transcriptFile: '/tmp/transcript.jsonl',
    transcriptCaps: { maxBytes: 1000 },
  });
  assert.equal(event.contract_version, 'lvibe.operator_handoff.v1');
  assert.equal(event.event_type, 'operator_handoff');
  assert.equal(event.workspace_uri, 'file:///workspace/demo');
  assert.deepEqual(event.context.selected_paths, ['README.md']);
  assert.equal(event.local_only, true);
});

test('handoff audit appends JSONL entries locally', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-handoff-'));
  const file = path.join(dir, 'audit.jsonl');
  const event = buildOperatorHandoffEvent({ workspaceUri: 'file:///workspace/demo' });
  appendOperatorHandoffAudit(file, event);
  const all = loadAuditEvents(file);
  assert.equal(all.length, 1);
  assert.equal(all[0].event_type, 'operator_handoff');
});
