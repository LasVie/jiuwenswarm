# Google: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `images` | `private_content_read` / `medium` | `opencli google images "<keyword>" [--limit <limit>] [--lang "<lang>"] [--resolve <true\|false>] -f json`<br>Search Google Images for photos and image results | `keyword` (str, required, positional); `limit` (int, optional, default=20); `lang` (str, optional, default='en'); `resolve` (bool, optional, default=True) | auth=required; transport=browser_dom; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `images`: sensitive output: private content, account identifiers
