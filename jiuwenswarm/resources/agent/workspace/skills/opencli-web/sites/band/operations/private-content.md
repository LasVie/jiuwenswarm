# Band: private-content

Read content that depends on an authenticated account.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `mentions` | `private_content_read` / `medium` | `opencli band mentions [--filter "<mentioned\|all\|post\|comment>"] [--limit <limit>] [--unread <true\|false>] -f json`<br>Show Band notifications where you are @mentioned | `filter` (str, optional, default='mentioned', choices=mentioned,all,post,comment); `limit` (int, optional, default=20); `unread` (bool, optional, default=False) | auth=required; transport=browser_intercept; fallback_before=browser_agent; fallback_after=none |
| `post` | `private_content_read` / `medium` | `opencli band post <band_no> <post_no> [--output "<output>"] [--comments <true\|false>] -f json`<br>Export full content of a post including comments | `band_no` (int, required, positional); `post_no` (int, required, positional); `output` (str, optional, default=''); `comments` (bool, optional, default=True) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |
| `posts` | `private_content_read` / `medium` | `opencli band posts <band_no> [--limit <limit>] -f json`<br>List posts from a Band | `band_no` (int, required, positional); `limit` (int, optional, default=20) | auth=required; transport=browser_cookie; fallback_before=browser_agent; fallback_after=none |

## Operation-specific constraints

- `mentions`: Source-audited against OpenCLI 1.8.6 band/mentions.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private group content, account identifiers
- `post`: sensitive output: private content, account identifiers
- `posts`: Source-audited against OpenCLI 1.8.6 band/posts.js; reads authenticated or session-scoped content that can expose private account data.; sensitive output: private group content, account identifiers
