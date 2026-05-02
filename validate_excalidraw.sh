#!/usr/bin/env bash
# Validate .excalidraw files for text overflow + binding consistency.
#
# Usage:
#   ./validate_excalidraw.sh                        # batch: every .excalidraw under output/ + temp/
#   ./validate_excalidraw.sh path/to/file.excalidraw [more.excalidraw]
#   ./validate_excalidraw.sh path/to/dir/
#   ./validate_excalidraw.sh --fix path/to/file.excalidraw   # auto-fix safe binding issues
#   ./validate_excalidraw.sh --json                 # JSON report

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_REF_DIR="$SCRIPT_DIR/.claude/skills/excalidraw-diagram/references"
GLOBAL_REF_DIR="/Users/charles/.codex/skills/excalidraw-diagram/references"

if [[ -f "$LOCAL_REF_DIR/validate_excalidraw.py" ]]; then
  REF_DIR="$LOCAL_REF_DIR"
elif [[ -f "$GLOBAL_REF_DIR/validate_excalidraw.py" ]]; then
  REF_DIR="$GLOBAL_REF_DIR"
else
  echo "找不到 validate_excalidraw.py。請確認 .claude/skills/excalidraw-diagram/references/ 已存在。" >&2
  exit 1
fi

VALIDATE_SCRIPT="$REF_DIR/validate_excalidraw.py"

if ! command -v uv >/dev/null 2>&1; then
  echo "找不到 uv，請先安裝 uv。" >&2
  exit 1
fi

# First-time setup: install playwright + chromium if missing.
if ! (cd "$REF_DIR" && uv run python -c "from playwright.sync_api import sync_playwright" >/dev/null 2>&1); then
  echo "📦 首次使用，安裝 Playwright chromium..." >&2
  (cd "$REF_DIR" && uv sync && uv run playwright install chromium)
fi

# Resolve relative paths to absolute before changing directory, otherwise
# the python script (which runs from $REF_DIR) won't find them.
ARGS=()
for arg in "$@"; do
  case "$arg" in
    --*)
      ARGS+=("$arg")
      ;;
    *)
      if [[ -e "$arg" ]]; then
        if [[ "$arg" = /* ]]; then
          ARGS+=("$arg")
        else
          ARGS+=("$(cd "$(dirname "$arg")" && pwd)/$(basename "$arg")")
        fi
      else
        ARGS+=("$arg")
      fi
      ;;
  esac
done

# When no path argument given, default to repo's output/ + temp/.
HAS_PATH=0
for arg in "${ARGS[@]:-}"; do
  if [[ "$arg" != --* ]]; then
    HAS_PATH=1
    break
  fi
done
if [[ $HAS_PATH -eq 0 ]]; then
  [[ -d "$SCRIPT_DIR/output" ]] && ARGS+=("$SCRIPT_DIR/output")
  [[ -d "$SCRIPT_DIR/temp" ]] && ARGS+=("$SCRIPT_DIR/temp")
fi

cd "$REF_DIR"
exec uv run python "$VALIDATE_SCRIPT" "${ARGS[@]}"
