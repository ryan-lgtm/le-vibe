'use strict';

const http = require('node:http');
const https = require('node:https');

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

function createOllamaClient({ endpoint, timeoutMs = 2500, model = 'mistral:latest' }) {
  const base = normalizeEndpoint(endpoint);
  async function listModels() {
    const payload = await requestJson('GET', `${base}/api/tags`, timeoutMs);
    const models = Array.isArray(payload.models) ? payload.models : [];
    return models.map((item) => ({
      name: item && item.name ? String(item.name) : '',
      size: item && typeof item.size === 'number' ? item.size : null,
      modified_at: item && item.modified_at ? String(item.modified_at) : null,
    }));
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
            if (res.statusCode < 200 || res.statusCode > 299) {
              reject(
                Object.assign(new Error(`Ollama returned status ${res.statusCode}.`), {
                  code: 'OLLAMA_HTTP_ERROR',
                }),
              );
              return;
            }
            let buffer = '';
            res.on('data', (chunk) => {
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
                  onEvent({ type: 'token', value: String(payload.response) });
                }
                if (payload.done) {
                  onEvent({ type: 'done', value: '' });
                }
              });
            });
            res.on('end', () => resolve());
            res.on('error', (error) => reject(error));
          },
        );
        reqRef = req;
        req.on('timeout', () => {
          req.destroy(Object.assign(new Error('Timed out contacting Ollama.'), { code: 'OLLAMA_TIMEOUT' }));
        });
        req.on('error', (error) => {
          if (cancelled) {
            reject(Object.assign(new Error('Request cancelled.'), { code: 'OLLAMA_CANCELLED' }));
            return;
          }
          reject(
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
    probeHealth,
    listModels,
    streamPrompt,
  };
}

module.exports = {
  createOllamaClient,
};
