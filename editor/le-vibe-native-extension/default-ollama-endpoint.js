'use strict';

/**
 * Must match `leVibeNative.ollamaEndpoint` default in package.json and the managed
 * port in `le-vibe/le_vibe/paths.py` (`LE_VIBE_MANAGED_OLLAMA_PORT`, default 11435).
 */
const DEFAULT_OLLAMA_HTTP_ENDPOINT = 'http://127.0.0.1:11435';

module.exports = {
  DEFAULT_OLLAMA_HTTP_ENDPOINT,
};
