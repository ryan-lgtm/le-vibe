'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { levibeNativeChatDir } = require('./storage-inventory');

function workspaceFsOpsAuditPath() {
  return path.join(levibeNativeChatDir(), 'workspace-fs-ops-audit.jsonl');
}

/**
 * @param {{
 *   op: 'delete',
 *   workspaceUri: string,
 *   relativePath: string,
 *   targetUri: string,
 *   outcome: 'success' | 'failed',
 *   detail?: string,
 *   isDirectory?: boolean,
 * }} fields
 */
function buildWorkspaceFsOpsAuditEvent(fields) {
  return {
    contract_version: 'lvibe.workspace_fs_ops_audit.v1',
    timestamp_iso: new Date().toISOString(),
    op: fields.op,
    workspace_uri: fields.workspaceUri,
    relative_path: fields.relativePath,
    target_uri: fields.targetUri,
    outcome: fields.outcome,
    ...(fields.detail ? { detail: fields.detail } : {}),
    ...(typeof fields.isDirectory === 'boolean' ? { is_directory: fields.isDirectory } : {}),
  };
}

function appendWorkspaceFsOpsAudit(filePath, event) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(filePath, `${JSON.stringify(event)}\n`, 'utf8');
}

module.exports = {
  workspaceFsOpsAuditPath,
  buildWorkspaceFsOpsAuditEvent,
  appendWorkspaceFsOpsAudit,
};
