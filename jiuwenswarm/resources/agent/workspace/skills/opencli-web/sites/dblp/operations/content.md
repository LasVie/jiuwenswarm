# Dblp: content

Read site content and metadata.

| Command | Effect / risk | Exact usage | Arguments | Runtime |
|---|---|---|---|---|
| `author` | `public_read` / `low` | `opencli dblp author ["<author>"] [--pid "<pid>"] [--limit <limit>] -f json`<br>List dblp publications by a given author (newest first; resolves to top PID match) | `author` (str, optional, positional); `pid` (str, optional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `paper` | `public_read` / `low` | `opencli dblp paper "<key>" -f json`<br>Fetch a dblp record by canonical key (e.g. conf/nips/VaswaniSPUJGKP17) | `key` (str, required, positional) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
| `venue` | `public_read` / `low` | `opencli dblp venue "<query>" [--limit <limit>] -f json`<br>Search dblp venue registry (conferences / journals) by name or acronym | `query` (str, required, positional); `limit` (int, optional, default=20) | auth=none; transport=public_http; fallback_before=browser_agent; fallback_after=browser_agent |
