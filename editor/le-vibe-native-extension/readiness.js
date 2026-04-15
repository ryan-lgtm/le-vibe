'use strict';

const STARTUP_STATES = Object.freeze([
  'checking',
  'ready',
  'needs_ollama',
  'needs_model',
  'needs_auth_or_setup',
]);

const STATE_CONTENT = Object.freeze({
  checking: {
    title: 'Checking local runtime',
    detail: 'Running startup checks for local Lé Vibe prerequisites.',
    actions: [],
  },
  ready: {
    title: 'Ready',
    detail: 'Local startup checks passed. You can start an agent interaction.',
    actions: [],
  },
  needs_ollama: {
    title: 'Ollama is not reachable',
    detail: 'Lé Vibe needs local Ollama running on this machine before agent chat can start.',
    actions: [{ id: 'openOllamaSetupHelp', label: 'Open Ollama Setup Help' }],
  },
  needs_model: {
    title: 'No local model is available',
    detail: 'Install at least one local Ollama model to continue with local-first agent runs.',
    actions: [{ id: 'openModelPullHelp', label: 'Show Local Model Install Steps' }],
  },
  needs_auth_or_setup: {
    title: 'Workspace setup is required',
    detail: 'Complete workspace setup to enable deterministic agent startup behavior.',
    actions: [{ id: 'openWorkspaceSetup', label: 'Open Setup Workflow' }],
  },
});

function getConfiguredState(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  const configured = config.get('devStartupState', 'needs_auth_or_setup');
  return STARTUP_STATES.includes(configured) ? configured : 'needs_auth_or_setup';
}

function resolveStartupState(vscode) {
  return getConfiguredState(vscode);
}

function getStateContent(state) {
  return STATE_CONTENT[state] || STATE_CONTENT.needs_auth_or_setup;
}

module.exports = {
  STARTUP_STATES,
  STATE_CONTENT,
  resolveStartupState,
  getStateContent,
};
