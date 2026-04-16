'use strict';

const { createOllamaClient } = require('./ollama');
const { isFirstPartyAgentSurfaceEnabled } = require('./feature-flags');

const REFRESH_INTERVAL_MS = 90_000;

/**
 * Register an optional status bar entry (task-n17-3): Lé Vibe Chat + local Ollama reachability; click opens agent surface.
 * @param {typeof import('vscode')} vscode
 * @param {import('vscode').ExtensionContext} context
 * @param {{ openAgentSurfaceCommand: string }} opts
 * @returns {import('vscode').Disposable}
 */
function registerLeVibeChatStatusBar(vscode, context, opts) {
  const { openAgentSurfaceCommand } = opts;
  let item = null;
  let intervalId = null;

  function clearTimers() {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  }

  function disposeItem() {
    clearTimers();
    if (item) {
      item.dispose();
      item = null;
    }
  }

  async function refresh() {
    if (!item) {
      return;
    }
    const cfg = vscode.workspace.getConfiguration('leVibeNative');
    const endpoint = cfg.get('ollamaEndpoint', 'http://127.0.0.1:11434');
    const timeoutMs = cfg.get('ollamaTimeoutMs', 2500);
    const model = cfg.get('ollamaModel', 'mistral:latest');
    const streamStallMs = cfg.get('ollamaStreamStallMs', 60000);
    const streamMaxMs = cfg.get('ollamaStreamMaxMs', 120000);
    const maxRetries = cfg.get('ollamaMaxRetries', 2);
    const retryDelayMs = cfg.get('ollamaRetryBackoffMs', 400);
    try {
      const client = createOllamaClient({
        endpoint,
        timeoutMs,
        model,
        streamStallMs,
        streamMaxMs,
        maxRetries: 0,
        retryDelayMs,
      });
      const health = await client.probeHealth();
      if (!item) {
        return;
      }
      const modelsNote =
        health.modelCount > 0 ? `${health.modelCount} local model(s)` : 'no models installed';
      item.text = `$(comment-discussion) Lé Vibe Chat · Ollama OK`;
      item.tooltip = `Lé Vibe Chat — idle. Click to open the agent surface. Local Ollama: reachable (${modelsNote}). Endpoint: ${endpoint}`;
    } catch (e) {
      if (!item) {
        return;
      }
      const detail = e && e.message ? String(e.message) : String(e);
      item.text = `$(comment-discussion) Lé Vibe Chat · Ollama unreachable`;
      item.tooltip = `Lé Vibe Chat — local Ollama not reachable. Click to open the panel for remediation. Endpoint: ${endpoint}. ${detail}`;
    }
  }

  function sync() {
    disposeItem();
    const cfg = vscode.workspace.getConfiguration('leVibeNative');
    if (cfg.get('showStatusBarEntry', false) !== true) {
      return;
    }
    if (!isFirstPartyAgentSurfaceEnabled(vscode)) {
      return;
    }
    item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 25);
    item.name = 'Lé Vibe Chat status';
    item.command = openAgentSurfaceCommand;
    void refresh();
    item.show();
    intervalId = setInterval(() => {
      void refresh();
    }, REFRESH_INTERVAL_MS);
  }

  sync();

  const configListener = vscode.workspace.onDidChangeConfiguration((e) => {
    if (e.affectsConfiguration('leVibeNative')) {
      sync();
    }
  });

  const disposable = new vscode.Disposable(() => {
    configListener.dispose();
    disposeItem();
  });

  context.subscriptions.push(disposable);
  return disposable;
}

module.exports = {
  registerLeVibeChatStatusBar,
  REFRESH_INTERVAL_MS,
};
