---
name: instagram-refresh
description: >
  Runs the full data refresh pipeline for this Instagram analysis project.
  Archives the previous export, unzips the new Instagram data export, and
  regenerates the HTML dashboard with complete data including dates.
  Automatically finds the newest export zip in ~/Downloads/ if no path is
  given. Use when the user asks to "atualizar dados", "update data",
  "refresh", "rodar atualização", or any request to refresh the Instagram
  follower/following dashboard.
---

# Instagram Data Refresh Pipeline

This is a project-specific skill for the `analise_instagram` workspace.

## How to trigger

The user says "atualizar dados" or similar. The agent then:

1. Checks for the newest `instagram-tubr_cdgirassois-*.zip` in `~/Downloads/`
2. If found, runs the pipeline immediately (no questions needed)
3. If not found, tells the user to download the export first:
   Instagram → Configurações → Your Activity → Download your information
   → select "Connections" → wait for email → download the zip
   → then say "atualizar dados" again

## Running the pipeline

```bash
# Auto-detect newest zip in ~/Downloads/
ZIP=$(ls -t ~/Downloads/instagram-tubr_cdgirassois-*.zip 2>/dev/null | head -1)
bash .agents/skills/instagram-followers-analysis/scripts/update.sh "$ZIP"
```

The script handles everything:

| Step | Action | Confirmation needed |
|------|--------|-------------------|
| 1 | Archives previous export to `~/archive/` | No |
| 2 | Unzips new export to project root | No |
| 3 | Parses and generates HTML with dates | No |
| 4 | Reports counts | No |

## What to do after running

1. Read the counts from the script output
2. Report them to the user
3. If the user asks, open the HTML

## If no zip is found

Tell the user:

> Não encontrei um novo export em ~/Downloads/. Para gerar:
> 1. Instagram → Configurações → Your Activity → Download your information
> 2. Selecione "Connections"
> 3. Espere o e-mail com o link e baixe o zip
> 4. Depois me avise para eu rodar a atualização
