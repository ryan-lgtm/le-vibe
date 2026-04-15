'use strict';

const OPEN_AGENT_SURFACE_COMMAND = 'leVibeNative.openAgentSurface';

function openAgentSurface() {
  const vscode = require('vscode');
  return vscode.window.showInformationMessage(
    'Lé Vibe native agent surface scaffold is active. Readiness states arrive in task-n1-2.',
  );
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const vscode = require('vscode');
  const disposable = vscode.commands.registerCommand(OPEN_AGENT_SURFACE_COMMAND, openAgentSurface);
  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
  OPEN_AGENT_SURFACE_COMMAND,
};
