const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  compactTranscript,
  transcriptPath,
  appendEntry,
  loadTranscript,
  totalBytes,
} = require('../chat-transcript');

test('compactTranscript drops oldest until under maxMessages', () => {
  const msgs = Array.from({ length: 5 }, (_, i) => ({
    id: `m${i}`,
    ts: i,
    role: 'user',
    content: `x${i}`,
  }));
  const { messages, removedCount } = compactTranscript(msgs, { maxBytes: 1_000_000, maxMessages: 3 });
  assert.equal(removedCount, 2);
  assert.equal(messages.length, 3);
  assert.equal(messages[0].role, 'system');
  assert.ok(messages[0].content.includes('2 older message'));
});

test('compactTranscript enforces maxBytes with predictable stub', () => {
  const big = 'y'.repeat(500);
  const msgs = [
    { id: 'a', ts: 1, role: 'user', content: big },
    { id: 'b', ts: 2, role: 'assistant', content: big },
  ];
  const caps = { maxMessages: 100, maxBytes: 400 };
  const { messages, removedCount } = compactTranscript(msgs, caps);
  assert.ok(removedCount >= 1);
  assert.ok(totalBytes(messages) <= caps.maxBytes || messages.length === 1);
  assert.equal(messages[0].role, 'system');
});

test('appendEntry writes under temp dir and respects cap', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'lvibe-chat-'));
  const filePath = path.join(dir, 't.jsonl');
  const caps = { maxBytes: 2000, maxMessages: 2 };
  appendEntry(filePath, { id: '1', ts: 1, role: 'user', content: 'hello' }, caps);
  appendEntry(filePath, { id: '2', ts: 2, role: 'assistant', content: 'hi' }, caps);
  const loaded = loadTranscript(filePath);
  assert.ok(loaded.length >= 1);
});

test('transcriptPath stays under config le-vibe', () => {
  const p = transcriptPath('file:///workspace/foo');
  assert.ok(p.includes('.config'));
  assert.ok(p.includes('le-vibe'));
  assert.ok(p.endsWith('.jsonl'));
});
