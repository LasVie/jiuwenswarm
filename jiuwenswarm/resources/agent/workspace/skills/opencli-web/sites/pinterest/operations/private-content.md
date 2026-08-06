# Pinterest: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `board-pins` | `private_content_read` / `medium` | `opencli pinterest board-pins "<board>" [--limit <limit>] -f json`<br>List pins inside a Pinterest board | `board` (string, required, positional); `limit` (int, optional, default=25) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `board-sections` | `private_content_read` / `medium` | `opencli pinterest board-sections "<board>" [--limit <limit>] -f json`<br>List the sections inside a Pinterest board | `board` (string, required, positional); `limit` (int, optional, default=50) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `pin` | `private_content_read` / `medium` | `opencli pinterest pin "<pin>" -f json`<br>Get details of a Pinterest pin | `pin` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search-boards` | `private_content_read` / `medium` | `opencli pinterest search-boards "<query>" [--limit <limit>] -f json`<br>Search for boards on Pinterest | `query` (string, required, positional); `limit` (int, optional, default=25) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search-pins` | `private_content_read` / `medium` | `opencli pinterest search-pins "<query>" [--limit <limit>] -f json`<br>Search pins on Pinterest | `query` (string, required, positional); `limit` (int, optional, default=25) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `search-users` | `private_content_read` / `medium` | `opencli pinterest search-users "<query>" [--limit <limit>] -f json`<br>Search for users on Pinterest | `query` (string, required, positional); `limit` (int, optional, default=25) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `user` | `private_content_read` / `medium` | `opencli pinterest user "<username>" -f json`<br>Get a Pinterest user's public profile stats | `username` (string, required, positional) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `user-boards` | `private_content_read` / `medium` | `opencli pinterest user-boards "<username>" [--limit <limit>] [--sort "<last_pinned_to\|alphabetical\|custom>"] -f json`<br>List a user's boards | `username` (string, required, positional); `limit` (int, optional, default=25); `sort` (string, optional, default='last_pinned_to', choices=last_pinned_to,alphabetical,custom) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `user-pins` | `private_content_read` / `medium` | `opencli pinterest user-pins "<username>" [--limit <limit>] -f json`<br>List pins created by a Pinterest user | `username` (string, required, positional); `limit` (int, optional, default=25) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `board-pins`: sensitive output: private content, account identifiers
- `board-sections`: sensitive output: private content, account identifiers
- `pin`: sensitive output: private content, account identifiers
- `search-boards`: sensitive output: private content, account identifiers
- `search-pins`: sensitive output: private content, account identifiers
- `search-users`: sensitive output: private content, account identifiers
- `user`: sensitive output: private content, account identifiers
- `user-boards`: sensitive output: private content, account identifiers
- `user-pins`: sensitive output: private content, account identifiers
