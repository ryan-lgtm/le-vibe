#!/usr/bin/env bash
# Stage an AppDir for Lé Vibe (H7) and optionally run appimagetool (PRODUCT_SPEC — lvibe).
# Pytest: le-vibe/tests/test_flatpak_appimage_doc_h7_contract.py; verify JSON stubs —
#   le-vibe/tests/test_verify_step14_closeout_contract.py (fcntl lock; .gitignore: le-vibe/.pytest-verify-step14-contract.lock).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
APPDIR="${ROOT}/packaging/appimage/AppDir"
TOOL="${APPIMAGETOOL:-appimagetool}"

rm -rf "${APPDIR}"
mkdir -p "${APPDIR}/usr/share/le-vibe" "${APPDIR}/usr/bin"

cp -a "${ROOT}/le-vibe" "${APPDIR}/usr/share/le-vibe/"
python3 -m pip install --target "${APPDIR}/usr/share/le-vibe/pythondist" -r "${ROOT}/le-vibe/requirements.txt"

install -m0755 "${ROOT}/packaging/appimage/AppRun" "${APPDIR}/AppRun"
sed 's|^Exec=.*|Exec=AppRun %F|' "${ROOT}/packaging/applications/le-vibe.desktop" >"${APPDIR}/le-vibe.desktop"
chmod 0644 "${APPDIR}/le-vibe.desktop"
install -D -m0644 "${ROOT}/packaging/icons/hicolor/scalable/apps/le-vibe.svg" "${APPDIR}/le-vibe.svg"

echo "AppDir ready: ${APPDIR}"
echo "Runtime uses the host python3 (see packaging/appimage/README.md)."

if command -v "${TOOL}" >/dev/null 2>&1; then
  out="${ROOT}/packaging/Le-vibe-x86_64.AppImage"
  "${TOOL}" "${APPDIR}" "${out}"
  echo "Wrote ${out}"
else
  echo "appimagetool not found; staged AppDir only. Install appimagetool to emit the .AppImage." >&2
fi
