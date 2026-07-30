# Pixiv: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `illusts` | `public_read` / `low` | `opencli pixiv illusts "<user-id>" [--limit <limit>] -f json`<br>List a Pixiv artist's illustrations | `user-id` (str, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `ranking` | `public_read` / `low` | `opencli pixiv ranking [--mode "<daily\|weekly\|monthly\|rookie\|original\|male\|female\|daily_r18\|weekly_r18>"] [--page <page>] [--limit <limit>] -f json`<br>Pixiv illustration rankings (daily/weekly/monthly) | `mode` (str, optional, default='daily', choices=daily,weekly,monthly,rookie,original,male,female,daily_r18,weekly_r18); `page` (int, optional, default=1); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli pixiv search "<query>" [--limit <limit>] [--order "<date_d\|date\|popular_d\|popular_male_d\|popular_female_d>"] [--mode "<all\|safe\|r18>"] [--page <page>] -f json`<br>Search Pixiv illustrations by keyword | `query` (str, required, positional); `limit` (int, optional, default=20); `order` (str, optional, default='date_d', choices=date_d,date,popular_d,popular_male_d,popular_female_d); `mode` (str, optional, default='all', choices=all,safe,r18); `page` (int, optional, default=1) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `illusts`: Source-audited against OpenCLI 1.8.6 pixiv/illusts.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `ranking`: Source-audited against OpenCLI 1.8.6 pixiv/ranking.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `search`: Source-audited against OpenCLI 1.8.6 pixiv/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
