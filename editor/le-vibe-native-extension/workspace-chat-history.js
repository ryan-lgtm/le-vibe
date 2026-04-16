'use strict';

const fs = require('node:fs');
const path = require('node:path');

/**
 * @typedef {{ id: string, ts: number, role: 'user'|'assistant'|'system', content: string }} WorkspaceChatEntry
 */

function workspaceChatHistoryPath(workspaceFsPath) {
  if (!workspaceFsPath) {
    return null;
  }
  return path.join(workspaceFsPath, '.lvibe', 'chat-history.jsonl');
}

function parseJsonlLines(raw) {
  const out = [];
  const lines = String(raw || '')
    .split('\n')
    .filter((line) => line.trim().length > 0);
  for (const line of lines) {
    try {
      const row = JSON.parse(line);
      if (
        row &&
        typeof row === 'object' &&
        typeof row.id === 'string' &&
        Number.isFinite(row.ts) &&
        typeof row.role === 'string' &&
        typeof row.content === 'string'
      ) {
        out.push({
          id: row.id,
          ts: Number(row.ts),
          role: row.role,
          content: row.content,
        });
      }
    } catch {
      /* ignore malformed lines */
    }
  }
  return out;
}

function loadWorkspaceChatHistory(filePath) {
  if (!filePath || !fs.existsSync(filePath)) {
    return [];
  }
  try {
    return parseJsonlLines(fs.readFileSync(filePath, 'utf8'));
  } catch {
    return [];
  }
}

function pruneEntriesByRetention(entries, retentionHours) {
  const hours = Number(retentionHours);
  if (!Number.isFinite(hours) || hours <= 0) {
    return [...entries];
  }
  const cutoff = Date.now() - hours * 60 * 60 * 1000;
  return entries.filter((entry) => Number(entry.ts) >= cutoff);
}

function serialize(entries) {
  return entries.map((entry) => JSON.stringify(entry)).join('\n') + (entries.length ? '\n' : '');
}

function atomicWrite(filePath, text) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  const tmp = `${filePath}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, text, 'utf8');
  fs.renameSync(tmp, filePath);
}

function saveWorkspaceChatHistory(filePath, entries) {
  if (!filePath) {
    return;
  }
  atomicWrite(filePath, serialize(entries));
}

function appendWorkspaceChatHistoryEntry(filePath, entry, options = {}) {
  if (!filePath) {
    return [];
  }
  const retentionHours = Number(options.retentionHours ?? 24);
  const maxEntries = Number(options.maxEntries ?? 2000);
  const existing = loadWorkspaceChatHistory(filePath);
  const next = [...existing, entry];
  const retained = pruneEntriesByRetention(next, retentionHours);
  const bounded = Number.isFinite(maxEntries) && maxEntries > 0 ? retained.slice(-maxEntries) : retained;
  saveWorkspaceChatHistory(filePath, bounded);
  return bounded;
}

function readWorkspaceChatHistoryWindow(filePath, retentionHours = 24) {
  const rows = loadWorkspaceChatHistory(filePath);
  return pruneEntriesByRetention(rows, retentionHours);
}

module.exports = {
  workspaceChatHistoryPath,
  loadWorkspaceChatHistory,
  saveWorkspaceChatHistory,
  appendWorkspaceChatHistoryEntry,
  readWorkspaceChatHistoryWindow,
  pruneEntriesByRetention,
};

