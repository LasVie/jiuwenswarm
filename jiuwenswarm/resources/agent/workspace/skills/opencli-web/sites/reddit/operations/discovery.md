# Reddit: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `frontpage` | `public_read` / `low` | `opencli reddit frontpage [--limit <limit>] -f json`<br>Reddit Frontpage / r/all | `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `hot` | `public_read` / `low` | `opencli reddit hot [--subreddit "<subreddit>"] [--limit <limit>] -f json`<br>Reddit 热门帖子 | `subreddit` (str, optional, default=''); `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `popular` | `public_read` / `low` | `opencli reddit popular [--limit <limit>] -f json`<br>Reddit Popular posts (/r/popular) | `limit` (int, optional, default=20) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli reddit search "<query>" [--subreddit "<subreddit>"] [--sort "<sort>"] [--time "<time>"] [--limit <limit>] -f json`<br>Search Reddit Posts | `query` (string, required, positional); `subreddit` (string, optional, default=''); `sort` (string, optional, default='relevance'); `time` (string, optional, default='all'); `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `subreddit` | `public_read` / `low` | `opencli reddit subreddit "<name>" [--sort "<sort>"] [--time "<time>"] [--limit <limit>] -f json`<br>Get posts from a specific Subreddit | `name` (string, required, positional); `sort` (string, optional, default='hot'); `time` (string, optional, default='all'); `limit` (int, optional, default=15) | auth=optional; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `frontpage`: Source-audited against OpenCLI 1.8.6 reddit/frontpage.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `hot`: Source-audited against OpenCLI 1.8.6 reddit/hot.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `popular`: Source-audited against OpenCLI 1.8.6 reddit/popular.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `search`: Source-audited against OpenCLI 1.8.6 reddit/search.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
- `subreddit`: Source-audited against OpenCLI 1.8.6 reddit/subreddit.js; reads public site content through the browser session. Login may affect availability, but no account-private fields are intended.
