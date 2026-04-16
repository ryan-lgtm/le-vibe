'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  buildWorkspaceFsOpsAuditEvent,
  appendWorkspaceFsOpsAudit,
} = require('../workspace-fs-ops-audit.js');

test('buildWorkspaceFsOpsAuditEvent matches lvibe.workspace_fs_ops_audit.v1 (task-n11-3)', () => {
  const ev = buildWorkspaceFsOpsAuditEvent({
    op: 'delete',
    workspaceUri: 'file:///proj/',
    relativePath: 'tmp/x.txt',
    targetUri: 'file:///proj/tmp/x.txt',
    outcome: 'success',
    isDirectory: false,
  });
  assert.equal(ev.contract_version, 'lvibe.workspace_fs_ops_audit.v1');
  assert.equal(ev.op, 'delete');
  assert.equal(ev.outcome, 'success');
  assert.equal(ev.is_directory, false);
  assert.ok(ev.timestamp_iso);
});

test('appendWorkspaceFsOpsAudit writes JSONL line (task-n11-3)', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-fs-audit-'));
  const file = path.join(dir, 'workspace-fs-ops-audit.jsonl');
  const ev = buildWorkspaceFsOpsAuditEvent({
    op: 'delete',
    workspaceUri: 'file:///w/',
    relativePath: 'a',
    targetUri: 'file:///w/a',
    outcome: 'failed',
    detail: 'test detail',
  });
  appendWorkspaceFsOpsAudit(file, ev);
  const line = fs.readFileSync(file, 'utf8').trim();
  const parsed = JSON.parse(line);
  assert.equal(parsed.outcome, 'failed');
  assert.equal(parsed.detail, 'test detail');
});
