const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  workspaceChatHistoryPath,
  appendWorkspaceChatHistoryEntry,
  readWorkspaceChatHistoryWindow,
  pruneEntriesByRetention,
} = require('../workspace-chat-history');

test('workspaceChatHistoryPath resolves to .lvibe/chat-history.jsonl', () => {
  const p = workspaceChatHistoryPath('/tmp/ws-demo');
  assert.equal(p, path.join('/tmp/ws-demo', '.lvibe', 'chat-history.jsonl'));
});

test('pruneEntriesByRetention keeps only recent rows', () => {
  const now = Date.now();
  const rows = [
    { id: 'old', ts: now - 30 * 60 * 60 * 1000, role: 'user', content: 'old' },
    { id: 'new', ts: now - 2 * 60 * 60 * 1000, role: 'assistant', content: 'new' },
  ];
  const kept = pruneEntriesByRetention(rows, 24);
  assert.equal(kept.length, 1);
  assert.equal(kept[0].id, 'new');
});

test('appendWorkspaceChatHistoryEntry applies retention and maxEntries', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-ws-history-'));
  const filePath = path.join(dir, '.lvibe', 'chat-history.jsonl');
  const now = Date.now();
  appendWorkspaceChatHistoryEntry(
    filePath,
    { id: 'old', ts: now - 26 * 60 * 60 * 1000, role: 'user', content: 'drop me' },
    { retentionHours: 24, maxEntries: 3 },
  );
  appendWorkspaceChatHistoryEntry(
    filePath,
    { id: 'a', ts: now - 1000, role: 'assistant', content: 'a' },
    { retentionHours: 24, maxEntries: 3 },
  );
  appendWorkspaceChatHistoryEntry(
    filePath,
    { id: 'b', ts: now - 900, role: 'user', content: 'b' },
    { retentionHours: 24, maxEntries: 3 },
  );
  appendWorkspaceChatHistoryEntry(
    filePath,
    { id: 'c', ts: now - 800, role: 'assistant', content: 'c' },
    { retentionHours: 24, maxEntries: 3 },
  );
  const rows = readWorkspaceChatHistoryWindow(filePath, 24);
  assert.equal(rows.length, 3);
  assert.deepEqual(
    rows.map((r) => r.id),
    ['a', 'b', 'c'],
  );
});

