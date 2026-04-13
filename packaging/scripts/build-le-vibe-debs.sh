#!/usr/bin/env bash
# One-shot: build le-vibe (stack) and optionally le-vibe-ide .deb artifacts.
# --with-ide delegates to packaging/scripts/build-le-vibe-ide-deb.sh (stage + dpkg-buildpackage + optional lintian).
# Requires: find (findutils), sort, head (coreutils) to locate emitted *.deb files beside the repo.
# Authority: docs/PM_DEB_BUILD_ITERATION.md — PM-scoped convenience; not a v1 production gate.
# H1 / §7.3: default CI uploads le-vibe-deb (stack le-vibe .deb + SBOM + SHA256SUMS only); --with-ide here adds le-vibe-ide_*.deb for full-product drops — docs/apt-repo-releases.md (IDE package).
# Optional: LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 with --with-ide runs ci-editor-gate.sh before build-le-vibe-ide-deb.sh (§7.3 product.json identity).
# Fresh clone (14.b): git submodule update --init editor/vscodium — editor/README.md when building --with-ide and editor/vscodium/ is empty.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT"

WITH_IDE=0
DO_INSTALL=0
ASSUME_YES=0
VS_BUILD=""

usage() {
  cat <<'EOF'
Usage: packaging/scripts/build-le-vibe-debs.sh [options]

The script resolves the monorepo root from its own path and cds there before building —
your shell cwd does not need to be the clone root (doc examples still use paths from repo root).

Build Debian binary packages from this monorepo:
  (default)        Build the le-vibe stack .deb only.
  --with-ide       Also build le-vibe-ide (requires editor/vscodium/VSCode-linux-*).
  --install        After build, sudo apt install the produced .deb files (interactive sudo).
  --yes            Non-interactive apt (adds -y for apt install).
  --vs-build PATH  Use this VSCode-linux-* directory for IDE staging (implies --with-ide).
  -h, --help       Show this message and exit.

Common invocations (repository root):
  packaging/scripts/build-le-vibe-debs.sh
  packaging/scripts/build-le-vibe-debs.sh --install [--yes]
  packaging/scripts/build-le-vibe-debs.sh --with-ide
  LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 packaging/scripts/build-le-vibe-debs.sh --with-ide
  DEB_BUILD_OPTIONS=parallel=$(nproc) packaging/scripts/build-le-vibe-debs.sh

Environment:
  DEB_BUILD_OPTIONS           Passed through to dpkg-buildpackage when set (e.g. parallel=$(nproc) for faster stack builds).
  LEVIBE_IDE_LINTIAN_STRICT   When set to 1, fail the IDE build if lintian fails (see packaging/scripts/build-le-vibe-ide-deb.sh).
  LEVIBE_STAGE_IDE_ASSERT_BRAND  When set to 1, fail IDE staging if VSCode-linux-*/resources/app/product.json lacks Lé Vibe strings (§7.3 — packaging/scripts/stage-le-vibe-ide-deb.sh).
  LEVIBE_STAGE_IDE_VERBOSE   When set to 1, print a line when §7.3 identity check passes (same staging script).
  LEVIBE_EDITOR_GATE_ASSERT_BRAND  When set to 1 with --with-ide, run packaging/scripts/ci-editor-gate.sh first (same §7.3 product.json check as ./editor/smoke.sh — fails fast before staging).

Prerequisites (stack): debhelper, build-essential, dpkg-dev (sudo apt install build-essential debhelper).
Prerequisites (IDE):  a successful dev/build.sh under editor/vscodium (see editor/BUILD.md).
  Without editor/vscodium/VSCode-linux-*, --with-ide fails after the stack .deb — fetch vscode
  (./editor/fetch-vscode-sources.sh), then ./packaging/scripts/ci-vscodium-linux-dev-build.sh, or see editor/BUILD.md.
  Fresh clone (14.b): git submodule update --init editor/vscodium from repo root if editor/vscodium/ is empty — editor/README.md.

Artifacts:
  Stack:  typically ../le-vibe_*.deb (parent of repo root — standard dpkg-buildpackage).
  IDE:    packaging/le-vibe-ide_*.deb (see packaging/debian-le-vibe-ide/README.md).

Publishing / releases (H1):
  docs/apt-repo-releases.md — Dual changelog discipline (debian/changelog vs CHANGELOG.md); Pre-publish artifact checklist, SHA256SUMS
  when tagging; dpkg-parsechangelog -S Version -l debian/changelog before stack v... tag / gh release — same doc (Versioned changelog).
  default ci.yml le-vibe-deb is stack-only vs full-product Stack + IDE drops.
  Combined drop: CI stack artifact + le-vibe-ide built separately — merge into one folder, regenerate SHA256SUMS
  (CI SHA256SUMS alone is wrong once you add the second .deb) — same doc (Pre-publish — Combined drop).
  Full-product GitHub Release (both .debs on one Release) — docs/apt-repo-releases.md (Checklist — full-product GitHub Release).
  Tagging discipline — ide-v* (linux_compile CI) vs stack debian/changelog: same doc (Tagging discipline).
  Stack v... release tags vs ide-v* — apt-repo-releases.md (Stack release tags vs ide-v* — publishing).
  CI le-vibe-deb artifact is a .zip — unzip before sha256sum -c or lvibe verify-checksums (same doc — GitHub Releases + checksums).
  H1 quick pointer (stack-only vs full-product checklists before gh release create) — docs/apt-repo-releases.md (GitHub Releases + checksums).
  apt-repo-releases.md Related docs (H1 index) — CHANGELOG.md (dual changelog), ci-qa-hardening→editor/README (H3 Full Linux compile), PM_STAGE_MAP (H1 vs §7.3), PM_DEB_BUILD_ITERATION (this one-shot).

Full-product (--with-ide): When both .deb files are produced, the script prints a Full-product install
  line (sudo apt install with both resolved paths) before "Done." — docs/PM_DEB_BUILD_ITERATION.md
  (Success output (--with-ide)); releases — docs/apt-repo-releases.md (IDE package, Maintainer build output).
  Before attaching to a GitHub Release, regenerate SHA256SUMS over both .deb files + SBOM if shipped — same doc (Pre-publish Integrity).
  If --with-ide is set but le-vibe-ide_*.deb is not found under packaging/ after the IDE build, the script exits with status 1 (§7.3 full-product expectation).

Exit codes:
  0  Success (stack .deb; with --with-ide, both stack and packaging/le-vibe-ide_*.deb found).
  1  --with-ide but IDE build failed or le-vibe-ide_*.deb missing under packaging/ — PM_DEB_BUILD_ITERATION.md (Failure (--with-ide)).
  2  Missing dpkg-buildpackage/debhelper, bad CLI, missing find/sort/head, or --install without sudo/apt-get — PM_DEB_BUILD_ITERATION.md (Exit codes (build-le-vibe-debs.sh)).

EOF
}

