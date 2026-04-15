'use strict';

const OPEN_AGENT_SURFACE_COMMAND = 'leVibeNative.openAgentSurface';
const OPEN_OLLAMA_SETUP_HELP_COMMAND = 'leVibeNative.openOllamaSetupHelp';
const OPEN_MODEL_PULL_HELP_COMMAND = 'leVibeNative.openModelPullHelp';
const OPEN_WORKSPACE_SETUP_COMMAND = 'leVibeNative.openWorkspaceSetup';

const { STARTUP_STATES, resolveStartupState, getStateContent } = require('./readiness');

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function panelHtml(state) {
  const content = getStateContent(state);
  const actionButtons = content.actions
    .map((action) => `<button data-action="${escapeHtml(action.id)}">${escapeHtml(action.label)}</button>`)
    .join('');
  const actionsBlock = actionButtons || '<p class="muted">No actions required.</p>';
  const states = STARTUP_STATES.map((value) => {
    const active = value === state ? 'class="active"' : '';
    return `<li ${active}>${escapeHtml(value)}</li>`;
  }).join('');
  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <style>
    body { font-family: var(--vscode-font-family); color: var(--vscode-foreground); padding: 1rem 1.25rem; line-height: 1.45; font-size: 13px; }
    h2 { margin-bottom: 0.35rem; }
    .state { margin: 0.5rem 0 0.75rem 0; }
    .muted { opacity: 0.8; }
    .pill-list { display: flex; flex-wrap: wrap; gap: 0.35rem; list-style: none; padding: 0; margin: 0.25rem 0 1rem 0; }
    .pill-list li { border: 1px solid var(--vscode-panel-border); border-radius: 999px; padding: 0.15rem 0.55rem; }
    .pill-list li.active { border-color: var(--vscode-focusBorder); }
    button { margin-right: 0.5rem; margin-top: 0.5rem; padding: 0.35rem 0.75rem; cursor: pointer; }
  </style>
</head>
<body>
  <h2>Lé Vibe Native Startup</h2>
  <p class="muted">Deterministic readiness state with local-first remediation actions.</p>
  <ul class="pill-list">${states}</ul>
  <div class="state"><strong>${escapeHtml(state)}</strong></div>
  <p>${escapeHtml(content.detail)}</p>
  <div>${actionsBlock}</div>
  <script>
    const vscode = acquireVsCodeApi();
    document.querySelectorAll('button[data-action]').forEach((button) => {
      button.addEventListener('click', () => {
        vscode.postMessage({ type: 'action', actionId: button.getAttribute('data-action') });
      });
    });
  </script>
</body>
</html>`;
}

function openAgentSurface() {
  const vscode = require('vscode');
  const state = resolveStartupState(vscode);
  const panel = vscode.window.createWebviewPanel(
    'leVibeNativeReadiness',
    'Lé Vibe Native Readiness',
    vscode.ViewColumn.Active,
    { enableScripts: true, retainContextWhenHidden: true },
  );
  panel.webview.html = panelHtml(state);
  panel.webview.onDidReceiveMessage((msg) => {
    if (!msg || msg.type !== 'action') {
      return;
    }
    if (msg.actionId === 'openOllamaSetupHelp') {
      void vscode.commands.executeCommand(OPEN_OLLAMA_SETUP_HELP_COMMAND);
      return;
    }
    if (msg.actionId === 'openModelPullHelp') {
      void vscode.commands.executeCommand(OPEN_MODEL_PULL_HELP_COMMAND);
      return;
    }
    if (msg.actionId === 'openWorkspaceSetup') {
      void vscode.commands.executeCommand(OPEN_WORKSPACE_SETUP_COMMAND);
    }
  });
  return panel;
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const vscode = require('vscode');
  context.subscriptions.push(
    vscode.commands.registerCommand(OPEN_AGENT_SURFACE_COMMAND, openAgentSurface),
    vscode.commands.registerCommand(OPEN_OLLAMA_SETUP_HELP_COMMAND, () =>
      vscode.env.openExternal(vscode.Uri.parse('https://ollama.com/download/linux')),
    ),
    vscode.commands.registerCommand(OPEN_MODEL_PULL_HELP_COMMAND, () =>
      vscode.window.showInformationMessage('Run `ollama pull mistral:latest` to install a local model.'),
    ),
    vscode.commands.registerCommand(OPEN_WORKSPACE_SETUP_COMMAND, async () => {
      const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
      if (!folder) {
        await vscode.window.showWarningMessage('Open a folder workspace first.');
        return;
      }
      const workflowUri = vscode.Uri.joinPath(folder.uri, '.lvibe', 'workflows', 'setup-workspace.md');
      try {
        await vscode.workspace.fs.stat(workflowUri);
        await vscode.window.showTextDocument(workflowUri);
      } catch {
        await vscode.window.showInformationMessage(
          'setup-workspace.md not found. Prepare the workspace to generate it.',
        );
      }
    }),
  );

  const config = vscode.workspace.getConfiguration('leVibeNative');
  if (config.get('openPanelOnStartup', true)) {
    setTimeout(() => {
      void vscode.commands.executeCommand(OPEN_AGENT_SURFACE_COMMAND);
    }, 0);
  }
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
  OPEN_AGENT_SURFACE_COMMAND,
  OPEN_OLLAMA_SETUP_HELP_COMMAND,
  OPEN_MODEL_PULL_HELP_COMMAND,
  OPEN_WORKSPACE_SETUP_COMMAND,
  panelHtml,
};
