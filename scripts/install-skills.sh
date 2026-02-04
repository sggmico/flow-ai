#!/usr/bin/env bash
set -euo pipefail

REPO="sggmico/flow-ai"
TARGET_DIR="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
MODE="install"
VERSION=""
MIRROR=""
ASSET_PATTERN="flow-ai-skills-.*\\.tar\\.gz"
API_BASE="${GITHUB_API_BASE:-https://api.github.com}"

usage() {
  cat <<'USAGE'
Usage: scripts/install-skills.sh [options]

Options:
  --install              Install skills (default)
  --update               Update skills (same as install)
  --uninstall            Remove installed skills (backup first)
  --rollback             Restore from latest backup
  --version <tag>        Install specific release tag (e.g. v0.1.0)
  --repo <owner/name>    GitHub repo (default: sggmico/flow-ai)
  --target <dir>         Install directory (default: ~/.codex/skills)
  --mirror <url>         Mirror base URL or direct .tar.gz URL
  --asset-pattern <re>   Regex for release asset name
  -h, --help             Show help

Env:
  CODEX_SKILLS_DIR        Override install directory
  GITHUB_API_BASE         Override GitHub API base
USAGE
}

log() { printf '%s\n' "$*"; }
fail() { printf 'error: %s\n' "$*" >&2; exit 1; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing command: $1"
}

download() {
  local url="$1" out="$2"
  curl -fsSL "$url" -o "$out"
}

checksum_verify() {
  local checksum_file="$1" work_dir="$2"
  if command -v sha256sum >/dev/null 2>&1; then
    (cd "$work_dir" && sha256sum -c "$(basename "$checksum_file")")
    return
  fi
  if command -v shasum >/dev/null 2>&1; then
    local line file expected actual
    line="$(cat "$checksum_file")"
    expected="${line%% *}"
    file="${line##* }"
    file="${file#./}"
    actual="$(shasum -a 256 "$work_dir/$file" | awk '{print $1}')"
    [[ "$expected" == "$actual" ]] || fail "checksum mismatch"
    return
  fi
  fail "missing checksum tool: sha256sum or shasum"
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --install) MODE="install"; shift ;;
      --update) MODE="install"; shift ;;
      --uninstall) MODE="uninstall"; shift ;;
      --rollback) MODE="rollback"; shift ;;
      --version) VERSION="$2"; shift 2 ;;
      --repo) REPO="$2"; shift 2 ;;
      --target) TARGET_DIR="$2"; shift 2 ;;
      --mirror) MIRROR="$2"; shift 2 ;;
      --asset-pattern) ASSET_PATTERN="$2"; shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) fail "unknown option: $1" ;;
    esac
  done
}

