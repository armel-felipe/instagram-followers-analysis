#!/usr/bin/env node
/**
 * Instagram Export Request — browser automation flow reference.
 * The agent (via cua_repl) orchestrates the steps; the user confirms
 * at each point marked [USER].
 *
 * Flow:
 * 1. Agent opens data_download page in the in-app browser (logged as tubr_cdgirassois)
 * 2. Agent clicks "Solicitar download" → selects HTML + Connections
 * 3. Instagram asks password/2FA → AGENT PAUSES → USER confirms
 * 4. Instagram sends confirmation email → AGENT PAUSES → USER confirms in email
 * 5. Instagram generates the export (minutes to hours)
 * 6. User downloads the zip to ~/Downloads/
 * 7. Agent runs update.sh (fully automated)
 *
 * The agent cannot bypass steps 3 and 4: Instagram requires human confirmation
 * for data export requests (GDPR/LGPD compliance). Everything else is automated.
 */

const EXPORT_URL = "https://www.instagram.com/accounts/account_recovery/privacy_and_security/data_download/";

// For cua_repl runtime — steps the agent executes:
const AGENT_STEPS = [
  { step: 1, action: "open", url: EXPORT_URL, pause: false },
  { step: 2, action: "click_request_download", pause: false },
  { step: 3, action: "select_html_format", pause: false },
  { step: 4, action: "select_connections", pause: false },
  { step: 5, action: "confirm_request", pause: "PASSWORD_OR_2FA" },
  { step: 6, action: "wait_for_email_confirmation", pause: "USER_MUST_CLICK_EMAIL_LINK" },
  { step: 7, action: "wait_for_export_generation", pause: "MINUTES_TO_HOURS" },
  { step: 8, action: "user_downloads_zip", pause: "USER_DOWNLOADS" },
  { step: 9, action: "run_update_sh", pause: false },
];

// The agent asks the user at these points:
const USER_CONFIRMATIONS = [
  { step: 5, reason: "Instagram may ask for password or 2FA code — only the user can provide this" },
  { step: 6, reason: "Instagram sends a confirmation email — the user must click the link to authorize the export" },
  { step: 8, reason: "The user must download the zip from the email — Instagram does not allow programmatic download" },
];

module.exports = { EXPORT_URL, AGENT_STEPS, USER_CONFIRMATIONS };
