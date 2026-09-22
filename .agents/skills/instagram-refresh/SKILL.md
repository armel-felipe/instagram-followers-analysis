---
name: instagram-refresh
description: >
  Runs the full data refresh pipeline for this Instagram analysis project.
  Archives the previous export folder, unzips the new Instagram data export
  (provided by the user), and regenerates the HTML dashboard with complete
  data including dates. Use when the user asks to "atualizar dados",
  "update data", "refresh", "rodar atualização", or any request to refresh
  the Instagram follower/following dashboard. The user must provide the path
  to the downloaded .zip export file.
---

# Instagram Data Refresh Pipeline

This is a project-specific skill for the `analise_instagram` workspace.
It runs the official Instagram data export pipeline: archive previous
export → unzip new export → regenerate HTML.

## Pipeline steps

1. **Archive**: moves any existing `instagram-tubr_cdgirassois-*` folder to
   `~/archive/` (creates the folder if it doesn't exist)
2. **Unzip**: extracts the new export zip to the project root
3. **Parse**: runs `parse_instagram.py` to generate the HTML dashboard

## How to run

```bash
bash .agents/skills/instagram-followers-analysis/scripts/update.sh <path-to-new-export.zip>
```

Example:

```bash
bash .agents/skills/instagram-followers-analysis/scripts/update.sh ~/Downloads/instagram-tubr_cdgirassois-2026-09-22-AB3XK9.zip
```

## What the script does

| Step | Action |
|------|--------|
| 1 | Moves `instagram-tubr_cdgirassois-*` folders to `~/archive/` |
| 2 | Unzips the new export to the project root |
| 3 | Runs `parse_instagram.py` (export mode — includes dates) |
| 4 | Writes `instagram_followers_following.html` in the project root |

## Prerequisites

The user must download the export first:

1. Instagram → Settings → Your Activity → Download your information
2. Select "Connections" (or full export)
3. Wait for the email with the download link
4. Download the zip

Instagram does not allow programmatic download of the export (requires email
confirmation), so step 2 is manual. The agent runs steps 1 and 3-4 after the
user provides the zip path.

## What to tell the user after running

1. Confirm the counts printed in the output (total, mutual, churners, onboarding)
2. The HTML includes dates for each relationship direction
3. Previous export is safely archived in `~/archive/`

## Files

- `SKILL.md` — this file
- The pipeline script lives in
  `.agents/skills/instagram-followers-analysis/scripts/update.sh`
