'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { DEFAULT_OLLAMA_HTTP_ENDPOINT } = require('./default-ollama-endpoint');
const { createOllamaClient } = require('./ollama');

function leVibeConfigDir() {
  const xdg = process.env.XDG_CONFIG_HOME;
  const base = xdg ? path.join(xdg, 'le-vibe') : path.join(os.homedir(), '.config', 'le-vibe');
  return base;
}

/**
 * Read `~/.config/le-vibe/managed_ollama.json` (same file `lvibe` writes when starting managed Ollama).
 * @returns {string | null} e.g. `http://127.0.0.1:11435` or null if missing/invalid
 */
function readManagedOllamaHttpEndpointSync() {
  const file = path.join(leVibeConfigDir(), 'managed_ollama.json');
  try {
    const raw = fs.readFileSync(file, 'utf8');
    const data = JSON.parse(raw);
    const host =
      data.host != null && String(data.host).trim() !== '' ? String(data.host).trim() : '127.0.0.1';
    const port = Number(data.port);
    if (!Number.isFinite(port) || port <= 0 || port > 65535) {
      return null;
    }
    return `http://${host}:${port}`;
  } catch {
    return null;
  }
}

/**
 * True if the user or workspace set `leVibeNative.ollamaEndpoint` explicitly (not relying on default only).
 * @param {typeof import('vscode')} vscode
 */
function isOllamaEndpointUserConfigured(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  if (typeof config.inspect !== 'function') {
    return false;
  }
  const i = config.inspect('ollamaEndpoint');
  if (!i) {
    return false;
  }
  return (
    i.globalValue !== undefined ||
    i.workspaceValue !== undefined ||
    i.workspaceFolderValue !== undefined
  );
}

/**
 * Prefer managed Ollama URL from disk when `lvibe` is running (state file present), unless the user
 * overrode the setting — keeps Lé Vibe Chat aligned with the launcher even if the packaged default
 * still points at a legacy port.
 * @param {typeof import('vscode')} vscode
 */
function getEffectiveOllamaEndpoint(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  if (isOllamaEndpointUserConfigured(vscode)) {
    return config.get('ollamaEndpoint', DEFAULT_OLLAMA_HTTP_ENDPOINT);
  }
  const managed = readManagedOllamaHttpEndpointSync();
  if (managed) {
    return managed;
  }
  return config.get('ollamaEndpoint', DEFAULT_OLLAMA_HTTP_ENDPOINT);
}

/**
 * True if the user or workspace set `leVibeNative.ollamaModel` explicitly.
 * @param {typeof import('vscode')} vscode
 */
function isOllamaModelUserConfigured(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  if (typeof config.inspect !== 'function') {
    return false;
  }
  const i = config.inspect('ollamaModel');
  if (!i) {
    return false;
  }
  return (
    i.globalValue !== undefined ||
    i.workspaceValue !== undefined ||
    i.workspaceFolderValue !== undefined
  );
}

function readLockedOllamaModelSync() {
  const file = path.join(leVibeConfigDir(), 'locked-model.json');
  try {
    const raw = fs.readFileSync(file, 'utf8');
    const data = JSON.parse(raw);
    const tag = data && data.ollama_model ? String(data.ollama_model).trim() : '';
    return tag || null;
  } catch {
    return null;
  }
}

/**
 * Resolve model robustly:
 * 1) explicit user/workspace setting
 * 2) launcher-locked model from ~/.config/le-vibe/locked-model.json
 * 3) first model currently installed on active endpoint
 * 4) default setting fallback
 * @param {typeof import('vscode')} vscode
 * @returns {Promise<string>} model tag
 */
async function resolveEffectiveOllamaModel(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  const fallback = config.get('ollamaModel', 'mistral:latest');
  if (isOllamaModelUserConfigured(vscode)) {
    return fallback;
  }
  const locked = readLockedOllamaModelSync();
  if (locked) {
    return locked;
  }
  try {
    const endpoint = getEffectiveOllamaEndpoint(vscode);
    const timeoutMs = config.get('ollamaTimeoutMs', 2500);
    const client = createOllamaClient({
      endpoint,
      timeoutMs,
      model: fallback,
      maxRetries: 0,
      retryDelayMs: 0,
    });
    const models = await client.listModels();
    const first = models.find((m) => m && m.name && String(m.name).trim());
    if (first && first.name) {
      return String(first.name).trim();
    }
  } catch {
    // ignore; keep fallback
  }
  return fallback;
}

module.exports = {
  readManagedOllamaHttpEndpointSync,
  getEffectiveOllamaEndpoint,
  isOllamaEndpointUserConfigured,
  isOllamaModelUserConfigured,
  readLockedOllamaModelSync,
  resolveEffectiveOllamaModel,
};
