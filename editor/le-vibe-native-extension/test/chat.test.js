const test = require('node:test');
const assert = require('node:assert/strict');

const { createChatController } = require('../chat');

test('chat controller streams token and completes', async () => {
  const events = [];
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
  });
  assert.deepEqual(events, ['token:hello ', 'token:world', 'done:false']);
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
});

test('chat retries transient stream failures before succeeding', async () => {
  let calls = 0;
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
  });
  assert.equal(calls, 2);
  assert.equal(retries.length, 1);
});
