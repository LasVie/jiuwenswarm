# Rednote: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `feed` | `private_content_read` / `medium` | `opencli rednote feed [--limit <limit>] -f json`<br>Rednote home feed (reads hydrated Pinia store) | `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `notifications` | `private_content_read` / `medium` | `opencli rednote notifications [--type "<type>"] [--limit <limit>] -f json`<br>Rednote notifications (mentions/likes/connections) | `type` (str, optional, default='mentions'); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `feed`: sensitive output: private content, account identifiers
- `notifications`: sensitive output: private content, account identifiers
