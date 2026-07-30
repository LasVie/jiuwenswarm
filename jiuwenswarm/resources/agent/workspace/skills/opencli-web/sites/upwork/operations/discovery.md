# Upwork: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `public_read` / `low` | `opencli upwork search "<query>" [--location "<location>"] [--category "<category>"] [--sort "<sort>"] [--page <page>] [--per_page <per_page>] -f json`<br>Upwork keyword job search (logged-in browser session, US site) | `query` (str, required, positional); `location` (string, optional, default=''); `category` (string, optional, default=''); `sort` (string, optional, default='recency'); `page` (int, optional, default=1); `per_page` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `search`: Source-audited against OpenCLI 1.8.6 upwork/search.js; the adapter requires a logged-in browser session, but returns public site content rather than account-private state.
