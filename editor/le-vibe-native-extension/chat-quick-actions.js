'use strict';

/**
 * Stable IDs for panel quick-action buttons (task-n12-2). Templates are local-only strings;
 * Ollama is contacted only when the user clicks **Send Prompt**.
 */
const QUICK_ACTION_ID = Object.freeze({
  EXPLAIN: 'explain',
  REFACTOR_SELECTION: 'refactor_selection',
  GENERATE_TESTS: 'generate_tests',
});

const QUICK_ACTION_TEMPLATES = Object.freeze({
  [QUICK_ACTION_ID.EXPLAIN]:
    'Explain the following code or notes in plain language. Call out assumptions and edge cases.\n\n',
  [QUICK_ACTION_ID.REFACTOR_SELECTION]:
    'Refactor the code below for clarity and consistency with the rest of the project. Prefer small, behavior-preserving steps. Constraints: preserve public APIs unless noted.\n\n',
  [QUICK_ACTION_ID.GENERATE_TESTS]:
    'Generate focused unit tests for the code below. Prefer fast, isolated tests with minimal mocks. Note any testing gaps.\n\n',
});

/**
 * @param {string} id one of {@link QUICK_ACTION_ID}
 * @returns {string}
 */
function getQuickActionTemplate(id) {
  const t = QUICK_ACTION_TEMPLATES[id];
  return typeof t === 'string' ? t : '';
}

module.exports = {
  QUICK_ACTION_ID,
  QUICK_ACTION_TEMPLATES,
  getQuickActionTemplate,
};
