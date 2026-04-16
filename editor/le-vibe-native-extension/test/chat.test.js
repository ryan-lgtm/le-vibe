const test = require('node:test');
const assert = require('node:assert/strict');

const { createChatController } = require('../chat');

test('chat controller streams token and completes', async () => {
  const events = [];
  const states = [];
  const controller = createChatController({
    streamPrompt() {
      return {
        cancel() {},
        async done(onEvent) {
          onEvent({ type: 'token', value: 'hello ' });
          onEvent({ type: 'token', value: 'world' });
          onEvent({ type: 'done', value: '' });
        },
      };
    },
  });
  await controller.sendPrompt('test', {
    onToken: (token) => events.push(`token:${token}`),
    onDone: (cancelled) => events.push(`done:${cancelled}`),
    onError: (error) => events.push(`error:${error.message}`),
    onStateChange: ({ state }) => states.push(state),
  });
  assert.deepEqual(events, ['token:hello ', 'token:world', 'done:false']);
  assert.deepEqual(states, ['sending', 'streaming', 'streaming', 'completed', 'idle']);
  assert.equal(controller.getState(), 'idle');
});

test('chat controller marks cancelled requests as done(cancelled)', async () => {
  let cancelCalled = false;
  const controller = createChatController({
    streamPrompt() {
      return {
        cancel() {
          cancelCalled = true;
        },
        async done() {
          throw { code: 'OLLAMA_CANCELLED' };
        },
      };
    },
  });
  let doneState = null;
  await controller.sendPrompt('test', {
    onToken: () => {},
    onDone: (cancelled) => {
      doneState = cancelled;
    },
    onError: () => {},
  });
  const result = controller.cancelPrompt();
  assert.equal(result, false);
  assert.equal(doneState, true);
  assert.equal(cancelCalled, false);
  assert.equal(controller.getState(), 'idle');
});

test('cancelPrompt returns true when a request is active', async () => {
  let release;
  let cancelCalled = false;
  const controller = createChatController({
    streamPrompt() {
      return {
        cancel() {
          cancelCalled = true;
          if (release) {
            release();
          }
        },
        done() {
          return new Promise((resolve) => {
            release = resolve;
          });
        },
      };
    },
  });
  const pending = controller.sendPrompt('test', {
    onToken: () => {},
    onDone: () => {},
    onError: () => {},
  });
  const didCancel = controller.cancelPrompt();
  await pending;
  assert.equal(didCancel, true);
  assert.equal(cancelCalled, true);
  assert.equal(controller.getState(), 'idle');
});

test('chat retries transient stream failures before succeeding', async () => {
  let calls = 0;
  const states = [];
  const controller = createChatController(
    {
      streamPrompt() {
        calls += 1;
        return {
          cancel() {},
          async done(onEvent) {
            if (calls === 1) {
              throw Object.assign(new Error('timeout'), { code: 'OLLAMA_TIMEOUT' });
            }
            onEvent({ type: 'done', value: '' });
          },
        };
      },
    },
    { maxRetries: 2, retryDelayMs: 0 },
  );
  const retries = [];
  await controller.sendPrompt('test', {
    onToken: () => {},
    onDone: (cancelled) => assert.equal(cancelled, false),
    onError: () => assert.fail('unexpected error'),
    onRetry: (info) => retries.push(info),
    onStateChange: ({ state }) => states.push(state),
  });
  assert.equal(calls, 2);
  assert.equal(retries.length, 1);
  assert.deepEqual(states, ['sending', 'retrying', 'sending', 'completed', 'idle']);
  assert.equal(controller.getState(), 'idle');
});

test('chat timeout transitions to error and returns idle', async () => {
  const controller = createChatController(
    {
      streamPrompt() {
        return {
          cancel() {},
          async done() {
            throw Object.assign(new Error('timeout'), { code: 'OLLAMA_TIMEOUT' });
          },
        };
      },
    },
    { maxRetries: 0, retryDelayMs: 0 },
  );
  const states = [];
  let errorMessage = '';
  const retries = [];
  await controller.sendPrompt('test', {
    onToken: () => {},
    onDone: () => assert.fail('expected timeout to fail'),
    onRetry: (info) => retries.push(info),
    onError: (error) => {
      errorMessage = error.message;
    },
    onStateChange: ({ state }) => states.push(state),
  });
  assert.equal(errorMessage, 'timeout');
  assert.equal(retries.length, 1);
  assert.equal(retries[0].willRetry, false);
  assert.deepEqual(states, ['sending', 'error', 'idle']);
  assert.equal(controller.getState(), 'idle');
});

test('chat retries once with installed fallback model when configured model returns HTTP 404', async () => {
  let calls = 0;
  const seenModels = [];
  const fallbackEvents = [];
  const controller = createChatController(
    {
      model: 'mistral:latest',
      async listModels() {
        return [{ name: 'deepseek-r1:14b' }];
      },
      streamPrompt({ model }) {
        calls += 1;
        seenModels.push(model || 'default');
        return {
          cancel() {},
          async done(onEvent) {
            if (calls === 1) {
              throw Object.assign(new Error('missing model'), { code: 'OLLAMA_HTTP_ERROR', statusCode: 404 });
            }
            onEvent({ type: 'done', value: '' });
          },
        };
      },
    },
    { maxRetries: 0, retryDelayMs: 0 },
  );

  await controller.sendPrompt('test', {
    onToken: () => {},
    onDone: (cancelled) => assert.equal(cancelled, false),
    onError: () => assert.fail('expected fallback retry to succeed'),
    onModelFallback: (info) => fallbackEvents.push(info),
    onStateChange: () => {},
  });

  assert.equal(calls, 2);
  assert.deepEqual(seenModels, ['default', 'deepseek-r1:14b']);
  assert.equal(fallbackEvents.length, 1);
  assert.equal(fallbackEvents[0].requestedModel, 'mistral:latest');
  assert.equal(fallbackEvents[0].fallbackModel, 'deepseek-r1:14b');
});
