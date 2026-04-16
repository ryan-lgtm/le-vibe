'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { levibeNativeChatDir } = require('./storage-inventory');

const ORCHESTRATOR_EVENT_CONTRACT = 'lvibe.orchestrator_event.v1';

function orchestratorEventAuditPath() {
  return path.join(levibeNativeChatDir(), 'orchestrator-events.jsonl');
}

/**
 * @param {'chat_turn'|'edit_apply'|'plan_run'|'terminal_exec'} eventType
 * @param {string} workspaceUri
 * @param {object} payload
 */
function buildOrchestratorEvent(eventType, workspaceUri, payload) {
  return {
    contract_version: ORCHESTRATOR_EVENT_CONTRACT,
    event_type: eventType,
    timestamp_iso: new Date().toISOString(),
    workspace_uri: workspaceUri || 'no-workspace',
    local_only: true,
    payload: payload || {},
  };
}

/**
 * @param {string} filePath
 * @param {object} event
 */
function appendOrchestratorEvent(filePath, event) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(filePath, `${JSON.stringify(event)}\n`, 'utf8');
}

module.exports = {
  ORCHESTRATOR_EVENT_CONTRACT,
  orchestratorEventAuditPath,
  buildOrchestratorEvent,
  appendOrchestratorEvent,
};
