# Confluence: private-content

Read credential-gated content from a configured Confluence tenant.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `page` | `private_content_read` / `medium` | `opencli confluence page "<id>" -f json`<br>Confluence page by id with storage and Markdown body | `id` (str, required, positional) | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |
| `search` | `private_content_read` / `medium` | `opencli confluence search "<cql>" [--space "<space>"] [--limit <limit>] -f json`<br>Search Confluence content with CQL | `cql` (str, required, positional); `space` (string, optional); `limit` (int, optional, default=20) | auth=required; transport=public_http; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `page`: Requires a configured Confluence tenant and credentials.; sensitive output: private content, account identifiers
- `search`: Requires a configured Confluence tenant and credentials.; sensitive output: private content, account identifiers
