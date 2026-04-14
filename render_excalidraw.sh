#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_RENDER_DIR="$SCRIPT_DIR/.claude/skills/excalidraw-diagram/references"
GLOBAL_RENDER_DIR="/Users/charles/.codex/skills/excalidraw-diagram/references"

if [[ -f "$LOCAL_RENDER_DIR/render_excalidraw.py" ]]; then
  RENDER_DIR="$LOCAL_RENDER_DIR"
else
  RENDER_DIR="$GLOBAL_RENDER_DIR"
fi

RENDER_SCRIPT="$RENDER_DIR/render_excalidraw.py"

# Separate input path from flags
INPUT_PATH=""
EXTRA_FLAGS=()

for arg in "$@"; do
  case "$arg" in
    --dark|--light|--scale|--width|-s|-w)
      EXTRA_FLAGS+=("$arg")
      ;;
    *)
      if [[ -z "$INPUT_PATH" ]]; then
        INPUT_PATH="$arg"
      else
        EXTRA_FLAGS+=("$arg")
      fi
      ;;
  esac
done

INPUT_PATH="${INPUT_PATH:-$SCRIPT_DIR/output/diagram.excalidraw}"

# Resolve to absolute path before cd
[[ "$INPUT_PATH" != /* ]] && INPUT_PATH="$(pwd)/$INPUT_PATH"

if ! command -v uv >/dev/null 2>&1; then
  echo "找不到 uv，請先安裝 uv。" >&2
  exit 1
fi

if [[ ! -f "$RENDER_SCRIPT" ]]; then
  echo "找不到 render script：${RENDER_SCRIPT}" >&2
  exit 1
fi

# --- Single file mode ---
render_one() {
  local file="$1"
  cd "$RENDER_DIR"
  if [[ ${#EXTRA_FLAGS[@]} -gt 0 ]]; then
    uv run python "$RENDER_SCRIPT" "$file" "${EXTRA_FLAGS[@]}"
  else
    uv run python "$RENDER_SCRIPT" "$file"
  fi
}

# --- Directory mode ---
if [[ -d "$INPUT_PATH" ]]; then
  # Strip trailing slash for cleaner display
  INPUT_PATH="${INPUT_PATH%/}"

  FILES=()
  while IFS= read -r -d '' f; do
    FILES+=("$f")
  done < <(find "$INPUT_PATH" -maxdepth 1 -name '*.excalidraw' -print0 | sort -z)

  if [[ ${#FILES[@]} -eq 0 ]]; then
    echo "目錄中沒有 .excalidraw 檔案：${INPUT_PATH}"
    exit 0
  fi

  TOTAL=${#FILES[@]}
  OK=0
  FAIL=0

  echo "批次渲染 ${TOTAL} 個檔案（from ${INPUT_PATH}）"
  echo ""

  for f in "${FILES[@]}"; do
    NAME="$(basename "$f")"
    IDX=$((OK + FAIL + 1))
    printf "  [%d/%d] %s ... " "$IDX" "$TOTAL" "$NAME"
    if OUTPUT=$(render_one "$f" 2>&1); then
      PNG="${f%.excalidraw}.png"
      if [[ -f "$PNG" ]]; then
        echo "✓ → $(basename "$PNG")"
      else
        echo "✓ (output: $OUTPUT)"
      fi
      ((OK++))
    else
      echo "✗"
      echo "    $OUTPUT" >&2
      ((FAIL++))
    fi
  done

  echo ""
  echo "完成：${OK} 成功, ${FAIL} 失敗（共 ${TOTAL} 個）"
  exit 0
fi

# --- Single file mode ---
if [[ ! -f "$INPUT_PATH" ]]; then
  echo "找不到檔案：${INPUT_PATH}" >&2
  exit 1
fi

if [[ "${INPUT_PATH##*.}" != "excalidraw" ]]; then
  echo "請傳入 .excalidraw 檔案或包含 .excalidraw 的目錄。" >&2
  exit 1
fi

render_one "$INPUT_PATH"

OUTPUT_PATH="${INPUT_PATH%.excalidraw}.png"

if [[ -f "$OUTPUT_PATH" ]]; then
  echo "已輸出：${OUTPUT_PATH}"
else
  echo "render 已執行，但找不到輸出的 PNG：${OUTPUT_PATH}" >&2
  exit 1
fi
