'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { levibeNativeChatDir } = require('./storage-inventory');
const { WORKSPACE_PLAN_KIND } = require('./workspace-plan.js');
const {
  applyEditProposalBatchAsWorkspaceEdit,
  applyFullFileAsSingleWorkspaceEdit,
} = require('./workspace-edit-apply.js');
const { EDIT_PROPOSAL_KIND } = require('./edit-proposal.js');

function workspacePlanAuditPath() {
  return path.join(levibeNativeChatDir(), 'workspace-plan-audit.jsonl');
}

/**
 * @param {string} auditPath
 * @param {object} record
 */
function appendWorkspacePlanAuditLine(auditPath, record) {
  const dir = path.dirname(auditPath);
  fs.mkdirSync(dir, { recursive: true });
  fs.appendFileSync(auditPath, `${JSON.stringify(record)}\n`, 'utf8');
}

/**
 * @param {number} stepIndex 0-based
 * @param {number} totalSteps
 * @param {string} op
 * @param {string} pathLabel workspace-relative or fs path
 * @param {'running'|'done'|'failed'|'cancelled'} status
 * @returns {string}
 */
function formatWorkspacePlanProgressStatus(stepIndex, totalSteps, op, pathLabel, status) {
  const n = stepIndex + 1;
  const m = totalSteps;
  const p = String(pathLabel || '—');
  return `Lé Vibe Chat: plan step ${n}/${m} — ${op} — ${p} — ${status}`;
}

/**
 * @param {import('vscode')} vscode
 * @param {import('vscode').WorkspaceFolder | undefined} folder
 * @param {string} uriStr
 */
function pathLabelForStep(vscode, folder, uriStr) {
  try {
    const u = vscode.Uri.parse(uriStr);
    if (folder) {
      return vscode.workspace.asRelativePath(u, false);
    }
    return u.fsPath;
  } catch {
    return uriStr;
  }
}

/**
 * @param {object} params
 * @returns {object}
 */
function buildAuditRecord(params) {
  return {
    contract_version: 'lvibe.workspace_plan_audit.v1',
    event_type: 'workspace_plan_step',
    timestamp_iso: new Date().toISOString(),
    workspace_uri: params.workspaceUri || 'no-workspace',
    plan_kind: WORKSPACE_PLAN_KIND,
    step_index: params.stepIndex,
    step_total: params.stepTotal,
    step_id: params.stepId,
    op: params.op,
    path: params.pathLabel,
    phase: params.phase,
    run_cancelled: Boolean(params.runCancelled),
    error: params.error || undefined,
    local_only: true,
  };
}

/**
 * @param {import('vscode')} vscode
 * @param {object} planValue validated workspace plan
 * @param {object} opts
 * @param {import('vscode').WorkspaceFolder | undefined} opts.workspaceFolder
 * @param {string} opts.workspaceUriStr
 * @param {(statusLine: string) => void} [opts.onProgress]
 * @param {() => boolean} [opts.shouldCancel]
 * @param {string} [opts.auditPath]
 * @returns {Promise<
 *   | { ok: true, completedSteps: number, cancelled: boolean }
 *   | { ok: false, error: string, completedSteps: number }
 * >}
 */
