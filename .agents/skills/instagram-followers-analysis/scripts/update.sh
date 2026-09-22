#!/bin/bash
# Instagram Followers Analysis — Update script
# Archives the previous export, unzips a new one, and regenerates the HTML.

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
ARCHIVE_DIR="$HOME/archive"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <path-to-new-export.zip>"
  exit 1
fi

ZIP_PATH="$1"

if [ ! -f "$ZIP_PATH" ]; then
  echo "Error: file not found: $ZIP_PATH"
  exit 1
fi

# Step 1: Archive previous export folders from project root
# Use timestamp subfolder to avoid conflicts with previous archives
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVE_SUBDIR="$ARCHIVE_DIR/$TIMESTAMP"
mkdir -p "$ARCHIVE_SUBDIR"

for old_dir in "$PROJECT_ROOT"/connections "$PROJECT_ROOT"/files; do
  if [ -d "$old_dir" ]; then
    echo "Archiving: $(basename "$old_dir") -> ~/archive/$TIMESTAMP/"
    mv "$old_dir" "$ARCHIVE_SUBDIR/"
  fi
done

# Step 2: Unzip the new export into project root
echo "Unzipping $ZIP_PATH -> $PROJECT_ROOT"
unzip -q -o "$ZIP_PATH" -d "$PROJECT_ROOT/"

EXPORT_DIR="$PROJECT_ROOT"
if [ ! -d "$EXPORT_DIR/connections/followers_and_following" ]; then
  echo "Error: connections/followers_and_following/ not found after unzip"
  exit 1
fi

echo "Export folder: $EXPORT_DIR"

# Step 3: Parse and generate HTML
cd "$SCRIPT_DIR"
/usr/bin/python3 parse_instagram.py "$EXPORT_DIR" -o "$PROJECT_ROOT/instagram_followers_following.html"

echo ""
echo "Done. Updated: $PROJECT_ROOT/instagram_followers_following.html"
