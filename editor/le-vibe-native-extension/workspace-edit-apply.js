'use strict';

/**
 * Apply text edits through vscode.workspace.applyEdit so the editor records
 * a single undo stop per accepted batch (Epic N9 task-n9-3).
 */

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').TextDocument} doc
 * @returns {import('vscode').Range}
 */
function fullDocumentRange(vscode, doc) {
  if (doc.lineCount === 0) {
    return new vscode.Range(new vscode.Position(0, 0), new vscode.Position(0, 0));
  }
  const last = doc.lineCount - 1;
  const lastLine = doc.lineAt(last);
  return new vscode.Range(new vscode.Position(0, 0), new vscode.Position(last, lastLine.text.length));
}

/**
 * Replace entire file contents in one WorkspaceEdit (one applyEdit → one undo step when focused in editor).
 * Creates the file when missing (still a single WorkspaceEdit: createFile + insert).
 *
 * @param {import('vscode')} vscode
 * @param {import('vscode').Uri} uri
 * @param {string} fullText
 * @returns {Promise<boolean>}
 */
async function applyFullFileAsSingleWorkspaceEdit(vscode, uri, fullText) {
  let exists = true;
  try {
    await vscode.workspace.fs.stat(uri);
  } catch {
    exists = false;
  }

  const we = new vscode.WorkspaceEdit();
  if (!exists) {
    we.createFile(uri, { overwrite: false });
    we.insert(uri, new vscode.Position(0, 0), fullText);
  } else {
    const doc = await vscode.workspace.openTextDocument(uri);
    we.replace(uri, fullDocumentRange(vscode, doc), fullText);
  }
  return vscode.workspace.applyEdit(we);
}

/**
 * Apply a validated `levibe.edit_proposal.v1` object: all file edits in **one** WorkspaceEdit.
 *
 * @param {import('vscode')} vscode
 * @param {object} proposal validated `validateEditProposal` success value
 * @returns {Promise<boolean>}
 */
async function applyEditProposalBatchAsWorkspaceEdit(vscode, proposal) {
  const we = new vscode.WorkspaceEdit();
  const items = Array.isArray(proposal && proposal.proposals) ? proposal.proposals : [];
  if (items.length === 0) {
    throw new Error('Lé Vibe Chat: proposal batch is empty; refusing applyEdit.');
  }

  for (const item of items) {
    const uri = vscode.Uri.parse(item.targetUri);
    const { edit } = item;
    if (edit.kind === 'full_file') {
      let exists = true;
      try {
        await vscode.workspace.fs.stat(uri);
      } catch {
        exists = false;
      }
      if (!exists) {
        we.createFile(uri, { overwrite: false });
        we.insert(uri, new vscode.Position(0, 0), edit.content);
      } else {
        const doc = await vscode.workspace.openTextDocument(uri);
        we.replace(uri, fullDocumentRange(vscode, doc), edit.content);
      }
    } else if (edit.kind === 'range_replace') {
      const doc = await vscode.workspace.openTextDocument(uri);
      const start = new vscode.Position(edit.range.start.line, edit.range.start.character);
      const end = new vscode.Position(edit.range.end.line, edit.range.end.character);
      we.replace(uri, new vscode.Range(start, end), edit.newText);
    }
  }

  // Single applyEdit call keeps this accepted batch as one undo transaction.
  return vscode.workspace.applyEdit(we);
}

module.exports = {
  fullDocumentRange,
  applyFullFileAsSingleWorkspaceEdit,
  applyEditProposalBatchAsWorkspaceEdit,
};
