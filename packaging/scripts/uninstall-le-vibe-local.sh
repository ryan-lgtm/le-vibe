#!/usr/bin/env bash
# Safe local uninstall helper for Lé Vibe stack + IDE packages on Debian/Ubuntu.
# Default behavior removes packages and known install paths; optional flags remove user data.
set -euo pipefail

ASSUME_YES=0
PURGE_USER_DATA=0
PURGE_WORKSPACE=""

usage() {
  cat <<'EOF'
Usage: packaging/scripts/uninstall-le-vibe-local.sh [options]

Safely uninstall Lé Vibe from a Debian/Ubuntu host, including partial/failed installs.

Default actions:
  1) Stop known Lé Vibe-managed processes (best effort).
  2) apt remove --purge le-vibe le-vibe-ide (best effort).
  3) dpkg force remove/purge fallback for half-installed states (best effort).
  4) Remove known installed paths under /usr/bin, /usr/lib/le-vibe, /usr/share/applications, /usr/share/icons, /usr/share/doc.
  5) Refresh shell/desktop caches.

Options:
  --yes                    Non-interactive apt/autoremove.
  --purge-user-data        Remove ~/.config/le-vibe after package uninstall.
  --purge-workspace PATH   Remove PATH/.lvibe (exact path only, safety checked).
  -h, --help               Show this message.

Examples:
  packaging/scripts/uninstall-le-vibe-local.sh
  packaging/scripts/uninstall-le-vibe-local.sh --yes --purge-user-data
  packaging/scripts/uninstall-le-vibe-local.sh --yes --purge-workspace "/home/user/my-project"
EOF
}

have_cmd() { command -v "$1" >/dev/null 2>&1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --yes) ASSUME_YES=1 ;;
    --purge-user-data) PURGE_USER_DATA=1 ;;
    --purge-workspace)
      PURGE_WORKSPACE="${2:-}"
      if [[ -z "$PURGE_WORKSPACE" ]]; then
        echo "uninstall-le-vibe-local: --purge-workspace requires a path." >&2
        exit 2
      fi
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "uninstall-le-vibe-local: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if ! have_cmd sudo; then
  echo "uninstall-le-vibe-local: sudo is required." >&2
  exit 2
fi

APT_ARGS=()
[[ "$ASSUME_YES" -eq 1 ]] && APT_ARGS+=("-y")

echo "==> Stopping Lé Vibe/IDE managed processes (best effort)"
pkill -f "/usr/lib/le-vibe/bin/codium" 2>/dev/null || true
pkill -f "le_vibe.launcher" 2>/dev/null || true
pkill -f "ollama serve.*11435" 2>/dev/null || true

if have_cmd apt-get; then
  echo "==> Removing packages via apt (best effort)"
  sudo apt-get remove --purge "${APT_ARGS[@]}" le-vibe le-vibe-ide 2>/dev/null || true
  sudo apt-get autoremove "${APT_ARGS[@]}" 2>/dev/null || true
else
  echo "==> apt-get not found; skipping apt remove step"
fi

if have_cmd dpkg; then
  echo "==> Removing dpkg half-installed states (best effort)"
  sudo dpkg --remove --force-remove-reinstreq le-vibe le-vibe-ide 2>/dev/null || true
  sudo dpkg --purge --force-all le-vibe le-vibe-ide 2>/dev/null || true
fi

echo "==> Removing known install leftovers"
sudo rm -f /usr/bin/lvibe /usr/bin/le-vibe /usr/bin/lvibe-hygiene /usr/bin/le-vibe-setup-continue
sudo rm -rf /usr/lib/le-vibe
sudo rm -f /usr/share/applications/le-vibe.desktop
sudo rm -f /usr/share/icons/hicolor/scalable/apps/le-vibe.svg
sudo rm -rf /usr/share/doc/le-vibe /usr/share/doc/le-vibe-ide

if [[ "$PURGE_USER_DATA" -eq 1 ]]; then
  echo "==> Removing user data: ~/.config/le-vibe"
  rm -rf "$HOME/.config/le-vibe"
fi

if [[ -n "$PURGE_WORKSPACE" ]]; then
  if [[ "$PURGE_WORKSPACE" != /* ]]; then
    echo "uninstall-le-vibe-local: --purge-workspace must be an absolute path." >&2
    exit 2
  fi
  if [[ "$PURGE_WORKSPACE" == "/" ]]; then
    echo "uninstall-le-vibe-local: refusing to operate on root path '/'" >&2
    exit 2
  fi
  echo "==> Removing workspace memory: $PURGE_WORKSPACE/.lvibe"
  rm -rf "$PURGE_WORKSPACE/.lvibe"
fi

echo "==> Refreshing caches"
hash -r
if have_cmd update-desktop-database; then sudo update-desktop-database >/dev/null 2>&1 || true; fi
if have_cmd gtk-update-icon-cache; then sudo gtk-update-icon-cache /usr/share/icons/hicolor >/dev/null 2>&1 || true; fi

echo "==> Verification"
if command -v lvibe >/dev/null 2>&1; then
  echo "WARN: lvibe is still on PATH: $(command -v lvibe)"
else
  echo "OK: lvibe not on PATH"
fi
if have_cmd dpkg && dpkg -l 2>/dev/null | awk '{print $2}' | rg -n "^(le-vibe|le-vibe-ide)$" >/dev/null 2>&1; then
  echo "WARN: dpkg still reports le-vibe packages installed."
else
  echo "OK: dpkg does not report le-vibe/le-vibe-ide installed"
fi

echo "==> Done."
