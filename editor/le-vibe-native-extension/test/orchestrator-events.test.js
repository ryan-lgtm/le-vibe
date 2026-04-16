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
  readRecentOrchestratorEvents,
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

test('readRecentOrchestratorEvents filters by workspace and limit', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'levibe-orch-'));
  const file = path.join(dir, 'orchestrator-events.jsonl');
  appendOrchestratorEvent(file, buildOrchestratorEvent('chat_turn', 'file:///ws-a', { idx: 1 }));
  appendOrchestratorEvent(file, buildOrchestratorEvent('chat_turn', 'file:///ws-b', { idx: 2 }));
  appendOrchestratorEvent(file, buildOrchestratorEvent('plan_run', 'file:///ws-a', { idx: 3 }));
  const rows = readRecentOrchestratorEvents(file, { workspaceUri: 'file:///ws-a', limit: 1 });
  assert.equal(rows.length, 1);
  assert.equal(rows[0].workspace_uri, 'file:///ws-a');
  assert.equal(rows[0].event_type, 'plan_run');
});
