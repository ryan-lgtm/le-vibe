'use strict';

const { sleep, isRetryableOllamaError } = require('./retry-helpers');

function createChatController(client, options = {}) {
  const maxRetries = options.maxRetries ?? 2;
  const retryDelayMs = options.retryDelayMs ?? 400;
  let active = null;

  async function sendPrompt(prompt, handlers) {
    if (active) {
      active.cancel();
      active = null;
    }

    let attempt = 0;
    const maxAttempts = maxRetries + 1;

    while (attempt < maxAttempts) {
      const stream = client.streamPrompt({ prompt });
      active = stream;
      try {
        await stream.done((event) => {
          if (event.type === 'token') {
            handlers.onToken(event.value);
          } else if (event.type === 'done') {
            handlers.onDone(false);
          }
        });
        if (active === stream) {
          active = null;
        }
        return;
      } catch (error) {
        if (active === stream) {
          active = null;
        }
        if (error && error.code === 'OLLAMA_CANCELLED') {
          handlers.onDone(true);
          return;
        }
        const canRetry = isRetryableOllamaError(error) && attempt < maxAttempts - 1;
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
          return;
        }
        const backoff = retryDelayMs * 2 ** attempt;
        await sleep(backoff);
        attempt += 1;
      }
    }
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
  };
}

module.exports = {
  createChatController,
};
