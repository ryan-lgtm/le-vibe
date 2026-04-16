'use strict';

/**
 * Build a local-only completion prompt for Ollama.
 * @param {string} prefix
 * @returns {string}
 */
function buildInlinePrompt(prefix) {
  return [
    'Complete the following code at cursor.',
    'Return only the completion text, no markdown, no backticks, no explanation.',
    'If unsure, return empty output.',
    '',
    'CODE_BEFORE_CURSOR:',
    prefix,
  ].join('\n');
}

/**
 * @param {string} raw
 * @returns {string}
 */
function sanitizeSuggestion(raw) {
  let text = String(raw || '').replace(/\r/g, '');
  text = text.replace(/^```[\w-]*\s*/g, '').replace(/\s*```[\s]*$/g, '');
  return text.trimEnd();
}

/**
 * @param {object} client
 * @param {() => boolean} isEnabled
 * @param {() => { debounceMs: number, maxChars: number }} [getOptions]
 */
function createInlineSuggestionProvider(client, isEnabled, getOptions = () => ({ debounceMs: 150, maxChars: 160 })) {
  let lastRequestAt = 0;
  let activeStream = null;
  let activeRequestId = 0;

  /**
   * Minimal ranking: prefer candidates that extend prefix and are concise.
   * @param {string} prefix
   * @param {string} raw
   * @param {number} maxChars
   * @returns {string}
   */
  function rankAndSelectSuggestion(prefix, raw, maxChars) {
    const clipped = String(raw || '').slice(0, Math.max(1, maxChars));
    const candidates = clipped
      .split(/\n{2,}/)
      .map((c) => sanitizeSuggestion(c))
      .map((c) => c.trim())
      .filter(Boolean);
    if (!candidates.length) {
      return '';
    }
    const scored = candidates.map((candidate) => {
      let score = 0;
      if (candidate.startsWith(prefix)) {
        score += 10;
      } else if (candidate.includes(prefix.trim())) {
        score += 3;
      }
      score -= Math.min(candidate.length, 300) / 200;
      return { candidate, score };
    });
    scored.sort((a, b) => b.score - a.score);
    return scored[0].candidate;
  }

  return {
    /**
     * @param {import('vscode').TextDocument} document
     * @param {import('vscode').Position} position
     * @param {unknown} _context
     * @param {{ isCancellationRequested?: boolean, onCancellationRequested?: (cb: () => void) => unknown }} token
     */
    async provideInlineCompletionItems(document, position, _context, token) {
      if (!isEnabled()) {
        return [];
      }
      const opts = getOptions();
      const debounceMs = Math.max(0, Number(opts && opts.debounceMs ? opts.debounceMs : 0));
      const maxChars = Math.max(1, Number(opts && opts.maxChars ? opts.maxChars : 160));
      if (token && token.isCancellationRequested) {
        return [];
      }
      const now = Date.now();
      if (now - lastRequestAt < debounceMs) {
        return [];
      }
      lastRequestAt = now;
      const linePrefix = document.lineAt(position.line).text.slice(0, position.character);
      if (!linePrefix.trim()) {
        return [];
      }

      const stream = client.streamPrompt({ prompt: buildInlinePrompt(linePrefix) });
      activeRequestId += 1;
      const requestId = activeRequestId;
      if (activeStream && typeof activeStream.cancel === 'function') {
        activeStream.cancel();
      }
      activeStream = stream;
      let cancelled = false;
      if (token && typeof token.onCancellationRequested === 'function') {
        token.onCancellationRequested(() => {
          cancelled = true;
          stream.cancel();
        });
      }

      let out = '';
      try {
        await stream.done((event) => {
          if (cancelled) {
            return;
          }
          if (event.type === 'token') {
            out += event.value;
          }
        });
      } catch {
        return [];
      } finally {
        if (activeStream === stream) {
          activeStream = null;
        }
      }

      if (cancelled || (token && token.isCancellationRequested) || requestId !== activeRequestId) {
        return [];
      }
      const suggestion = rankAndSelectSuggestion(linePrefix, out, maxChars);
      if (!suggestion.trim()) {
        return [];
      }
      const insertText = suggestion.startsWith(linePrefix) ? suggestion.slice(linePrefix.length) : suggestion;
      if (!insertText.trim()) {
        return [];
      }
      return [{ insertText, range: undefined }];
    },
  };
}

module.exports = {
  buildInlinePrompt,
  sanitizeSuggestion,
  createInlineSuggestionProvider,
};
