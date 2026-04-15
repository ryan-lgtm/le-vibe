'use strict';

const OPEN_AGENT_SURFACE_COMMAND = 'leVibeNative.openAgentSurface';
const OPEN_OLLAMA_SETUP_HELP_COMMAND = 'leVibeNative.openOllamaSetupHelp';
const OPEN_MODEL_PULL_HELP_COMMAND = 'leVibeNative.openModelPullHelp';
const OPEN_WORKSPACE_SETUP_COMMAND = 'leVibeNative.openWorkspaceSetup';

const { STARTUP_STATES, resolveStartupSnapshot, getStateContent } = require('./readiness');
const { createOllamaClient } = require('./ollama');
const { createChatController } = require('./chat');

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function panelHtml(state, detailOverride, diagnostics) {
  const content = getStateContent(state, detailOverride);
  const actionButtons = content.actions
    .map((action) => `<button data-action="${escapeHtml(action.id)}">${escapeHtml(action.label)}</button>`)
    .join('');
  const actionsBlock = actionButtons || '<p class="muted">No actions required.</p>';
  const diagnosticsText = diagnostics ? `<pre class="diag">${escapeHtml(JSON.stringify(diagnostics, null, 2))}</pre>` : '';
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
    textarea { width: 100%; box-sizing: border-box; margin-top: 0.5rem; margin-bottom: 0.5rem; min-height: 74px; }
    .chat-log { margin-top: 0.75rem; border: 1px solid var(--vscode-panel-border); border-radius: 6px; padding: 0.6rem; min-height: 80px; white-space: pre-wrap; word-break: break-word; }
    .diag { margin-top: 0.75rem; background: var(--vscode-textCodeBlock-background); padding: 0.6rem; border-radius: 6px; white-space: pre-wrap; word-break: break-word; }
  </style>
</head>
<body>
  <h2>Lé Vibe Native Startup</h2>
  <p class="muted">Deterministic readiness state with local-first remediation actions.</p>
  <ul class="pill-list">${states}</ul>
  <div class="state"><strong>${escapeHtml(state)}</strong></div>
  <p>${escapeHtml(content.detail)}</p>
  <div>${actionsBlock}</div>
  <h3>Local prompt test</h3>
  <p class="muted">Send a prompt to local Ollama and receive streaming tokens.</p>
  <textarea id="promptInput" placeholder="Ask local model something..."></textarea>
  <div>
    <button id="sendPrompt">Send Prompt</button>
    <button id="cancelPrompt">Cancel Request</button>
  </div>
  <div id="chatStatus" class="muted">Idle.</div>
  <div id="chatLog" class="chat-log"></div>
  ${diagnosticsText}
  <script>
    const vscode = acquireVsCodeApi();
    document.querySelectorAll('button[data-action]').forEach((button) => {
      button.addEventListener('click', () => {
        vscode.postMessage({ type: 'action', actionId: button.getAttribute('data-action') });
      });
    });
    document.getElementById('sendPrompt').addEventListener('click', () => {
      const prompt = document.getElementById('promptInput').value || '';
      vscode.postMessage({ type: 'chat', actionId: 'sendPrompt', prompt });
    });
    document.getElementById('cancelPrompt').addEventListener('click', () => {
      vscode.postMessage({ type: 'chat', actionId: 'cancelPrompt' });
    });
    window.addEventListener('message', (event) => {
      const msg = event.data;
      if (!msg || msg.type !== 'chatUpdate') {
        return;
      }
      const status = document.getElementById('chatStatus');
      const log = document.getElementById('chatLog');
      if (msg.status) {
        status.textContent = msg.status;
      }
      if (typeof msg.replaceLog === 'string') {
        log.textContent = msg.replaceLog;
      } else if (typeof msg.append === 'string') {
        log.textContent += msg.append;
      }
    });
  </script>
</body>
</html>`;
}

function openAgentSurface() {
  const vscode = require('vscode');
  const config = vscode.workspace.getConfiguration('leVibeNative');
  const client = createOllamaClient({
    endpoint: config.get('ollamaEndpoint', 'http://127.0.0.1:11434'),
    timeoutMs: config.get('ollamaTimeoutMs', 2500),
    model: config.get('ollamaModel', 'mistral:latest'),
  });
  const chat = createChatController(client);
  const panel = vscode.window.createWebviewPanel(
    'leVibeNativeReadiness',
    'Lé Vibe Native Readiness',
    vscode.ViewColumn.Active,
    { enableScripts: true, retainContextWhenHidden: true },
  );
  panel.webview.html = panelHtml('checking', null, { mode: 'startup_probe' });
  resolveStartupSnapshot(vscode).then((snapshot) => {
    panel.webview.html = panelHtml(snapshot.state, snapshot.detailOverride, snapshot.diagnostics);
  });
  panel.webview.onDidReceiveMessage((msg) => {
    if (!msg) {
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'openOllamaSetupHelp') {
      void vscode.commands.executeCommand(OPEN_OLLAMA_SETUP_HELP_COMMAND);
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'openModelPullHelp') {
      void vscode.commands.executeCommand(OPEN_MODEL_PULL_HELP_COMMAND);
      return;
    }
    if (msg.type === 'action' && msg.actionId === 'openWorkspaceSetup') {
      void vscode.commands.executeCommand(OPEN_WORKSPACE_SETUP_COMMAND);
      return;
    }
    if (msg.type === 'chat' && msg.actionId === 'sendPrompt') {
      const prompt = (msg.prompt || '').trim();
      if (!prompt) {
        panel.webview.postMessage({ type: 'chatUpdate', status: 'Enter a prompt first.' });
        return;
      }
      panel.webview.postMessage({
        type: 'chatUpdate',
        status: 'Streaming response from local Ollama...',
        replaceLog: '',
      });
      void chat.sendPrompt(prompt, {
        onToken(token) {
          panel.webview.postMessage({ type: 'chatUpdate', append: token });
        },
        onDone(cancelled) {
          panel.webview.postMessage({
            type: 'chatUpdate',
            status: cancelled ? 'Request cancelled.' : 'Response complete.',
          });
        },
        onError(error) {
          panel.webview.postMessage({
            type: 'chatUpdate',
            status: `Stream failed: ${(error && error.message) || 'unknown error'}`,
          });
        },
      });
      return;
    }
    if (msg.type === 'chat' && msg.actionId === 'cancelPrompt') {
      const didCancel = chat.cancelPrompt();
      panel.webview.postMessage({
        type: 'chatUpdate',
        status: didCancel ? 'Cancelling request...' : 'No request is currently running.',
      });
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
