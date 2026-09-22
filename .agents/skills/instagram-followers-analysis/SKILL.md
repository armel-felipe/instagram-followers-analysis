---
name: instagram-followers-analysis
description: >
  Parses an Instagram data export folder (containing following.html and
  followers_1.html under connections/followers_and_following/) OR fetches
  the data directly via Instaloader, and generates a self-contained HTML
  page with all unique profiles, filterable by relationship status: mutual,
  churners (we follow but they don't follow back) and onboarding (they
  follow us but we don't follow back). Use this skill whenever the user
  mentions Instagram followers, following, churn, unfollow, or wants to
  analyze their Instagram connections from a data export. If the user wants
  to update/refresh data without a manual export, use the fetch mode.
---

# Instagram Followers Analysis

## What this skill does

Produces a single-file HTML dashboard with:

- **Summary cards**: total unique profiles, mutual, churners, onboarding
- **Searchable, sortable table** of every profile
- **Status tags** for each relationship type
- **Dates** (export mode only) showing when you started following / when they started following you

The output is fully offline — all data is embedded in the HTML — so the
resulting file can be shared or opened anywhere without a server.

## Two modes

### Mode 1: From data export (official, no password needed)

Parse `following.html` and `followers_1.html` from an Instagram download.

```bash
python3 scripts/parse_instagram.py <path-to-instagram-export-folder> [-o output.html]
```

Includes dates. Requires the manual export download.

### Mode 2: Direct fetch via Instaloader (no export needed)

Fetches followers/following lists directly from Instagram using login.

```bash
pip install instaloader
python3 scripts/fetch_instagram.py --username YOUR_IG_USERNAME [-o output.html]
```

First run prompts for password and caches the session in
`~/.config/instaloader/session-YOUR_IG_USERNAME`. Subsequent runs connect
directly. Set `IG_PASSWORD` to avoid interactive prompt.

> Does not include dates (Instaloader doesn't provide them).

> **Python note:** Requires `_lzma`. On macOS use `/usr/bin/python3` if
> pyenv builds lack the module.

## How it works

1. Reads profile blocks from either the export HTML files or via the API
2. Extracts the username (from the `href`) and the date (export mode)
3. Merges both sets into a single list of unique profiles
4. Computes the relationship status for each
5. Embeds all data as a JSON array inside a self-contained HTML page with
   vanilla JavaScript filtering and sorting

## Relationship categories

| Category | Definition |
|----------|-----------|
| **Mutual** | You follow them and they follow you |
| **Churner** | You follow them but they do not follow you back |
| **Onboarding** | They follow you but you do not follow them back |

## Files

- `SKILL.md` — this file
- `scripts/parse_instagram.py` — parser + HTML generator (export mode)
- `scripts/fetch_instagram.py` — direct fetch + HTML generator (Instaloader mode)
