# Twitter: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `followers` | `public_read` / `low` | `opencli twitter followers ["<user>"] [--limit <limit>] -f json`<br>Get accounts following a Twitter/X user (defaults to the logged-in user when no user is given) | `user` (string, optional, positional); `limit` (int, optional, default=50) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `following` | `public_read` / `low` | `opencli twitter following ["<user>"] [--limit <limit>] -f json`<br>Get accounts a Twitter/X user is following (defaults to the logged-in user when no user is given) | `user` (string, optional, positional); `limit` (int, optional, default=50) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `search` | `public_read` / `low` | `opencli twitter search "<query>" [--filter "<top\|live>"] [--product "<top\|live\|photos\|videos>"] [--from "<from>"] [--has "<media\|images\|videos\|links\|replies>"] [--exclude "<replies\|retweets\|media\|links>"] [--limit <limit>] [--top-by-engagement <top-by-engagement>] -f json`<br>Search Twitter/X for tweets, with optional --from / --has / --exclude / --product filters mapped to X's search operators | `query` (string, required, positional); `filter` (string, optional, default='top', choices=top,live); `product` (string, optional, choices=top,live,photos,videos); `from` (string, optional); `has` (string, optional, choices=media,images,videos,links,replies); `exclude` (string, optional, choices=replies,retweets,media,links); `limit` (int, optional, default=15); `top-by-engagement` (int, optional, default=0) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |
| `trending` | `public_read` / `low` | `opencli twitter trending [--limit <limit>] -f json`<br>Twitter/X trending topics | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `followers`: Source-audited against OpenCLI 1.8.6 twitter/followers.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `following`: Source-audited against OpenCLI 1.8.6 twitter/following.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `search`: Source-audited against OpenCLI 1.8.6 twitter/search.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
- `trending`: Source-audited against OpenCLI 1.8.6 twitter/trending.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
