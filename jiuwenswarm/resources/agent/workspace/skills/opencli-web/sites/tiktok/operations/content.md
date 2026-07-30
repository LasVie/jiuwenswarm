# Tiktok: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `profile` | `public_read` / `low` | `opencli tiktok profile "<username>" -f json`<br>Get TikTok user profile info | `username` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli tiktok user "<username>" [--limit <limit>] -f json`<br>Get recent videos from a TikTok user via page-context APIs | `username` (str, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `profile`: Source-audited against OpenCLI 1.8.6 tiktok/profile.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user`: Source-audited against OpenCLI 1.8.6 tiktok/user.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
