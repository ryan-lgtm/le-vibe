'use strict';

const { sleep, isRetryableOllamaError } = require('./retry-helpers');

function createChatController(client, options = {}) {
  const maxRetries = options.maxRetries ?? 2;
  const retryDelayMs = options.retryDelayMs ?? 400;
  let active = null;
  let state = 'idle';

  function emitState(nextState, handlers, meta = {}) {
    state = nextState;
    if (handlers && typeof handlers.onStateChange === 'function') {
      handlers.onStateChange({ state: nextState, ...meta });
    }
  }

  async function sendPrompt(prompt, handlers) {
    if (active) {
      active.cancel();
      active = null;
    }
    emitState('sending', handlers, { attempt: 1, maxAttempts: maxRetries + 1 });

    let attempt = 0;
    const maxAttempts = maxRetries + 1;

    while (attempt < maxAttempts) {
      const stream = client.streamPrompt({ prompt });
      active = stream;
      try {
        await stream.done((event) => {
          if (event.type === 'token') {
            emitState('streaming', handlers, { attempt: attempt + 1, maxAttempts });
            handlers.onToken(event.value);
          } else if (event.type === 'done') {
            handlers.onDone(false);
          }
        });
        if (active === stream) {
          active = null;
        }
        emitState('completed', handlers, { attempt: attempt + 1, maxAttempts });
        emitState('idle', handlers, { attempt: attempt + 1, maxAttempts });
        return;
      } catch (error) {
        if (active === stream) {
          active = null;
        }
        if (error && error.code === 'OLLAMA_CANCELLED') {
          emitState('cancelled', handlers, { attempt: attempt + 1, maxAttempts, error });
          handlers.onDone(true);
          emitState('idle', handlers, { attempt: attempt + 1, maxAttempts });
          return;
        }
        const canRetry = isRetryableOllamaError(error) && attempt < maxAttempts - 1;
        emitState(canRetry ? 'retrying' : 'error', handlers, {
          attempt: attempt + 1,
          maxAttempts,
          error,
        });
        if (handlers.onRetry) {
          handlers.onRetry({
            attempt: attempt + 1,
            maxAttempts,
            willRetry: canRetry,
            error,
          });
        }
        if (!canRetry) {
          handlers.onError(error);
          emitState('idle', handlers, { attempt: attempt + 1, maxAttempts, error });
          return;
        }
        const backoff = retryDelayMs * 2 ** attempt;
        await sleep(backoff);
        attempt += 1;
        emitState('sending', handlers, { attempt: attempt + 1, maxAttempts });
      }
    }
    emitState('idle', handlers, { attempt: maxAttempts, maxAttempts });
  }

  function cancelPrompt() {
    if (!active) {
      return false;
    }
    active.cancel();
    return true;
  }

  return {
    sendPrompt,
    cancelPrompt,
    getState() {
      return state;
    },
  };
}

module.exports = {
  createChatController,
};
