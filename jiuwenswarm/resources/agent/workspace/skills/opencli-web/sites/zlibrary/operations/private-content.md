# Zlibrary: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `info` | `private_content_read` / `medium` | `opencli zlibrary info "<url>" -f json`<br>Get book details and available download formats from a Z-Library book page | `url` (str, required, positional) | auth=required; transport=browser_cookie; fallback_before=none; fallback_after=none |
| `search` | `private_content_read` / `medium` | `opencli zlibrary search "<query>" [--limit <limit>] -f json`<br>Search Z-Library for books by title, author, ISBN, or keyword | `query` (str, required, positional); `limit` (int, optional, default=10) | auth=required; transport=browser_cookie; fallback_before=none; fallback_after=none |

## Operation-specific constraints

- `info`: sensitive output: private content, account identifiers
- `search`: sensitive output: private content, account identifiers
