const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const { appendEntry, loadTranscript, clearTranscript, totalBytes } = require('../chat-transcript');

test('appendEntry keeps persisted line count within maxMessages after many turns', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-bounds-'));
  const filePath = path.join(dir, 'chat.jsonl');
  const caps = { maxBytes: 50_000, maxMessages: 4 };
  try {
    for (let i = 0; i < 40; i += 1) {
      appendEntry(
        filePath,
        { id: `u${i}`, ts: i, role: 'user', content: `message ${i} `.repeat(20) },
        caps,
      );
      appendEntry(
        filePath,
        { id: `a${i}`, ts: i + 0.5, role: 'assistant', content: `reply ${i} `.repeat(20) },
        caps,
      );
      const loaded = loadTranscript(filePath);
      assert.ok(
        loaded.length <= caps.maxMessages,
        `after pair ${i} expected <= ${caps.maxMessages} messages, got ${loaded.length}`,
      );
      assert.ok(totalBytes(loaded) <= caps.maxBytes + 1, 'respects byte cap (allow tiny slack for newline rounding)');
    }
  } finally {
    clearTranscript(filePath);
  }
});

test('appendEntry respects tight byte cap with compaction stub', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-bounds-'));
  const filePath = path.join(dir, 'small.jsonl');
  const caps = { maxBytes: 800, maxMessages: 20 };
  try {
    for (let i = 0; i < 15; i += 1) {
      appendEntry(filePath, { id: `m${i}`, ts: i, role: 'user', content: `x${i}`.repeat(100) }, caps);
    }
    const loaded = loadTranscript(filePath);
    assert.ok(loaded.length <= caps.maxMessages);
    assert.ok(totalBytes(loaded) <= caps.maxBytes + 2);
    const systemLines = loaded.filter((m) => m.role === 'system');
    assert.ok(systemLines.length >= 1, 'compaction leaves explicit system stub');
    assert.ok(systemLines[0].content.includes('compacted'));
  } finally {
    clearTranscript(filePath);
  }
});
