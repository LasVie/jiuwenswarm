# 1Point3Acres: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli 1point3acres search "<query>" [--limit <limit>] [--fid "<fid>"] -f json`<br>一亩三分地 站内关键字搜索（需要登录） | `query` (str, required, positional); `limit` (int, optional, default=20); `fid` (string, optional, default='') | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 1point3acres/search.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
