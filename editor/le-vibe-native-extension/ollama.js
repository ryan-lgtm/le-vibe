'use strict';

const http = require('node:http');
const https = require('node:https');
const { sleep, isRetryableOllamaError } = require('./retry-helpers');

function requestJson(method, url, timeoutMs) {
  return new Promise((resolve, reject) => {
    let parsedUrl;
    try {
      parsedUrl = new URL(url);
    } catch {
      reject(Object.assign(new Error('Invalid Ollama endpoint URL.'), { code: 'OLLAMA_BAD_ENDPOINT' }));
      return;
    }
    const transport = parsedUrl.protocol === 'https:' ? https : http;
    const req = transport.request(
      {
        method,
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
        path: `${parsedUrl.pathname}${parsedUrl.search}`,
        timeout: timeoutMs,
      },
      (res) => {
        const chunks = [];
        res.on('data', (chunk) => chunks.push(chunk));
        res.on('end', () => {
          const text = Buffer.concat(chunks).toString('utf8');
          if (res.statusCode < 200 || res.statusCode > 299) {
            reject(
              Object.assign(new Error(`Ollama returned status ${res.statusCode}.`), {
                code: 'OLLAMA_HTTP_ERROR',
                statusCode: res.statusCode,
                body: text,
              }),
            );
            return;
          }
          try {
            resolve(text ? JSON.parse(text) : {});
          } catch {
            reject(Object.assign(new Error('Ollama returned invalid JSON.'), { code: 'OLLAMA_BAD_JSON' }));
          }
        });
      },
    );
    req.on('timeout', () => {
      req.destroy(Object.assign(new Error('Timed out contacting Ollama.'), { code: 'OLLAMA_TIMEOUT' }));
    });
    req.on('error', (error) => {
      reject(
        Object.assign(new Error('Could not connect to local Ollama.'), {
          code: error && error.code === 'OLLAMA_TIMEOUT' ? 'OLLAMA_TIMEOUT' : 'OLLAMA_UNREACHABLE',
        }),
      );
    });
    req.end();
  });
}

function normalizeEndpoint(endpoint) {
  const value = String(endpoint || '').trim();
  return value.replace(/\/+$/, '');
}

