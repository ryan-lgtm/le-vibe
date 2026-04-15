'use strict';

const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');

/**
 * @typedef {{ id: string, ts: number, role: 'user' | 'assistant' | 'system', content: string }} TranscriptLine
 */

function transcriptDir() {
  return path.join(os.homedir(), '.config', 'le-vibe', 'levibe-native-chat');
}

function workspaceKeyFromUri(workspaceFolderUri) {
  const key = workspaceFolderUri || 'no-workspace';
  return crypto.createHash('sha256').update(key).digest('hex').slice(0, 16);
}

function transcriptPath(workspaceFolderUri) {
  const dir = transcriptDir();
  const file = `transcript-${workspaceKeyFromUri(workspaceFolderUri)}.jsonl`;
  return path.join(dir, file);
}

function lineBytes(line) {
  return Buffer.byteLength(`${JSON.stringify(line)}\n`, 'utf8');
}

function totalBytes(lines) {
  return lines.reduce((sum, m) => sum + lineBytes(m), 0);
}

/**
 * Oldest-first removal until under maxMessages and maxBytes; prepend explicit summary stub (never silent loss).
 * @param {TranscriptLine[]} messages
 * @param {{ maxBytes: number, maxMessages: number }} caps
 * @returns {{ messages: TranscriptLine[], removedCount: number }}
 */
function compactTranscript(messages, caps) {
  const { maxBytes, maxMessages } = caps;
  const out = [...messages];
  let removed = 0;

  while (out.length > 0 && (out.length > maxMessages || totalBytes(out) > maxBytes)) {
    out.shift();
    removed += 1;
  }

  if (removed === 0) {
    return { messages: out, removedCount: 0 };
  }

  out.unshift({
    id: `compact-${Date.now()}`,
    ts: Date.now(),
    role: 'system',
    content: `[Lé Vibe Chat: ${removed} older message(s) were compacted to stay within the configured size/message cap. Adjust caps in Settings → Lé Vibe Native Extension.]`,
  });

  while (out.length > maxMessages || totalBytes(out) > maxBytes) {
    if (out.length <= 1) {
      break;
    }
    out.splice(1, 1);
  }

  return { messages: out, removedCount: removed };
}

function parseJsonl(text) {
  const lines = text.split('\n').filter((line) => line.trim().length > 0);
  const result = [];
  for (const line of lines) {
    try {
      const obj = JSON.parse(line);
      if (obj && typeof obj === 'object' && typeof obj.content === 'string' && typeof obj.role === 'string') {
        result.push(obj);
      }
    } catch {
      /* skip corrupt line */
    }
  }
  return result;
}

function serializeJsonl(messages) {
  return messages.map((m) => JSON.stringify(m)).join('\n') + (messages.length ? '\n' : '');
}

function atomicWrite(filePath, text) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  const tmp = `${filePath}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, text, 'utf8');
  fs.renameSync(tmp, filePath);
}

function loadTranscript(filePath) {
  if (!fs.existsSync(filePath)) {
    return [];
  }
  try {
    return parseJsonl(fs.readFileSync(filePath, 'utf8'));
  } catch {
    return [];
  }
}

function saveTranscript(filePath, messages, caps) {
  const { messages: bounded } = compactTranscript(messages, caps);
  atomicWrite(filePath, serializeJsonl(bounded));
  return bounded;
}

/**
 * @param {TranscriptLine} entry
 * @param {{ maxBytes: number, maxMessages: number }} caps
 */
function appendEntry(filePath, entry, caps) {
  const existing = loadTranscript(filePath);
  const next = [...existing, entry];
  return saveTranscript(filePath, next, caps);
}

module.exports = {
  transcriptDir,
  transcriptPath,
  workspaceKeyFromUri,
  compactTranscript,
  loadTranscript,
  saveTranscript,
  appendEntry,
  totalBytes,
  lineBytes,
};
