'use strict';

function createChatController(client) {
  let active = null;

  async function sendPrompt(prompt, handlers) {
    if (active) {
      active.cancel();
      active = null;
    }
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
    } catch (error) {
      if (error && error.code === 'OLLAMA_CANCELLED') {
        handlers.onDone(true);
        return;
      }
      handlers.onError(error);
    } finally {
      if (active === stream) {
        active = null;
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
