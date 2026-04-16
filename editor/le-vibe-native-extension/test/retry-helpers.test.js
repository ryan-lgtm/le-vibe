const test = require('node:test');
const assert = require('node:assert/strict');

const { isRetryableOllamaError, formatOllamaDiagnostic } = require('../retry-helpers');

test('isRetryableOllamaError recognizes transient codes', () => {
  assert.equal(isRetryableOllamaError({ code: 'OLLAMA_TIMEOUT' }), true);
  assert.equal(isRetryableOllamaError({ code: 'OLLAMA_STREAM_STALL' }), true);
  assert.equal(isRetryableOllamaError({ code: 'OLLAMA_HTTP_ERROR', statusCode: 503 }), true);
  assert.equal(isRetryableOllamaError({ code: 'OLLAMA_STREAM_MAX_DURATION' }), false);
  assert.equal(isRetryableOllamaError({ code: 'OLLAMA_BAD_JSON' }), false);
});

test('formatOllamaDiagnostic includes code and endpoint', () => {
  const text = formatOllamaDiagnostic({ code: 'X', message: 'oops' }, 'http://127.0.0.1:11435');
  assert.ok(text.includes('[X]'));
  assert.ok(text.includes('127.0.0.1:11435'));
});

test('formatOllamaDiagnostic adds hint for Ollama HTTP 404 (model missing or wrong port)', () => {
  const text = formatOllamaDiagnostic(
    { code: 'OLLAMA_HTTP_ERROR', message: 'Ollama returned status 404.', statusCode: 404 },
    'http://127.0.0.1:11435',
  );
  assert.ok(text.includes('OLLAMA_HTTP_ERROR'));
  assert.ok(text.includes('managed Ollama'));
});
