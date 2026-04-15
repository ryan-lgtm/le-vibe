'use strict';

/**
 * Partial selection apply (Epic N9 task-n9-4): single non-empty selection only.
 * Multi-cursor / multiple regions are rejected with deterministic copy.
 */

/** @typedef {{ line: number, character: number }} EditorPosition */
/** @typedef {{ start: EditorPosition, end: EditorPosition, isEmpty?: boolean }} EditorRangeLike */

/**
 * @param {null | { selections?: EditorRangeLike[]; selection?: EditorRangeLike }} editor
 * @returns {{ ok: true, range: EditorRangeLike } | { ok: false, code: string, message: string }}
 */
function resolveSingleSelectionForPartialApply(editor) {
  if (!editor) {
    return {
      ok: false,
      code: 'NO_ACTIVE_EDITOR',
      message:
        'Lé Vibe Chat: no active editor — open a file, then select a non-empty range for partial apply.',
    };
  }

  const raw = editor.selections;
  if (!Array.isArray(raw) || raw.length === 0) {
    return {
      ok: false,
      code: 'NO_SELECTIONS',
      message: 'Lé Vibe Chat: no selection state — select text in the active editor.',
    };
  }

  if (raw.length > 1) {
    return {
      ok: false,
      code: 'MULTI_SELECTION',
      message:
        'Lé Vibe Chat: partial apply supports one selection only (multiple cursors or regions are not merged). Use a single range or whole-file flows from the panel.',
    };
  }

  const sel = raw[0];
  const empty =
    typeof sel.isEmpty === 'boolean'
      ? sel.isEmpty
      : sel.start &&
        sel.end &&
        sel.start.line === sel.end.line &&
        sel.start.character === sel.end.character;

  if (empty) {
    return {
      ok: false,
      code: 'EMPTY_SELECTION',
      message:
        'Lé Vibe Chat: no text selected — highlight a non-empty range to apply a replacement.',
    };
  }

  return { ok: true, range: sel };
}

/** Short markdown for README / OPERATOR (human-readable limits). */
const SELECTION_APPLY_LIMITATIONS_MD = [
  '- **No active editor:** command shows a warning; nothing is written.',
  '- **Empty selection (caret only):** blocked — select a non-empty range.',
  '- **Multiple selections (multi-cursor):** blocked — Lé Vibe Chat does not merge regions; use one cursor/selection or a whole-file edit from the panel.',
].join('\n');

module.exports = {
  resolveSingleSelectionForPartialApply,
  SELECTION_APPLY_LIMITATIONS_MD,
};
