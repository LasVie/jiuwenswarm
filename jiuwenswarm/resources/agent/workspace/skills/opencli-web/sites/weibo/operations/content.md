# Weibo: content

Read one public item, record, page, or resource.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `comments` | `public_read` / `low` | `opencli weibo comments "<id>" [--limit <limit>] -f json`<br>Get comments on a Weibo post | `id` (str, required, positional); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `post` | `public_read` / `low` | `opencli weibo post "<id>" -f json`<br>Get a single Weibo post | `id` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli weibo user "<id>" -f json`<br>Get Weibo user profile | `id` (str, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `comments`: Source-audited against OpenCLI 1.8.6 weibo/comments.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `post`: Source-audited against OpenCLI 1.8.6 weibo/post.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user`: Source-audited against OpenCLI 1.8.6 weibo/user.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
