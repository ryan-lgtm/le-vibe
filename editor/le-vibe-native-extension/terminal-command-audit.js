'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { levibeNativeChatDir } = require('./storage-inventory');

function terminalCommandAuditPath() {
  return path.join(levibeNativeChatDir(), 'terminal-command-audit.jsonl');
}

/**
 * @param {{
 *   auditId: string,
 *   workspaceUri: string | null,
 *   cwd: string | null,
 *   commandLine: string,
 * }} fields
 */
function buildTerminalCommandAuditSent(fields) {
  return {
    contract_version: 'lvibe.terminal_command_audit.v1',
    phase: 'sent',
    timestamp_iso: new Date().toISOString(),
    audit_id: fields.auditId,
    workspace_uri: fields.workspaceUri,
    cwd: fields.cwd,
    command_line: fields.commandLine,
    exit_code: null,
    exit_observation: 'pending_shell_integration_or_unavailable',
  };
}

/**
 * @param {{
 *   auditId: string,
 *   exitCode: number | undefined | null,
 * }} fields
 */
function buildTerminalCommandAuditEnded(fields) {
  const code = fields.exitCode;
  return {
    contract_version: 'lvibe.terminal_command_audit.v1',
    phase: 'shell_ended',
    timestamp_iso: new Date().toISOString(),
    audit_id: fields.auditId,
    exit_code: code === undefined || code === null ? null : code,
  };
}

function appendTerminalCommandAudit(filePath, event) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(filePath, `${JSON.stringify(event)}\n`, 'utf8');
}

module.exports = {
  terminalCommandAuditPath,
  buildTerminalCommandAuditSent,
  buildTerminalCommandAuditEnded,
  appendTerminalCommandAudit,
};
