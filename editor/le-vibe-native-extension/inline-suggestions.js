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
 */
function createInlineSuggestionProvider(client, isEnabled) {
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
      if (token && token.isCancellationRequested) {
        return [];
      }
      const linePrefix = document.lineAt(position.line).text.slice(0, position.character);
      if (!linePrefix.trim()) {
        return [];
      }

      const stream = client.streamPrompt({ prompt: buildInlinePrompt(linePrefix) });
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
      }

      if (cancelled || (token && token.isCancellationRequested)) {
        return [];
      }
      const suggestion = sanitizeSuggestion(out);
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
