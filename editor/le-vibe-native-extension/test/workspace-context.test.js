const test = require('node:test');
const assert = require('node:assert/strict');

const { isSafeRelativePath, clipTextByBudget, buildPromptWithContext } = require('../workspace-context');

test('isSafeRelativePath rejects traversal and absolute paths', () => {
  assert.equal(isSafeRelativePath('../secrets.txt'), false);
  assert.equal(isSafeRelativePath('/etc/passwd'), false);
  assert.equal(isSafeRelativePath('src/app.js'), true);
});

test('clipTextByBudget enforces line and character caps', () => {
  const source = 'line1\nline2\nline3\nline4';
  const clipped = clipTextByBudget(source, 9, 2);
  assert.equal(clipped, 'line1\nlin');
});

test('buildPromptWithContext injects selected file excerpts within cap', () => {
  const prompt = buildPromptWithContext(
    'What does this project do?',
    [
      { path: 'README.md', content: 'Project summary here.' },
      { path: 'src/main.js', content: 'console.log("hello");' },
    ],
    500,
  );
  assert.ok(prompt.includes('### FILE: README.md'));
  assert.ok(prompt.includes('### USER PROMPT'));
  assert.ok(prompt.includes('What does this project do?'));
});
