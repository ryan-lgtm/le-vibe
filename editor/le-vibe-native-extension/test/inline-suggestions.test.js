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

test('provider debounce suppresses rapid repeated requests (task-cp4-2)', async () => {
  let calls = 0;
  const provider = createInlineSuggestionProvider(
    {
      streamPrompt() {
        calls += 1;
        return {
          cancel() {},
          async done(onEvent) {
            onEvent({ type: 'token', value: 'A' });
            onEvent({ type: 'done', value: '' });
          },
        };
      },
    },
    () => true,
    () => ({ debounceMs: 999999, maxChars: 160 }),
  );
  const doc = { lineAt: () => ({ text: 'const x = ' }) };
  const pos = { line: 0, character: 10 };
  const token = { isCancellationRequested: false, onCancellationRequested() {} };
  await provider.provideInlineCompletionItems(doc, pos, {}, token);
  const second = await provider.provideInlineCompletionItems(doc, pos, {}, token);
  assert.equal(calls, 1);
  assert.deepEqual(second, []);
});

test('provider keeps only latest request result (task-cp4-2)', async () => {
  let firstResolver;
  let secondResolver;
  const provider = createInlineSuggestionProvider(
    {
      streamPrompt() {
        const id = firstResolver ? 2 : 1;
        return {
          cancel() {},
          done(onEvent) {
            return new Promise((resolve) => {
              const resolver = () => {
                onEvent({ type: 'token', value: id === 1 ? 'OLD' : 'NEW' });
                onEvent({ type: 'done', value: '' });
                resolve();
              };
              if (id === 1) firstResolver = resolver;
              else secondResolver = resolver;
            });
          },
        };
      },
    },
    () => true,
    () => ({ debounceMs: 0, maxChars: 160 }),
  );
  const doc = { lineAt: () => ({ text: 'let y = ' }) };
  const pos = { line: 0, character: 8 };
  const token = { isCancellationRequested: false, onCancellationRequested() {} };
  const p1 = provider.provideInlineCompletionItems(doc, pos, {}, token);
  const p2 = provider.provideInlineCompletionItems(doc, pos, {}, token);
  firstResolver();
  secondResolver();
  const r1 = await p1;
  const r2 = await p2;
  assert.deepEqual(r1, []);
  assert.equal(r2.length, 1);
  assert.equal(r2[0].insertText, 'NEW');
});

