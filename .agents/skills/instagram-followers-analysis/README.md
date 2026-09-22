# instagram-followers-analysis

Parses an Instagram data export and generates a self-contained HTML dashboard
with all unique profiles, filterable by relationship status.

Also supports fetching the data directly via Instaloader (no export needed).

## Categories

| Category | Definition |
|----------|-----------|
| **Mutual** | You follow them and they follow you |
| **Churner** | You follow them but they do not follow you back |
| **Onboarding** | They follow you but you do not follow them back |

## Output

A single HTML file (no dependencies, no server needed) with:

- Summary cards (click to filter)
- Searchable, sortable table
- Dates for each relationship direction (export mode only)
- Links to each Instagram profile

## Installation

### Option 1: `.agents/skills/` (Codex / OpenCode)

```bash
git clone https://github.com/armel-felipe/instagram-followers-analysis.git .agents/skills/instagram-followers-analysis
```

### Option 2: `.claude/skills/` (Claude Code)

```bash
git clone https://github.com/armel-felipe/instagram-followers-analysis.git .claude/skills/instagram-followers-analysis
```

### Option 3: `.opencode/skills/` (OpenCode)

```bash
git clone https://github.com/armel-felipe/instagram-followers-analysis.git .opencode/skills/instagram-followers-analysis
```

### Option 4: npm (global)

```bash
npm install -g instagram-followers-analysis
```

## Usage

### Mode 1: From data export (official, no password needed)

```bash
python3 scripts/parse_instagram.py ~/Downloads/instagram-username-2026-01-15-AB3XK9
```

### Mode 2: Direct fetch via Instaloader (no export needed)

```bash
pip install instaloader
python3 scripts/fetch_instagram.py --username YOUR_IG_USERNAME
```

First run prompts for password and caches the session in
`~/.config/instaloader/session-YOUR_IG_USERNAME`. Subsequent runs skip login.

You can also set the password via environment variable:

```bash
IG_PASSWORD=xxx python3 scripts/fetch_instagram.py --username YOUR_IG_USERNAME
```

> **Note:** Requires Python 3.9+ with the `_lzma` module. On macOS the system
> Python (`/usr/bin/python3`) works out of the box; pyenv builds need
> `brew install xz && pyenv install <version>`.

## Requirements

- Python 3.9+ (standard library only)
- Mode 2 additionally requires `pip install instaloader`

## How to get an Instagram export (Mode 1)

1. Go to **Instagram → Settings → Your Activity → Download your information**
2. Request a download (select "Connections" or the full export)
3. Wait for the email with the download link
4. Extract the zip
5. Point this tool at the extracted folder

## License

MIT
