---
name: instagram-refresh
description: >
  Runs the data refresh for this Instagram analysis project. Fetches the
  latest followers/following lists via Instaloader and regenerates the HTML
  dashboard. Use when the user asks to "atualizar dados", "update data",
  "refresh", "rodar atualização", or any request to get fresh Instagram
  follower/following numbers without a manual export.
---

# Instagram Data Refresh

This is a project-specific skill for the `analise_instagram` workspace.
It wraps `fetch_instagram.py` from the `instagram-followers-analysis` skill
with the project's known configuration.

## Project configuration

| Setting | Value |
|---------|-------|
| Instagram username | `tubr_cdgirassois` |
| Output file | `instagram_followers_following.html` (project root) |
| Session cache | `~/.config/instaloader/session-tubr_cdgirassois` |
| Python to use | `/usr/bin/python3` (system — pyenv 3.12 lacks `_lzma`) |

## How to run

```bash
/usr/bin/python3 .agents/skills/instagram-followers-analysis/scripts/fetch_instagram.py --username tubr_cdgirassois -o instagram_followers_following.html
```

If a session file already exists at the cache path, the script connects
directly without prompting. On the first run (or after session expiry) it
prompts for the password interactively, or you can set `IG_PASSWORD` as an
environment variable.

## What to tell the user after running

1. Confirm the counts printed in the output (total, mutual, churners, onboarding)
2. Open the regenerated `instagram_followers_following.html` if asked
3. Note that this uses the direct-fetch mode, so dates are not available
   (unlike the export mode, which includes them)

## Troubleshooting

- **"Instaloader not installed"** → `pip install instaloader`
- **`ModuleNotFoundError: No module named '_lzma'`** → use `/usr/bin/python3` instead of pyenv
- **Login challenge / checkpoint** → open the Instagram app or browser, complete the verification, then retry
- **Session expired** → delete `~/.config/instaloader/session-tubr_cdgirassois` and run again
