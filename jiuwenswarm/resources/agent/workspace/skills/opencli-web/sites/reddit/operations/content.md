# Reddit: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `read` | `public_read` / `low` | `opencli reddit read "<post-id>" [--sort "<sort>"] [--limit <limit>] [--depth <depth>] [--replies <replies>] [--max-length <max-length>] [--expand-more <true\|false>] [--expand-rounds <expand-rounds>] -f json`<br>Read a Reddit post and its comments | `post-id` (str, required, positional); `sort` (str, optional, default='best'); `limit` (int, optional, default=25); `depth` (int, optional, default=2); `replies` (int, optional, default=5); `max-length` (int, optional, default=2000); `expand-more` (bool, optional, default=False); `expand-rounds` (int, optional, default=2) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `subreddit-info` | `public_read` / `low` | `opencli reddit subreddit-info "<name>" -f json`<br>Show metadata for a Reddit subreddit (subscribers, description, created date, NSFW) | `name` (string, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli reddit user "<username>" -f json`<br>View a Reddit user profile | `username` (string, required, positional) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user-comments` | `public_read` / `low` | `opencli reddit user-comments "<username>" [--limit <limit>] -f json`<br>View a Reddit user's comment history | `username` (string, required, positional); `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `user-posts` | `public_read` / `low` | `opencli reddit user-posts "<username>" [--limit <limit>] -f json`<br>View a Reddit user's submitted posts | `username` (string, required, positional); `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `read`: Source-audited against OpenCLI 1.8.6 reddit/read.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `subreddit-info`: Source-audited against OpenCLI 1.8.6 reddit/subreddit-info.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user`: Source-audited against OpenCLI 1.8.6 reddit/user.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user-comments`: Source-audited against OpenCLI 1.8.6 reddit/user-comments.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `user-posts`: Source-audited against OpenCLI 1.8.6 reddit/user-posts.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
