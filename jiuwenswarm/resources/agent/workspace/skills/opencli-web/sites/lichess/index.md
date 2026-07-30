# Lichess

- Site slug: `lichess`
- Domains: `lichess.org`
- Aliases: none

## Operations

| Operation | Purpose | Commands | Terminal contract |
|---|---|---|---|
| `public-data` | Read low-risk public data without browser state. | `top`, `user` | `sites/lichess/index.md` |

## Commands

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `top` | `public_read` / `low` | `opencli lichess top "<perf>" [--limit <limit>] -f json`<br>Top-N Lichess leaderboard for a perf type (bullet/blitz/rapid/classical/...) | `perf` (str, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `user` | `public_read` / `low` | `opencli lichess user "<username>" -f json`<br>Fetch a Lichess player profile by username (rating, perfs, counts) | `username` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
