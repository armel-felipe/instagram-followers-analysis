# instagram-followers-analysis

Parses an Instagram data export and generates a self-contained HTML dashboard
with all unique profiles, filterable by relationship status.

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
- Dates for each relationship direction
- Links to each Instagram profile

## Installation

### Option 1: `.agents/skills/` (Codex / OpenCode)

Clone into your project or home directory:

```bash
git clone https://github.com/armel-felipe/instagram-followers-analysis.git .agents/skills/instagram-followers-analysis
```

Or copy manually:

```bash
git clone https://github.com/armel-felipe/instagram-followers-analysis.git /tmp/ifa
cp -r /tmp/ifa .agents/skills/instagram-followers-analysis
rm -rf /tmp/ifa
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

Then run directly:

```bash
npx instagram-followers-analysis <path-to-export>
```

## Usage

```bash
# Standard
python3 .agents/skills/instagram-followers-analysis/scripts/parse_instagram.py ~/Downloads/instagram-username-2026-01-15-AB3XK9

# Custom output filename
python3 .agents/skills/instagram-followers-analysis/scripts/parse_instagram.py ~/Downloads/instagram-username-2026-01-15-AB3XK9 -o my_dashboard.html
```

## Requirements

- Python 3.6+ (standard library only, no pip install needed)

## How to get an Instagram export

1. Go to **Instagram → Settings → Your Activity → Download your information**
2. Request a download (select "Connections" or the full export)
3. Wait for the email with the download link
4. Extract the zip
5. Point this tool at the extracted folder

## License

MIT
