---
name: instagram-followers-analysis
description: >
  Parses an Instagram data export folder (containing following.html and
  followers_1.html under connections/followers_and_following/) and generates
  a self-contained HTML page with all unique profiles, filterable by
  relationship status: mutual, churners (we follow but they don't follow back)
  and onboarding (they follow us but we don't follow back). Use this skill
  whenever the user mentions Instagram followers, following, churn, unfollow,
  or wants to analyze their Instagram connections from a data export.
---

# Instagram Followers Analysis

## What this skill does

Given a directory containing an Instagram data export (the zip you download
from Instagram → Settings → Your Activity → Download your information),
this skill parses `following.html` and `followers_1.html` and produces a
single-file HTML dashboard with:

- **Summary cards**: total unique profiles, mutual, churners, onboarding
- **Searchable, sortable table** of every profile
- **Status tags** for each relationship type
- **Dates** showing when you started following / when they started following you

The output is fully offline — all data is embedded in the HTML — so the
resulting file can be shared or opened anywhere without a server.

## Prerequisites

- Python 3.6+ (standard library only, no external packages needed)

## Usage

Run the bundled script, pointing it at the export folder:

```bash
python3 scripts/parse_instagram.py <path-to-instagram-export-folder> [-o output.html]
```

The export folder is the one that contains `connections/followers_and_following/`.
If you extracted the zip, this is the top-level folder named
`instagram-<username>-<date>-<hash>/`.

### Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `path` | required | Path to the Instagram export folder |
| `-o` | `instagram_followers_following.html` | Output HTML filename |

### Example

```bash
python3 scripts/parse_instagram.py ~/Downloads/instagram-johndoe-2026-01-15-AB3XK9
# → writes instagram_followers_following.html in the current directory
```

## How it works

1. Reads `connections/followers_and_following/following.html` and
   `followers_1.html`
2. Extracts each profile block (`<div class="pam ...">`) and pulls out the
   username (from the `href`) and the date (from the text matching a
   Portuguese month pattern)
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
- `scripts/parse_instagram.py` — the parser and HTML generator
