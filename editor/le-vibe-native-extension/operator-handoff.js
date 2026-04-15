'use strict';

const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

function handoffAuditPath() {
  return path.join(os.homedir(), '.config', 'le-vibe', 'levibe-native-chat', 'operator-handoff-audit.jsonl');
}

function buildOperatorHandoffEvent(payload) {
  return {
    contract_version: 'lvibe.operator_handoff.v1',
    event_type: 'operator_handoff',
    timestamp_iso: new Date().toISOString(),
    workspace_uri: payload.workspaceUri || 'no-workspace',
    startup_state: payload.startupState || 'checking',
    diagnostics: payload.diagnostics || {},
    ollama: {
      endpoint: payload.ollamaEndpoint || 'http://127.0.0.1:11434',
      model: payload.ollamaModel || 'mistral:latest',
    },
    context: {
      selected_paths: Array.isArray(payload.selectedContextPaths) ? payload.selectedContextPaths : [],
      budget: payload.contextBudget || {},
    },
    transcript: {
      path: payload.transcriptFile || '',
      caps: payload.transcriptCaps || {},
    },
    local_only: true,
  };
}

function appendOperatorHandoffAudit(filePath, event) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  const line = `${JSON.stringify(event)}\n`;
  fs.appendFileSync(filePath, line, 'utf8');
}

function loadAuditEvents(filePath) {
  if (!fs.existsSync(filePath)) {
    return [];
  }
  const text = fs.readFileSync(filePath, 'utf8');
  return text
    .split('\n')
    .filter((line) => line.trim())
    .map((line) => JSON.parse(line));
}

module.exports = {
  handoffAuditPath,
  buildOperatorHandoffEvent,
  appendOperatorHandoffAudit,
  loadAuditEvents,
};
