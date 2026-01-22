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
  "/Users/sggmico/course/.gemini/skills"
  "/Users/sggmico/ws/cc/flow-ai/.gemini/skills"
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

FLAT_DIR="$(mktemp -d)"
SEEN_LIST="$(mktemp)"
trap 'rm -rf "$FLAT_DIR" "$SEEN_LIST"' EXIT

conflicts=()

while IFS= read -r -d '' action_dir; do
  action="$(basename "$action_dir")"
  if grep -Fqx "$action" "$SEEN_LIST"; then
    prev_dir="$(awk -F '\t' -v name="$action" '$1==name{print $2; exit}' "$SEEN_LIST")"
    conflicts+=("$action: $prev_dir and $action_dir")
  else
    printf "%s\t%s\n" "$action" "$action_dir" >> "$SEEN_LIST"
  fi
done < <(find "$SRC_DIR" -mindepth 2 -maxdepth 2 -type d -print0)

if (( ${#conflicts[@]} > 0 )); then
  conflict_report="$SRC_DIR/sync_conflicts.txt"
  {
    echo "skill name conflicts detected:"
    printf '%s\n' "${conflicts[@]}"
  } > "$conflict_report"
  echo "conflicts found; see $conflict_report" >&2
  exit 1
fi

while IFS=$'\t' read -r action src_dir; do
  [[ -n "$action" && -n "$src_dir" ]] || continue
  dst_dir="$FLAT_DIR/$action"
  mkdir -p "$dst_dir"
  rsync "${RSYNC_FLAGS[@]}" "$src_dir/" "$dst_dir/"
done < "$SEEN_LIST"

for target in "${TARGET_DIRS[@]}"; do
  mkdir -p "$target"
  rsync "${RSYNC_FLAGS[@]}" "$FLAT_DIR/" "$target/"
  echo "synced to $target"
done
