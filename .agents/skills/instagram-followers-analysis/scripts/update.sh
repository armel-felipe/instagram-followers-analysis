#!/bin/bash
# Instagram Followers Analysis — Update script
# Archives the previous export, unzips a new one, and regenerates the HTML.
#
# Usage:
#   ./update.sh <path-to-new-export.zip>
#
# The script assumes it lives in .agents/skills/instagram-followers-analysis/scripts/
# relative to the project root.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
ARCHIVE_DIR="$PROJECT_ROOT/~archive"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <path-to-new-export.zip>"
  echo ""
  echo "Example:"
  echo "  ./update.sh ~/Downloads/instagram-tubr_cdgirassois-2026-09-22-XXXXX.zip"
  exit 1
fi

ZIP_PATH="$1"

if [ ! -f "$ZIP_PATH" ]; then
  echo "Error: file not found: $ZIP_PATH"
  exit 1
fi

# Step 1: Archive previous export folder(s)
mkdir -p "$PROJECT_ROOT/~archive"
for old_dir in "$PROJECT_ROOT"/instagram-tubr_cdgirassois-*; do
  if [ -d "$old_dir" ]; then
    echo "Archiving: $(basename "$old_dir") -> ~archive/"
    mv "$old_dir" "$PROJECT_ROOT/~archive/"
  fi
done

# Step 2: Unzip the new export
BASENAME=$(basename "$ZIP_PATH" .zip)
echo "Unzipping $ZIP_PATH -> $PROJECT_ROOT/$BASENAME"
unzip -q -o "$ZIP_PATH" -d "$PROJECT_ROOT/"
EXPORT_DIR="$PROJECT_ROOT/$BASENAME"

if [ ! -d "$EXPORT_DIR/connections/followers_and_following" ]; then
  # Sometimes the zip has a nested folder
  NESTED=$(find "$EXPORT_DIR" -maxdepth 1 -type d -name "instagram-*" | head -1)
  if [ -n "$NESTED" ]; then
    EXPORT_DIR="$NESTED"
  else
    echo "Error: connections/followers_and_following/ not found in extracted files"
    exit 1
  fi
fi

echo "Export folder: $EXPORT_DIR"

# Step 3: Parse and generate HTML
cd "$SCRIPT_DIR"
/usr/bin/python3 parse_instagram.py "$EXPORT_DIR" -o "$PROJECT_ROOT/instagram_followers_following.html"

echo ""
echo "Done. Updated: $PROJECT_ROOT/instagram_followers_following.html"
