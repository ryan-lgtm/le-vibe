'use strict';

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

/**
 * Transient failures suitable for local-first retry (no cloud fallback).
 */
function isRetryableOllamaError(error) {
  if (!error || !error.code) {
    return false;
  }
  const retryable = new Set([
    'OLLAMA_TIMEOUT',
    'OLLAMA_UNREACHABLE',
    'OLLAMA_STREAM_STALL',
    'ECONNRESET',
    'ECONNREFUSED',
    'ETIMEDOUT',
    'EPIPE',
  ]);
  if (error.code === 'OLLAMA_STREAM_MAX_DURATION') {
    return false;
  }
  if (retryable.has(error.code)) {
    return true;
  }
  if (error.code === 'OLLAMA_HTTP_ERROR' && error.statusCode) {
    const sc = Number(error.statusCode);
    return sc === 502 || sc === 503 || sc === 504;
  }
  return false;
}

function formatOllamaDiagnostic(error, endpoint) {
  const code = error && error.code ? String(error.code) : 'UNKNOWN';
  const msg = error && error.message ? String(error.message) : 'unknown error';
  return `Lé Vibe Chat: request failed [${code}] ${msg} (endpoint: ${endpoint || 'unset'})`;
}

module.exports = {
  sleep,
  isRetryableOllamaError,
  formatOllamaDiagnostic,
};
