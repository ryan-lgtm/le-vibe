'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  ORCHESTRATOR_EVENT_CONTRACT,
  buildOrchestratorEvent,
  appendOrchestratorEvent,
  orchestratorEventAuditPath,
} = require('../orchestrator-events');

test('buildOrchestratorEvent uses stable v1 envelope', () => {
  const ev = buildOrchestratorEvent('chat_turn', 'file:///tmp/ws', { outcome: 'completed' });
  assert.equal(ev.contract_version, ORCHESTRATOR_EVENT_CONTRACT);
  assert.equal(ev.event_type, 'chat_turn');
  assert.equal(ev.workspace_uri, 'file:///tmp/ws');
  assert.equal(ev.local_only, true);
  assert.equal(ev.payload.outcome, 'completed');
  assert.ok(typeof ev.timestamp_iso === 'string');
});

test('appendOrchestratorEvent writes jsonl line', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'levibe-orch-'));
  const file = path.join(dir, 'orchestrator-events.jsonl');
  appendOrchestratorEvent(file, buildOrchestratorEvent('plan_run', 'no-workspace', { phase: 'started' }));
  const lines = fs.readFileSync(file, 'utf8').trim().split('\n');
  assert.equal(lines.length, 1);
  const row = JSON.parse(lines[0]);
  assert.equal(row.event_type, 'plan_run');
  assert.equal(row.payload.phase, 'started');
});

test('orchestratorEventAuditPath uses canonical levibe-native-chat dir', () => {
  const p = orchestratorEventAuditPath();
  assert.ok(p.endsWith('orchestrator-events.jsonl'));
  assert.ok(p.includes('levibe-native-chat'));
});
