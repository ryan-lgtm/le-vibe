'use strict';

const crypto = require('node:crypto');

const {
  normalizeCommandLine,
  evaluateTerminalCommand,
  getTerminalExecutionPolicy,
} = require('./terminal-execution-policy.js');
const {
  terminalCommandAuditPath,
  buildTerminalCommandAuditSent,
  buildTerminalCommandAuditEnded,
  appendTerminalCommandAudit,
} = require('./terminal-command-audit.js');

/** Visible integrated terminal — not a hidden child_process PTY (task-n13-2). */
const LEVIBE_CHAT_TERMINAL_NAME = 'Lé Vibe Chat';

/** In-memory: user chose “skip further prompts this session” (cleared on workspace change / reset command). */
let sessionSkipBatchConfirmation = false;

function clearTerminalSessionAllow() {
  sessionSkipBatchConfirmation = false;
}

/**
 * @param {boolean} value
 */
function setTerminalSessionSkipConfirmForTests(value) {
  sessionSkipBatchConfirmation = Boolean(value);
}

/**
 * @param {typeof import('vscode')} vscode
 */
function shouldSkipBatchConfirmation(vscode) {
  const cfg = vscode.workspace.getConfiguration('leVibeNative');
  if (cfg.get('terminalSkipBatchConfirmation', false) === true) {
    return true;
  }
  return sessionSkipBatchConfirmation === true;
}

/**
 * @param {import('vscode').TerminalShellExecution | undefined} execution
 * @returns {string}
 */
function executionCommandLineText(execution) {
  if (!execution) {
    return '';
  }
  const cl = execution.commandLine;
  if (typeof cl === 'string') {
    return cl;
  }
  if (cl && typeof cl.value === 'string') {
    return cl.value;
  }
  return '';
}

/**
 * When the editor exposes shell integration, append a second audit line with exit code (task-n13-3).
 * @param {typeof import('vscode')} vscode
 * @param {string} commandLine
 * @param {string} auditId
 * @param {string} auditFilePath
 */
function scheduleExitAuditAppend(vscode, commandLine, auditId, auditFilePath) {
  const hook = vscode.window.onDidEndTerminalShellExecution;
  if (typeof hook !== 'function') {
    return;
  }
  const want = normalizeCommandLine(commandLine);
  let finished = false;
  /** @type {{ dispose: () => void } | undefined} */
  let disposable;
  const timer = setTimeout(() => {
    if (!finished) {
      finished = true;
      try {
        disposable?.dispose();
      } catch {
        /* ignore */
      }
    }
  }, 120000);
  disposable = hook((e) => {
    if (finished || !e || !e.terminal) {
      return;
    }
    if (e.terminal.name !== LEVIBE_CHAT_TERMINAL_NAME) {
      return;
    }
    const got = normalizeCommandLine(executionCommandLineText(e.execution));
    if (!got || got !== want) {
      return;
    }
    finished = true;
    clearTimeout(timer);
    try {
      disposable?.dispose();
    } catch {
      /* ignore */
    }
    try {
      appendTerminalCommandAudit(
        auditFilePath,
        buildTerminalCommandAuditEnded({ auditId, exitCode: e.exitCode }),
      );
    } catch {
      /* ignore audit failures */
    }
  });
}

/**
 * Run a one-line shell command in a **visible** VS Code integrated terminal (sendText — user sees full I/O).
 * @param {typeof import('vscode')} vscode
 * @param {string} commandLine
 * @param {{ panel?: import('vscode').WebviewPanel | null, auditPath?: string }} [opts]
 * @returns {Promise<{ ok: true } | { ok: false, reason: string }>}
 */
async function runCommandInVisibleTerminal(vscode, commandLine, opts = {}) {
  const panel = opts.panel;
  const policy = getTerminalExecutionPolicy(vscode);
  const decision = evaluateTerminalCommand(commandLine, policy);
  if (!decision.ok) {
    const reason = decision.reason;
    if (panel) {
      panel.webview.postMessage({ type: 'chatUpdate', status: reason });
    }
    await vscode.window.showWarningMessage(reason);
    return { ok: false, reason };
  }

  const line = normalizeCommandLine(commandLine);
  const folder = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];

  if (!shouldSkipBatchConfirmation(vscode)) {
    const detail = folder
      ? `Workspace folder: ${folder.uri.fsPath}\nCommand:\n${line}`
      : `No single workspace folder open — terminal cwd may be editor-default.\nCommand:\n${line}`;
    const choice = await vscode.window.showWarningMessage(
      'Lé Vibe Chat: run this command in the integrated terminal? It will be visible in the Terminal panel (no hidden PTY).',
      { modal: true, detail },
      'Run in integrated terminal',
      'Cancel',
      'Run and skip further prompts (this session)',
    );
    if (choice === 'Cancel' || choice === undefined) {
      if (panel) {
        panel.webview.postMessage({ type: 'chatUpdate', status: 'Lé Vibe Chat: terminal command cancelled.' });
      }
      return { ok: false, reason: 'cancelled' };
    }
    if (choice === 'Run and skip further prompts (this session)') {
      sessionSkipBatchConfirmation = true;
    }
  }

  const existing = vscode.window.terminals.find((t) => t.name === LEVIBE_CHAT_TERMINAL_NAME);
  /** @type {import('vscode').Terminal} */
  const terminal =
    existing ||
    vscode.window.createTerminal({
      name: LEVIBE_CHAT_TERMINAL_NAME,
      cwd: folder ? folder.uri.fsPath : undefined,
    });
  terminal.show(true);
  terminal.sendText(line, true);

  const auditFilePath = opts.auditPath ?? terminalCommandAuditPath();
  const auditId = crypto.randomUUID();
  let workspaceUri = null;
  let cwd = null;
  if (folder && folder.uri) {
    cwd = folder.uri.fsPath || null;
    workspaceUri =
      typeof folder.uri.toString === 'function' ? folder.uri.toString() : cwd ? `file://${cwd}` : null;
  }
  try {
    appendTerminalCommandAudit(
      auditFilePath,
      buildTerminalCommandAuditSent({
        auditId,
        workspaceUri,
        cwd,
        commandLine: line,
      }),
    );
  } catch {
    /* ignore audit failures — command still ran */
  }
  scheduleExitAuditAppend(vscode, line, auditId, auditFilePath);

  if (panel) {
    panel.webview.postMessage({
      type: 'chatUpdate',
      status: `Lé Vibe Chat: sent to integrated terminal “${LEVIBE_CHAT_TERMINAL_NAME}” (visible).`,
    });
  }
  return { ok: true };
}

module.exports = {
  LEVIBE_CHAT_TERMINAL_NAME,
  runCommandInVisibleTerminal,
  clearTerminalSessionAllow,
  shouldSkipBatchConfirmation,
  setTerminalSessionSkipConfirmForTests,
};