have_cmd() { command -v "$1" >/dev/null 2>&1; }

require_stack_build_deps() {
  local missing=()
  if ! have_cmd dpkg-buildpackage; then missing+=("dpkg-dev"); fi
  if ! have_cmd dh; then missing+=("debhelper"); fi
  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "build-le-vibe-debs: missing packages: ${missing[*]}" >&2
    echo "  Install: sudo apt install -y build-essential debhelper dpkg-dev" >&2
    exit 2
  fi
}

find_stack_deb() {
  # dpkg-buildpackage from repo root writes *.deb to the parent directory.
  local p
  p="$(find "$(cd "$ROOT/.." && pwd)" -maxdepth 1 -name 'le-vibe_*.deb' -type f 2>/dev/null | sort -r | head -1)"
  if [[ -n "$p" ]]; then
    echo "$p"
    return 0
  fi
  # Some workflows run from a subdir; search repo root parent only.
  p="$(find "$ROOT/.." -maxdepth 1 -name 'le-vibe_*.deb' -type f 2>/dev/null | sort -r | head -1)"
  if [[ -n "$p" ]]; then
    echo "$p"
    return 0
  fi
  echo ""
}

find_ide_deb() {
  local p
  p="$(find "$ROOT/packaging" -maxdepth 1 -name 'le-vibe-ide_*.deb' -type f 2>/dev/null | sort -r | head -1)"
  if [[ -n "$p" ]]; then
    echo "$p"
    return 0
  fi
  echo ""
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-ide) WITH_IDE=1 ;;
    --install) DO_INSTALL=1 ;;
    --yes) ASSUME_YES=1 ;;
    --vs-build)
      VS_BUILD="${2:-}"
      if [[ -z "$VS_BUILD" ]]; then echo "build-le-vibe-debs: --vs-build needs a path" >&2; exit 2; fi
      WITH_IDE=1
      shift
      ;;
    -h|--help) usage; exit 0 ;;
    *) echo "build-le-vibe-debs: unknown option: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

require_stack_build_deps

if ! command -v find >/dev/null 2>&1; then
  echo "build-le-vibe-debs: find not on PATH — install findutils (e.g. sudo apt install findutils) (docs/PM_DEB_BUILD_ITERATION.md)." >&2
  exit 2
fi
if ! command -v sort >/dev/null 2>&1; then
  echo "build-le-vibe-debs: sort not on PATH — install coreutils (e.g. sudo apt install coreutils) (docs/PM_DEB_BUILD_ITERATION.md)." >&2
  exit 2
fi
if ! command -v head >/dev/null 2>&1; then
  echo "build-le-vibe-debs: head not on PATH — install coreutils (e.g. sudo apt install coreutils) (docs/PM_DEB_BUILD_ITERATION.md)." >&2
  exit 2
