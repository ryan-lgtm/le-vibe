'use strict';

/**
 * Unified diff + preview/apply gate for Epic N9 (no silent writes when preview is required).
 */

/**
 * @param {boolean} requireEditPreviewBeforeApply
 * @param {boolean} previewShown
 * @param {boolean} userAcceptedPreview
 * @returns {{ ok: true } | { ok: false, reason: string }}
 */
function canApplyAfterPreview({ requireEditPreviewBeforeApply, previewShown, userAcceptedPreview }) {
  if (!previewShown) {
    return {
      ok: false,
      reason: 'Preview was not shown — cannot apply (Lé Vibe Chat).',
    };
  }
  if (!requireEditPreviewBeforeApply) {
    return { ok: true };
  }
  if (!userAcceptedPreview) {
    return {
      ok: false,
      reason:
        'Accept the preview before applying. Turn off leVibeNative.requireEditPreviewBeforeApply only if you accept direct applies after preview is shown.',
    };
  }
  return { ok: true };
}

/**
 * Line-based unified diff (minimal LCS) for webview / operator visibility.
 * @param {string} before
 * @param {string} after
 * @param {string} label
 * @returns {string}
 */
function buildUnifiedDiff(before, after, label) {
  const safeLabel = String(label || 'file').replace(/\r?\n/g, ' ');
  const a = String(before ?? '').replace(/\r\n/g, '\n').split('\n');
  const b = String(after ?? '').replace(/\r\n/g, '\n').split('\n');
  if (a.join('\n') === b.join('\n')) {
    return `--- ${safeLabel}\n+++ ${safeLabel}\n@@ no changes @@\n`;
  }
  const ops = diffLineOps(a, b);
  const body = ops
    .map((op) => {
      if (op.t === 'keep') return ` ${op.line}`;
      if (op.t === 'del') return `-${op.line}`;
      return `+${op.line}`;
    })
    .join('\n');
  return `--- ${safeLabel}\n+++ ${safeLabel}\n@@ preview @@\n${body}\n`;
}

/**
 * @param {string[]} a
 * @param {string[]} b
 * @returns {{ t: 'keep'|'del'|'add', line: string }[]}
 */
function diffLineOps(a, b) {
  const m = a.length;
  const n = b.length;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (a[i - 1] === b[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
      else dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
    }
  }
  const out = [];
  let i = m;
  let j = n;
  const stack = [];
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && a[i - 1] === b[j - 1]) {
      stack.push({ t: 'keep', line: a[i - 1] });
      i--;
      j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      stack.push({ t: 'add', line: b[j - 1] });
      j--;
    } else if (i > 0) {
      stack.push({ t: 'del', line: a[i - 1] });
      i--;
    }
  }
  while (stack.length) out.push(stack.pop());
  return out;
}

module.exports = {
  canApplyAfterPreview,
  buildUnifiedDiff,
};
