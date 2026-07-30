# Xiaoyuzhou: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `episode` | `private_content_read` / `medium` | `opencli xiaoyuzhou episode "<id>" -f json`<br>View details of a Xiaoyuzhou podcast episode | `id` (str, required, positional) | auth=required; transport=local; fallback_before=browser_agent; fallback_after=none |
| `podcast` | `private_content_read` / `medium` | `opencli xiaoyuzhou podcast "<id>" -f json`<br>View a Xiaoyuzhou podcast profile | `id` (str, required, positional) | auth=required; transport=local; fallback_before=browser_agent; fallback_after=none |
| `podcast-episodes` | `private_content_read` / `medium` | `opencli xiaoyuzhou podcast-episodes "<id>" [--limit <limit>] -f json`<br>List episodes of a Xiaoyuzhou podcast | `id` (str, required, positional); `limit` (int, optional, default=20) | auth=required; transport=local; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `episode`: sensitive output: private content, account identifiers
- `podcast`: sensitive output: private content, account identifiers
- `podcast-episodes`: sensitive output: private content, account identifiers