fi

echo "==> Building stack package (le-vibe) from: $ROOT"
dpkg-buildpackage -us -uc -b

STACK_DEB="$(find_stack_deb)"
if [[ -z "$STACK_DEB" || ! -f "$STACK_DEB" ]]; then
  echo "build-le-vibe-debs: could not locate le-vibe_*.deb under $(cd "$ROOT/.." && pwd) — if dpkg-buildpackage failed, fix errors above; on success the stack .deb is emitted beside the repo directory (../le-vibe_*.deb from repo root)." >&2
else
  echo "==> Stack .deb: $STACK_DEB"
fi

IDE_DEB=""
if [[ "$WITH_IDE" -eq 1 ]]; then
  if [[ "${LEVIBE_EDITOR_GATE_ASSERT_BRAND:-0}" == "1" ]]; then
    echo "==> §7.3 pre-check: ci-editor-gate.sh (LEVIBE_EDITOR_GATE_ASSERT_BRAND=1)"
    LEVIBE_EDITOR_GATE_ASSERT_BRAND=1 "$ROOT/packaging/scripts/ci-editor-gate.sh"
  fi
  echo "==> Building IDE package (le-vibe-ide) via build-le-vibe-ide-deb.sh (stage + dpkg-buildpackage + optional lintian)"
  _ide_args=()
  [[ -n "$VS_BUILD" ]] && _ide_args+=("$VS_BUILD")
  if ! "$ROOT/packaging/scripts/build-le-vibe-ide-deb.sh" "${_ide_args[@]}"; then
    echo "build-le-vibe-debs: §7.3 remediation — produce VSCode-linux-*: ./editor/fetch-vscode-sources.sh (14.b), then ./packaging/scripts/ci-vscodium-linux-dev-build.sh + dev/build.sh (14.e / editor/BUILD.md 14.c), or Docker ./packaging/scripts/docker-le-vibe-vscodium-linux-compile.sh (full compile) / prepare-only ./packaging/scripts/docker-le-vibe-vscodium-prepare-only.sh (branding layers only); then re-run --with-ide; or pass --vs-build PATH. CI vs maintainer bundles: docs/PM_STAGE_MAP.md (H1 vs §7.3 .deb bundles); packaging/debian-le-vibe-ide/README.md." >&2
    exit 1
  fi
  IDE_DEB="$(find_ide_deb)"
  if [[ -n "$IDE_DEB" && -f "$IDE_DEB" ]]; then
    echo "==> IDE .deb: $IDE_DEB"
  else
    echo "build-le-vibe-debs: could not locate le-vibe-ide_*.deb under packaging/ after build-le-vibe-ide-deb.sh — unexpected; see editor/BUILD.md (14.c), docs/PM_STAGE_MAP.md (H1 vs §7.3 .deb bundles), packaging/debian-le-vibe-ide/README.md." >&2
    exit 1
  fi
fi

if [[ "$DO_INSTALL" -eq 1 ]]; then
  if ! have_cmd sudo; then
    echo "build-le-vibe-debs: --install requires sudo" >&2
    exit 2
  fi
  if ! have_cmd apt-get; then
    echo "build-le-vibe-debs: apt-get not on PATH — --install requires apt (Debian/Ubuntu)." >&2
    exit 2
  fi
  APT_ARGS=()
  [[ "$ASSUME_YES" -eq 1 ]] && APT_ARGS+=("-y")
  if [[ -n "$STACK_DEB" && -f "$STACK_DEB" ]]; then
    echo "==> Installing: $STACK_DEB"
    sudo apt-get install "${APT_ARGS[@]}" "$STACK_DEB"
  fi
  if [[ -n "$IDE_DEB" && -f "$IDE_DEB" ]]; then
    echo "==> Installing: $IDE_DEB"
    sudo apt-get install "${APT_ARGS[@]}" "$IDE_DEB"
  fi
fi

# §7.3 — stack .deb is beside the repo directory; IDE .deb is under packaging/ (paths differ; apt accepts both).
if [[ "$WITH_IDE" -eq 1 && -n "$STACK_DEB" && -f "$STACK_DEB" && -n "$IDE_DEB" && -f "$IDE_DEB" ]]; then
  echo "==> Full-product install (paths printed above): sudo apt install \"$STACK_DEB\" \"$IDE_DEB\""
  echo "    Post-install: /usr/share/doc/le-vibe/README.Debian — packaging/debian-le-vibe-ide/README.md (*Install both packages*)"
  echo "    §7.3 maintainer smoke (ci-editor-gate + lvibe ide-prereqs --json, no new .deb): ./editor/verify-73-maintainer.sh — editor/README.md"
fi

echo "==> Done."
