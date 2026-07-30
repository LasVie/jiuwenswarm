# Chess: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `analyze` | `public_read` / `low` | `opencli chess analyze "<game-url>" -f json`<br>Open a Chess.com game in the browser analysis board | `game-url` (string, required, positional) | auth=none; transport=browser_dom; fallback_before=browser_agent; fallback_after=browser_agent |
| `game` | `public_read` / `low` | `opencli chess game "<game-url>" -f json`<br>Chess.com single-game detail (white, black, result, ECO, time control) by full game URL | `game-url` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `games` | `public_read` / `low` | `opencli chess games "<username>" [--limit <limit>] -f json`<br>Chess.com recent games for a player, newest first | `username` (string, required, positional); `limit` (int, optional, default=10) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |

## Operation-specific constraints

- `analyze`: Source-audited against OpenCLI 1.8.6 chess/analyze.js; navigates the bound browser to a public analysis URL and reports the resolved URL without remote state mutation.
