#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(pwd)}"
SKILLS_DIR="$ROOT_DIR/skills"
OUT_DIR="$ROOT_DIR/dist"

if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "skills dir not found: $SKILLS_DIR" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

version="${RELEASE_VERSION:-$(date +%Y.%m.%d)}"
archive="$OUT_DIR/flow-ai-skills-$version.tar.gz"
checksum="$archive.sha256"

if [[ ! -f "$SKILLS_DIR/manifest.json" ]]; then
  echo "manifest not found: $SKILLS_DIR/manifest.json" >&2
  echo "run: python3 scripts/gen-skills-manifest.py" >&2
  exit 1
fi

# tar 包内保留 skills 目录, 便于安装脚本定位
(tar -C "$ROOT_DIR" -czf "$archive" skills)

if command -v sha256sum >/dev/null 2>&1; then
  (cd "$OUT_DIR" && sha256sum "$(basename "$archive")" > "$(basename "$checksum")")
elif command -v shasum >/dev/null 2>&1; then
  (cd "$OUT_DIR" && shasum -a 256 "$(basename "$archive")" > "$(basename "$checksum")")
else
  echo "missing checksum tool: sha256sum or shasum" >&2
  exit 1
fi

echo "release assets generated:"
echo "- $archive"
echo "- $checksum"
