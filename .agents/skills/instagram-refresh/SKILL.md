---
name: instagram-refresh
description: >
  Runs the full data refresh pipeline for this Instagram analysis project.
  Orchestration via browser automation (cua_repl): agent navigates the
  Instagram data export request, the user confirms at each blocking point
  (password/2FA, email link, zip download), then the agent runs the full
  pipeline (archive → unzip → parse → HTML). Use when the user asks to
  "atualizar dados", "update data", "refresh", "rodar atualização".
---

# Instagram Data Refresh Pipeline

This is a project-specific skill for the `analise_instagram` workspace.

## Flow overview

The agent orchestrates everything via the integrated browser. The user only
confirms at three points where Instagram requires human identity verification:

| Phase | Who does it | User interaction |
|-------|------------|-----------------|
| Request export | Agent (browser) | None — agent fills the form |
| Confirm password/2FA | **User** | Agent pauses, asks user to type password or code |
| Confirm email | **User** | Instagram sends email; user must click the link |
| Wait for generation | Nobody | Instagram processes (minutes to hours) |
| Download zip | **User** | Agent pauses, asks user to download |
| Parse + HTML | Agent (terminal) | None — runs update.sh |

## Orchestration steps (for the agent, via cua_repl)

### Phase 1: Request export in browser

```javascript
// 1. Find or create tab in the in-app browser (browser id "2")
let tab = await cua.getTab("2", { browser: "2" });
if (!tab) tab = await cua.createBrowserTab("2");

// 2. Navigate to the data download page
await tab.goto("https://www.instagram.com/accounts/account_recovery/privacy_and_security/data_download/");
// Verify logged in as tubr_cdgirassois — if not, pause and ask user to log in

// 3. Click "Solicitar download" / "Request download"
// 4. Select HTML format
// 5. Select "Connections" / "Seguidores e seguindo"
// 6. Click confirm → Instagram may ask password/2FA
```

**→ PAUSE: tell the user** "O Instagram pedirá a senha ou código 2FA. Quando
aparecer, digite ou me avise para eu aguardar você completar."

### Phase 2: Email confirmation

Instagram sends a confirmation email to the account's registered address.
The user must open it and click the link. The agent **cannot** do this —
Instagram requires human authorization for data exports.

**→ PAUSE: tell the user** "O Instagram enviou um e-mail de confirmação para
o endereço da conta. Abra o e-mail e clique no link para autorizar o export.
Me avise quando terminar."

### Phase 3: Wait + download

The export takes minutes to hours depending on data volume. The user
downloads the zip to `~/Downloads/`.

**→ PAUSE: tell the user** "O export está sendo gerado. Quando o zip aparecer
em ~/Downloads/, me avise para eu rodar o pipeline."

### Phase 4: Run pipeline (fully automated by the agent)

```bash
ZIP=$(ls -t ~/Downloads/instagram-tubr_cdgirassois-*.zip 2>/dev/null | head -1)
bash .agents/skills/instagram-followers-analysis/scripts/update.sh "$ZIP"
```

## When to ask vs. when to proceed

| Situation | Agent behavior |
|-----------|---------------|
| Page loads, form is visible | Proceed — fill and click without asking |
| Instagram asks password/2FA | **Pause and ask user** — agent cannot and should not type credentials |
| Instagram sends confirmation email | **Pause and ask user** — only the user can click the email link |
| Export is being generated | Tell user to wait, no action needed from agent |
| Zip is in ~/Downloads | Proceed — run update.sh immediately |
| No zip found in ~/Downloads | Tell user to download it and come back |

## What to tell the user after running

1. Counts (total, mutual, churners, onboarding)
2. HTML includes dates for each direction
3. Previous export archived in ~/archive/
