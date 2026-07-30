# Github Trending

- Site slug: `github-trending`
- Domains: `github.com`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `repos` | `sites/github-trending/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `repos` | `public_read` / `low` | `opencli github-trending repos [--since "<since>"] [--language "<language>"] [--limit <limit>] -f json`<br>GitHub Trending repositories (public, no login). Filter by --language and --since. | `since` (string, optional, default='daily'); `language` (string, optional, default=''); `limit` (int, optional, default=25) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
