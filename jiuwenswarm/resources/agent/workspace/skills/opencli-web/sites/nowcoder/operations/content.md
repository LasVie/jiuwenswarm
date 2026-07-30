# Nowcoder: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `companies` | `public_read` / `low` | `opencli nowcoder companies [--job "<job>"] -f json`<br>Hot companies for interview prep | `job` (str, optional, default='11002') | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `creators` | `public_read` / `low` | `opencli nowcoder creators [--limit <limit>] -f json`<br>Top content creators leaderboard | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `detail` | `public_read` / `low` | `opencli nowcoder detail "<id>" -f json`<br>Post detail view (supports ID / UUID / URL) | `id` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `experience` | `public_read` / `low` | `opencli nowcoder experience [--page <page>] [--limit <limit>] -f json`<br>Interview experience posts | `page` (int, optional, default=1); `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `hot` | `public_read` / `low` | `opencli nowcoder hot [--limit <limit>] -f json`<br>Hot search ranking | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `jobs` | `public_read` / `low` | `opencli nowcoder jobs -f json`<br>Career category listing | none | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `papers` | `public_read` / `low` | `opencli nowcoder papers [--job "<job>"] [--company "<company>"] [--limit <limit>] -f json`<br>Interview question bank by company and job | `job` (str, optional, default='11002'); `company` (str, optional, default=''); `limit` (int, optional, default=10) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `recommend` | `public_read` / `low` | `opencli nowcoder recommend [--page <page>] [--limit <limit>] -f json`<br>Recommended feed | `page` (int, optional, default=1); `limit` (int, optional, default=15) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `referral` | `public_read` / `low` | `opencli nowcoder referral [--page <page>] [--limit <limit>] -f json`<br>Internal referral posts | `page` (int, optional, default=1); `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `salary` | `public_read` / `low` | `opencli nowcoder salary [--page <page>] [--limit <limit>] -f json`<br>Salary disclosure posts | `page` (int, optional, default=1); `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `topics` | `public_read` / `low` | `opencli nowcoder topics [--limit <limit>] -f json`<br>Hot discussion topics | `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `detail`: Source-audited against OpenCLI 1.8.6 nowcoder/detail.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `experience`: Source-audited against OpenCLI 1.8.6 nowcoder/experience.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `papers`: Source-audited against OpenCLI 1.8.6 nowcoder/papers.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `referral`: Source-audited against OpenCLI 1.8.6 nowcoder/referral.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `salary`: Source-audited against OpenCLI 1.8.6 nowcoder/salary.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
