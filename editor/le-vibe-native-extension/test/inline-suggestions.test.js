const test = require('node:test');
const assert = require('node:assert/strict');

const { buildInlinePrompt, sanitizeSuggestion, createInlineSuggestionProvider } = require('../inline-suggestions.js');

test('buildInlinePrompt includes strict no-markdown contract (task-cp4-1)', () => {
  const out = buildInlinePrompt('const x = ');
  assert.ok(out.includes('Return only the completion text'));
  assert.ok(out.includes('CODE_BEFORE_CURSOR:'));
});

test('sanitizeSuggestion strips fences and trailing whitespace (task-cp4-1)', () => {
  const out = sanitizeSuggestion('```ts\nconst v = 1;\n```\n');
  assert.equal(out, 'const v = 1;');
});

test('provider returns no suggestions when feature is disabled (task-cp4-1)', async () => {
  const provider = createInlineSuggestionProvider(
    {
      streamPrompt() {
        return {
          cancel() {},
          async done() {},
        };
      },
    },
    () => false,
  );
  const items = await provider.provideInlineCompletionItems(
    { lineAt: () => ({ text: 'const x = ' }) },
    { line: 0, character: 10 },
    {},
    { isCancellationRequested: false, onCancellationRequested() {} },
  );
  assert.deepEqual(items, []);
});

test('provider returns inline insert text from local stream (task-cp4-1)', async () => {
  const provider = createInlineSuggestionProvider(
    {
      streamPrompt() {
        return {
          cancel() {},
          async done(onEvent) {
            onEvent({ type: 'token', value: '42' });
            onEvent({ type: 'done', value: '' });
          },
        };
      },
    },
    () => true,
  );
  const items = await provider.provideInlineCompletionItems(
    { lineAt: () => ({ text: 'const x = ' }) },
    { line: 0, character: 10 },
    {},
    { isCancellationRequested: false, onCancellationRequested() {} },
  );
  assert.equal(Array.isArray(items), true);
  assert.equal(items.length, 1);
  assert.equal(items[0].insertText, '42');
});

