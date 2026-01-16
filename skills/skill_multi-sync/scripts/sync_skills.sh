#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
SRC_DIR="$ROOT_DIR/skills"

TARGET_DIRS=(
  "$HOME/.claude/skills"
  "$HOME/.codex/skills"
  "$HOME/.gemini/skills"
  "/Users/sggmico/ws/cc/learn-flow/.gemini/skills"
  "/Users/sggmico/ws/cc/agent-flow-ws/.gemini/skills"
)
if [[ -n "${SYNC_TARGETS:-}" ]]; then
  IFS=',:' read -r -a TARGET_DIRS <<< "$SYNC_TARGETS"
fi

if [[ ! -d "$SRC_DIR" ]]; then
  echo "source skills dir not found: $SRC_DIR" >&2
  exit 1
fi

RSYNC_FLAGS=(-a --delete --exclude '.DS_Store' --exclude '.*' --filter 'P .*')
if [[ "${SYNC_DRY_RUN:-}" == "1" ]]; then
  RSYNC_FLAGS+=(--dry-run --itemize-changes)
fi

for target in "${TARGET_DIRS[@]}"; do
  mkdir -p "$target"
  rsync "${RSYNC_FLAGS[@]}" "$SRC_DIR/" "$target/"
  echo "synced to $target"
done