find_latest_backup() {
  local backup_root="$1"
  ls -1dt "$backup_root"/* 2>/dev/null | head -n 1 || true
}

backup_existing() {
  local backup_root="$1"
  mkdir -p "$backup_root"
  if [[ -d "$TARGET_DIR" && -n "$(ls -A "$TARGET_DIR" 2>/dev/null)" ]]; then
    local ts backup_dir
    ts="$(date +%Y%m%d-%H%M%S)"
    backup_dir="$backup_root/$ts"
    mkdir -p "$backup_dir"
    if command -v rsync >/dev/null 2>&1; then
      rsync -a --exclude '.flowai-install.json' --exclude '.flowai-backups' "$TARGET_DIR/" "$backup_dir/"
    else
      cp -a "$TARGET_DIR/." "$backup_dir/"
    fi
    log "backup saved: $backup_dir"
  fi
}

flatten_skills() {
  local skills_dir="$1" flat_dir="$2"
  local seen_list conflicts
  seen_list="$(mktemp)"
  conflicts=()

  while IFS= read -r -d '' action_dir; do
    local action prev_dir
    action="$(basename "$action_dir")"
    if grep -Fqx "$action" "$seen_list"; then
      prev_dir="$(awk -F '\t' -v name="$action" '$1==name{print $2; exit}' "$seen_list")"
      conflicts+=("$action: $prev_dir and $action_dir")
    else
      printf '%s\t%s\n' "$action" "$action_dir" >> "$seen_list"
    fi
  done < <(find "$skills_dir" -mindepth 2 -maxdepth 2 -type d -print0)

  if (( ${#conflicts[@]} > 0 )); then
    local report="$skills_dir/sync_conflicts.txt"
    {
      echo "skill name conflicts detected:"
      printf '%s\n' "${conflicts[@]}"
    } > "$report"
    rm -f "$seen_list"
    fail "conflicts found; see $report"
  fi

  while IFS=$'\t' read -r action src_dir; do
    [[ -n "$action" && -n "$src_dir" ]] || continue
    local dst_dir="$flat_dir/$action"
    mkdir -p "$dst_dir"
    if command -v rsync >/dev/null 2>&1; then
      rsync -a "$src_dir/" "$dst_dir/"
    else
      cp -a "$src_dir/." "$dst_dir/"
    fi
  done < "$seen_list"

  rm -f "$seen_list"
}

install_from_release() {
  require_cmd curl
  require_cmd tar

  local tmp_dir archive release_json asset_url asset_name checksum_url
  tmp_dir="$(mktemp -d)"
  archive="$tmp_dir/skills.tar.gz"

  if [[ -n "$MIRROR" && "$MIRROR" =~ \\.tar\\.gz$ ]]; then
    asset_url="$MIRROR"
  else
    local release_endpoint
    if [[ -n "$VERSION" ]]; then
      release_endpoint="$API_BASE/repos/$REPO/releases/tags/$VERSION"
    else
      release_endpoint="$API_BASE/repos/$REPO/releases/latest"
    fi
    release_json="$tmp_dir/release.json"
    download "$release_endpoint" "$release_json"

    asset_name="$(python3 - <<'PY'
import json, os, re
import sys
path = sys.argv[1]
pattern = os.environ.get('ASSET_PATTERN', 'flow-ai-skills-.*\\.tar\\.gz')
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
assets = data.get('assets', [])
for asset in assets:
    name = asset.get('name', '')
    if re.match(pattern, name):
        print(name)
        sys.exit(0)
print('')
PY
"$release_json")"

    if [[ -z "$asset_name" ]]; then
      fail "no release asset matched pattern: $ASSET_PATTERN"
    fi

    if [[ -n "$MIRROR" ]]; then
      asset_url="$MIRROR/$asset_name"
    else
      asset_url="https://github.com/$REPO/releases/download/$(python3 - <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    data = json.load(f)
print(data.get('tag_name', ''))
PY
"$release_json")/$asset_name"
    fi

    checksum_url="$(python3 - <<'PY'
import json, sys
path, asset_name = sys.argv[1], sys.argv[2]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
for asset in data.get('assets', []):
    name = asset.get('name', '')
    if name == asset_name + '.sha256':
        print(asset.get('browser_download_url', ''))
        break
PY
"$release_json" "$asset_name")"
  fi

  log "downloading: $asset_url"
  download "$asset_url" "$archive"

  if [[ -n "${checksum_url:-}" ]]; then
    log "verifying checksum"
    download "$checksum_url" "$tmp_dir/skills.sha256"
    checksum_verify "$tmp_dir/skills.sha256" "$tmp_dir"
  fi

  tar -xzf "$archive" -C "$tmp_dir"

  local skills_dir
  local manifest_path
  manifest_path="$(find "$tmp_dir" -type f -path '*/skills/manifest.json' -print -quit || true)"
  if [[ -n "$manifest_path" ]]; then
    skills_dir="$(dirname "$manifest_path")"
  else
    skills_dir=""
  fi
  if [[ -z "$skills_dir" ]]; then
    skills_dir="$(find "$tmp_dir" -type d -name skills -print -quit)"
  fi
  [[ -n "$skills_dir" ]] || fail "skills directory not found in archive"

  local flat_dir
  flat_dir="$(mktemp -d)"
  flatten_skills "$skills_dir" "$flat_dir"

  local backup_root
  backup_root="${TARGET_DIR}.backups"
  backup_existing "$backup_root"

  rm -rf "$TARGET_DIR"
  mkdir -p "$TARGET_DIR"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$flat_dir/" "$TARGET_DIR/"
  else
    cp -a "$flat_dir/." "$TARGET_DIR/"
  fi

  cat <<META > "$TARGET_DIR/.flowai-install.json"
{
  "repo": "$REPO",
  "version": "${VERSION:-latest}",
  "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "source": "$asset_url"
}
META

  log "installed to: $TARGET_DIR"
}

uninstall_skills() {
  local backup_root
  backup_root="${TARGET_DIR}.backups"
  backup_existing "$backup_root"
  rm -rf "$TARGET_DIR"
  log "removed: $TARGET_DIR"
}

rollback_skills() {
  local backup_root latest
  backup_root="${TARGET_DIR}.backups"
  latest="$(find_latest_backup "$backup_root")"
  [[ -n "$latest" ]] || fail "no backups found in $backup_root"
  rm -rf "$TARGET_DIR"
  mkdir -p "$TARGET_DIR"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$latest/" "$TARGET_DIR/"
  else
    cp -a "$latest/." "$TARGET_DIR/"
  fi
  log "restored from: $latest"
}

main() {
  parse_args "$@"
  case "$MODE" in
    install) install_from_release ;;
    uninstall) uninstall_skills ;;
    rollback) rollback_skills ;;
    *) fail "invalid mode" ;;
  esac
}

main "$@"
