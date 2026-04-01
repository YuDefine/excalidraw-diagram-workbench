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
    --dark|--light)
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

if [[ ! -f "$INPUT_PATH" ]]; then
  echo "找不到檔案：$INPUT_PATH" >&2
  exit 1
fi

if [[ "${INPUT_PATH##*.}" != "excalidraw" ]]; then
  echo "請傳入 .excalidraw 檔案。" >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "找不到 uv，請先安裝 uv。" >&2
  exit 1
fi

if [[ ! -f "$RENDER_SCRIPT" ]]; then
  echo "找不到 render script：$RENDER_SCRIPT" >&2
  exit 1
fi

cd "$RENDER_DIR"
if [[ ${#EXTRA_FLAGS[@]} -gt 0 ]]; then
  uv run python "$RENDER_SCRIPT" "$INPUT_PATH" "${EXTRA_FLAGS[@]}"
else
  uv run python "$RENDER_SCRIPT" "$INPUT_PATH"
fi

OUTPUT_PATH="${INPUT_PATH%.excalidraw}.png"

if [[ -f "$OUTPUT_PATH" ]]; then
  echo "已輸出：$OUTPUT_PATH"
else
  echo "render 已執行，但找不到輸出的 PNG：$OUTPUT_PATH" >&2
  exit 1
fi