async function executeValidatedWorkspacePlan(vscode, planValue, opts) {
  const auditPath = opts.auditPath || workspacePlanAuditPath();
  const wf = opts.workspaceFolder;
  const workspaceUriStr = opts.workspaceUriStr || (wf ? wf.uri.toString() : 'no-workspace');
  const onProgress = typeof opts.onProgress === 'function' ? opts.onProgress : () => {};
  const shouldCancel = typeof opts.shouldCancel === 'function' ? opts.shouldCancel : () => false;

  const steps = planValue.steps;
  const total = steps.length;

  const logAudit = (partial) => {
    appendWorkspacePlanAuditLine(
      auditPath,
      buildAuditRecord({
        workspaceUri: workspaceUriStr,
        stepIndex: partial.stepIndex,
        stepTotal: total,
        stepId: partial.stepId,
        op: partial.op,
        pathLabel: partial.pathLabel,
        phase: partial.phase,
        runCancelled: partial.runCancelled,
        error: partial.error,
      }),
    );
  };

  for (let i = 0; i < total; i++) {
    if (shouldCancel()) {
      logAudit({
        stepIndex: i,
        stepId: steps[i].id,
        op: steps[i].op,
        pathLabel: pathLabelForStep(vscode, wf, primaryUriForStep(steps[i])),
        phase: 'cancelled',
        runCancelled: true,
      });
      onProgress(
        `Lé Vibe Chat: plan run cancelled after ${i}/${total} step(s) — no further steps executed.`,
      );
      return { ok: true, completedSteps: i, cancelled: true };
    }

    const step = steps[i];
    const pathLabel = pathLabelForStep(vscode, wf, primaryUriForStep(step));
    onProgress(formatWorkspacePlanProgressStatus(i, total, step.op, pathLabel, 'running'));
    logAudit({
      stepIndex: i,
      stepId: step.id,
      op: step.op,
      pathLabel,
      phase: 'start',
      runCancelled: false,
    });

    try {
      await runOneStep(vscode, step);
      onProgress(formatWorkspacePlanProgressStatus(i, total, step.op, pathLabel, 'done'));
      logAudit({
        stepIndex: i,
        stepId: step.id,
        op: step.op,
        pathLabel,
        phase: 'completed',
        runCancelled: false,
      });
    } catch (e) {
      const msg = e && e.message ? e.message : String(e);
      logAudit({
        stepIndex: i,
        stepId: step.id,
        op: step.op,
        pathLabel,
        phase: 'failed',
        runCancelled: false,
        error: msg,
      });
      onProgress(`Lé Vibe Chat: plan step failed — ${step.op} — ${pathLabel} — ${msg}`);
      return { ok: false, error: msg, completedSteps: i };
    }
  }

  onProgress(`Lé Vibe Chat: plan finished — ${total}/${total} step(s) completed.`);
  return { ok: true, completedSteps: total, cancelled: false };
}

/**
 * @param {object} step
 */
function primaryUriForStep(step) {
  if (step.op === 'move_file') return step.fromUri;
  return step.targetUri;
}

/**
 * @param {import('vscode')} vscode
 * @param {object} step
 */
async function runOneStep(vscode, step) {
  if (step.op === 'create_file') {
    const uri = vscode.Uri.parse(step.targetUri);
    const content = typeof step.content === 'string' ? step.content : '';
    const ok = await applyFullFileAsSingleWorkspaceEdit(vscode, uri, content);
    if (!ok) {
      throw new Error('WorkspaceEdit apply returned false');
    }
    return;
  }
  if (step.op === 'apply_edit') {
    const proposal = {
      kind: EDIT_PROPOSAL_KIND,
      proposals: [{ targetUri: step.targetUri, edit: step.edit }],
    };
    const ok = await applyEditProposalBatchAsWorkspaceEdit(vscode, proposal);
    if (!ok) {
      throw new Error('WorkspaceEdit apply returned false');
    }
    return;
  }
  if (step.op === 'delete_file') {
    const uri = vscode.Uri.parse(step.targetUri);
    const we = new vscode.WorkspaceEdit();
    we.deleteFile(uri, { recursive: false, ignoreIfNotExists: true });
    const ok = await vscode.workspace.applyEdit(we);
    if (!ok) {
      throw new Error('deleteFile applyEdit returned false');
    }
    return;
  }
  if (step.op === 'move_file') {
    const from = vscode.Uri.parse(step.fromUri);
    const to = vscode.Uri.parse(step.toUri);
    const we = new vscode.WorkspaceEdit();
    if (typeof we.renameFile === 'function') {
      we.renameFile(from, to, { overwrite: false });
      const ok = await vscode.workspace.applyEdit(we);
      if (!ok) {
        throw new Error('renameFile applyEdit returned false');
      }
      return;
    }
    await vscode.workspace.fs.rename(from, to, { overwrite: false });
    return;
  }
  throw new Error(`unsupported op: ${step.op}`);
}

module.exports = {
  workspacePlanAuditPath,
  appendWorkspacePlanAuditLine,
  formatWorkspacePlanProgressStatus,
  buildAuditRecord,
  executeValidatedWorkspacePlan,
};
