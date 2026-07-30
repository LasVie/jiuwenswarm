# Chess: analytics

Read aggregate metrics, trends, or rankings.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `stats` | `public_read` / `low` | `opencli chess stats "<username>" -f json`<br>Chess.com player ratings + win/loss record across game kinds | `username` (string, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
