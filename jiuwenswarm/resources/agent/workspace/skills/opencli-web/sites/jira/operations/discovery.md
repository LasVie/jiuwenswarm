# Jira: discovery

Search, browse, recommend, or discover site content.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `search` | `private_content_read` / `high` | `opencli jira search "<jql>" [--limit <limit>] -f json`<br>Search Jira issues with JQL | `jql` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=public_http; fallback_before=none; fallback_after=none |

## Operation-specific constraints

- `search`: Requires a configured Jira base URL and secret-bound authentication.; sensitive output: private issue content, account identifiers
