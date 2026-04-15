'use strict';

/**
 * Rollout toggles (task-n7-1). Default keeps first-party Lé Vibe Chat enabled; operators can disable without uninstalling.
 */
function isFirstPartyAgentSurfaceEnabled(vscode) {
  const config = vscode.workspace.getConfiguration('leVibeNative');
  return config.get('enableFirstPartyAgentSurface', true) !== false;
}

module.exports = {
  isFirstPartyAgentSurfaceEnabled,
};