function createOllamaClient({
  endpoint,
  timeoutMs = 2500,
  model = 'mistral:latest',
  streamStallMs = 60000,
  streamMaxMs = 120000,
  maxRetries = 2,
  retryDelayMs = 400,
}) {
  const base = normalizeEndpoint(endpoint);
  const maxAttempts = maxRetries + 1;

  async function listModels() {
    let lastError;
    for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
      try {
        const payload = await requestJson('GET', `${base}/api/tags`, timeoutMs);
        const models = Array.isArray(payload.models) ? payload.models : [];
        return models.map((item) => ({
          name: item && item.name ? String(item.name) : '',
          size: item && typeof item.size === 'number' ? item.size : null,
          modified_at: item && item.modified_at ? String(item.modified_at) : null,
        }));
      } catch (error) {
        lastError = error;
        const canRetry = isRetryableOllamaError(error) && attempt < maxAttempts - 1;
        if (!canRetry) {
          throw error;
        }
        await sleep(retryDelayMs * 2 ** attempt);
      }
    }
    throw lastError;
  }

  async function probeHealth() {
    const models = await listModels();
    return { ok: true, modelCount: models.length };
  }

  function streamPrompt({ prompt, model: requestedModel }) {
    let parsedUrl;
    try {
      parsedUrl = new URL(`${base}/api/generate`);
    } catch {
      return {
        cancel() {},
        done: async () => {
          throw Object.assign(new Error('Invalid Ollama endpoint URL.'), { code: 'OLLAMA_BAD_ENDPOINT' });
        },
      };
    }
    const transport = parsedUrl.protocol === 'https:' ? https : http;
    let reqRef = null;
    let cancelled = false;
    const done = (onEvent) =>
      new Promise((resolve, reject) => {
        let lastActivity = Date.now();
        const bump = () => {
          lastActivity = Date.now();
        };
        let stallTimer = null;
        let maxTimer = null;
        let settled = false;

        function cleanupTimers() {
          if (stallTimer) {
            clearInterval(stallTimer);
            stallTimer = null;
          }
          if (maxTimer) {
            clearTimeout(maxTimer);
            maxTimer = null;
          }
        }

        function finish(ok, err) {
          if (settled) {
            return;
          }
          settled = true;
          cleanupTimers();
          if (ok) {
            resolve();
          } else {
            reject(err);
          }
        }

        const req = transport.request(
          {
            method: 'POST',
            hostname: parsedUrl.hostname,
            port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
            path: parsedUrl.pathname,
            timeout: timeoutMs,
            headers: { 'content-type': 'application/json' },
          },
          (res) => {
            bump();
            if (res.statusCode < 200 || res.statusCode > 299) {
              finish(
                false,
                Object.assign(new Error(`Ollama returned status ${res.statusCode}.`), {
                  code: 'OLLAMA_HTTP_ERROR',
                  statusCode: res.statusCode,
                }),
              );
              return;
            }
            let buffer = '';
            stallTimer = setInterval(() => {
              if (Date.now() - lastActivity > streamStallMs) {
                if (reqRef) {
                  reqRef.destroy();
                }
                finish(
                  false,
                  Object.assign(new Error('Ollama stream stalled (no activity).'), { code: 'OLLAMA_STREAM_STALL' }),
                );
              }
            }, 2000);
            maxTimer = setTimeout(() => {
              if (reqRef) {
                reqRef.destroy();
              }
              finish(
                false,
                Object.assign(new Error('Ollama stream exceeded max duration.'), {
                  code: 'OLLAMA_STREAM_MAX_DURATION',
                }),
              );
            }, streamMaxMs);
            res.on('data', (chunk) => {
              bump();
              buffer += chunk.toString('utf8');
              const lines = buffer.split('\n');
              buffer = lines.pop() || '';
              lines.forEach((line) => {
                const trimmed = line.trim();
                if (!trimmed) {
                  return;
                }
                let payload;
                try {
                  payload = JSON.parse(trimmed);
                } catch {
                  return;
                }
                if (payload.response) {
                  bump();
                  onEvent({ type: 'token', value: String(payload.response) });
                }
                if (payload.done) {
                  bump();
                  onEvent({ type: 'done', value: '' });
                }
              });
            });
            res.on('end', () => finish(true));
            res.on('error', (error) =>
              finish(
                false,
                Object.assign(new Error(error.message || 'response error'), {
                  code: error.code || 'OLLAMA_STREAM_ERROR',
                }),
              ),
            );
          },
        );
        reqRef = req;
        req.on('timeout', () => {
          req.destroy(Object.assign(new Error('Timed out contacting Ollama.'), { code: 'OLLAMA_TIMEOUT' }));
        });
        req.on('error', (error) => {
          if (cancelled) {
            finish(false, Object.assign(new Error('Request cancelled.'), { code: 'OLLAMA_CANCELLED' }));
            return;
          }
          finish(
            false,
            Object.assign(new Error('Could not stream from local Ollama.'), {
              code: error && error.code ? error.code : 'OLLAMA_STREAM_ERROR',
            }),
          );
        });
        req.write(
          JSON.stringify({
            model: requestedModel || model,
            prompt,
            stream: true,
          }),
        );
        req.end();
      });

    return {
      cancel() {
        cancelled = true;
        if (reqRef) {
          reqRef.destroy();
        }
      },
      done,
    };
  }

  return {
    endpoint: base,
    timeoutMs,
    streamStallMs,
    streamMaxMs,
    maxRetries,
    retryDelayMs,
    probeHealth,
    listModels,
    streamPrompt,
  };
}

module.exports = {
  createOllamaClient,
};
